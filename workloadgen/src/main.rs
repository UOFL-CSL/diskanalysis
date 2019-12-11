#![allow(dead_code)]

use std::io::Write;
use std::convert::TryInto;
use rand::Rng;
use clap::{Arg, App};

mod util;
use util::convert_to_int;

mod parser;
use parser::{ parse, RepeatLbas };

// Magic value passed with the ioctl - first 2 bytes are the magic, last two are the version number
const MAGIC: u32 = 0x65617407;

// First 16 bits are MAJOR, last 16 are MINOR
// Fio can replace this value 
const BLKDEV: u32 = (259<<16) | 3;

// Masks for the operation type
const TRACE_TYPE_QUEUE: u32 = 1 << 0;
const TRACE_TYPE_READ: u32 = 1 << 16;
const TRACE_TYPE_WRITE: u32 = 1 << 17;

#[derive(Default)]
#[derive(Debug)]
#[allow(non_camel_case_types)]
#[repr(C)] // Allocate memory in order 
struct blk_io_trace {
    magic: u32, // constant magic
    seq: u32, // sequence number, sequential
    time: u64, // time in ns
    sector: u64, // sector number
    bytes: u32, // bytes
    act: u32, // action type
    pid: u32, // process id 
    dev: u32, // block device id
    cpu: u32, // cpu core number
    error: u16, // error
    pd: u16 // pdu
}

#[allow(non_camel_case_types)]
struct replay_configuration {
    size: u32,
    range: u64,
    block_sizes: Vec<u32>,
    repeat_lbas: RepeatLbas,
}

unsafe fn to_u8_slice<T: Sized>(obj: &T) -> &[u8] {
    std::slice::from_raw_parts((obj as *const T) as *const u8, std::mem::size_of::<T>())
}

fn create_trace(seq: u32, time: u64, lba: u64) -> blk_io_trace {
    let mut trace: blk_io_trace = { Default::default() };
    trace.magic = MAGIC;
    trace.dev = BLKDEV;
    trace.act = TRACE_TYPE_WRITE | TRACE_TYPE_QUEUE;
    trace.pid = 0xFF;

    trace.sector = lba;
    trace.bytes = 4 << 10; 

    trace.seq = seq;
    trace.time = time;

    trace
}

fn write_traces(traces: &Vec<blk_io_trace>) -> std::io::Result<()> {
    let file = std::fs::File::create("replay.bin")?;
    let mut buf = std::io::BufWriter::new(&file);

    for trace in traces.iter() {
        let bytes: &[u8] = unsafe { to_u8_slice(trace) };
        //println!("{:?}", trace.sector);
        buf.write(bytes)?;
    }

    Ok(())
}

fn generate_traces(config: &replay_configuration) -> Vec::<blk_io_trace> {
    let mut traces = Vec::<blk_io_trace>::new();

    let mut seq = 0;
    let mut time = 0; // Time is stored in ns

    let mut random_data = Vec::<u64>::with_capacity(config.size.try_into().unwrap());
    let mut generator = rand::thread_rng();

    // Generate random sectors based on the size of the block device
    for _n in 0..config.size {
        let number = generator.gen_range(0, config.range);
        random_data.push(number);

        //println!("{:?}", number);
    }

    // Generate traces
    for n in 0..config.size {
        let mut sector = random_data[n as usize];
        let probability: f32 = generator.gen();

        // Create specified sequential writes
        // Only one of these can occur per iteration
        for lba_list in &config.repeat_lbas.sequential {
            let mut done = false;

            for lba in lba_list {
                if lba.probability < probability {
                    continue;
                }
 
                traces.push(create_trace(seq, time, lba.value));
                seq += 1;
                done = true;
            }

            if done {
                println!("Sequential write");
                break;
            }
        }

        // Create a random write 
        for lba in &config.repeat_lbas.random {
            if lba.probability < probability {
                continue;
            } 
            
            traces.push(create_trace(seq, time, lba.value));
            seq += 1;
            break;
        }

        // Create the default random write
        traces.push(create_trace(seq, time, sector));

        //println!("{}", sector);
        
        seq += 1;
        time += 100;
    }

    println!("Created {} writes.", seq);

    traces
}

fn main() {
    let matches = App::new("Fio Workload Generator")
                        .version("1.0")
                        .arg(Arg::with_name("size")
                            .short("s")
                            .help("Sets the size of the workload")
                            .takes_value(true)
                            .required(true))
                        .arg(Arg::from_usage("[range] 'Specifies the range of sectors to generate operations'")
                            .short("r")
                            .takes_value(true)
                            .required(true))
                        .arg(Arg::from_usage("[iosize] 'Sets the size of the IO operations in KB'")
                            .short("i")
                            .takes_value(true)
                            .default_value("4")
                            .required(true))
                        .arg(Arg::from_usage("[repeat_config] 'Sets the file to read to configure repeated LBAs")
                            .short("c")
                            .takes_value(true)
                            .default_value("lbas.txt"))
                        .get_matches();

    let size = convert_to_int::<u32>(matches.value_of("size"));
    let blocksize = vec![convert_to_int::<u32>(matches.value_of("iosize"))];

    let mut repeat_lbas: RepeatLbas = Default::default();
    if matches.is_present("repeat_config") {
        repeat_lbas = parse(matches.value_of("repeat_config").unwrap());
    }

    let range = convert_to_int::<u64>(matches.value_of("range"));

    let config = replay_configuration { size: size, 
        range: range,
        block_sizes: blocksize, 
        repeat_lbas: repeat_lbas 
    };

    println!("Generating workload...");

    let traces = generate_traces(&config);

    let _ret = write_traces(&traces);

    println!("Wrote workload to replay.bin");
}