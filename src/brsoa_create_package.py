# Copyright (C) 2025 Bellande Robotics Sensors Research Innovation Center, Ronaldson Bellande
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import argparse
import yaml
from bellande_parser.bellande_parser import Bellande_Format

TEMPLATE_DIR = "templates"

def create_package_bellande(package_name, language, dependencies):
    content = {
        "name": package_name,
        "language": language,
        "dependencies": dependencies
    }
    return yaml.dump(content, default_flow_style=False)

def create_cpp_source(package_name):
    return f"""#include "common_msgs.hpp"
#include <iostream>
#include <chrono>
#include <thread>

class {package_name.capitalize()} {{
public:
    void run() {{
        while (true) {{
            // TODO: Implement node logic
            std::cout << "Running {package_name}" << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }}
    }}
}};

int main(int argc, char** argv) {{
    {package_name.capitalize()} node;
    node.run();
    return 0;
}}
"""

def create_python_source(package_name):
    return f"""from common_msgs import *
import time

class {package_name.capitalize()}:
    def run(self):
        while True:
            # TODO: Implement node logic
            print(f"Running {package_name}")
            time.sleep(1)

if __name__ == "__main__":
    node = {package_name.capitalize()}()
    node.run()
"""

def create_java_source(package_name):
    return f"""import common_msgs.Messages.*;

public class {package_name.capitalize()} {{
    public void run() {{
        while (true) {{
            // TODO: Implement node logic
            System.out.println("Running {package_name}");
            try {{
                Thread.sleep(1000);
            }} catch (InterruptedException e) {{
                e.printStackTrace();
            }}
        }}
    }}

    public static void main(String[] args) {{
        {package_name.capitalize()} node = new {package_name.capitalize()}();
        node.run();
    }}
}}
"""

def create_rust_source(package_name):
    return f"""use common_msgs::*;
use std::{{thread, time}};

struct {package_name.capitalize()};

impl {package_name.capitalize()} {{
    fn run(&self) {{
        loop {{
            // TODO: Implement node logic
            println!("Running {package_name}");
            thread::sleep(time::Duration::from_secs(1));
        }}
    }}
}}

fn main() {{
    let node = {package_name.capitalize()}{{}};
    node.run();
}}
"""

def create_go_source(package_name):
    return f"""package main

import (
    "fmt"
    "time"
    "common_msgs"
)

type {package_name.capitalize()} struct{{}}

func (n *{package_name.capitalize()}) Run() {{
    for {{
        // TODO: Implement node logic
        fmt.Println("Running {package_name}")
        time.Sleep(1 * time.Second)
    }}
}}

func main() {{
    node := &{package_name.capitalize()}{{}}
    node.Run()
}}
"""

def create_package(directory, package_name, language):
    package_dir = os.path.join(directory, package_name)
    os.makedirs(package_dir, exist_ok=True)

    # Make Directory for package if it exits
    os.makedirs(package_dir, exist_ok=True)
    
    # Create package.bellande
    with open(os.path.join(package_dir, "package.bellande"), "w") as f:
        f.write(create_package_bellande(package_name, language, ["common_msgs"]))

    # Create source file
    source_creators = {
        "cpp": create_cpp_source,
        "python": create_python_source,
        "java": create_java_source,
        "rust": create_rust_source,
        "go": create_go_source
    }

    if language in source_creators:
        source_content = source_creators[language](package_name)
        source_filename = f"{package_name}.{language}"
        if language == "cpp":
            source_filename = f"{package_name}.cpp"
        elif language == "python":
            source_filename = f"{package_name}.py"
        elif language == "java":
            source_filename = f"{package_name.capitalize()}.java"
        elif language == "rust":
            source_filename = f"{package_name}.rust"
            
            with open(os.path.join(package_dir, "Cargo.toml"), "w") as f:
                f.write(f"[package]\nname = \"{package_name}\"\nversion = \"0.1.0\"\nedition = \"2021\"\n\n[dependencies]\ncommon_msgs = {{ path = \"../../build/common_msgs\" }}\n")
        
        elif language == "go":
            source_filename = f"{package_name}.go"
        
        with open(os.path.join(package_dir, source_filename), "w") as f:
            f.write(source_content)
    else:
        print(f"Unsupported language: {language}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new package for the robot architecture.")
    parser.add_argument("directory", help="Directory where you want to make it")
    parser.add_argument("package_name", help="Name of the package to create")
    parser.add_argument("language", choices=["cpp", "python", "java", "rust", "go"], help="Programming language for the package")
    
    args = parser.parse_args()
    
    create_package(args.directory, args.package_name, args.language)
    print(f"Created package {args.package_name} using {args.language}")
