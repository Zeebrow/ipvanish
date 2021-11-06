#!/usr/bin/python3
import os
from pathlib import Path
import re
import getpass
import random
from collections import defaultdict
import hashlib 

from .utils import *
from .constants import ctry_dict

class ConfigurationSet:
    """
    representation of all ipvanish config files
    """
    def __init__(self, cfg_dir=get_ovpn_config_dir()):
        self.cfg_dir = Path(cfg_dir)
        self.configs = []
        self.countries = []
        self.country_details = {}
        self.cityXcountry = defaultdict(set)
        self.abvXcountry = defaultdict(set)
        self.serverXcity = defaultdict(list)
        self.serverXabv = defaultdict(list)
        self.city_abv = defaultdict(set)
        self.abv_city = defaultdict(set)

        self.load()

    def load(self):
        files = os.listdir(self.cfg_dir)
        for f in files:
            try:
                 self.configs.append(Config(f))
            except OSError:
                pass
        _unordered = []
        
        for C in self.configs:
            if C.country not in _unordered:
                self.country_details[C.country] = ctry_dict[C.country]
                _unordered.append(C.country)
            self.cityXcountry[C.country].add(C.city)
            self.abvXcountry[C.country].add(C.city_short)
            self.serverXcity[C.city].append(C.server)
            self.serverXabv[C.city_short].append(C.server)
            self.city_abv[C.city].add(C.city_short)
            self.abv_city[C.city_short].add(C.city)
        for c in sorted(_unordered):
            self.countries.append(c)

    def get_abv(self, guess: str) -> str:
        """ return a city's abreviation from city name or city abv"""
        c = guess.lower()
        c = c.replace(' ','-')
        c = c.replace('_','-')
        if t in self.city_abv.keys():
            return self.city_abv[t]
        if c in self.city_abv.values():
            return self.abv_city[c]

    def get_cities(self, country):
        if country not in self.countries:
            print("WARN: '{country}' is not a valid country.")
            return None
        return (self.cityXcountry[country])
    
    def city_abv_pair(self):
        for C in self.configs:
            city = C.city 
            abv = C.city_short
            self.city_lookup[abv] = city
            self.abv_lookup[city] = abv
        return pairs
    

class Config:
    def __init__(self, fpath):
        self.fpath = Path(fpath)
        if self.fpath.suffix != '.ovpn':
            raise OSError(f"Unsupported file type '{self.fpath.suffix}'!")
        self.fname = self.fpath.name
        self.__dict__.update(self.parse_ipv_fname(self.fname))
        self.md5 = ''

    def __repr__(self):
        return f"{self.country}-{self.city_short}-{self.server}"

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

    def get_md5(self):
        with open(self.fname, 'r') as f:
            data = f.read()
            self.md5 = hashlib.md5(data.encode())


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


#def get_countries(cfgdir=get_ovpn_config_dir()):
#    cfgs = os.listdir(Path(cfgdir))
#    countries = []
#    for c in cfgs:
#        try:
#            countries.append(Config(c).country)
#        except OSError:
#            pass
#    return set(countries)

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
