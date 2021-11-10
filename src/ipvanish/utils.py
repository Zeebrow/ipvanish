from pathlib  import Path
import os
import getpass
import shutil
from time import time

PROG_NAME = "ipvanish"
DEFAULT_CONFIGS_DIR = str(Path(os.path.expanduser("~")) / f".config/{PROG_NAME}/configs")
CA_CERTFILE = lambda cfgdir: str(Path(cfgdir)/"ca.ipvanish.com.crt")

def get_ovpn_config_dir(cfg_dir=None) -> Path:
    """
    returns the full path to a directory containing openvpn configuration files.
    Use this to reference configuration files, and resources relative to them.

    resolution order (from most preferred to least preferred):
        1) function argument
        2) environment variable IPVANISH_CONFIG_DIR
        3) defaul XDG user configuration directory, plus 'ipvanish/configs' ($HOME/.config/ipvanish/configs)

    cfg_dir: str : absolute path to directory where openvpn configuration files live
    env vars should (must?) be absolute paths
    """
    if cfg_dir is not None:
        try:
            os.stat(cfg_dir)
            return cfg_dir
        except Exception as e:
            print(e)
            print(f"No such directory '{cfg_dir}'")
            print("NOT falling back to environ, as config_dir was specified!!")
            raise IndentationError

    if os.getenv("IPVANISH_CONFIG_DIR"):
        #ovpn_config_dir = str( Path(os.getenv("IPVANISH_CONFIG_DIR")) )
        ovpn_config_dir = Path(os.getenv("IPVANISH_CONFIG_DIR"))
    elif os.getenv("XDG_CONFIG_HOME"):
        #ovpn_config_dir = str( Path(os.getenv("XDG_CONFIG_HOME")) / f"{PROG_NAME}/configs" )
        ovpn_config_dir = Path(os.getenv("XDG_CONFIG_HOME")) / f"{PROG_NAME}/configs"
    else:
        try:
            #ovpn_config_dir = str( Path( DEFAULT_CONFIGS_DIR ) ) 
            ovpn_config_dir = Path( DEFAULT_CONFIGS_DIR )
            os.stat(ovpn_config_dir)
        except Exception as e:
            print(e)
            print(f"No such directory '{str(ovpn_config_dir)}'")
            raise IndentationError

    return ovpn_config_dir

def get_backup_dir(bkup_dir=get_ovpn_config_dir(), create_if_missing=True):
    """
    bkup_dir is the full path to a directory containing .zip archives of configuration files.
    """
    rtn = Path(bkup_dir) / '../backup'
    if ( not rtn.exists() ) and create_if_missing:
        rtn.mkdir()
    return rtn


def create_config_backup(dest=None):
    """
    Creates an archive of the current working configuration.
    """
    if not dest:
        dest = get_backup_dir()
    shutil.make_archive(
            root_dir=get_ovpn_config_dir(), 
            base_name=dest / f'configs-{int(time())}',
            format='zip')
    return 

def list_configs(cfg_dir=get_ovpn_config_dir()) -> list:
    """
    return a list of all valid config files
    cfg_dir: path to directory containing config files
    """
    configs = []
    for x in os.listdir(cfg_dir):
        if os.path.splitext(x)[1] == '.ovpn':
            configs.append(x)
    return configs

class InvalidConfiguration(Exception):
    """Raise when no configuration files can be loaded"""
    pass

def ovpn_config_dir_is_invalid(ovpn_config_dir):
    try:
        os.stat(ovpn_config_dir)
        os.stat(CA_CERTFILE(ovpn_config_dir))
        return False
    except FileNotFoundError as e:
        return e

if __name__ == '__main__':
    print(get_ovpn_config_dir())
