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
            try:
                assert reparsed == node
            except Exception:
                """
# node.ctes[1].select.select.where, reparsed.ctes[1].select.select.where
# select * from a where p.u_i is null and not (d.b_u = 'p' and p.u_i is null and c.u_i is null);
# select * from a where p.u_i is null and not ((d.b_u = 'p') and p.u_i is null) and c.u_i is null
0 = {BinaryExpr} BinaryExpr(left=IsNull(value=QualifiedName(parts=[Identifier(name='p'), Identifier(name='u_i')]), not_=False), op=<BinaryOp.AND: 'and'>, right=UnaryExpr(op=<UnaryOp.NOT: 'not'>, value=BinaryExpr(left=BinaryExpr(left=BinaryExpr(left=QualifiedName(parts=[Ide
1 = {BinaryExpr} BinaryExpr(left=BinaryExpr(left=IsNull(value=QualifiedName(parts=[Identifier(name='p'), Identifier(name='u_i')]), not_=False), op=<BinaryOp.AND: 'and'>, right=UnaryExpr(op=<UnaryOp.NOT: 'not'>, value=BinaryExpr(left=BinaryExpr(left=QualifiedName(parts=[Ide
                """
                raise

            print()
