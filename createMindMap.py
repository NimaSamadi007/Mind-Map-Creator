# Based on https://graphviz.org/Gallery/twopi/happiness.html
import sys
import subprocess

class Subject:
    def __init__(self, file_path, rank_sep=10):
        self.rank_sep = rank_sep
        self.file_path = file_path
        self.subject = self._get_subject()
        self.factors = self._get_factors()
        self.out_file = open(f"{self.subject}.dot", "w")

    def _get_subject(self):
        file_name_with_pre = self.file_path.split("/")[-1]
        subject = file_name_with_pre.split(".")[0]
        return subject

    def _get_factors(self):
        try:
            with open(self.file_path, 'r') as f:
                factors = f.readlines()
                return factors
        except FileNotFoundError:
            print("File not found! Try again...")
            sys.exit(1)

    def _write_base_file(self):
        base_file = "graph base {" + "\n\t" \
                    'labelloc="t"' + "\n\t" \
                    'fontname="URW Chancery L, Apple Chancery, Comic Sans MS, cursive"' + "\n\t"\
                    f"layout=twopi; graph [ranksep={self.rank_sep}];" + "\n\t"\
                    'edge [penwidth=5 color="#f0f0ff"]' + "\n\t"\
                    'node [fontname="URW Chancery L, Apple Chancery, Comic Sans MS, cursive"]' + "\n\t"\
                    'node [style="filled" penwidth=0 fillcolor="#f0f0ffA0" fontcolor=indigo]' + "\n\t"\
                    f'{self.subject} [fontsize=50 fontcolor=goldenrod]' + "\n\t"\
                    'node [fontsize=32]\n'
            
        self.out_file.write(base_file)

    def write_dot_file(self):
        self._write_base_file()

        # Write graph structure to file
        self.out_file.write(f"\t{self.subject} -- {{\n")
        for i in range(len(self.factors)):
            self.out_file.write(f"\t\tfac{i+1}\n")
        self.out_file.write("\t}\n")

        # Write labels:
        for i in range(len(self.factors)):
            label = f'\tfac{i+1} [label="{self.factors[i].strip()}"]\n'
            self.out_file.write(label)
        self.out_file.write('\tc [label="© 2020-2022 Costa Shulyupin" fontsize=12 shape=plain style="" fontcolor=gray]\n')
        self.out_file.write("}\n")

        print(f"{self.subject}.dot file saved!")
        self.out_file.close()

    def create_image(self):
        subprocess.check_call(f"dot -Tpng {self.subject}.dot -o {self.subject}.png", shell=True)
        print(f"{self.subject}.png file saved!")        

    def __del__(self):
        try:
            self.out_file.close()
        except IOError:
            print("Unable to close file!")
        except AttributeError:
            # File is not created in first place
            pass


if __name__ == "__main__":
    print("Input rank sep parameter: ", end="")
    rank_sep = int(input())
    print("Input file path: ", end="")
    file_path = input()

    sub = Subject(file_path, rank_sep)
    sub.write_dot_file()
    sub.create_image()
 