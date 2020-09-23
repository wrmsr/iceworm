import fnmatch
import os
import sys
import warnings

import setuptools.command.install

import distutils.cmd
import distutils.log


if sys.version_info < (3, 7):
    raise EnvironmentError('python >= 3.7 required')


warnings.filterwarnings(
    'ignore',
    message=r"Normalizing '[^'-]+-[^'-]+' to '[^'-]+\.[^'-]+'",
    module=r'setuptools\.dist',
)


PROJECT = 'iceworm'

BASE_DIR = os.path.dirname(__file__)
ABOUT = {}


def _read_about():
    with open(os.path.join(BASE_DIR, PROJECT, '__about__.py'), 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ABOUT)


_read_about()


EXCLUDED_STATIC_FILE_PATHS = [
    '*.py',
    '*/__pycache__/*',
    '*/tests/*',
]


def _get_static_files(path):
    return [
        filepath
        for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True)
        for filename in filenames
        for filepath in [os.path.join(dirpath, filename)]
        if not any(fnmatch.fnmatch(filepath, pat) for pat in EXCLUDED_STATIC_FILE_PATHS)
    ]


PACKAGE_DATA = [
] + _get_static_files(PROJECT)


INSTALL_REQUIRES = [

    'Jinja2>=2.11',
    'protobuf>=3.13',
    'PyYAML>=5.3',
    'SQLAlchemy>=1.3',

    # @omnibus-dep@
    'omnibus @ git+https://github.com/wrmsr/omnibus@4ce8f94e5176577bed1f19421fc9b0447d045957',

]

EXTRAS_REQUIRE = {
}

EXT_MODULES = [
]


BREW_DEPS = {
    'graphviz',
    'libyaml',
}


class SysdepsCommand(distutils.cmd.Command):
    description = 'install sysdeps'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce('Installing sysdeps')

        if sys.platform == 'darwin':
            import shutil
            if not shutil.which('brew'):
                self.announce('brew not found, skipping')
                return

            os.system(f'brew install {" ".join(BREW_DEPS)}')


class CyamlCommand(distutils.cmd.Command):
    description = 'install cyaml'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce('Installing cyaml')

        import tempfile
        dp = tempfile.mkdtemp()

        import os.path
        fp = os.path.join(dp, 'cyaml.tar.gz')

        import urllib.request
        urllib.request.urlretrieve('http://pyyaml.org/download/pyyaml/PyYAML-5.3.1.tar.gz', fp)

        os.system(
            f'cd {dp} && '
            f'{os.path.abspath(sys.executable)} -m pip install cyaml.tar.gz --global-option="--with-libyaml"'
        )


class InstallCommand(setuptools.command.install.install):
    user_options = setuptools.command.install.install.user_options + [
        ('cyaml', None, 'install cyaml'),
        ('sysdeps', None, 'install sysdeps'),
    ]

    def initialize_options(self):
        super().initialize_options()

        self.sysdeps = 0
        self.cyaml = 0

        if sys.platform == 'darwin':
            import subprocess
            pid_chain = []
            cur_pid = int(os.getpid())
            while cur_pid != 1:
                buf = subprocess.check_output(f'ps -o pid=,ppid=,command= -p {cur_pid}'.split(' ')).decode('utf-8')
                pid_str, _, buf = buf.strip().partition(' ')
                ppid_str, _, buf = buf.strip().partition(' ')
                if int(pid_str) != cur_pid:
                    raise Exception(f'{pid_str} != {cur_pid}')
                tup = (int(ppid_str), buf)
                pid_chain.append(tup)
                cur_pid = tup[0]

            """
            29251 29243 /usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python -u -c import sys, setuptools, tokenize; sys.argv[0] = '/private/var/folders/s7/z0_hyvy14txdpyh8j7j4bljr0000gn/T/pip-req    -build-9ehuvpb0/setup.py'; __file__='/private/var/folders/s7/z0_hyvy14txdpyh8j7j4bljr0000gn/T/pip-req-build-9ehuvpb0/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exe    c')) bdist_wheel -d /private/var/folders/s7/z0_hyvy14txdpyh8j7j4bljr0000gn/T/pip-wheel-84jjswdf
            29243 29235 /usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python -m pip install --no-dependencies /Users/spinlock/src/wrmsr/iceworm/dist/iceworm-0.0.1.dev0.zip
            29235 88867 /usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python /usr/local/Cellar/pipx/0.15.5.1/libexec/bin/pipx install --verbose --force src/wrmsr/iceworm/dist/iceworm-0.0.1.dev0.zi    p
            88867   713 -zsh
            713     1 tmux -2
            29279 29267 /usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python -u -c import sys, setuptools, tokenize; sys.argv[0] = '/private/var/folders/s7/z0_hyvy14txdpyh8j7j4bljr0000gn/T/pip-req    -build-jr3wqzfh/setup.py'; __file__='/private/var/folders/s7/z0_hyvy14txdpyh8j7j4bljr0000gn/T/pip-req-build-jr3wqzfh/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exe    c')) bdist_wheel -d /private/var/folders/s7/z0_hyvy14txdpyh8j7j4bljr0000gn/T/pip-wheel-_u9fhm5c
            29267 29235 /usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python -m pip install /Users/spinlock/src/wrmsr/iceworm/dist/iceworm-0.0.1.dev0.zip
            29235 88867 /usr/local/Cellar/python@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python /usr/local/Cellar/pipx/0.15.5.1/libexec/bin/pipx install --verbose --force src/wrmsr/iceworm/dist/iceworm-0.0.1.dev0.zi    p
            88867   713 -zsh
            713     1 tmux -2
            """

            with open('/tmp/asdf', 'a') as f:
                f.write(repr(pid_chain) + '\n')

            # self.announce('activating pipx extras')

            # self.sysdeps = 1
            # self.cyaml = 1

    def run(self):
        if self.sysdeps:
            self.run_command('sysdeps')
        if self.cyaml:
            self.run_command('cyaml')

        super().run()


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        cmdclass={
            'cyaml': CyamlCommand,
            'install': InstallCommand,
            'sysdeps': SysdepsCommand,
        },

        python_requires=ABOUT['__python_requires__'],
        classifiers=ABOUT['__classifiers__'],

        setup_requires=['setuptools'],

        packages=setuptools.find_packages(
            include=[PROJECT, PROJECT + '.*'],
            exclude=['tests', '*.tests', '*.tests.*'],
        ),
        py_modules=[PROJECT],

        package_data={PROJECT: PACKAGE_DATA},
        include_package_data=True,

        entry_points={
            'console_scripts': [
                f'{PROJECT} = {PROJECT}.cli:main',
            ],
        },

        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,

        ext_modules=EXT_MODULES,
    )
