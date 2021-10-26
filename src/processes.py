import os
import subprocess
import getpass
import tempfile
import shutil
import zipfile
import io
# TODO: refactor to save requests dependency 
from requests import get
from ipvanish import get_ovpn_config_dir

def update_configs(cfg_dir=get_ovpn_config_dir()):
    # backup existing config
    cfg_dir_bkup = tempfile.TemporaryDirectory(prefix='ipvanish-', suffix='-conf.bkup' )
    shutil.copytree(src=cfg_dir, dst=cfg_dir_bkup+'/configs', copy_function=shutil.copy2)
    
    try:
        # TODO: host proxy for configs.zip
        url = "https://www.ipvanish.com/software/configs/configs.zip"
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(cfg_dir)
    except Exception as e:
        print(e)
        # compress backup
        #TODO: nowzers -> datetime
        nowzers='ryenow'
        shutil.make_archive(f'configs-bkup-{nowzers}.zip')
        print(f"backup config accessible at '{cfg_dir_bkup.name}'")
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
    print(cmd)
    with open("ipvanish.log", "a+") as logf:
        c = subprocess.Popen(cmd, stdout=logf, stderr=logf)
    with open("ipvanish.pid", "w+") as pidf:
        print(c.pid)
        pidf.write(str(c.pid))


def stop(self):
    with open(f"ipvanish.pid", "r") as pidf:
        p = pidf.read()


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            start(cfgfile="tests/configs/ipvanish-RS-Belgrade-beg-c01.ovpn", upfile="/home/zeebrow/.up")
        elif "stop" == sys.argv[1]:
            stop()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("no")
        sys.exit(1)

# sudo openvpn --config configs/ipvanish-RS-Belgrade-beg-c01.ovpn --ca configs/ca.ipvanish.com.crt     --user zeebrow --auth-user-pass "$HOME/.up"
