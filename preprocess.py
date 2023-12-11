import re


class PreProcess:
    def __init__(self, full_path=None, lines=[]):
        self.path = full_path
        self.lines = lines
        self.name_conversion = {}
        self.all_symptoms = set()
        self.counter = 0

    def divide(self, line):
        return re.split("“(?:S|C)\s*((?:(?:\w|\*|-)*\s*)*)”", line)

    def process(self, line):
        split_list = re.split("“((?:S|C)\s*(?:(?:\w|\*|-)*\s*)*)”", line)

        for i in range(1, len(split_list), 2):
            current_string = split_list[i]
            aux = current_string.split()
            c_or_s, name = aux[0], " ".join(aux[1:])

            if name in self.name_conversion:
                split_list[i] = f"“{c_or_s} {self.name_conversion[name]}”"

                if c_or_s == "S":
                    self.all_symptoms.add(str(self.name_conversion[name]))

            else:
                self.name_conversion[name] = self.counter
                self.name_conversion[self.counter] = name

                split_list[i] = f"“{c_or_s} {self.counter}”"

                if c_or_s == "S":
                    self.all_symptoms.add(str(self.counter))

                self.counter += 1

        return "".join(split_list)

    def execute(self):
        if self.path:
            with open(self.path, "r", encoding="utf8") as f:
                self.lines = f.readlines()

        num_lines = len(self.lines)

        for i in range(num_lines):
            self.lines[i] = self.process(self.lines[i])

        return self.lines


if __name__ == "__main__":
    a = PreProcess("teste2.txt")
    # print(a.process("“C causa 1”, (“S sintoma 1”; “S sintoma 2”), 0.5"))
    a.execute()
    for i in a.lines:
        print(i)

    print(a.all_symptoms)
