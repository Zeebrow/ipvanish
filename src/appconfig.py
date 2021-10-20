from pathlib  import Path
import os
import getpass

PROG_NAME = "ipvanish"
def get_ovpn_config_dir():
    if os.getenv("IPVANISH_CONFIGS_DIR"):
        ovpn_config_dir = os.getenv("IPVANISH_CONFIGS_DIR")
    elif os.getenv("XDG_CONFIG_HOME"):
        ovpn_config_dir = Path(os.getenv("XDG_CONFIG_HOME")) / f"{PROG_NAME}/configs"
    else:
        try:
            ovpn_config_dir = Path(os.path.expanduser("~")) / f".config/{PROG_NAME}/configs"
            os.stat(ovpn_config_dir)
        except:
            print(f"No configs file found at '{ovpn_config_dir}'")

    return ovpn_config_dir

