import sys
from setuptools import setup

if sys.version_info[0] == 3:
    if not sys.version_info >= (3, 3):
        raise ValueError('This package requires Python 3.3 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

__project__ = 'quickdraw'
__desc__ = 'An API for downloading and reading the google quickdraw data.'
__version__ = '0.2.0'
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin@ohanlonweb.com'
__license__ = 'MIT'
__url__ = 'https://github.com/martinohanlon/quickdraw_python'
__requires__ = ['pillow', 'requests', ]
__long_description__ = """# quickdraw

[Google Quick, Draw!](https://quickdraw.withgoogle.com/) is a game which is 
training a neural network to recognise doodles.

`quickdraw` is an API for using the Google Quick, Draw! data 
[quickdraw.withgoogle.com/data](https://quickdraw.withgoogle.com/data), 
downloading the data files as and when needed, caching them locally and 
allowing them to be used.

## Getting started

+ Windows

```bash
pip install quickdraw
```

+ macOS

```bash
pip3 install quickdraw
```

+ Linux / Raspberry Pi

```bash
sudo pip3 install quickdraw
```

## Use

Open the Quick Draw data, pull back an **anvil** drawing and save it.

```python
    from quickdraw import QuickDrawData
    qd = QuickDrawData()
    anvil = qd.get_drawing("anvil")
    anvil.image.save("my_anvil.gif")
```

## Documentation

[quickdraw.readthedocs.io](https://quickdraw.readthedocs.io)

"""

__classifiers__ = [
#   "Development Status :: 3 - Alpha",
   "Development Status :: 4 - Beta",
#   "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Scientific/Engineering :: Image Recognition",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

if __name__ == '__main__':
    setup(
        name='quickdraw',
        version = __version__,
        description = __desc__,
        long_description=__long_description__,
        long_description_content_type='text/markdown',
        url = __url__,
        author = __author__,
        author_email = __author_email__,
        license= __license__,
        packages = [__project__],
        install_requires = __requires__,
        zip_safe=False)
