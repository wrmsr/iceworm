from .. import eval as ev
from .. import nodes as no


def test_eval():
    e = ev.StmtEvaluator()
    q = no.Select(
        [
            no.AllSelectItem(),
        ],
        [
            no.Table(
                no.QualifiedNameNode.of(['t'])),
        ],
        no.BinaryExpr(
            no.QualifiedNameNode.of(['id']),
            no.BinaryOp.EQ,
            no.Integer(2)),
    )
    print(e.eval(q))
