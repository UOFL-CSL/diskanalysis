use std::fs;

pub struct RepeatLbas {
    sequential: Vec<Vec<u64>>,
    random: Vec<u64>
}

// Parses a configuration file with the following format:
// [sequential]
// <start>-<end>
// <start>-<end>
// [random]
// <lba>
// <lba>
pub fn parse<'a>(filename: &str) -> RepeatLbas {
    let contents = fs::read_to_string(filename)
                            .expect("Failed to read configuration file.");

                            println!("{:?}", contents);

    let parsed: Vec<&str> = contents.split("[random]\r\n").collect();

    let mut sequential: Vec<&str> = parsed[0].split("\r\n").collect::<Vec<&str>>();
    let mut random: Vec<&str> = parsed[1].split("\r\n").collect();

    sequential.remove(0);
    sequential.pop();
    random.pop();

    let mut repeat_lbas = RepeatLbas { sequential: vec![], random: vec![] };

    for line in sequential.iter() {
        let range: Vec<&str> = line.trim_end_matches("\r\n").split("-").collect();
        let mut sequence: Vec<u64> = Vec::new();

        for i in range[0].parse::<u64>().unwrap()..=range[1].parse::<u64>().unwrap() {
            sequence.push(i);
        }

        repeat_lbas.sequential.push(sequence);
    }

    for line in random.iter() {
        repeat_lbas.random.push(line.parse().unwrap());
    }

    repeat_lbas
}