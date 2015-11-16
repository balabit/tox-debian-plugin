import py
from datetime import datetime

from tox import hookimpl
from tox import exception

@hookimpl
def tox_addoption(parser):
    with open('/tmp/debug.txt', 'a') as fp:
        print('{} -- tox_addoption'.format(datetime.now()), file=fp)
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
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    self._pcall(argv, cwd=session.envconfig.config.toxinidir, action=action)
    sys.stdout = old_stdout
