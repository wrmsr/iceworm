import os.path
import tempfile

from omnibus import dataclasses as dc

from .. import gen


class MyProto(dc.Pure):
    name: str
    val: int


def test_gen():
    dp = tempfile.mkdtemp()

    g = gen.Gen(
        objs=[MyProto],
        output_file_path=os.path.join(dp, 'icewormtest.proto'),
        compile=True,
    )

    print(g.gen())


def test_compiled():
    from .._gen import iceworm_pb2 as ip

    t = ip._Stub()
    t.data = 'barf'

    print(t)

    s = t.SerializeToString()
    print(s)

    t2 = ip._Stub()
    t2.ParseFromString(s)
    assert t == t2
