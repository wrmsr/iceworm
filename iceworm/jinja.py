"""
TODO:
 - https://github.com/kolypto/j2cli/blob/master/j2cli
"""
import logging

from omnibus import argparse as oap
from omnibus import logs
import jinja2  # noqa


log = logging.getLogger(__name__)


class Cli(oap.Cli):

    @oap.command()
    def render(self) -> None:
        pass


def main():
    logs.configure_standard_logging(logging.INFO)
    Cli()()


if __name__ == '__main__':
    main()
