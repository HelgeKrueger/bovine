from glob import glob


def make_link(filename):
    short = filename.split("/")[-1]
    return f"[{short}]({filename})"


all_tests = glob("../tests/**/*.py", recursive=True)

tests = {}
for name in all_tests:
    with open(name, "r") as f:
        tests[name] = f.read()

with open("specification_template.md", "r") as f:
    with open("specification.md", "w") as fw:
        for line in f:
            fw.write(line)
            if line.startswith("####"):
                key = line[5:-1]
                for name, content in tests.items():
                    if key in content:
                        fw.write(make_link(name))
