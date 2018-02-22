import sys
from parse_data import Parser
from check_consistency import Consistency


def checker(history_file):
    parser = Parser()
    check = Consistency()
    
    with open(history_file) as history:
        for line in history:
            if not parser.parse_data(line):
                continue
            parse_dict = parser.parse_data(line)
            check.consistency(parse_dict)

checker(sys.argv[1])
