#![allow(dead_code)]

use std::io::Write;
use std::convert::TryInto;
use rand::Rng;
use clap::{Arg, App};

mod util;
use util::convert_to_int;

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
    repeat_lbas: Vec<u64>,
    freq: f32
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
        //println!("{:x?}", bytes);
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
        random_data.push(generator.gen_range(0, config.range));
    }

    let mut cur_index = 0;
    let lba_index = config.repeat_lbas.len()-1;

    // Generate traces
    for n in 0..config.size {
        let mut sector = random_data[n as usize];
        let repeat: f32 = generator.gen();

        if repeat < config.freq {
            sector = config.repeat_lbas[cur_index];

            if cur_index < lba_index {
                cur_index += 1 
            } else {
                cur_index = 0
            }
        }

        traces.push(create_trace(seq, time, sector));

        //println!("{}", sector);
        
        seq += 1;
        time += 1000000000;
    }

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
                        .arg(Arg::from_usage("[repeated_lbas] 'Specifies the LBA offsets to be repeated; comma delimited'")
                            .short("l")
                            .takes_value(true)
                            .required(true))
                        .arg(Arg::from_usage("[repeat_frequency] 'Sets the probability of a block repeat'")
                            .short("f")
                            .required_unless("repeat_temporal")
                            .takes_value(true))
                        .arg(Arg::from_usage("[repeat_temporal] 'Sets the distance of a block repeat")
                            .short("t")
                            .takes_value(true))
                        .get_matches();

    let size = convert_to_int::<u32>(matches.value_of("size"));
    let blocksize = vec![convert_to_int::<u32>(matches.value_of("iosize"))];
    let mut repeat_frequency: f32 = 0.0;
    let mut repeat_temporal: u32 = 0;

    if matches.is_present("repeat_temporal") {
        repeat_temporal = convert_to_int::<u32>(matches.value_of("repeat_temporal"));
    } else {
        repeat_frequency = convert_to_int::<f32>(matches.value_of("repeat_frequency"));
    }

    let repeat_lbas: Vec<u64> = matches.value_of("repeated_lbas").unwrap().split(',').collect::<Vec<_>>().into_iter()
                                            .map(|x| {
                                                x.parse::<u64>().unwrap()
                                            }).collect();

    let range = convert_to_int::<u64>(matches.value_of("range"));

    let config = replay_configuration { size: size, 
        range: range,
        block_sizes: blocksize, 
        repeat_lbas: repeat_lbas,
        freq: repeat_frequency };

    println!("Generating workload...");

    let traces = generate_traces(&config);

    let _ret = write_traces(&traces);

    println!("Wrote workload to replay.bin");
}