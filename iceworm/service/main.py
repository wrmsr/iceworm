from omnibus import argparse as oap
from omnibus import logs


class Main(oap.Cli):

    @oap.command()
    def run(self):
        print('run')


def main():
    logs.configure_standard_logging()
    Main()()


if __name__ == '__main__':
    main()
