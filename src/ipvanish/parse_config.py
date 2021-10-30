#!/usr/bin/python3
import os
from pathlib import Path
import re
import getpass

from .utils import *
#from utils import get_ovpn_config_dir

#from appconfig import get_ovpn_config_dir, list_configs

# ### apconfig.py globalse
# PROG_NAME = "ipvanish"
# DEFAULT_CONFIGS_DIR = str(Path(os.path.expanduser("~")) / f".config/{PROG_NAME}/configs")
# CA_CERTFILE = lambda cfgdir: str(Path(cfgdir)/"ca.ipvanish.com.crt")
# 
# ### appconfig.py functions
# 
# def get_ovpn_config_dir(default_configs_dir=DEFAULT_CONFIGS_DIR):
#     """
#     default_configs_dir: str
#     env vars should (must?) be absolute paths
#     """
#     if os.getenv("IPVANISH_CONFIG_DIR"):
#         ovpn_config_dir = str( Path(os.getenv("IPVANISH_CONFIG_DIR")) )
#     elif os.getenv("XDG_CONFIG_HOME"):
#         ovpn_config_dir = str( Path(os.getenv("XDG_CONFIG_HOME")) / f"{PROG_NAME}/configs" )
#     else:
#         try:
#             ovpn_config_dir = str( Path( default_configs_dir ) ) 
#             os.stat(ovpn_config_dir)
#         except Exception as e:
#             print(e)
#             print(f"No such directory '{str(ovpn_config_dir)}'")
# 
#     return ovpn_config_dir
# 
# def _sanitize_path(p):
#     return str(Path(p))
# 
# def list_configs(cfg_dir=get_ovpn_config_dir()) -> list:
#     """
#     return a list of all valid config files
#     cfg_dir: path to directory containing config files
#     """
#     cfg_dir = _sanitize_path(cfg_dir) 
#     configs = []
#     for x in os.listdir(cfg_dir):
#         if os.path.splitext(x)[1] == '.ovpn':
#             configs.append(x)
#     return configs
# 
# class InvalidConfiguration(Exception):
#     """Raise when no configuration files can be loaded"""
#     pass
# 
# def ovpn_config_dir_is_invalid(ovpn_config_dir):
#     try:
#         os.stat(ovpn_config_dir)
#         os.stat(CA_CERTFILE(ovpn_config_dir))
#         return False
#     except FileNotFoundError as e:
#         return e
# 
# ### end appconfig functions

class Config:
    def __init__(self, fpath):
        self.fpath = Path(fpath)
        if self.fpath.suffix != '.ovpn':
            raise IOError(f"Unsupported file type '{self.fpath.suffix}'!")
        self.fname = self.fpath.name
        self.__dict__.update(self.parse_ipv_fname(self.fname))

    @classmethod
    def parse_ipv_fname(self, ipv_fname):
        """
        If ipv_fname is a valid ipvanish config file,
        returns a dict with the following keys:
        country
        city
        city_short
        server
        """
        cfgrex = r'^(?:ipvanish-)(?P<country>[A-Z]{2})-(?P<city>.*)-(?P<city_short>[a-z]{3})-(?P<server>[a-z][0-9]{2})(?:\.ovpn)$'
        r = re.compile(cfgrex).match(ipv_fname)
        return r.groupdict()

def get_city_servers(city_short, cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    servers = []
    for cfg in cfgs:
        try:
            c = Config(cfg)
            if c.city_short == city_short:
                servers.append(c.server)
        except IOError:
            pass
    return servers
    

def get_countries(cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    countries = []
    for c in cfgs:
        try:
            countries.append(Config(c).country)
        except IOError:
            pass
    return set(countries)

def get_country_cities(country, cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    ccs = []
    for c in cfgs:
        try:
            if country == Config(c).country:
                ccs.append(Config(c).city_short)
        except IOError:
            pass
    return set(ccs)




if __name__ == "__main__":
    cfgs = get_ovpn_config_dir()
    print(cfgs)
    print(len(os.listdir(cfgs)))
    print(get_countries())
