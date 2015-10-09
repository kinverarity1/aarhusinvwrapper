import argparse
import logging
import os
import sys

import numpy
import pandas

import gdp32datatools


logger = logging.getLogger(__name__)



TEM = """Created by {script_fn} from {input_fn}
  7  3                     !source type, field polarization
  {tx_x:8.2f} {tx_y:8.2f} {tx_z:1.0f} {rx_x:8.2f} {rx_y:8.2f} {rx_z:1.0f}   !tx and rx - x,y,z, truncated
  20 20                  !tx loop size
  3 3 4                    !in/out inversion
  3 1                      !tx waveform - userdefined, only one
  2 -7.8125e-3 -7.3125e-3 0.00 1.00 0.00e+0 2.0e-6 1.00 0.00 !tx waveform
  0 0 0                    !no front gate filter
"""

MOD = """Created by {script_fn} from {input_fn}
1 1  0    ! # of tem files, some vertical constraints yes, no topo
1 1 {TEMfn}
50    ! max # of iterations
{nlayers:6.0f}   !# of layers in model
"""


def mainfunc(avgfile, invpath, stnfn):
    # Reference Lines 4-9
    txramp = 0.015          # ms
    rxramp = 0.002          # ms
    antialias = 0.001       # ms

    # Reference Lines 10-11
    ramptime = txramp

    # Ref lines 12-14
    area_tx = 400
    area_rx = 250

    assert os.path.isfile(avgfile)
    avg_dirname = os.path.dirname(avgfile)
    avg_basename = os.path.basename(avgfile)
    avg_pre, ext = os.path.splitext(avg_basename)
    if not os.path.isdir(invpath):
        os.makedirs(invpath)

    with open(avgfile, mode="r") as avgfobj:
        avg = gdp32datatools.read_avg1(avgfobj)
    stations = avg.Station.unique()

    stnlocs = None
    if stnfn:
        assert os.path.isfile(stnfn)
        stnlocs = pandas.read_csv(stnfn, delim_whitespace=True, 
            names=["Station", "Easting", "Northing", "Elevation"], 
            index_col="Station")
        logger.debug('Read station file %s' % stnfn)
    if stnlocs is None:
        stn = pandas.Series([0, 0, 0], index=["Easting", "Northing", "Elevation"])
        logger.debug('No station file, using coordinates 0, 0, 0')

    # Inversion setup. 1l through 7l, and a 20l
    for nlayers in (range(1, 8) + [20]):
        linvpath = os.path.join(invpath, "%.0fl" % nlayers)
        if not os.path.isdir(linvpath):
            os.makedirs(linvpath)

        for station in stations:
            if not stnlocs is None:
                stn = stnlocs.loc[station]
            data = avg[avg.Station == station]

            fnprefix = "{avgpre}_{nlayers}l_{station}".format(
                avgpre=avg_pre, nlayers=nlayers, station=str(station))
            
            temfn = fnprefix + ".tem"
            temfnpath = os.path.join(linvpath, temfn)
            
            rtime = (numpy.asarray(data.Time) + ramptime) / 1e3  # Time after Tx turn-off
            norm_mag = numpy.asarray(data.Magnitude) / (area_rx * 1e6) # Magnitude in V/A not uV/A
            norm_pc_mag = numpy.asarray(data["%Mag"] / 100.)  # Zonge errors not relative.
            log_late_res = numpy.asarray(numpy.log10(
                numpy.power(area_rx * area_tx / data.Magnitude, 2/3.) *
                numpy.power(data.Time, -5/3.) *
                6.3219e-3
                ))
            norm_pc_mag[norm_pc_mag < 0.05] = 0.05
            data_lines = []
            skip = numpy.asarray(data.skp)
            for i in range(len(rtime)):
                skip_char = " "
                if skip[i] == 1:
                    skip_char = "%"
                # print station, i, rtime[i]
                data_lines.append(
                    "%s%4.3e %4.3e %3.2e 1 0" % (skip_char, rtime[i],
                        norm_mag[i], norm_pc_mag[i]))

            with open(temfnpath, mode="w") as temfobj:
                temfobj.write(str(TEM).format(
                    script_fn=__file__, input_fn=avgfile,
                    tx_x=stn.Easting, tx_y=stn.Northing, tx_z=stn.Elevation,
                    rx_x=stn.Easting, rx_y=stn.Northing, rx_z=stn.Elevation))
                temfobj.write("\n".join(data_lines))
                logger.info('Written TEM data file %s' % temfnpath)

            geomean_late_res = 10 ** numpy.mean(log_late_res)
            late_time = sorted(numpy.asarray(data.Time))[-1] / 1e3
            bos_depth2 = numpy.sqrt(
                late_time * geomean_late_res / numpy.pi * 2 * 4e-7)
            bos_depth = numpy.sqrt(
                (late_time * geomean_late_res) / (numpy.pi * 2 * 4e-7))
            log_step = numpy.log10(bos_depth) / nlayers

            # ================= Model file ===========================

            modfn = fnprefix + ".mod"
            modfnpath = os.path.join(linvpath, modfn)

            if nlayers != 20:   # ------- DISCRETE LAYER MODEL ---------------
                # Starting resistivities...
                mod_lines = [
                    "  {start_res:6.2f}   -1   0.6 !r {nlayer:2.0f}".format(
                        start_res=geomean_late_res, nlayer=n+1)
                    for n in range(nlayers)]

                if nlayers > 1:
                    # Starting thicknesses...
                    thks = numpy.empty((nlayers - 1))
                    thks[0] = 10 ** log_step
                    for i in range(1, len(thks)):
                        thks[i] = 10**(i * log_step) - 10**((i - 1) * log_step)
                    mod_lines += [
                        "  {start_thk:6.2f}   -1   9e9 !t {nlayer:2.0f}".format(
                            start_thk=thks[i], nlayer=i+1)
                        for i in range(len(thks))]

                    # Starting depths...
                    mod_lines += [
                        ("  -1 -1.000e+00     !z %2.0f" % (i + 1))
                        for i in range(len(thks))]

            elif nlayers == 20:     # ---------- SMOOTH MODEL ---------------
                # Starting resistivities
                mod_lines = [
                    "  {start_res:6.2f}   -1   .3 !r {nlayer:2.0f}".format(
                        start_res=geomean_late_res, nlayer=n+1)
                    for n in range(nlayers)]

                # Starting thicknesses...
                thks = numpy.empty((nlayers - 1))
                thks[0] = 10 ** log_step
                for i in range(1, len(thks)):
                    thks[i] = 10**(i * log_step) - 10**((i - 1) * log_step)
                mod_lines += [
                    "  {start_thk:6.2f}  1.000e-03 1e3  9e9 !t {nlayer:2.0f}".format(
                        start_thk=thks[i], nlayer=i+1)
                    for i in range(len(thks))]

                # Starting depths...
                mod_lines += [
                    ("  -1 -1.000e+00     !z %2.0f" % (i + 1))
                    for i in range(len(thks))]

            with open(modfnpath, mode="w") as modfobj:
                modfobj.write(str(MOD).format(
                    script_fn=__file__, input_fn=avgfile,
                    TEMfn=os.path.basename(temfnpath), nlayers=nlayers))
                modfobj.write("\n".join(mod_lines))
                logger.info('Written model file %s' % modfnpath)



def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s  %(levelname)s  %(filename)s  "
                "line %(lineno)d %(funcName)s : %(message)s"))
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--invpath', default='.', help="Path to conduct inversions in")
    p.add_argument('-s', '--stnfn', default=None, help="Optional .stn file")
    p.add_argument('avgfile', help="Required data in .avg file")
    args = p.parse_args(sys.argv[1:])
    return mainfunc(**args.__dict__)


if __name__ == "__main__":
    main()