aarhusinvwrapper
================

This package is a wrapper for the `AarhusInv <http://hgg.au.dk/download/inversionkernel/>`__ modelling software, to somewhat automate the process of creating models and inverting data, and so on.

See the `Jupyter/IPython notebooks <https://github.com/kinverarity1/aarhusinvwrapper/tree/master/notebooks>`__ for examples of how to use it.

It was modified from code written originally by Mike Hatch and is not associated with the Aarhus group.

Setting up inversion from .avg data
-----------------------------------

First make sure you have the required packages (numpy, pandas, and gdp32datatools):

.. code:: bash

    $ pip install -r optional-dependencies.txt

Then you will need:

- Zonge TEM data in the form of an .avg file
- (optional) station locations as a .stn file (whitespace-delimited, no header line, with columns from left to right: station number, easting, northing, and elevation).

First setup the inversions:

.. code:: bash

    $ aarhusinv_setup_avg.exe --help
    usage: aarhusinv_setup_avg-script.py [-h] [-i INVPATH] [-s STNFN] avgfile

    positional arguments:
      avgfile               Required data in .avg file

    optional arguments:
      -h, --help            show this help message and exit
      -i INVPATH, --invpath INVPATH
                            Path to conduct inversions in
      -s STNFN, --stnfn STNFN
                            Optional .stn file

And then recursively run them all:

.. code:: bash

    $ aarhusinv_run.exe --help
    usage: aarhusinv_run-script.py [-h] [-d] [-r] [models [models ...]]

    positional arguments:
      models         model files to run OR paths to recurse over

    optional arguments:
      -h, --help     show this help message and exit
      -d, --dry-run  don't actually make any changes
      -r, --recurse  look recursively

