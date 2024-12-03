import argparse


class Solution:
    def __init__(self, input_file: str, log_file: str, output_file: str):
        self.namespace: dict = {}
        self.input_file: str = input_file
        self.log_file: str = log_file
        self.output_file: str = output_file
        self.free_address: int = -1
        self.logs: list = []
        open(output_file, 'wb').close()
        with open(self.input_file, 'r') as f:
            self.lines = f.readlines()

    def paginate(self, num: int, length: int) -> str:
        return "0" * (length - len(bin(num)[2:])) + bin(num)[2:]

    def log(self, text: dict, method="last") -> None:
        if method == "last":
            self.logs.append(text)
        elif method == "append":
            self.logs[-1].update(text)

    def get_free_adress(self) -> int:
        self.free_address += 1
        return self.free_address

    def add_var_to_namespace(self, var: str) -> int:
        address = self.get_free_adress()
        self.namespace[var] = address
        return address

    def output_binary(self, bytes: bytes) -> None:
        logged = ", ".join(["0x" + hex(i)[2:].ljust(2, '0') for i in bytes])
        self.log({"bin": logged}, method='append')

        with open(self.output_file, 'ab') as f:
            f.write(bytes)

    def constant_handler(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})
        a, b, c = self.paginate(a, 7), self.paginate(b, 7), self.paginate(c, 28)
        all_combined = a + b + c
        fixed_zeros = all_combined + '0' * (48 - len(all_combined))
        return int(fixed_zeros, 2).to_bytes(6)

    def read_handler(self, a: int, b: int, c: int, d: int) -> bytes:
        self.log({"A": a, "B": b, "C": c, "D": d})
        a, b, c, d = self.paginate(a, 7), self.paginate(b, 7), self.paginate(c, 7), self.paginate(d, 6)
        all_combined = a + b + c + d
        fixed_zeroes = all_combined + '0' * (48 - len(all_combined))
        return int(fixed_zeroes, 2).to_bytes(6)

    def write_handler(self, a: int, b: int, c: int) -> bytes:
        self.log({"A": a, "B": b, "C": c})
        a, b, c = self.paginate(a, 7), self.paginate(b, 7), self.paginate(c, 13)
        all_combined = a + b + c
        fixed_zeros = all_combined + '0' * (48 - len(all_combined))
        return int(fixed_zeros, 2).to_bytes(6)

    def mult_handler(self, a: int, b: int, c: int, d: int) -> bytes:
        self.log({"A": a, "B": b, "C": c, "D": d})
        a, b, c, d = self.paginate(a, 7), self.paginate(b, 7), self.paginate(c, 7), self.paginate(d, 7)
        all_combined = a + b + c + d
        fixed_zeroes = all_combined + '0' * (48 - len(all_combined))
        return int(fixed_zeroes, 2).to_bytes(6)

    def log_dump(self):
        with open(self.log_file, 'w') as f:
            f.write("<logs>\n")
            for i in self.logs:
                for j in i.keys():
                    f.write(f"\t<{j}>{i[j]}</{j}>\n")
            f.write("</logs>")

    def main(self):
        for line in self.lines:
            if line.startswith("const"):
                _, var, value = line.split()

                if var not in self.namespace.keys():
                    address_to = self.add_var_to_namespace(var)
                else:
                    address_to = self.namespace[var]

                binary = self.constant_handler(36, address_to, int(value))
                self.output_binary(binary)

            elif line.startswith("move"):
                _, TO, FROM, shift = line.split()

                if FROM not in self.namespace.keys():
                    raise Exception(f"Variable {FROM} not declaired.")
                if TO not in self.namespace.keys():
                    address_to = self.add_var_to_namespace(TO)
                else:
                    address_to = self.namespace[TO]

                address_from = self.namespace[FROM]
                binary = self.read_handler(58, address_to, address_from, int(shift))
                self.output_binary(binary)

            elif line.startswith("write"):
                _, FROM, TO = line.split()

                if FROM not in self.namespace.keys():
                    raise Exception(f"Variable {FROM} not declaired.")
                if TO not in self.namespace.keys():
                    address_to = self.add_var_to_namespace(TO)
                else:
                    address_to = self.namespace[TO]

                address_from = self.namespace[FROM]
                binary = self.write_handler(25, address_from, address_to)
                self.output_binary(binary)

            elif line.startswith("mult"):
                _, var, mult2, mult1 = line.split()

                if mult1 not in self.namespace.keys():
                    raise Exception(f"Variable {mult1} not declaired.")
                if mult2 not in self.namespace.keys():
                    raise Exception(f"Variable {mult2} not declaired.")
                if var not in self.namespace.keys():
                    address = self.add_var_to_namespace(var)
                else:
                    address = self.namespace[var]

                address_mult1 = self.namespace[mult1]
                address_mult2 = self.namespace[mult2]
                binary = self.mult_handler(32, address, address_mult2, address_mult1)
                self.output_binary(binary)

        self.log_dump()


class Interpreter:
    def __init__(self, binary_path: str, result_path: str):
        with open(binary_path, 'rb') as f:
            self.bin = f.read()
        self.memory = [0] * 128
        self.result_file = result_path
        open(self.result_file, 'w').close()

    def run(self):
        bits = bin(int.from_bytes(self.bin))[2:]
        bits = '0' * (48 - len(bits) % 48) + bits
        commands = [bits[i:i+48] for i in range(0, len(bits), 48)]

        for command in commands:
            op = command[0:7]
            if op == bin(36)[2:].rjust(7, '0'):
                new_var = int(command[7:14], 2)
                val = int(command[14:42], 2)
                self.memory[new_var] = val
            elif op == bin(58)[2:].rjust(7, '0'):
                new_var = int(command[7:14], 2)
                address_c = int(command[14:21], 2)
                shift = int(command[21:27], 2)
                self.memory[new_var] = self.memory[address_c + shift]
            elif op == bin(25)[2:].rjust(7, '0'):
                address = int(command[7:14], 2)
                new_var = int(command[14:27], 2)
                self.memory[new_var] = self.memory[address]
            elif op == bin(32)[2:].rjust(7, '0'):
                new_var = int(command[7:14], 2)
                address1 = int(command[14:21], 2)
                address2 = int(command[21:28], 2)
                self.memory[new_var] = self.memory[address1] * self.memory[address2]

        self.write_log()

    def write_log(self):
        with open(self.result_file, 'w') as f:
            print("not null elements:", 128 - self.memory.count(0))
            f.write("<logs>\n")
            for i in range(len(self.memory)):
                f.write(f"\t<{bin(i)[1:]}>{self.memory[i]}</{bin(i)[1:]}>\n")
            f.write("</logs>")



if __name__ == "__main__":
    mode = 1
    if mode == 0:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i')
        parser.add_argument('-b')
        parser.add_argument('-l')
        parser.add_argument('-o')

        args = parser.parse_args()
        program_file = args.i
        bin_output = args.b
        log_file = args.l
        result = args.o
        sol = Solution(program_file, log_file, bin_output)
        sol.main()
        interpreter = Interpreter(bin_output, result)
        interpreter.run()
    elif mode == 1:
        program_file = "script.txt"
        bin_output = "assembler.bin"
        log_file = "logs.xml"
        result = "result.xml"
        sol = Solution(program_file, log_file, bin_output)
        sol.main()
        interpreter = Interpreter(bin_output, result)
        interpreter.run()