# Copyright (c) 2015 BalaBit
# All Rights Reserved.

pytest_plugins = "pytester"

from  tox_DEBIAN.install import install_debian_deps, __ensure_commands, InvocationError


def test_ensure_command():
    try:
        __ensure_commands(['invalid-command'])
    except InvocationError as error:
        assert error.args[0] == 'Could not find executables: invalid-command'
    else:
        assert False, 'invalid-command should raise an error'


def test_install_debian_deps():
    action = Action()
    install_debian_deps('virtuelenv/path', ['dependency-a', 'dependency-b'], ['--option-a', '--option-b'], action)

    assert action.log == [
        {'command': 'apt-get download', 'details': 'dependency-a, dependency-b'},
    ]

    assert [call['args'] for call in action.calls] == [
        ['apt-get', 'download', '--option-a', '--option-b', 'dependency-a', 'dependency-b'],
    ]


class Action:
    def __init__(self):
        self.log = []
        self.calls = []

    def setactivity(self, command, details):
        self.log.append({'command': command, 'details': details})

    def popen(self, args, *, cwd):
        self.calls.append({'args': args, 'cwd': cwd})
