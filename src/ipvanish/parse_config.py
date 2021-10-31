#!/usr/bin/python3
import os
from pathlib import Path
import re
import getpass
import random

from .utils import *

class Config:
    def __init__(self, fpath):
        self.fpath = Path(fpath)
        if self.fpath.suffix != '.ovpn':
            raise OSError(f"Unsupported file type '{self.fpath.suffix}'!")
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
def get_config_files(cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    files = []
    for cfg in cfgs:
        try:
            c = Config(cfg)
            if c.city_short == city_short:
                servers.append(c.server)
        except OSError:
            pass

    pass

def get_city_servers(city_short, cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    servers = []
    for cfg in cfgs:
        try:
            c = Config(cfg)
            if c.city_short == city_short:
                servers.append(c.server)
        except OSError:
            pass
    return servers
    
def get_countries_status(cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    countries = []
    fake_status_list = ['red', 'green', 'yellow']
    for c in cfgs:
        try:
            status = {'fg': random.choice(fake_status_list)}
            countries.append({Config(c).country: status})
        except OSError:
            pass


def get_countries(cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    countries = []
    for c in cfgs:
        try:
            countries.append(Config(c).country)
        except OSError:
            pass
    return set(countries)

def get_country_cities(country, cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    ccs = []
    for c in cfgs:
        try:
            if country == Config(c).country:
                ccs.append(Config(c).city_short)
        except OSError:
            pass
    return set(ccs)

# TODO test
def city_abv_pair(cfgdir=get_ovpn_config_dir()):
    cfgs = os.listdir(Path(cfgdir))
    pairs = []
    for c in cfgs:
        try:
            cf = Config(c)
            city = cf.city 
            abv = cf.city_short
            pairs.append((city,abv))
        except OSError:
           pass 
    return pairs



if __name__ == "__main__":
    cfgs = get_ovpn_config_dir()
    print(cfgs)
    print(len(os.listdir(cfgs)))
    print(get_countries())
    print(city_abv_pair())
