#!/usr/bin/python3
import os
from pathlib import Path
import re

from appconfig import get_ovpn_config_dir, list_configs

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
