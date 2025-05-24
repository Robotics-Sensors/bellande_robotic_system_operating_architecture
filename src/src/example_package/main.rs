use common_msgs::*;
use std::{thread, time};

struct Example_package;

impl Example_package {
    fn run(&self) {
        loop {
            // TODO: Implement node logic
            println!("Running example_package");
            thread::sleep(time::Duration::from_secs(1));
        }
    }
}

fn main() {
    let node = Example_package{};
    node.run();
}
