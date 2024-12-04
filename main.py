import argparse
import os
from Assembler import Assembler
from Interpreter import Interpreter

if __name__ == "__main__":
    mode = 0
    if mode == 0:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i')
        parser.add_argument('-b')
        parser.add_argument('-l')
        parser.add_argument('-o')
        parser.add_argument('-r', default='0-127')

        args = parser.parse_args()
        program_file = args.i
        bin_output = args.b
        log_file = args.l
        result = args.o
        boundaries = args.r
        l_bound = int(boundaries.split('-')[0])
        r_bound = int(boundaries.split('-')[1])
        sol = Assembler(program_file, log_file, bin_output)
        sol.main()
        interpreter = Interpreter(bin_output, result, l_bound, r_bound)
        interpreter.run()
    elif mode == 1:
        program_file = "script.txt"
        bin_output = "assembler.bin"
        log_file = "logs.xml"
        result = "result.xml"
        sol = Solution(program_file, log_file, bin_output)
        sol.main()
        interpreter = Interpreter(bin_output, result, 10, 24)
        interpreter.run()