from pathlib  import Path
import os
import getpass

def get_ovpn_config_dir():
    if os.getenv("XDG_CONFIG_HOME"):
        ovpn_config_dir = Path(os.getenv("XDG_CONFIG_HOME")) / "ipvanish/configs"
    else:
        try:
            ovpn_config_dir = Path(os.path.expanduser("~")) / ".config/ipvanish/configs"
            os.stat(ovpn_config_dir)
        except:
            print(f"No configs file found at '{ovpn_config_dir}'")

    return ovpn_config_dir

