"""
TODO:
 - https://crates.io/crates/rusty_v8
"""
import os
import subprocess
import tempfile
import textwrap
import typing as ta


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


def launch_node(body: str, *, tag: ta.Optional[str] = None) -> subprocess.Popen:
    fd, path = tempfile.mkstemp((('-' + tag) if tag is not None else '') + '.js')
    os.close(fd)

    with open(path, 'w') as f:
        f.write(body)

    return subprocess.Popen(
        ['node', path],
        bufsize=1024 * 1024,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
