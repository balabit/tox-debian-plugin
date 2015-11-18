# tox_DEBIAN

tox_DEBIAN.py is a tox plugin which extracts debian packages
into the tox managed virtual environment.

## Dependency

### Hook dependency

The plugin implements **tox_setupenv** pluggy hook,
which is not released yet into tox, but it can be fetched from the
[github working branch](https://github.com/nyirog/tox).

### External dependency

The plugin uses **apt-get**, **dpkg** and **cp** tools.

### Test dependency

tox_DEBIAN like tox uses **py.test** for test automatization.

## Syntax

The debian dependencies has to be listed in the **testenv** section
as **debian_deps** multi line option.

```ini
[testenv]
debian_deps =
  python3-ipaddr
  python3-yaml
```

Extra option can be defined for **apt-get** with **apt_opts** option.

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

```
pip install git+https://github.com/nyirog/tox.git
```

tox uses _RequirementParseError_ from **pkg_resources** therefore setuptools has to be upgraded.

```
pip install --upgrade setuptools
```

### Install tox_DEBIAN

```
pip install git+https://github.com/nyirog/tox-debian-plugin.git
```

## Test

### Local tox_DEBIAN install

```
git clone https://github.com/nyirog/tox-debian-plugin.git
pip install -e tox-debian-plugin
```

### Install **py.test**

```sh
pip install pytest
```

### Test run

```
cd tox-debian-plugin
py.test tests
```
