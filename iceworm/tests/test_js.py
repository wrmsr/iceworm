import io

from omnibus import iterables as it
import pytest

from .. import js


@pytest.mark.xfail()
def test_fallback_js(tmpdir):
    loop = js.build_loop('function(s){ return s + "!" }')
    proc = js.launch_node(loop)

    lines = it.cut_lines()(iter(io.TextIOWrapper(proc.stdout).readline, ''))

    proc.stdin.write(b'"abc"\n')
    proc.stdin.write(b'"def"\n')
    proc.stdin.write(b'"ghi"\n')
    proc.stdin.flush()
    proc.stdin.close()

    print(list(lines))

    rc = proc.wait()
    print(rc)
