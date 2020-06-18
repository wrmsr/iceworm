import glob
import os.path

from .. import parsing
from .. import rendering


def test_iceworm():
    for file_path in glob.glob(os.path.join(os.path.dirname(__file__), 'sql', '*.sql'), recursive=True):
        print(file_path)
        with open(file_path, 'r') as f:
            lines = f.read()

        for line in lines.splitlines():
            line = line.strip()
            if not line or line.startswith('--'):
                continue

            print(line)

            node = parsing.parse_statement(line)
            print(node)

            rendered = rendering.render(node)
            print(rendered)

            print()
