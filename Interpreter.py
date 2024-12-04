class Interpreter:
    def __init__(self, binary_path: str, result_path: str, l_boundary: int = 0, r_boundary: int = 127):
        with open(binary_path, 'rb') as f:
            self.bin = f.read()
        self.l = l_boundary
        self.r = r_boundary
        self.memory = [0] * (self.r - self.l + 1)
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
            print("not null elements:", (self.r - self.l + 1) - self.memory.count(0))
            f.write("<logs>\n")
            for i in range(len(self.memory)):
                it = i + self.l
                f.write(f"\t<{bin(it)[1:]}>{self.memory[i]}</{bin(it)[1:]}>\n")
            f.write("</logs>")