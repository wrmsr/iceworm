import io
import os.path
import subprocess
import textwrap

from omnibus import iterables as it
import pytest


@pytest.mark.xfail()
def test_fallback_js(tmpdir):
    def build_loop(func: str, setup: str = '') -> str:
        return textwrap.dedent(f"""
            {setup}
            (function(fn) {{
              const readline = require('readline');
              async function run() {{
                const lines = readline.createInterface({{
                  input: process.stdin,
                  crlfDelay: Infinity
                }});
                for await (const line of lines) {{
                  process.stdout.write(JSON.stringify(fn(JSON.parse(line))) + '\\n');
                }}
              }}
              return run
            }})({func})()
        """)

    loop = build_loop('function(s){ return s + "!" }')
    loop_path = os.path.join(str(tmpdir), 'loop.js')
    with open(loop_path, 'w') as f:
        f.write(loop)

    proc = subprocess.Popen(
        ['node', loop_path],
        bufsize=1024 * 1024,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    lines = it.cut_lines()(iter(io.TextIOWrapper(proc.stdout).readline, ''))

    proc.stdin.write(b'"abc"\n')
    proc.stdin.write(b'"def"\n')
    proc.stdin.write(b'"ghi"\n')
    proc.stdin.flush()
    proc.stdin.close()

    print(list(lines))

    rc = proc.wait()
    print(rc)
