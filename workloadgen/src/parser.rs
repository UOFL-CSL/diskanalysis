use std::fs;
use std::collections::BTreeSet;
use std::cmp::{Ordering};
use std::slice::IterMut;

pub struct Lba {
    pub value: u64,
    pub probability: f32
}

impl PartialEq for Lba {
    fn eq(&self, other: &Self) -> bool {
        self.value == other.value
    }
}

impl Eq for Lba { }

impl PartialOrd for Lba {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        self.probability.partial_cmp(&other.probability)
    }
}

impl Ord for Lba {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.probability < other.probability {
            Ordering::Less
        } else if self.probability > other.probability {
            Ordering::Greater
        } else {
            Ordering::Equal
        }
    }
}

#[derive(Default)]
pub struct RepeatLbas {
    pub sequential: BTreeSet<Vec<Lba>>,
    pub random: BTreeSet<Lba>
}

// Parses a configuration file with the following format:
// [sequential]
// <start>-<end>;<prob>
// <start>-<end>;<prob>
// [random]
// <lba>;<prob>
// <lba>;<prob>
pub fn parse<'a>(filename: &str) -> RepeatLbas {
    let contents = fs::read_to_string(filename)
                            .expect("Failed to read configuration file.");

    //println!("{:?}", contents);

    let parsed: Vec<&str> = contents.split("[random]\n").collect();

    let mut sequential: Vec<&str> = parsed[0].split("\n").collect::<Vec<&str>>();
    let mut random: Vec<&str> = parsed[1].split("\n").collect();

    sequential.remove(0);
    sequential.pop();
    random.pop();

    let mut repeat_lbas = RepeatLbas { sequential: BTreeSet::new(), random: BTreeSet::new() };
    let mut t_probability: f32 = 0.0;

    for line in sequential.iter() {
        let split: Vec<&str> = line.trim_end_matches("\n").split(";").collect();
        let range: Vec<&str> = split[0].split("-").collect();
        let probability: f32 = split[1].parse().unwrap();

        let mut sequence: Vec<Lba> = Vec::new();

        for i in range[0].parse::<u64>().unwrap()..=range[1].parse::<u64>().unwrap() {
            sequence.push(Lba { value: i, probability: t_probability + probability });
        }
        
        t_probability += probability;

        repeat_lbas.sequential.insert(sequence);
    }

    t_probability = 0.0;
    for line in random.iter() {
        let split: Vec<&str> = line.trim_end_matches("\n").split(";").collect();
        let probability: f32 = split[1].parse().unwrap();

        repeat_lbas.random.insert(Lba { value: split[0].parse().unwrap(), probability: t_probability + probability });

        t_probability += probability;
    }

    // Normalize the probabilities
    //let total_probability_s: f32 = repeat_lbas.sequential.iter().map(|x| x[0].probability).sum();
    //let total_probability_r: f32 = repeat_lbas.random.iter().map(|x| x.probability).sum();

    repeat_lbas
}