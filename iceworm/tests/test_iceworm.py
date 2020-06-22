import glob
import os.path

from .. import parsing
from .. import rendering


def test_iceworm():
    file_paths = sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'sql', '*.sql'), recursive=True))
    for file_path in file_paths:
        print(file_path)
        with open(file_path, 'r') as f:
            lines = f.read()

        for line in lines.split(';'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue

            print(line)

            node = parsing.parse_statement(line + ';')
            print(node)

            rendered = rendering.render(node)
            print(rendered)

            reparsed = parsing.parse_statement(rendered + ';')
            assert reparsed == node

            print()
