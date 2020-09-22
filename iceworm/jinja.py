"""
TODO:
 - https://github.com/kolypto/j2cli/blob/master/j2cli
"""
import logging
import sys

from omnibus import argparse as oap
from omnibus import logs
import jinja2


log = logging.getLogger(__name__)


class Cli(oap.Cli):

    @oap.command(
        oap.arg('file'),
    )
    def render(self) -> None:
        if self.args.file == '-':
            buf = sys.stdin.read()
        elif self.args.file:
            with open(self.args.file, 'r') as f:
                buf = f.read()
        else:
            raise ValueError('Specify file')

        tmpl = jinja2.Template(buf)
        out = tmpl.render()
        print(out)


def main():
    logs.configure_standard_logging(logging.INFO)
    Cli()()


if __name__ == '__main__':
    main()
