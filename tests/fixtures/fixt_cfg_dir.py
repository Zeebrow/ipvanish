import pytest
from pytest import MonkeyPatch
import random
import string
from collections import defaultdict
from data import some_52_countries

import tempfile
import os
from pathlib import Path
from ipvanish import ConfigurationSet


def create_config_filename(namelen=10, **kw) -> string:
    """
    kwargs:  country city, abv
    """ 
    for k in kw.keys():
        if k not in ['country', 'city', 'abv', 'server']:
            print(f"WARN: ignoring keyword argument '{k}'")
            continue
    c,a = city_abv_pair(city_name_len=namelen)
    return f"ipvanish-{kw.get('country', random.choice(some_52_countries))}-{kw.get('city',c)}-{kw.get('abv',a)}-{kw.get('server', random_server_name())}.ovpn"

def rand_ascii(num=1, case=None) -> str:
    """
    Generate random ascii characters of definite length, or in a pattern
    """
    if case in ('u', 'upper'):
        _f = lambda: random.choice(string.ascii_uppercase)
    elif case in ('l', 'lower'):
        _f = lambda: random.choice(string.ascii_lowercase)
    elif case in ('p', 'proper'):
        _f = lambda: random.choice(string.ascii_lowercase)
        return random.choice(string.ascii_uppercase) + ''.join([_f() for i in range(num-1)])
    else:
        _f = lambda: random.choice(string.ascii_letters)
    return ''.join([_f() for i in range(num)])

def city_abv_pair(city_name_len=10) -> tuple:
    name = rand_ascii(city_name_len, 'proper')
    abv = name[0:2].lower() + name[-1]
    return name,abv

def random_server_name():
    #return rand_ascii(1,'l') + srvr_digits(2)
    return rand_ascii(1,'l') + f"{random.randint(0, 99):02}"

def fixture_config_dirs(tmp_path='', range_lo=5, range_hi=10):
    """
    returns a tuple of the path to a temporary directory and the randomly
    generated number of empty .ovpn files inside.
    """
    tdir = Path(tempfile.TemporaryDirectory().name)
    # tmp_path refers to pytest fixture. keeping JIC
    #tdir = tmp_path / "configs"
    tdir.mkdir()
    num_files = random.randint(range_lo,range_hi)
    for f in range(num_files):
        f1 = tdir / f"file{f}.ovpn"
        f1 = tdir / create_config_filename()
        f1.touch()
    # make some other files too
    for i in range(random.randint(1,3)):
        randofile = tdir/f"rando{i}"
        randofile.touch()

    return (tdir, num_files)

# TODO? turn into wrapper function
def fixture_filled_config_dir():
    fake_file_content = """
client
dev tun 
proto udp 
remote atl-a05.ipvanish.com 443 
resolv-retry infinite
nobind
persist-key
persist-tun
persist-remote-ip
ca ca.ipvanish.com.crt
verify-x509-name atl-a05.ipvanish.com name
auth-user-pass
comp-lzo
verb 3
auth SHA256
cipher AES-256-CBC
keysize 256 
tls-cipher TLS-DHE-RSA-WITH-AES-256-CBC-SHA:TLS-DHE-DSS-WITH-AES-256-CBC-SHA:TLS-RSA-WITH-AES-256-CBC-SHA
    """
    tdir, num_valid_files = fixture_config_dirs()
    for f in os.listdir(tdir):
        if f.endswith('.ovpn'):
            with open(f, 'wb') as cfgf:
                cfgf.write(fake_file_content.encode())
    return (tdir, num_valid_files)

@pytest.fixture
def fake_cfg_dir():
    """
    returns a length-2 tuple, (Path(tempdir), num_ovpn_files)
    where tempdir contains a random number of files (between 6 and 13),
    at least `num_ivpn_dirs` of which are valid ovpn config filenames.

    All files in `tempdir` are empty.
    """
    return fixture_config_dirs()

@pytest.fixture
def fake_filled_cfg_dir():
    """
    Similar to `fake_cfg_dir`, but files have dummy content.
    File content is not guaranteed to be a valid openvpn configuration.
    returns 2-tuple (Path(tempdir), num_ovpn_files)
    """

    return fixture_filled_config_dir() 

@pytest.fixture
def patched_cs():
    """
    Similar to fake_cfg_dir, but returns a 3-tuple,
    where the first item is a `ConfigurationSet()` that has been 
    monkeypatched.

    TODO: Depreciate in favor of passing the directory name to 
    the constructor, to override environment variables.
    """
    cfg_dir, ovpn_count = fixture_config_dirs()
    print(os.listdir(cfg_dir))
    mp = MonkeyPatch()
    with mp.context() as mc:
        rtn = ConfigurationSet(cfg_dir)
        return (rtn, cfg_dir, ovpn_count)

def test_patched_cs(patched_cs):
    cf, cfg, ct = patched_cs
    assert os.listdir(cfg) == os.listdir(cf.cfg_dir)

    print(f"TEST_PATCHED_CS: {cf.countries}")
    print(f"TEST_PATCHED_CS: {cfg}")
    print(f"TEST_PATCHED_CS: {cf.cfg_dir}")

if __name__ == '__main__':
    for i in range(25):
        print(random_server_name())
    print(some_52_countries)
#    for i in range(5):
#        gf, ct = fixture_config_dirs()
#        for j in os.listdir(gf):
#            print(f"({i}) {j}")
#
    # sanity checks
#    print()
#    print(f"{rand_ascii(2,'l')=}")
#    print(f"{rand_ascii(2,'u')=}")
#    print(f"{rand_ascii(10,'p')=}")
#    print()
#    print(f"{create_config_filename(namelen=15, country='US')=}")
#    print(f"{create_config_filename(country='US')=}")
#    print(f"{create_config_filename(city='Abbudabi')=}")
#    print(f"{create_config_filename(abv='adb')=}")
#    print(f"{create_config_filename(server='a01')=}")
#    print()
#    print(f"{srvr_digits(1)=}")
#    print(f"{srvr_digits(2)=}")
#    print()
#    print(f"{city_abv_pair()=}")
#    print(f"{city_abv_pair(15)=}")
#    print()
#    print(f"{random_server_name()=}")
#    print()
#    print(f"{create_config_filename()=}")
#    print(f"{create_config_filename(5)=}")
#    print(f"{create_config_filename(15)=}")
#    print(f"{create_config_filename(20)=}")
#
