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
import subprocess
from bellande_parser.bellande_parser import Bellande_Format

def load_config():
    bellande_parser = Bellande_Format()
    raw_content = bellande_parser.parse_bellande("project_config.bellande")

def build_cpp(package_dir, output_dir, config):
    src_file = os.path.join(package_dir, f"{os.path.basename(package_dir)}.cpp")
    output_file = os.path.join(output_dir, os.path.basename(package_dir))
    compiler = config['build_settings']['cpp']['compiler']
    flags = ' '.join(config['build_settings']['cpp']['flags'])
    
    cmd = f"{compiler} {flags} -I build/common_msgs {src_file} -o {output_file}"
    subprocess.run(cmd, shell=True, check=True)

def build_python(package_dir, output_dir, config):
    src_file = os.path.join(package_dir, f"{os.path.basename(package_dir)}.py")
    output_file = os.path.join(output_dir, os.path.basename(src_file))
    os.makedirs(output_dir, exist_ok=True)
    os.symlink(src_file, output_file)

def build_java(package_dir, output_dir, config):
    src_file = os.path.join(package_dir, f"{os.path.basename(package_dir)}.java")
    output_dir = os.path.join(output_dir, "classes")
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = f"javac -d {output_dir} -cp build/common_msgs {src_file}"
    subprocess.run(cmd, shell=True, check=True)

def build_rust(package_dir, output_dir, config):
    cmd = f"cargo build --release --manifest-path {os.path.join(package_dir, 'Cargo.toml')}"
    subprocess.run(cmd, shell=True, check=True)
    
    binary_name = os.path.basename(package_dir)
    src = os.path.join(package_dir, "target", "release", binary_name)
    dst = os.path.join(output_dir, binary_name)
    os.makedirs(output_dir, exist_ok=True)
    os.rename(src, dst)

def build_go(package_dir, output_dir, config):
    cmd = f"go build -o {output_dir} {os.path.join(package_dir, '*.go')}"
    subprocess.run(cmd, shell=True, check=True)

def main():
    config = load_config()
    
    # Generate common messages
    subprocess.run(["python", "generate_msgs.py"], check=True)
    
    build_functions = {
        'cpp': build_cpp,
        'python': build_python,
        'java': build_java,
        'rust': build_rust,
        'go': build_go,
    }
    
    for package in config['packages']:
        package_dir = os.path.join('src', package['name'])
        output_dir = os.path.join('build', package['name'])
        os.makedirs(output_dir, exist_ok=True)
        
        lang = package['language']
        if lang in build_functions:
            build_functions[lang](package_dir, output_dir, config)
        else:
            print(f"Warning: No build function for language '{lang}'")

if __name__ == "__main__":
    main()
