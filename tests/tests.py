import pytest
from main import Solution, Interpreter


def test_const():
    sol = Solution("test_const.txt", "test_logs.xml", "test_const.bin")
    sol.main()
    intr = Interpreter("test_const.bin", "test_const.xml")
    intr.run()
    with open("test_const.xml", 'r') as f:
        lines = f.readlines()
    assert lines[1] == '\t<b0>4</b0>\n' and lines[2] == '\t<b1>10</b1>\n'

def test_move():
    sol = Solution("test_move.txt", "test_logs.xml", "test_move.bin")
    sol.main()
    intr = Interpreter("test_move.bin", "test_move.xml")
    intr.run()
    with open("test_move.xml", 'r') as f:
        lines = f.readlines()
    assert lines[1] == '\t<b0>10</b0>\n' and lines[2] == '\t<b1>11</b1>\n' and lines[3] == '\t<b10>11</b10>\n'
    
def test_write():
    sol = Solution("test_write.txt", "test_logs.xml", "test_write.bin")
    sol.main()
    intr = Interpreter("test_write.bin", "test_write.xml")
    intr.run()
    with open("test_write.xml", 'r') as f:
        lines = f.readlines()
    assert lines[3] == '\t<b10>5</b10>\n' and lines[4] == '\t<b11>10</b11>\n'