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
from bellande_parser.bellande_parser import Bellande_Format

def parse_def_file(filename):
    bellande_parser = Bellande_Format()
    content = bellande_parser.parse_bellande(filename)

    structures = {}
    enums = {}
    current_struct = None
    current_enum = None

    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('struct'):
            current_struct = line.split()[1]
            structures[current_struct] = []
            current_enum = None
        elif line.startswith('enum'):
            current_enum = line.split()[1]
            enums[current_enum] = []
            current_struct = None
        elif current_struct:
            field_type, field_name = line.split()
            structures[current_struct].append((field_type, field_name))
        elif current_enum:
            enums[current_enum].append(line)

    return structures, enums

def generate_cpp(structures, enums):
    code = "#pragma once\n\n#include <string>\n#include <vector>\n#include <chrono>\n\nnamespace common_msgs {\n\n"
    
    for enum_name, enum_values in enums.items():
        code += f"enum class {enum_name} {{\n"
        code += ',\n'.join(f"    {value}" for value in enum_values)
        code += "\n};\n\n"

    for struct_name, fields in structures.items():
        code += f"struct {struct_name} {{\n"
        for field_type, field_name in fields:
            if field_type == 'timestamp':
                code += f"    std::chrono::system_clock::time_point {field_name};\n"
            elif field_type.startswith('list<'):
                inner_type = field_type[5:-1]
                code += f"    std::vector<{inner_type}> {field_name};\n"
            else:
                code += f"    {field_type} {field_name};\n"
        code += "};\n\n"

    code += "} // namespace common_msgs\n"
    return code

def generate_python(structures, enums):
    code = "from dataclasses import dataclass\nfrom typing import List\nimport datetime\n\n"

    for enum_name, enum_values in enums.items():
        code += f"class {enum_name}:\n"
        for i, value in enumerate(enum_values):
            code += f"    {value} = {i}\n"
        code += "\n"

    for struct_name, fields in structures.items():
        code += f"@dataclass\nclass {struct_name}:\n"
        for field_type, field_name in fields:
            if field_type == 'timestamp':
                code += f"    {field_name}: datetime.datetime\n"
            elif field_type.startswith('list<'):
                inner_type = field_type[5:-1]
                code += f"    {field_name}: List[{inner_type}]\n"
            else:
                code += f"    {field_name}: {field_type}\n"
        code += "\n"

    return code

def generate_java(structures, enums):
    code = "package common_msgs;\n\nimport java.time.Instant;\nimport java.util.List;\n\npublic class Messages {\n\n"

    for enum_name, enum_values in enums.items():
        code += f"    public enum {enum_name} {{\n"
        code += ',\n'.join(f"        {value}" for value in enum_values)
        code += "\n    }\n\n"

    for struct_name, fields in structures.items():
        code += f"    public static class {struct_name} {{\n"
        for field_type, field_name in fields:
            if field_type == 'timestamp':
                code += f"        public Instant {field_name};\n"
            elif field_type.startswith('list<'):
                inner_type = field_type[5:-1]
                code += f"        public List<{inner_type}> {field_name};\n"
            else:
                code += f"        public {field_type} {field_name};\n"
        code += "    }\n\n"

    code += "}\n"
    return code

def generate_rust(structures, enums):
    code = "use chrono::DateTime;\nuse chrono::Utc;\n\n"

    for enum_name, enum_values in enums.items():
        code += f"pub enum {enum_name} {{\n"
        code += ',\n'.join(f"    {value}" for value in enum_values)
        code += "\n}\n\n"

    for struct_name, fields in structures.items():
        code += f"pub struct {struct_name} {{\n"
        for field_type, field_name in fields:
            if field_type == 'timestamp':
                code += f"    pub {field_name}: DateTime<Utc>,\n"
            elif field_type.startswith('list<'):
                inner_type = field_type[5:-1]
                code += f"    pub {field_name}: Vec<{inner_type}>,\n"
            elif field_type == 'string':
                code += f"    pub {field_name}: String,\n"
            else:
                code += f"    pub {field_name}: {field_type},\n"
        code += "}\n\n"

    return code

def generate_go(structures, enums):
    code = "package common_msgs\n\nimport (\n\t\"time\"\n)\n\n"

    for enum_name, enum_values in enums.items():
        code += f"type {enum_name} int\n\nconst (\n"
        for i, value in enumerate(enum_values):
            code += f"    {value} {enum_name} = iota\n"
        code += ")\n\n"

    for struct_name, fields in structures.items():
        code += f"type {struct_name} struct {{\n"
        for field_type, field_name in fields:
            if field_type == 'timestamp':
                code += f"    {field_name.capitalize()} time.Time\n"
            elif field_type.startswith('list<'):
                inner_type = field_type[5:-1]
                code += f"    {field_name.capitalize()} []{inner_type}\n"
            elif field_type == 'string':
                code += f"    {field_name.capitalize()} string\n"
            else:
                code += f"    {field_name.capitalize()} {field_type}\n"
        code += "}\n\n"

    return code

def main():
    bellande_parser = Bellande_Format()
    
    config = bellande_parser.parse_bellande("project_config.bellande")
    structures, enums = parse_def_file('common_msgs.bellande')
    
    os.makedirs('build/common_msgs', exist_ok=True)

    generators = {
        'cpp': ('common_msgs.hpp', generate_cpp),
        'python': ('common_msgs.py', generate_python),
        'java': ('common_msgs.java', generate_java),
        'rust': ('common_msgs.rs', generate_rust),
        'go': ('common_msgs.go', generate_go),
    }

    for lang in config['languages']:
        if lang in generators:
            filename, generator = generators[lang]
            with open(f'build/common_msgs/{filename}', 'w') as f:
                f.write(generator(structures, enums))
        else:
            print(f"Warning: No generator for language '{lang}'")

if __name__ == "__main__":
    main()
