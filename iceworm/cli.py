import argparse

from omnibus import properties


def _cmd(cmds):
    def inner(fn):
        name = fn.__name__
        if not name.startswith('cmd_'):
            raise NameError(name)
        parser = cmds.add_parser(name[4:].replace('_', '-'))
        parser.set_defaults(fn=fn)
        return fn

    return inner


class Cli:

    def __init__(self, raw_args=None) -> None:
        super().__init__()

        self._raw_args = raw_args

    parser = argparse.ArgumentParser()

    @properties.cached
    def args(self):
        return self.parser.parse_args(self._raw_args)

    cmds = parser.add_subparsers()

    @_cmd(cmds)
    def cmd_run(self) -> None:
        print('hi')

    def run(self) -> None:
        fn = getattr(self.args, 'fn', None)
        if fn is None:
            self.parser.print_help()
            return

        fn(self)


def main():
    Cli().run()


if __name__ == '__main__':
    main()
