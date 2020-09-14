from .. import eval as ev
from .. import nodes as no


def test_eval():
    q = no.Select(
        [
            no.AllSelectItem(),
        ],
        [
            no.Table(
                no.QualifiedNameNode.of(['t0'])),
        ],
        no.BinaryExpr(
            no.QualifiedNameNode.of(['id']),
            no.BinaryOp.EQ,
            no.Integer(2)),
    )

    print(ev.StmtEvaluator().eval(q))


def test_rels():
    q = no.Select(
        [
            no.AllSelectItem()
        ],
        [
            no.Join(
                no.Table(
                    no.QualifiedNameNode.of(['t0'])),
                no.JoinType.DEFAULT,
                no.Table(
                    no.QualifiedNameNode.of(['t1'])),
            )
        ]
    )

    print(ev.StmtEvaluator().eval(q))
