from tox import hookimpl

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
