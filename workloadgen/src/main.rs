use std::io::Write;
use std::convert::TryInto;
use rand::Rng;

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
    start_lba: u64,
    end_lba: u64,
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
        println!("{:x?}", bytes);
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

    // Generate random sectors
    for _n in 0..config.size {
        random_data.push(generator.gen_range(config.start_lba, config.end_lba));
    }

    // Generate traces
    for n in 0..config.size {
        let mut sector = random_data[n as usize];
        let repeat: f32 = generator.gen();

        if repeat < config.freq {
            sector = config.repeat_lbas[0 as usize];
        }

        traces.push(create_trace(seq, time, sector));

        println!("{}", sector);
        
        seq += 1;
        time += 1000000000;
    }

    traces
}

fn main() {
    let config = replay_configuration { size: 10, 
        start_lba: 2048, 
        end_lba: 20973567, 
        block_sizes: vec![512], 
        repeat_lbas: vec![200],
        freq: 0.1 };

    let traces = generate_traces(&config);

    let _ret = write_traces(&traces);
}