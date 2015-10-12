import argparse
from ConfigParser import SafeConfigParser
import glob
import logging
import os
import shutil
import subprocess
import sys

import utils


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
        process = subprocess.Popen(
            ["AarhusInv64.exe", modfn_basefn],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        while process.returncode is None:
            line = process.stdout.readline().strip('\n')
            logger.debug(line)
            if 'Error in CConvJ01. Subroutine SqLoop1' in line:
                logger.error('Stopping inversion')
                process.kill()
            process.poll()
    except subprocess.CalledProcessError as e:
        d = '------------------------------------------------------------'
        utils.skip_exception("ERROR\n%s\n%s\n%s\n" % (d, e.output, d))
    finally:
        os.remove("AarhusInv64.exe")
        os.remove("AarhusInvLic.exe")
        os.chdir(startpath)
    return result


def mainfunc(models, recurse, dry_run, no_emo):
    if recurse:
        for modeldir in models:
            assert os.path.isdir(modeldir)
            modfns = []
            for root, dirs, files in os.walk(modeldir):
                modfns += [os.path.join(root, f) for f in files if f.endswith('.mod')]
    else:
        modfns = [fn for fn in models if os.path.isfile(fn)]

    if no_emo:
        modfns2 = []
        for modfn in modfns:
            if not os.path.isfile(modfn.replace('.mod', '.emo')):
                modfns2.append(modfn)
        modfns = modfns2

    for modfn in modfns:
        logger.info("Found .mod file %s" % modfn)

    n = len(modfns)
    for i, modfn in enumerate(modfns):
        logger.info("Start inversion (% 5d/% 5d) for %s" % (i + 1, n, modfn))
        if not dry_run:
            run(modfn)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s %(levelname)s %(filename)s"
                "#%(lineno)d.%(funcName)s: %(message)s"))
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--dry-run', action='store_true', default=False, help="don't actually make any changes")
    p.add_argument('-r', '--recurse', action='store_true', default=False, help="look recursively")
    p.add_argument('--no-emo', action='store_true', default=False)
    p.add_argument('models', nargs='*', help="model files to run OR paths to recurse over")
    args = p.parse_args(sys.argv[1:])
    return mainfunc(**args.__dict__)


def register_entryfunc():
    p = argparse.ArgumentParser()
    p.add_argument('path', help='location of AarhusInv64.exe etc.')
    args = p.parse_args(sys.argv[1:])
    register(args.path)
    if check_path(args.path):
        print('Successfully registered AarhusInv at %s' % args.path)


if __name__ == "__main__":
    main()

