import sys
from setuptools import setup

if sys.version_info[0] == 3:
    if not sys.version_info >= (3, 3):
        raise ValueError('This package requires Python 3.3 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

__project__ = 'quickdraw'
__desc__ = 'An API for downloading and reading the google quickdraw data.'
__version__ = '0.0.1'
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin@ohanlonweb.com'
__license__ = 'MIT'
__url__ = 'https://github.com/martinohanlon/quickdraw_python'
__requires__ = ['pillow',]
__long_description__ = """# quickdraw

quickdraw is an API for using the Google QuickDraw data set. [quickdraw.withgoogle.com/data](https://quickdraw.withgoogle.com/data)

## Install

### Windows

```
pip install quickdraw
```

### macOS

```
pip3 install quickdraw
```

### Linux / Raspberry Pi

```
sudo pip3 install quickdraw
```

## Use

to come.

## Documentation

to come.

"""

__classifiers__ = [
   "Development Status :: 3 - Alpha",
#   "Development Status :: 4 - Beta",
#   "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Communications",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]

if __name__ == '__main__':
    setup(name='quickdraw',
          version = __version__,
          description = __desc__,
          url = __url__,
          author = __author__,
          author_email = __author_email__,
          license= __license__,
          packages = [__project__],
          # install_requires = __requires__,
          zip_safe=False)
