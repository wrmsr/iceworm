from omnibus import argparse as oap
from omnibus.bootstrap import Bootstrap


class Main(oap.Cli):

    @oap.command()
    def run(self):
        print('run')


def main():
    with Bootstrap():
        Main()()


if __name__ == '__main__':
    main()
