import os
import re
from collections import defaultdict

PROJECT_PATHS = [
    "./log4j-api/src/main/java",
    "./log4j-core/src/main/java"
]

IMPORT_REGEX = re.compile(r'^\s*import\s+([a-zA-Z0-9_.]+);')

dependencies = defaultdict(set)
reverse_deps = defaultdict(set)

def get_java_files(root):
    java_files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".java"):
                java_files.append(os.path.join(dirpath, f))
    return java_files

def extract_imports(file_path):
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = IMPORT_REGEX.match(line)
                if match:
                    imp = match.group(1)
                    if imp.startswith("java.") or imp.startswith("javax."):
                        continue

                    imports.add(imp)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return imports

def build_graph(files):
    for file in files:
        imports = extract_imports(file)

        dependencies[file] = imports

        for imp in imports:
            reverse_deps[imp].add(file)

def analyze():
    fan_out = {f: len(deps) for f, deps in dependencies.items()}
    fan_in = {f: len(reverse_deps.get(f, [])) for f in dependencies.keys()}

    most_dependent = sorted(fan_out.items(), key=lambda x: x[1], reverse=True)
    least_dependent = sorted(fan_out.items(), key=lambda x: x[1])
    most_used = sorted(fan_in.items(), key=lambda x: x[1], reverse=True)

    print(" \nTOP 10 MOST DEPENDENT FILES ")
    for f, v in most_dependent[:10]:
        print(v, "->", os.path.basename(f))

    print("\n TOP 10 LEAST DEPENDENT FILES ")

    for f, v in least_dependent[:10]:
        print(v, "->", os.path.basename(f))

    print("\n TOP 10 MOST USED FILES ")

    for f, v in most_used[:10]:
        print(v, "->", os.path.basename(f))

if __name__ == "__main__":
    all_files = []

    for path in PROJECT_PATHS:
        all_files.extend(get_java_files(path))

    print(f"Total Java files analyzed: {len(all_files)}")

    build_graph(all_files)
    analyze()