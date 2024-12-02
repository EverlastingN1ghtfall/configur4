class Solution:
    def __init__(self, input_file: str, log_file: str, output_file: str):
        self.namespace: dict = {}
        self.input_file: str = input_file
        self.log_file: str = log_file
        self.output_file = output_file
        self.free_address: int = -1
        self.logs: list[str] = []

    def paginate(self, num: int, length: int) -> str:
        return "0" * (length - len(bin(num)[2:])) + bin(num)[2:]

    def log(self, text: dict, method="last") -> None:
        if method == "last":
            self.logs.append(text)
        elif method == "append":
            self.logs.update(text)

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



if __name__ == "__main__":
    sol = Solution()