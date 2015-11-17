pytest_plugins = "pytester"


def test_invalid_debian_package_name_cannot_be_fetched(cmd, initproj):
    initproj("debian123-0.42", filedefs={
        'tox.ini': '''
            [testenv]
            debian_deps=
              no-such-debian-package=123.42
        '''
    })
    result = cmd.run("tox", )
    result.stdout.fnmatch_lines([
        "E: Unable to locate package no-such-debian-package",
    ])
    assert result.ret


def test_debian_package_will_be_extracted_into_virtual_env(cmd, initproj):
    initproj("debian123-0.56", filedefs={
        'tox.ini': '''
            [testenv]
            debian_deps=
              graphviz
            commands= ls -1 .tox/python/bin
        '''
    })
    result = cmd.run("tox", )
    result.stdout.fnmatch_lines(["dot"])
    assert result.ret == 0


def test_can_extract_multiple_packages(cmd, initproj):
    initproj("debian123-0.56", filedefs={
        'tox.ini': '''
            [testenv]
            debian_deps=
              graphviz
              vim
            commands= ls -1 .tox/python/bin
        '''
    })
    result = cmd.run("tox", )
    assert result.ret == 0
    result.stdout.fnmatch_lines(["dot", "vim*"])


def test_empty_debian_dependency_dont_call_apt_get(cmd, initproj):
    initproj("debian123-0.56", filedefs={
        'tox.ini': '''
            [testenv]
            debian_deps=
        '''
    })
    result = cmd.run("tox", )
    assert 'apt-get' not in result.stdout.str()
    assert result.ret == 0


def test_can_pass_additional_options_to_apt_get(cmd, initproj):
    initproj("debian123-0.56", filedefs={
        'tox.ini': '''
            [testenv]
            apt_opts=
              --no-such-option
            debian_deps=
              graphviz
        '''
    })
    result = cmd.run("tox", )
    result.stdout.fnmatch_lines(["*no-such-option*"])
    assert result.ret
