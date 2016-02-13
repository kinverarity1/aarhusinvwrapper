# aarhusinvwrapper

![](https://img.shields.io/badge/status-alpha-red.svg)

This package is a wrapper for the [AarhusInv](http://hgg.au.dk/download/inversionkernel/) modelling software, to somewhat automate the process of creating models and inverting data, and so on.

See the [Jupyter notebooks](https://github.com/kinverarity1/aarhusinvwrapper/tree/master/notebooks>) for examples of how to use it.

It was modified from code written originally by Mike Hatch and is not associated with the Aarhus group.

There are several different parts of the package.

1. It's designed to work flexibly with AarhusInv64.exe and AarhusInvLic.exe no
   matter where those executables are kept on your computer. Say you keep them
   at ``y:\Stuff\other stuff\research\emd1dinv``. All you have to do is install
   this package like you would any other Python package:

        PS F:\> pip install aarhusinvwrapper

   And then you just need to register the location of AarhusInv64.exe with
   aarhusinvwrapper, like so:

        PS F:\> aarhusinv_register.exe --help
        usage: aarhusinv_register-script.py [-h] path

        positional arguments:
          path        location of AarhusInv64.exe etc.

        optional arguments:
          -h, --help  show this help message and exit
        PS F:\> aarhusinv_register.exe 'F:\Surface Geophysics\software\AarhusInv'
        Successfully registered AarhusInv at F:\Surface Geophysics\software\AarhusInv
        PS F:\>

   See the [example notebook](https://github.com/kinverarity1/aarhusinvwrapper/blob/master/notebooks/How%20to%20register%20the%20AarhusInv%20software%20location%20with%20aarhusinvwrapper.ipynb).

2. If you setup your inversions by hand or by other means you can use
   aarhusinvwrapper to run AarhusInv from a controlling Python script, just use:

        >>> import aarhusinvwrapper
        >>> aarhusinvwrapper.run('example.mod')

   See the [example notebook](https://github.com/kinverarity1/aarhusinvwrapper/blob/master/notebooks/How%20to%20register%20the%20AarhusInv%20software%20location%20with%20aarhusinvwrapper.ipynb)

3. You can read the .emo format files that AarhusInv produces easily with
   aarhusinvwrapper!:

        >>> emo = aarhusinvwrapper.read_emo('example.emo')
        {'SharpHorizontal': -1.0,
         'SharpPrior': 0.0,
         'SharpVertical': -1.0,
         'aniso_max': 0.0,
         'aniso_min': 0.0,
         'chrg_max': 0.0,
         'chrg_min': 0.0,
         'compile_datetime': None,
         'compile_time': datetime.time(0, 0),
         'data_fns': ['reedyck_7l_1000.tem'],
         'dds': [29],
         'doi': True,
         'dset_src_types': [7],
         'dset_types': [1],
         'final_norms': Ite_#    8.000
         Data     3.676
         VCon     2.751
         HCon     0.000
         Depth    0.000
         Apri     0.000
         Total    3.535
         Name: 8, dtype: float64,
         'final_rhos': array([ 0.1  ,  1.3  ,  3.136,  4.717,  3.143,  1.569,  6.148]),
         'final_thks': array([ 0.219,  0.832,  1.594,  3.307,  4.476,  8.445]),
         'final_tops': array([  0.   ,   0.219,   1.051,   2.645,   5.952,  10.428]),
         'fn': 'example.emo',
         'fwd_responses':         Time      Inp_Data    STD  WaveID  FiltID  DSet#       Ite#008  \
         0   0.000017  4.501000e-03  0.050       1       0      1  1.938400e-03   
         1   0.000018  3.576000e-03  0.050       1       0      1  1.820460e-03   
         2   0.000019  2.935000e-03  0.050       1       0      1  1.695450e-03   
         3   0.000020  2.467000e-03  0.050       1       0      1  1.570550e-03   
         4   0.000021  2.109000e-03  0.050       1       0      1  1.450940e-03   
         5   0.000023  1.707000e-03  0.050       1       0      1  1.278890e-03   
         6   0.000026  1.316000e-03  0.050       1       0      1  1.077490e-03   
         7   0.000028  1.037000e-03  0.050       1       0      1  9.033170e-04   
         8   0.000031  7.919000e-04  0.050       1       0      1  7.288500e-04   
         9   0.000035  5.881000e-04  0.050       1       0      1  5.674070e-04   
         10  0.000039  4.156000e-04  0.050       1       0      1  4.140980e-04   
         11  0.000046  2.725000e-04  0.050       1       0      1  2.766020e-04   
         12  0.000054  1.778000e-04  0.050       1       0      1  1.805170e-04   
         13  0.000063  1.142000e-04  0.050       1       0      1  1.144010e-04   
         14  0.000075  7.182000e-05  0.050       1       0      1  7.033890e-05   
         15  0.000091  4.384000e-05  0.050       1       0      1  4.176470e-05   
         16  0.000111  2.590000e-05  0.050       1       0      1  2.400190e-05   
         17  0.000136  1.530000e-05  0.050       1       0      1  1.384430e-05   
         18  0.000167  8.992000e-06  0.050       1       0      1  7.992760e-06   
         19  0.000206  5.196000e-06  0.050       1       0      1  4.566630e-06   
         20  0.000256  2.913000e-06  0.050       1       0      1  2.556000e-06   
         21  0.000319  1.592000e-06  0.050       1       0      1  1.398950e-06   
         22  0.000397  8.444000e-07  0.050       1       0      1  7.600910e-07   
         23  0.000495  4.436000e-07  0.050       1       0      1  4.058350e-07   
         24  0.000619  2.226000e-07  0.050       1       0      1  2.127020e-07   
         25  0.000776  1.101000e-07  0.050       1       0      1  1.104170e-07   
         26  0.000972  4.776000e-08  0.056       1       0      1  5.678850e-08   
         27  0.001221  2.314000e-08  0.151       1       0      1  2.899170e-08   
         28  0.001532  1.168000e-08  0.216       1       0      1  1.479710e-08   
         
                  Ite#007       Ite#006       Ite#005         ...           \
         0   1.913990e-03  1.817430e-03  1.697570e-03         ...            
         1   1.796940e-03  1.728570e-03  1.576090e-03         ...            
         2   1.673310e-03  1.629830e-03  1.456720e-03         ...            
         3   1.550010e-03  1.528320e-03  1.342000e-03         ...            
         4   1.432340e-03  1.427450e-03  1.236110e-03         ...            
         5   1.263110e-03  1.279160e-03  1.089160e-03         ...            
         6   1.065520e-03  1.098740e-03  9.209800e-04         ...            
         7   8.946840e-04  9.380040e-04  7.787450e-04         ...            
         8   7.237410e-04  7.717190e-04  6.375050e-04         ...            
         9   5.653710e-04  6.129350e-04  5.059600e-04         ...            
         10  4.147880e-04  4.573320e-04  3.801460e-04         ...            
         11  2.792710e-04  3.127380e-04  2.642060e-04         ...            
         12  1.839890e-04  2.080670e-04  1.797630e-04         ...            
         13  1.178490e-04  1.337250e-04  1.186090e-04         ...            
         14  7.326480e-05  8.279930e-05  7.547990e-05         ...            
         15  4.395500e-05  4.905500e-05  4.587210e-05         ...            
         16  2.546280e-05  2.782130e-05  2.653110e-05         ...            
         17  1.474970e-05  1.571050e-05  1.514000e-05         ...            
         18  8.528370e-06  8.861370e-06  8.568960e-06         ...            
         19  4.869830e-06  4.949730e-06  4.774410e-06         ...            
         20  2.721620e-06  2.720190e-06  2.608770e-06         ...            
         21  1.487450e-06  1.471470e-06  1.402870e-06         ...            
         22  8.073590e-07  7.960420e-07  7.557130e-07         ...            
         23  4.309370e-07  4.263170e-07  4.040980e-07         ...            
         24  2.259290e-07  2.255760e-07  2.141660e-07         ...            
         25  1.174150e-07  1.189480e-07  1.134930e-07         ...            
         26  6.049180e-08  6.247980e-08  6.009810e-08         ...            
         27  3.095270e-08  3.270300e-08  3.178110e-08         ...            
         28  1.584270e-08  1.716910e-08  1.688930e-08         ...            
         
             Ite#002ResidAbsPc  Ite#001Resid  Ite#001ResidAbs  Ite#001ResidAbsPc  \
         0            0.821118 -3.849994e-03     3.849994e-03           0.855364   
         1            0.804647 -3.014791e-03     3.014791e-03           0.843062   
         2            0.791759 -2.446720e-03     2.446720e-03           0.833635   
         3            0.782104 -2.039643e-03     2.039643e-03           0.826771   
         4            0.774157 -1.731957e-03     1.731957e-03           0.821222   
         5            0.764902 -1.391064e-03     1.391064e-03           0.814917   
         6            0.753680 -1.062363e-03     1.062363e-03           0.807267   
         7            0.743705 -8.300730e-04     8.300730e-04           0.800456   
         8            0.732073 -6.275130e-04     6.275130e-04           0.792414   
         9            0.718898 -4.606000e-04     4.606000e-04           0.783200   
         10           0.703804 -3.210659e-04     3.210659e-04           0.772536   
         11           0.685537 -2.069403e-04     2.069403e-04           0.759414   
         12           0.668071 -1.327524e-04     1.327524e-04           0.746639   
         13           0.651923 -8.388550e-05     8.388550e-05           0.734549   
         14           0.637885 -5.197360e-05     5.197360e-05           0.723665   
         15           0.626918 -3.132870e-05     3.132870e-05           0.714615   
         16           0.619856 -1.833530e-05     1.833530e-05           0.707927   
         17           0.616928 -1.076917e-05     1.076917e-05           0.703867   
         18           0.614633 -6.293240e-06     6.293240e-06           0.699871   
         19           0.611091 -3.608330e-06     3.608330e-06           0.694444   
         20           0.602358 -1.993809e-06     1.993809e-06           0.684452   
         21           0.588781 -1.066920e-06     1.066920e-06           0.670176   
         22           0.560910 -5.437650e-07     5.437650e-07           0.643966   
         23           0.529779 -2.725930e-07     2.725930e-07           0.614502   
         24           0.477412 -1.261866e-07     1.261866e-07           0.566876   
         25           0.411444 -5.583030e-08     5.583030e-08           0.507087   
         26           0.245984 -1.729980e-08     1.729980e-08           0.362224   
         27           0.138224 -6.116300e-09     6.116300e-09           0.264317   
         28           0.052902 -2.155950e-09     2.155950e-09           0.184585   
         
             Ite#000Resid  Ite#000ResidAbs  Ite#000ResidAbsPc  IterFinalResid  \
         0  -4.027960e-03     4.027960e-03           0.894903   -2.562600e-03   
         1  -3.172278e-03     3.172278e-03           0.887102   -1.755540e-03   
         2  -2.586804e-03     2.586804e-03           0.881364   -1.239550e-03   
         3  -2.164634e-03     2.164634e-03           0.877436   -8.964500e-04   
         4  -1.844073e-03     1.844073e-03           0.874383   -6.580600e-04   
         5  -1.487003e-03     1.487003e-03           0.871121   -4.281100e-04   
         6  -1.141158e-03     1.141158e-03           0.867141   -2.385100e-04   
         7  -8.955280e-04     8.955280e-04           0.863576   -1.336830e-04   
         8  -6.804200e-04     6.804200e-04           0.859225   -6.305000e-05   
         9  -5.022944e-04     5.022944e-04           0.854097   -2.069300e-05   
         10 -3.524343e-04     3.524343e-04           0.848013   -1.502000e-06   
         11 -2.289722e-04     2.289722e-04           0.840265    4.102000e-06   
         12 -1.480104e-04     1.480104e-04           0.832454    2.717000e-06   
         13 -9.418820e-05     9.418820e-05           0.824765    2.010000e-07   
         14 -5.871040e-05     5.871040e-05           0.817466   -1.481100e-06   
         15 -3.554872e-05     3.554872e-05           0.810874   -2.075300e-06   
         16 -2.085585e-05     2.085585e-05           0.805245   -1.898100e-06   
         17 -1.225294e-05     1.225294e-05           0.800846   -1.455700e-06   
         18 -7.158530e-06     7.158530e-06           0.796100   -9.992400e-07   
         19 -4.104660e-06     4.104660e-06           0.789965   -6.293700e-07   
         20 -2.272896e-06     2.272896e-06           0.780260   -3.570000e-07   
         21 -1.221323e-06     1.221323e-06           0.767163   -1.930500e-07   
         22 -6.292760e-07     6.292760e-07           0.745234   -8.430900e-08   
         23 -3.195730e-07     3.195730e-07           0.720408   -3.776500e-08   
         24 -1.517543e-07     1.517543e-07           0.681735   -9.898000e-09   
         25 -6.972490e-08     6.972490e-08           0.633287    3.170000e-10   
         26 -2.483490e-08     2.483490e-08           0.519994    9.028500e-09   
         27 -1.018930e-08     1.018930e-08           0.440333    5.851700e-09   
         28 -4.363670e-09     4.363670e-09           0.373602    3.117100e-09   
         
             IterFinalResidAbs  IterFinalResidAbsPc  
         0        2.562600e-03             0.569340  
         1        1.755540e-03             0.490923  
         2        1.239550e-03             0.422334  
         3        8.964500e-04             0.363377  
         4        6.580600e-04             0.312025  
         5        4.281100e-04             0.250797  
         6        2.385100e-04             0.181239  
         7        1.336830e-04             0.128913  
         8        6.305000e-05             0.079619  
         9        2.069300e-05             0.035186  
         10       1.502000e-06             0.003614  
         11       4.102000e-06             0.015053  
         12       2.717000e-06             0.015281  
         13       2.010000e-07             0.001760  
         14       1.481100e-06             0.020622  
         15       2.075300e-06             0.047338  
         16       1.898100e-06             0.073286  
         17       1.455700e-06             0.095144  
         18       9.992400e-07             0.111125  
         19       6.293700e-07             0.121126  
         20       3.570000e-07             0.122554  
         21       1.930500e-07             0.121263  
         22       8.430900e-08             0.099845  
         23       3.776500e-08             0.085133  
         24       9.898000e-09             0.044465  
         25       3.170000e-10             0.002879  
         26       9.028500e-09             0.189039  
         27       5.851700e-09             0.252882  
         28       3.117100e-09             0.266875  
         
         [29 rows x 46 columns],
         'min_apriori_std': 1e+60,
         'model_fn': 'REEDYCK_7l_1000.mod',
         'model_params': array([[ 0.   ,  4.43 ,  4.43 ,  4.43 ,  4.43 ,  4.43 ,  4.43 ,  4.43 ,
                  1.79 ,  0.79 ,  1.4  ,  2.51 ,  4.48 ,  8.   ],
                [ 1.   ,  3.048,  3.793,  3.459,  3.167,  3.272,  3.724,  3.94 ,
                  1.79 ,  0.79 ,  1.4  ,  2.51 ,  4.48 ,  8.   ],
                [ 2.   ,  2.297,  3.463,  2.973,  2.585,  2.812,  3.44 ,  3.754,
                  1.838,  0.781,  1.391,  2.539,  4.533,  8.022],
                [ 3.   ,  1.4  ,  3.068,  2.427,  1.991,  2.398,  3.167,  3.59 ,
                  2.018,  0.761,  1.374,  2.603,  4.62 ,  8.057],
                [ 4.   ,  0.628,  2.773,  2.14 ,  1.849,  2.402,  3.088,  3.619,
                  2.604,  0.738,  1.352,  2.612,  4.639,  8.075],
                [ 5.   ,  0.514,  2.801,  2.407,  2.104,  2.276,  2.841,  3.712,
                  1.359,  0.759,  1.378,  2.629,  4.754,  8.12 ],
                [ 6.   ,  0.243,  2.527,  3.414,  4.124,  2.492,  2.073,  4.174,
                  0.721,  0.807,  1.478,  2.681,  5.258,  8.502],
                [ 7.   ,  0.111,  1.593,  3.136,  4.098,  2.485,  1.664,  5.669,
                  0.252,  0.821,  1.526,  2.9  ,  4.727,  8.528],
                [ 8.   ,  0.1  ,  1.3  ,  3.136,  4.717,  3.143,  1.569,  6.148,
                  0.219,  0.832,  1.594,  3.307,  4.476,  8.445]]),
         'models': [{'rhos': array([ 4.43,  4.43,  4.43,  4.43,  4.43,  4.43,  4.43]),
           'thks': array([ 1.79,  0.79,  1.4 ,  2.51,  4.48,  8.  ]),
           'tops': array([  0.  ,   1.79,   2.58,   3.98,   6.49,  10.97])},
          {'rhos': array([ 3.048,  3.793,  3.459,  3.167,  3.272,  3.724,  3.94 ]),
           'thks': array([ 1.79,  0.79,  1.4 ,  2.51,  4.48,  8.  ]),
           'tops': array([  0.  ,   1.79,   2.58,   3.98,   6.49,  10.97])},
          {'rhos': array([ 2.297,  3.463,  2.973,  2.585,  2.812,  3.44 ,  3.754]),
           'thks': array([ 1.838,  0.781,  1.391,  2.539,  4.533,  8.022]),
           'tops': array([  0.   ,   1.838,   2.619,   4.01 ,   6.549,  11.082])},
          {'rhos': array([ 1.4  ,  3.068,  2.427,  1.991,  2.398,  3.167,  3.59 ]),
           'thks': array([ 2.018,  0.761,  1.374,  2.603,  4.62 ,  8.057]),
           'tops': array([  0.   ,   2.018,   2.779,   4.153,   6.756,  11.376])},
          {'rhos': array([ 0.628,  2.773,  2.14 ,  1.849,  2.402,  3.088,  3.619]),
           'thks': array([ 2.604,  0.738,  1.352,  2.612,  4.639,  8.075]),
           'tops': array([  0.   ,   2.604,   3.342,   4.694,   7.306,  11.945])},
          {'rhos': array([ 0.514,  2.801,  2.407,  2.104,  2.276,  2.841,  3.712]),
           'thks': array([ 1.359,  0.759,  1.378,  2.629,  4.754,  8.12 ]),
           'tops': array([  0.   ,   1.359,   2.118,   3.496,   6.125,  10.879])},
          {'rhos': array([ 0.243,  2.527,  3.414,  4.124,  2.492,  2.073,  4.174]),
           'thks': array([ 0.721,  0.807,  1.478,  2.681,  5.258,  8.502]),
           'tops': array([  0.   ,   0.721,   1.528,   3.006,   5.687,  10.945])},
          {'rhos': array([ 0.111,  1.593,  3.136,  4.098,  2.485,  1.664,  5.669]),
           'thks': array([ 0.252,  0.821,  1.526,  2.9  ,  4.727,  8.528]),
           'tops': array([  0.   ,   0.252,   1.073,   2.599,   5.499,  10.226])},
          {'rhos': array([ 0.1  ,  1.3  ,  3.136,  4.717,  3.143,  1.569,  6.148]),
           'thks': array([ 0.219,  0.832,  1.594,  3.307,  4.476,  8.445]),
           'tops': array([  0.   ,   0.219,   1.051,   2.645,   5.952,  10.428])}],
         'nds': 1,
         'niterations': 8,
         'nlayers_model': [7],
         'nm': 1,
         'norm_factor': 1.0,
         'norms':    Ite_#    Data   VCon  HCon  Depth  Apri   Total
         0      0  23.066  0.000     0      0     0  20.996
         1      1  18.339  0.253     0      0     0  16.694
         2      2  15.298  0.449     0      0     0  13.926
         3      3  10.311  0.795     0      0     0   9.391
         4      4   5.597  1.360     0      0     0   5.126
         5      5   4.671  1.516     0      0     0   4.298
         6      6   3.955  2.195     0      0     0   3.713
         7      7   3.713  2.686     0      0     0   3.558
         8      8   3.676  2.751     0      0     0   3.535,
         'nparams': 13,
         'path': '',
         'res_max': 20000.0,
         'res_min': 0.1,
         'run_date': datetime.date(2015, 10, 9),
         'run_datetime': datetime.datetime(2015, 10, 9, 15, 48, 9),
         'run_elapsed': 5.1,
         'run_time': datetime.time(15, 48, 9),
         'thk_max': 500.0,
         'thk_min': 0.1,
         'version': '6.10'}

   The  [example notebook](https://github.com/kinverarity1/aarhusinvwrapper/blob/master/notebooks/How%20to%20register%20the%20AarhusInv%20software%20location%20with%20aarhusinvwrapper.ipynb) also shows how to generate some basic plots of models and so on.

4. You can also use utility scripts/functions in aarhusinvwrapper to generate
   what I call "inversion sets" where you programatically generate a whole heap
   of different model setups (e.g. 3 layer, or a 20 layer smooth model, or you
   experiment with a range of different constraints, or error floors), and then
   run all the inversions in turn, all running over a profile, so a range of
   data sites.

   In this case I generally start with the data in the form of a Zonge
   Engineering .avg file, because that's how I usually collect data, but in
   the future I will build to accept data from other common sources, or from
   anywhere.

   The only script at the moment is:

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

        $ aarhusinv_run.exe --help
        usage: aarhusinv_run-script.py [-h] [-d] [-r] [models [models ...]]

        positional arguments:
          models         model files to run OR paths to recurse over

        optional arguments:
          -h, --help     show this help message and exit
          -d, --dry-run  don't actually make any changes
          -r, --recurse  look recursively

