#!/usr/bin/python3
import os
from pathlib import Path
import re
import getpass
import random
from collections import defaultdict
import hashlib 
from dataclasses import dataclass, field

from .utils import *
from .constants import ctry_dict
from .exceptions import InvalidConfigurationWarning


@dataclass
class ConfigFile:
    filepath: str
    filename: str = field(init=False)
    md5: str = field(init=False)
    country: str = field(init=False)
    city: str = field(init=False)
    abv: str = field(init=False)
    server: str = field(init=False)

    def __post_init__(self):
        print(f"=========> {self.filepath}")
        if not Path(self.filepath).exists():
            # might could hold off on raising an exception, so that we know
            # we attempted to load this file but could not.
            # Hesitent about relying on return here, since I can't figure out 
            # what errors this might cause.
            # return None
            raise FileNotFoundError(f"No such configuration file '{self.filepath}' to load. ")
        self.filename = Path(self.filepath).name
        cfgrex = r'^(?:ipvanish-)(?P<country>[A-Z]{2})-(?P<city>.*)-(?P<city_short>[a-z]{3})-(?P<server>[a-z][0-9]{2})(?:\.ovpn)$'
        r = re.compile(cfgrex)
        m = r.match(self.filename)
        if not m:
            raise InvalidConfigurationWarning(f"Ignoring configuration file '{self.filename}': could not parse filename.")
        else:
            self.country = m.groupdict()['country']
            self.city = m.groupdict()['city']
            self.abv = m.groupdict()['city_short']
            self.server = m.groupdict()['server']
            self.md5 = self.get_md5()

    # matches linux md5sum
    def get_md5(self, filepath=None):
        if filepath:
            try:
                with open(Path(filepath).is_dir(), 'r') as f:
                    data = f.read()
                    self.md5 = hashlib.md5(data.encode()).hexdigest()
            except FileNotFoundError:
                pass

class ConfigurationSet:
    """
    representation of all ipvanish config files
    """
    # most params can be supplemented/replaced by db
    def __init__(self, cfg_dir=get_ovpn_config_dir()):
        self.cfg_dir = Path(cfg_dir)
        self.configs = []
        self.countries = []
        self.country_details = ctry_dict
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
        
        # TODO set C.state depending on presence of file
        # meaning list is populated from details dict.
        # so would have to adjust details if there is a 
        # config file for a country that DNE in the details.
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

    # TODO test
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
        self.state = 'no'

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

    def get_db_object_thingy(self):
        return ConfigFile(self.fpath.absolute())

# fake for one cli func
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


if __name__ == "__main__":
    cfgs = get_ovpn_config_dir()
    print(cfgs)
    print(len(os.listdir(cfgs)))
    print(get_countries())
    print(city_abv_pair())
