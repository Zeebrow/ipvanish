from pathlib  import Path
import os
import getpass

PROG_NAME = "ipvanish"
DEFAULT_CONFIGS_DIR = str(Path(os.path.expanduser("~")) / f".config/{PROG_NAME}/configs")
CA_CERTFILE = lambda cfgdir: str(Path(cfgdir)/"ca.ipvanish.com.crt")

def get_ovpn_config_dir(default_configs_dir=DEFAULT_CONFIGS_DIR):
    """
    default_configs_dir: str
    env vars should (must?) be absolute paths
    """
    if os.getenv("IPVANISH_CONFIG_DIR"):
        ovpn_config_dir = str( Path(os.getenv("IPVANISH_CONFIG_DIR")) )
    elif os.getenv("XDG_CONFIG_HOME"):
        ovpn_config_dir = str( Path(os.getenv("XDG_CONFIG_HOME")) / f"{PROG_NAME}/configs" )
    else:
        try:
            ovpn_config_dir = str( Path( default_configs_dir ) ) 
            os.stat(ovpn_config_dir)
        except Exception as e:
            print(e)
            print(f"No such directory '{str(ovpn_config_dir)}'")

    return ovpn_config_dir

def ovpn_config_dir_is_invalid(ovpn_config_dir):
    try:
        os.stat(ovpn_config_dir)
        os.stat(CA_CERTFILE(ovpn_config_dir))
        return False
    except FileNotFoundError as e:
        return e

if __name__ == '__main__':
    print(get_ovpn_config_dir())
