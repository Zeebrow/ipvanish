import os
import subprocess
import getpass
import tempfile
import shutil
import zipfile
import io
import logging
from time import time
from pathlib import Path
import urllib3

from requests import get

from .utils import get_ovpn_config_dir, get_backup_dir

# this is fucked and you know it
from .utils import create_config_backup


logger = logging.getLogger(__name__)

"""
Functions that interact with the OS - 
writing files, starting processes, etc.

Try to keep it that way, so problems are easier to trace...
"""

def update_config_file(filename: str):
    pass

def _backup_configs(cfg_dir=get_ovpn_config_dir()):
    """ might be better to move this to a function """
    pass

def restore_configs(bkup_dir=get_backup_dir(), cfg_dir=get_ovpn_config_dir()):
    """
    restore config from a zip archive
    """
    for f in os.listdir(bkup_dir):
        fpath = os.path.join(bkup_dir, f)
        latest = ''
        latest_ctime = 0
        _st = os.stat(fpath)
        if (os.stat(f).st_ctime > latest_ctime):
           latest = fpath
           latest_ctime = os.stat(f).st_ctime

    return

def _load_config(file='configs.zip'):
    magic_bytes = lambda compressed_bytes: ''.join(compressed_bytes[0:2].decode())
    try:
        url = f"https://www.ipvanish.com/software/configs/{file}"
        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', url)
        if magic_bytes(resp.data) != 'PK':
            print(f"WARN: '{file}' does not appear to be a zip archive.")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(cfg_dir)

    except Exception as e:
        print(e)

def create_config_backup(dest=None):
    """
    Creates an archive of the current working configuration.
    """
    if not dest:
        dest = get_backup_dir()
    shutil.make_archive(
            root_dir=get_ovpn_config_dir(), 
            base_name=dest / f'configs-{int(time())}',
            format='zip'
            )

    return 

# TODO? I think this needs to be broken down into smaller steps.
def update_configs(cfg_dir=get_ovpn_config_dir(), file='configs.zip', bkup_dest=get_backup_dir()):
    cfg_dir_bkup = Path(tempfile.mkdtemp(prefix='ipvanish-cfg-bkup'))
    shutil.copytree(src=cfg_dir, dst=cfg_dir_bkup / 'configs', copy_function=shutil.copy2)
    try:
        url = f"https://www.ipvanish.com/software/configs/{file}"
        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', url)
        print(f"DEBUG: Grabbed '{file}' ({len(resp.data)} bytes) from {url}")
        z = zipfile.ZipFile(io.BytesIO(resp.data))
        z.extractall(cfg_dir)
        return True
    except Exception as e:
        print(e)
        logger.critical(e)
        nowzers=int(time())
        archive_filename = f'configs-bkup-{nowzers}'
        shutil.make_archive(archive_filename, format='zip', root_dir=cfg_dir_bkup)
        print(f"backup config accessible at '{cfg_dir_bkup / archive_filename}'")
        return False

def start(cfgfile, upfile=None):
    try:
        os.path.exists(upfile)
        autharg = ["--auth-user-pass", upfile]
    except FileNotFoundError:
        u = os.getenv("IPVANISH_AUTH_USER")
        p = os.getenv("IPVANISH_AUTH_PASSWORD")
        if not (u or p):
            raise RuntimeError
        else:
            cmd_append = [""]
            print(f"user/password file {upfile} not found - falling back to environment!")

    # must be run as root

    cmd = ['sudo', 'openvpn', 
            '--ca', 'tests/configs/ca.ipvanish.com.crt', 
            '--auth-user-pass', '"$HOME/.up"']
    cmd += ["--config", cfgfile]
    cmd += ["--user", getpass.getuser()]
    cmd += autharg
    logger.debug(f"running command: {cmd}")
    pidfile = "ipvanish.pid"
    logfile = "ipvanish.log"
    with open(logfile, "a+") as logf:
        c = subprocess.Popen(cmd, stdout=logf, stderr=logf)
    with open(pidfile, "w+") as pidf:
        logger.info(f"ipvanish pid '{c.pid}' saved to file '{pidfile}'")
        pidf.write(str(c.pid))


def stop(self):
    with open(f"ipvanish.pid", "r") as pidf:
        p = pidf.read()


if __name__ == "__main__":
    #restore_configs('.')
    update_configs(cfg_dir='./tmp/cfgtest')
#    import sys
#    if len(sys.argv) == 2:
#        if "start" == sys.argv[1]:
#            start(cfgfile="tests/configs/ipvanish-RS-Belgrade-beg-c01.ovpn", upfile="/home/zeebrow/.up")
#        elif "stop" == sys.argv[1]:
#            stop()
#        else:
#            print("Unknown command")
#            sys.exit(2)
#        sys.exit(0)
#    else:
#        print("no")
#        sys.exit(1)

# sudo openvpn --config configs/ipvanish-RS-Belgrade-beg-c01.ovpn --ca configs/ca.ipvanish.com.crt     --user zeebrow --auth-user-pass "$HOME/.up"
