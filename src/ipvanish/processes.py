import os
import subprocess
import getpass
import tempfile
import shutil
import zipfile
import io
import logging
from pathlib import Path
from requests import get

from .utils import get_ovpn_config_dir

#from ipvanish import get_ovpn_config_dir

logger = logging.getLogger(__name__)

def update_configs(cfg_dir=get_ovpn_config_dir()):
    cfg_dir_bkup = Path(tempfile.mkdtemp(prefix='ipvanish-cfg-bkup'))
    shutil.copytree(src=cfg_dir, dst=cfg_dir_bkup / 'configs', copy_function=shutil.copy2)
    print(cfg_dir_bkup)
    try:
        # TODO: host proxy for configs.zip
        url = "https://www.ipvanish.com/software/configs/configs.zip"
        r = get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(cfg_dir)
        raise Exception("test exception")
    except Exception as e:
        print(e)
        logger.critical(e)
        #TODO: nowzers -> datetime
        nowzers='ryenow'
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
    update_configs()
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
