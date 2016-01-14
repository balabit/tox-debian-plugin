# Copyright (c) 2015 BalaBit
# All Rights Reserved.

import sys
from codecs import getwriter

from tox import hookimpl

from .install import install_debian_deps, InvocationError


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
def tox_testenv_install_deps(venv, action):
    action.setactivity('debian_deps', 'install')

    old_stdout, sys.stdout = sys.stdout, getwriter('utf8')(sys.stdout)

    try:
        install_debian_deps(
            str(venv.path),
            __strip_list(venv.envconfig.debian_deps),
            __strip_list(venv.envconfig.apt_opts),
            action
        )
    except InvocationError as error:
        venv.status = str(error)
    finally:
        sys.stdout = old_stdout


def __strip_list(lst):
    return [item.strip() for item in lst]
