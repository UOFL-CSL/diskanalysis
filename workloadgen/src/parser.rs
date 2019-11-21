use std::fs;

pub struct RepeatLbas {
    sequential: Vec<Vec<u64>>,
    random: Vec<u64>
}

pub fn parse<'a>(filename: &str) -> &'a RepeatLbas {
    let mut contents = fs::read_to_string(filename)
                            .expect("Failed to read configuration file.");

    let parsed = contents.split("[random]\n");

    let sequential = parsed[0];
    let random = parsed[1];

    let repeat_lbas = RepeatLbas { sequential: vec![vec![]], random: vec![] };

    for i in 0..sequential.iter() {
        println!("{:?}", sequential[i]);
    }
}