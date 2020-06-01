# Online Disk I/O Analysis

This repository provides algorithms and tools developed to aid in the tracing and block pair correlation analysis for the purpose of optimizing state of the art storage devices.

## analysis/ [Python]
Contains algorithm that takes block transactions as input from a named pipe and generates block pair correlations and stream ids to be used for multi-stream storage devices.

## blktrace/ [C]
Contains modifications to the user level _blktrace_ and _blkparse_ applications that allow filtering by process id and sending INSERT block device writes to a named pipe.

## kernel/ [C]
Contains modifications to the kernel level _blktrace_ to accept a process id filter.

## workloadgen/ [Rust]
Provides synthetically generated disk I/O workloads through the binary output of `blk_io_trace` structures which may then be replayed by fio or blkreplay. These workloads may be generated through configuration files that specify block writes probabilistically or temporally. `cargo build` is used to build this program, see `workloadgen --help` for options.
