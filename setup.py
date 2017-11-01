# Use the setuptools package if it is available. It's preferred 
# because it creates an exe file on Windows for Python scripts.

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from distutils.core import setup

from aarhusinvwrapper import __version__


with open(path.join(path.dirname(__file__), "requirements.txt"), "r") as f:
    requirements = f.read().splitlines()

with open(path.join(path.dirname(__file__), "README.md"), "r") as f:
    README = f.read()

setup(name='aarhusinvwrapper',

      version=__version__,

      description='Unofficial wrapper for AarhusInv modelling software',
      long_description=README,

      url="https://github.com/kinverarity1/aarhusinvwrapper",

      author="Kent Inverarity",
      author_email="kinverarity@hotmail.com",

      license="MIT",

      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Customer Service",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: Other Audience",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Scientific/Engineering",
          "Topic :: System :: Filesystems",
          "Topic :: Scientific/Engineering :: Information Analysis",
      ],

      keywords="science geophysics modelling",

      packages=["aarhusinvwrapper", ],

      install_requires=requirements,

      entry_points={
          'console_scripts': [
              'aarhusinv_register = aarhusinvwrapper.runmodule:register_entryfunc',
              'aarhusinv_setup_avg = aarhusinvwrapper.setup_avg:main',
              'aarhusinv_run = aarhusinvwrapper.runmodule:main'
          ],
      }
      )
