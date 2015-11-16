import sys
import py

from codecs import getwriter
from glob import glob
from tempfile import mkdtemp
from shutil import rmtree, move
from os import remove
from os.path import join as path_join

from tox import hookimpl
from tox import exception

@hookimpl
def tox_addoption(parser):
    parser.add_testenv_attribute_obj(DebianDepOption())


class DebianDepOption:
    name = "debian_deps"
    type = "line-list"
    help = "debian package dependency"
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
    deps = ' '.join(venv.envconfig.debian_deps)
    if not deps:
        return

    toxinidir = venv.envconfig.config.toxinidir

    old_stdout = sys.stdout
    sys.stdout = getwriter('utf8')(sys.stdout)

    tmp_dir = mkdtemp(prefix='dpkg-')
    venv._pcall(['apt-get', 'download', deps], cwd=toxinidir, action=action)
    packages = glob('*.deb')
    venv._pcall(['dpkg', '-x'] + packages + [tmp_dir], cwd=toxinidir, action=action)
    tmp_usr = glob('{}/usr/*'.format(tmp_dir))
    venv._pcall(['cp', '-r'] + tmp_usr + [str(venv.path)], cwd=toxinidir, action=action)

    sys.stdout = old_stdout

    for package in packages:
        remove(package)
    rmtree(tmp_dir)
