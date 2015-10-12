aarhusinvwrapper
================

This package is a wrapper for the `AarhusInv <http://hgg.au.dk/download/inversionkernel/>`__ modelling software, to somewhat automate the process of creating models and inverting data, and so on.

See the `Jupyter/IPython notebooks <https://github.com/kinverarity1/aarhusinvwrapper/tree/master/notebooks>`__ for examples of how to use it.

It was modified from code written originally by Mike Hatch and is not associated with the Aarhus group.

There are several different parts of the package.

1. It's designed to work flexibly with AarhusInv64.exe and AarhusInvLic.exe no
   matter where those executables are kept on your computer. Say you keep them
   at ``y:\Stuff\other stuff\research\emd1dinv``. All you have to do is install
   this package like you would any other Python package:

.. code:: powershell

    PS F:\> pip install aarhusinvwrapper

   And then you just need to register the location of AarhusInv64.exe with
   aarhusinvwrapper, like so:

.. code::

    PS F:\> aarhusinv_register.exe --help
    usage: aarhusinv_register-script.py [-h] path

    positional arguments:
      path        location of AarhusInv64.exe etc.

    optional arguments:
      -h, --help  show this help message and exit
    PS F:\> aarhusinv_register.exe 'F:\Surface Geophysics\software\AarhusInv'
    Successfully registered AarhusInv at F:\Surface Geophysics\software\AarhusInv
    PS F:\>

   See the `example notebook <https://github.com/kinverarity1/aarhusinvwrapper/blob/master/notebooks/How%20to%20register%20the%20AarhusInv%20software%20location%20with%20aarhusinvwrapper.ipynb>`__.

2. If you setup your inversions by hand or by other means you can use
   aarhusinvwrapper to run AarhusInv from a controlling Python script, just use:

.. code:: python

    >>> import aarhusinvwrapper
    >>> aarhusinvwrapper.run('example.mod')

   See the `example notebook <https://github.com/kinverarity1/aarhusinvwrapper/blob/master/notebooks/Running%20AarhusInv%20via%20aarhusinvwrapper.ipynb>`__.

3. You can also use utility scripts/functions in aarhusinvwrapper to generate
   what I call "inversion sets" where you programatically generate a whole heap
   of different model setups (e.g. 3 layer, or a 20 layer smooth model, or you
   experiment with a range of different constraints, or error floors), and then
   run all the inversions in turn, all running over a profile, so a range of
   data sites.

   In this case I generally start with the data in the form of a Zonge
   Engineering .avg file, because that's how I usually collect data, but in
   the future I will build to accept data from other common sources, or from
   anywhere.

   The only script at the moment is

.. code::

    PS F:\> aarhusinv_setup_avg.exe --help
    usage: aarhusinv_setup_avg-script.py [-h] [-i INVPATH] [-s STNFN] avgfile

    positional arguments:
      avgfile               Required data in .avg file

    optional arguments:
      -h, --help            show this help message and exit
      -i INVPATH, --invpath INVPATH
                            Path to conduct inversions in
      -s STNFN, --stnfn STNFN
                            Optional .stn file
    PS F:\>


   You will need:

   - Zonge TEM data in the form of an .avg file
   - (optional) station locations as a .stn file (whitespace-delimited, no header line, with columns from left to right: station number, easting, northing, and elevation).

   First setup the inversions:

   TBW

   And then recursively run them all:

.. code::

    $ aarhusinv_run.exe --help
    usage: aarhusinv_run-script.py [-h] [-d] [-r] [models [models ...]]

    positional arguments:
      models         model files to run OR paths to recurse over

    optional arguments:
      -h, --help     show this help message and exit
      -d, --dry-run  don't actually make any changes
      -r, --recurse  look recursively

