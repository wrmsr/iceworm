from omnibus import argparse as oap
from omnibus.bootstrap import Bootstrap


class Main(oap.Cli):

    @oap.command()
    def web(self):
        from .web import main
        main()


def main():
    with Bootstrap():
        Main()()


if __name__ == '__main__':
    main()
