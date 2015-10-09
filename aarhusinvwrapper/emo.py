import datetime
import os
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO as StringIO

import attrdict
import numpy

import model1d


class AttrDict2(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict2, self).__init__(*args, **kwargs)
        self.__dict__ = self



def read_emo(emofile):
    '''
    Arguments:
        file (file-like object or filename): emo file

    '''
    fn = None
    if os.path.isfile(emofile):
        fn = emofile
        emofile = open(fn, mode="r")
    lines = [l.strip('\n').strip() for l in emofile.readlines()]
    emofile.close()

    # d = attrdict.AttrDict()
    d = AttrDict2()
    d.fn = fn
    if fn:
        d.path = os.path.dirname(fn)
    else:
        d.path = None
    
    d.version = lines[1]
    
    time, date = lines[3].split()
    hr, m, secs = [int(i) for i in time.split(':')]
    day, month, yr = [int(i) for i in date.split('.')]
    d.compile_time = datetime.time(hr, m, secs)
    try:
        d.compile_date = datetime.date(yr, month, day)
        d.compile_datetime = datetime.datetime(yr, month, day, hr, m, secs)
    except ValueError:
        d.compile_datetime = None

    time, date = lines[5].split()
    hr, m, secs = [int(i) for i in time.split(':')]
    day, month, yr = [int(i) for i in date.split('.')]
    d.run_time = datetime.time(hr, m, secs)
    try:
        d.run_date = datetime.date(yr, month, day)
        d.run_datetime = datetime.datetime(yr, month, day, hr, m, secs)
    except ValueError:
        d.run_datetime = None

    d.run_elapsed = float(lines[7])
    d.niterations = int(lines[9])
    d.nds, d.SharpPrior, d.SharpVertical, d.SharpHorizontal = [
        float(i) for i in lines[11].split()[:4]]
    d.nds = int(d.nds)
    d.dds = [int(i) for i in lines[13].split()]
    d.data_fns = [fn for fn in lines[15].split()]
    d.model_fn = lines[17]
    nm, doi = lines[19].split()
    d.nm = int(nm)
    d.doi = {0: False, 1: True}[int(doi)]
    d.nparams = int(lines[21])
    d.nlayers_model = [int(i) for i in lines[23].split()]

    d.res_min, d.res_max, d.thk_min, d.thk_max = [
        float(i) for i in lines[27].split()]
    d.aniso_min, d.aniso_max, d.chrg_min, d.chrg_max = [
        float(i) for i in lines[29].split()]
    d.min_apriori_std = float(lines[31])
    d.dset_types = [int(i) for i in lines[35].split()]
    d.dset_src_types = [int(i) for i in lines[37].split()]

    save_model_lines = False
    model_lines = []
    for i, line in enumerate(lines):
        if line.startswith('Parameters (0..NIte'):
            save_model_lines = True
            continue
        if line.startswith('Analysis: apriori'):
            save_model_lines = False
            continue
        if save_model_lines:
            model_lines.append(line)
    model_flobj = StringIO.StringIO('\n'.join(model_lines[1:]))
    d.model_params = numpy.loadtxt(model_flobj)
    d.models = []
    n = d.nlayers_model[0]
    for i in range(d.niterations + 1):
        # md = attrdict.AttrDict()
        md = AttrDict2()
        for j in range(n):
            md.rhos = d.model_params[i, 1: 1+n]
            md.thks = d.model_params[i, n+1: (n+1) + (n-1)]
            md.tops = model1d.thks2tops(md.thks)
        d.models.append(md)
    d.final_rhos = d.models[-1].rhos
    d.final_thks = d.models[-1].thks
    d.final_tops = d.models[-1].tops

    return d

