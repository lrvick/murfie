# Murfie #

<http://github.com/lrvick/murfie>

[![TravisCI][travis-badge]][travis-status]
[![Test Coverage][cc-coverage-badge]][cc-coverage]
[![Code Climate][cc-badge]][cc-repo]
[![PyPI version][pypy-badge]][pypy]
[![Wheel][wheel-badge]][wheel]
[![Dependencies][dependencies-badge]][dependencies]
[![License][license-badge]][license]

## About ##

Murfie is a Python CLI tool and library for interacting with the undocumented
[Murfie][1] API.

Note: This is an unofficial project not sponsored by Murfie.com 
This is also currently alpha quality software. Use at your own risk.

[1]: https://murfie.com

## Current Features ##

  * login
  * fetch library disc ids
  * bulk create download requests for entire library

## Requirements ##
  
  * Active Murfie account
  * Python 3.2+

## Installation ##

```bash
pip install --user --upgrade -e git+https://github.com/lrvick/murfie/#egg=murfie
```

## CLI Usage ##

1. Set credentials:

    ```bash
    murfie login YOUR_USERNAME YOUR_PASSWORD
    ```

2. Download entire library to current directory

    ```bash
    murfie library download
    ```

## Notes ##

  Use at your own risk. You may be eaten by a grue.

  Questions/Comments?

  You can find me on the web via:

  [Email](mailto://lance@lrvick.net) |
  [Blog](http://lrvick.net) |
  [Twitter](http://twitter.com/lrvick) |
  [Facebook](http://facebook.com/lrvick) |
  [Google+](http://plus.google.com/109278148620470841006) |
  [YouTube](http://youtube.com/lrvick) |
  [Last.fm](http://last.fm/user/lrvick) |
  [LinkedIn](http://linkedin.com/in/lrvick) |
  [Github](http://github.com/lrvick/)

[cc-badge]: https://codeclimate.com/github/lrvick/murfie/badges/gpa.svg
[cc-coverage-badge]: https://codeclimate.com/github/lrvick/murfie/badges/coverage.svg
[cc-repo]: https://codeclimate.com/github/lrvick/murfie
[cc-coverage]: https://codeclimate.com/github/lrvick/murfie/coverage
[pypy-badge]: https://badge.fury.io/py/murfie.svg
[pypy]: https://pypi.python.org/pypi/murfie
[travis-badge]: https://travis-ci.org/lrvick/murfie.svg?branch=master
[travis-status]: https://travis-ci.org/lrvick/murfie
[license-badge]: https://img.shields.io/github/license/lrvick/murfie.svg?maxAge=2592000
[license]: https://github.com/lrvick/murfie/blob/master/LICENSE.md
[wheel-badge]: https://img.shields.io/pypi/format/murfie.svg
[wheel]: https://pypi.python.org/pypi/murfie
[dependencies-badge]: https://www.versioneye.com/user/projects/5780ca085bb139003969dcf8/badge.svg?style=flat-square
[dependencies]: https://www.versioneye.com/user/projects/5780ca085bb139003969dcf8
