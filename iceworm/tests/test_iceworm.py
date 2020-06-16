import glob
import os.path

from .. import parsing


def test_iceworm():
    for file_path in glob.glob(os.path.join(os.path.dirname(__file__), 'sql', '*.sql'), recursive=True):
        print(file_path)
        with open(file_path, 'r') as f:
            lines = f.read()

        for line in lines.splitlines():
            print(line)
            node = parsing.parse_statement(line)
            print(node)
