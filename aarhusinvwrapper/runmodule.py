import argparse
from ConfigParser import SafeConfigParser
import glob
import logging
import os
import shutil
import subprocess
import sys


logger = logging.getLogger(__name__)


APP_ORGANISATION = "aarhusinvwrapper"
APP_TEAM = "aarhusinvwrapper"
APP_NAME = "aarhusinvwrapper"
WIN32_MYAPPID = "%s.%s.%s" % (APP_ORGANISATION, APP_TEAM, APP_NAME)
try:
    APPDATA_DIR = os.environ["APPDATA"]
except:
    APPDATA_DIR = "~"
APP_PATH = os.path.join(APP_ORGANISATION, APP_TEAM, APP_NAME)
CONFIG_DIR = os.path.join(APPDATA_DIR, APP_ORGANISATION, APP_TEAM, APP_NAME)
CONFIG_FN = os.path.join(CONFIG_DIR, 'aarhusinvwrapper.ini')
for subdir in ("rawdata", "probes"):
    if not os.path.isdir(os.path.join(CONFIG_DIR, subdir)):
        os.makedirs(os.path.join(CONFIG_DIR, subdir))


def register(path):
    check_path(path)    
    config = SafeConfigParser()
    config.read(CONFIG_FN)
    if not config.has_section('main'):
        config.add_section('main')
    config.set('main', 'aarhusinv_path', path)

    with open(CONFIG_FN, mode='w') as f:
        config.write(f)


def get_registered_path():
    config = SafeConfigParser()
    config.read(CONFIG_FN)
    path = config.get('main', 'aarhusinv_path')
    check_path(path)
    return path
        

def check_path(path):
    assert os.path.isdir(path)
    for expected_filename in [
            "AarhusInv.con",
            "AarhusInv64.exe",
            "AarhusInvLic.exe"
            ]:
        assert os.path.isfile(os.path.join(path, expected_filename))
    return True


def run(modfn):
    '''Run AarhusInv on model file.'''
    assert os.path.isfile(modfn)
    reg_path = get_registered_path()
    modfn_path, modfn_basefn = os.path.split(modfn)

    exefile = os.path.join(reg_path, "AarhusInv64.exe")
    licfile = os.path.join(reg_path, "AarhusInvLic.exe")
    confile = os.path.join(reg_path, "AarhusInv.con")
    shutil.copy(exefile, modfn_path)
    shutil.copy(licfile, modfn_path)
    if not os.path.isfile(os.path.join(modfn_path, "AarhusInv.con")):
        shutil.copy(confile, modfn_path)

    result = None
    startpath = os.getcwd()
    try:
        os.chdir(modfn_path)
        assert os.path.isfile(modfn_basefn)
        result = subprocess.check_output(["AarhusInv64.exe", modfn_basefn])
    except subprocess.CalledProcessError as e:
        print e.output
        raise
    finally:
        os.remove("AarhusInv64.exe")
        os.remove("AarhusInvLic.exe")
        os.chdir(startpath)
    return result


def mainfunc(models, recurse, dry_run):
    if recurse:
        for modeldir in models:
            assert os.path.isdir(modeldir)
            modfns = []
            for root, dirs, files in os.walk(modeldir):
                modfns += [os.path.join(root, f) for f in files if f.endswith('.mod')]
    else:
        modfns = [fn for fn in models if os.path.isfile(fn)]

    for modfn in modfns:
        logger.info("Found .mod file %s" % modfn)

    n = len(modfns)
    for i, modfn in enumerate(modfns):
        logger.info("Start inversion (% 5d/% 5d) for %s" % (i + 1, n, modfn))
        if not dry_run:
            logger.debug(run(modfn))


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s  %(levelname)s  %(filename)s  "
                "line %(lineno)d %(funcName)s : %(message)s"))
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--dry-run', action='store_true', default=False, help="don't actually make any changes")
    p.add_argument('-r', '--recurse', action='store_true', default=False, help="look recursively")
    p.add_argument('models', nargs='*', help="model files to run OR paths to recurse over")
    args = p.parse_args(sys.argv[1:])
    return mainfunc(**args.__dict__)


if __name__ == "__main__":
    main()

