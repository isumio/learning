use std::io;
use std::io::prelude::*;
use std::fs::File;
use std::env;

fn main() {
    let mut files = Vec::new();

    // The first file we want to write to is stdout
    match File::create("/dev/stdout") {
        Ok(f) => {
            files.push(f);
        }
        Err(error) => {
            println!("Error when creating file for writing: {}", error);
        }
    }

    // Process any additional files specified
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 {
        for file_name in args {
            match File::create(file_name) {
                Ok(f) => {
                    files.push(f);
                }
                Err(error) => {
                    println!("Error when creating file for writing: {}", error);
                }
            }
        }
    }

    // Read from standard input and write to all the files
    let mut line = String::new();
    loop {
        match io::stdin().read_line(&mut line) {
            Ok(n) => {
                // Have we read all the lines, if yes, break
                if n == 0 {
                    break;
                }
                for f in &mut files{
                    match f.write(line.as_bytes()) {
                        Ok(_) => {}
                        Err(error) => {
                            println!("Error when writing to file: {}", error);
                        }
                    }
                }
                // Clear the line we just read so that we don't keep
                // appending
                line.clear();
            }
            Err(error) => {
                println!("Error reading from stdin : {}", error);
            }
        }
    }
}
