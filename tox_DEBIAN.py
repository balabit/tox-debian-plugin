# Copyright (c) 2015 BalaBit
# All Rights Reserved.

import sys
import fnmatch
import py

from codecs import getwriter
from tempfile import mkdtemp
from shutil import rmtree
from os import listdir, walk
from os.path import curdir, join as path_join

from tox import hookimpl
from tox import exception

@hookimpl
def tox_addoption(parser):
    parser.add_testenv_attribute_obj(DebianDepOption())
    parser.add_testenv_attribute_obj(AptOptOption())


class DebianDepOption:
    name = "debian_deps"
    type = "line-list"
    help = "debian package dependency"
    default = ()

    def postprocess(self, testenv_config, value):
        return value


class AptOptOption:
    name = "apt_opts"
    type = "line-list"
    help = "options to pass to apt-get"
    default = ()

    def postprocess(self, testenv_config, value):
        return value


@hookimpl
def tox_setupenv(session, venv):
    action = session.newaction(venv, "install_debian_deps", venv.envconfig.envdir)

    with action:
        try:
            install_debian_deps(venv, action)
        except exception.InvocationError as error:
            venv.status = str(error)


def install_debian_deps(venv, action):
    deps = __strip_list(venv.envconfig.debian_deps)

    if not deps:
        return

    __ensure_commands(['apt-get', 'dpkg'])

    opts = __strip_list(venv.envconfig.apt_opts)

    toxinidir = venv.envconfig.config.toxinidir

    old_stdout = sys.stdout
    sys.stdout = getwriter('utf8')(sys.stdout)

    tmp_dir = mkdtemp(prefix='dpkg-')

    try:
        action.setactivity('apt-get download', ', '.join(deps))
        action.popen(['apt-get', 'download'] + opts + deps, cwd=tmp_dir)
        packages = fnmatch.filter(listdir(tmp_dir), '*.deb')

        for package in packages:
            action.setactivity('dpkg extract', package)
            action.popen(['dpkg', '--vextract', package, curdir], cwd=tmp_dir)

        tmp_usr = path_join(tmp_dir, 'usr')
        action.setactivity('copy', ', '.join(__list_files(tmp_usr)))
        action.popen(['cp', '-r'] + listdir(tmp_usr) + [str(venv.path)], cwd=tmp_usr)

    finally:
        sys.stdout = old_stdout

        rmtree(tmp_dir)


def __strip_list(lst):
    return [item.strip() for item in lst]


def __list_files(root):
    root_str_idx = len(root) + 1
    for root, dirs, files in walk(root):
        relative_root = root[root_str_idx:]
        for name in files:
            yield path_join(relative_root, name)


def __ensure_commands(commands):
    missing = [command for command in commands if py.path.local.sysfind(command) is None]
    if missing:
        raise exception.InvocationError('Could not find executables: {}'.format(', '.join(missing)))
