# Copyright (c) 2015 BalaBit
# All Rights Reserved.

import fnmatch
import py

from tempfile import mkdtemp
from shutil import rmtree
from os import listdir, walk
from os.path import curdir, isdir, join as path_join
from collections import Sequence


def install_debian_deps(path, deps, opts, action):
    if not deps:
        return

    __ensure_commands(['apt-get', 'dpkg', 'cp'])

    tmp_dir = mkdtemp(prefix='dpkg-')

    try:
        action.setactivity('apt-get download', ', '.join(deps))
        action.popen(['apt-get', 'download'] + opts + deps, cwd=tmp_dir)
        packages = fnmatch.filter(listdir(tmp_dir), '*.deb')

        for package in packages:
            action.setactivity('dpkg extract', package)
            action.popen(['dpkg', '--vextract', package, curdir], cwd=tmp_dir)

        tmp_usr = path_join(tmp_dir, 'usr')
        if isdir(tmp_usr):
            action.setactivity('copy', ', '.join(__iter_files(tmp_usr)))
            action.popen(['cp', '-r'] + listdir(tmp_usr) + [path], cwd=tmp_usr)

    finally:
        rmtree(tmp_dir)


def __iter_files(root):
    root_str_idx = len(root) + 1
    for root, dirs, files in walk(root):
        relative_root = root[root_str_idx:]
        for name in files:
            yield path_join(relative_root, name)


def __ensure_commands(commands):
    missing = [command for command in commands if py.path.local.sysfind(command) is None]
    if missing:
        raise InvocationError('Could not find executables: {}'.format(', '.join(missing)))


class InvocationError(Exception):
    pass
