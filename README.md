# tox_DEBIAN

`tox_DEBIAN.py` is a [tox][tox] plugin which extracts [Debian][deb] packages
into the tox managed virtual environment.

  [tox]: https://testrun.org/tox/latest/
  [deb]: http://www.debian.org/

## Dependency

### Hook dependency

The plugin implements the `tox_setupenv` [pluggy][pluggy] hook,
which is not merged into tox at the time of writing this document (merge
request to be sent soon), but it can be fetched from [GitHub][gh].

  [pluggy]: https://pypi.python.org/pypi/pluggy
  [gh]: https://github.com/nyirog/tox

### External dependency

The plugin uses the `apt-get`, `dpkg` and `cp` tools.

### Test dependency

`tox_DEBIAN`, like `tox`, uses [py.test][pt] for test automatization.

  [pt]: http://pytest.org/latest/

## Syntax

The debian dependencies has to be listed in the `testenv` section
as `debian_deps` multi line option.

```ini
[testenv]
debian_deps =
  python3-ipaddr
  python3-yaml
```

Extra options can be defined for `apt-get` with the `apt_opts` option:

```ini
[testenv]
apt_opts=
  --allow-unauthenticated
debian_deps =
  python3-ipaddr
  python3-yaml
```

## Install

### Install tox

```sh
pip install git+https://github.com/nyirog/tox.git
```

`tox` uses `RequirementParseError` from `pkg_resources`, therefore `setuptools`
might need to be upgraded:

```sh
pip install --upgrade setuptools
```

### Install `tox_DEBIAN`

```sh
pip install git+https://github.com/nyirog/tox-debian-plugin.git
```

## Test

### Local `tox_DEBIAN` install

```sh
git clone https://github.com/nyirog/tox-debian-plugin.git
pip install -e tox-debian-plugin
```

### Install `py.test`

```sh
pip install pytest
```

### Test run

```
cd tox-debian-plugin
py.test tests
```
