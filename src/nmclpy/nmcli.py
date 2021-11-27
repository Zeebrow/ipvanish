from argparse import Namespace
import subprocess
import os
from pathlib import Path
from types import SimpleNamespace

from .ipvanish import get_ovpn_config_dir

cmd_base = ['nmcli', '--color', 'no', '--terse']
IPV_USERNAME = 'mzborowski@yahoo.com'
with open(Path.home() / '.pwfile') as f:
    IPV_PLAINTEXT = f.read()

connection_field_values = [
        'NAME', 'UUID', 'TYPE', 'TIMESTAMP', 'TIMESTAMP-REAL',
        'AUTOCONNECT', 'AUTOCONNECT-PRIORITY', 'READONLY', 
        'DBUS-PATH', 'ACTIVE', 'DEVICE', 'STATE', 'ACTIVE-PATH', 
        'SLAVE', 'FILENAME'
        ]

def connections_show(*args, strip_headers=False, show_all=False):
    args = [ARG.upper() for ARG in args]

    if show_all:
        args = connection_field_values
    cmd = ['nmcli', '--color', 'no' ] + (['-f', ','.join(args)] if len(args) > 0 else []) + [ 'connection', 'show', ]

    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    r = result.stdout.split("\n")
    if result.stderr != '':
        print("Error:")
        print(result.stderr)
        return
    lines = []
    for i in r:
        if strip_headers:
            # get rid of line 1
            strip_headers = False
            continue
        lines.append(i.strip())
    return lines

def connection_down():
    """Deactivate the active vpn connection"""
    connections = connections_show('NAME', 'DEVICE', 'STATE', strip_headers=False)
    for ch in connections:
        print(f"Choices: {ch}")
    active_vpn_connections = []
    for count, c in enumerate(connections):
        if count == 0:
            headers = c.split()
            continue
        if (not c.startswith('ipvanish')):
            continue
        active_vpn_connections.append(c.split())
    ac = []
    print(f"{headers=}")
    for c in active_vpn_connections:
        obj = SimpleNamespace(**dict(zip(headers, c)))
        #obj = dict(zip(headers, c))
        ac.append(obj)
        print(f"Active connections: {c}")
    return ac 

def connection_up(name: str):
    connections = []
    for c in connections_show('NAME', strip_headers=True):
        if not c.startswith('ipvanish-'):
            continue
        connections.append(c)
    if name not in connections:
        print(f"No such connection: '{name}'")
        print(f"Choices are {connections}")
        return False

    cmd = ['nmcli', 'conn', 'up', name]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    if result.stderr != '':
        print(f"Something went wrong: {result.stderr}")
        return
    if "Warning" in result.stdout:
        print(f"Uh oh! looks like you're using an ad blocker. :^) ")
    print(result.stdout)
    return True



def add_vpn_connection(cfg_file: str):
    conn_name = cfg_file.split('.')[0]
    print(conn_name)
    conns = find_ipvanish_connections()
    for c in conns:
        _c = c.split(':')[0]
        print(f"{_c} == {conn_name}")
        if _c == conn_name:
            print(f"Connection '{conn_name}' already exists.'")
            return False

    cfg_dir = get_ovpn_config_dir()

    gogo = False
    for f in os.listdir(cfg_dir):
        if f == cfg_file:
            filepath = cfg_dir / cfg_file
            gogo = True
            break
    if not gogo:
        print("ERROR: no such config file '{cfg_file}'")
        return False

    cmd = ["nmcli", "con", "import", "type", "openvpn", "file", filepath]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"ERROR: command returned {result.returncode} - could not import '{filepath.name}'")
        print(f"message: {result.stderr}")
        return False

    cmd = ["nmcli", "con", "modify", conn_name, '+vpn.user-name', IPV_USERNAME]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"ERROR: command returned {result.returncode} - could not set '+vpn.user-name'for connection {conn_name}'!")
        print(f"message: {result.stderr}")
        return False
        
    cmd = ["nmcli", "con", "modify", conn_name, '+vpn.secrets', f"password={IPV_PLAINTEXT}"]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"ERROR: command returned {result.returncode} - could not set '+vpn.user-name'for connection {conn_name}'!")
        print(f"message: {result.stderr}")
        return False
    return True

def notes():
    # https://developer-old.gnome.org/NetworkManager/stable/index.html 
    # man 5 nm-settings

    # nmcli conn import type 
    # nmcli c modify ipvanish-RS-Belgrade-beg-c01 +vpn.user-name 'mzborowski@yahoo.com'
    # nmcli c modify ipvanish-RS-Belgrade-beg-c01 +vpn.secrets 'password=passw0rd'

    # nmcli general permissions
    pass

def find_ipvanish_connections():
    cmd = ["nmcli", "--terse", "-f", "NAME,STATE", "conn", "show"]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    firstline = True
    conn_matches = []
    for line in result.stdout.strip().split('\n'):
#        if firstline:
#            firstline = False
#            continue
        if line.split(':')[0].startswith('ipvanish'):
            conn_matches.append(line)
    return conn_matches

def active_connections():
    ipv_conns = find_ipvanish_connections()
    active_conns = []
    for conn in ipv_conns:
        if conn.split(':')[1] == 'activated':
            active_conns.append(conn.split(':')[0])
    if len(active_conns) == 1:
        return active_conns[0]
    else:
        return active_conns

def conn_down(conn_name):
    cmd = ["nmcli", "--terse", "connection", "down", conn_name]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"ERROR: command '{' '.join(cmd)}' returned {result.returncode} !")
        print(f"stderr message: {result.stderr}")
        return False
    print(f"stdout message: {result.stdout}")
    return True

def conn_up(conn_name):

    cmd = ["nmcli", "--terse", "connection", "up", conn_name]
    conns = find_ipvanish_connections()
    for c in conns:
        if conn_name == c.split(':')[0]:
            result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
            if result.returncode != 0:
                print(f"ERROR: command '{' '.join(cmd)}' returned {result.returncode} !")
                print(f"message: {result.stderr}")
                return False
            print(f"message: {result.stdout}")
            return True
    print(f"ERROR: is '{conn_name}' a valid connection?")
    print(f"possible options: {conns}")
    return False

def remove_ipv_connection(conn_name):
    cmd = ["nmcli", "--terse", "connection", "delete", conn_name]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"ERROR: command '{' '.join(cmd)}' returned {result.returncode} !")
        print(f"stderr message: {result.stderr}")
        return False
    print(f"stdout message: {result.stdout}")
    return True

if __name__ == '__main__':
#    import argparse
#    # EXAMPLE USAGE
#    # python3 nmcli -f NAME UUID --strip-headers
#
#    values = [
#            'NAME', 'UUID', 'TYPE', 'TIMESTAMP', 'TIMESTAMP-REAL',
#            'AUTOCONNECT', 'AUTOCONNECT-PRIORITY', 'READONLY', 
#            'DBUS-PATH', 'ACTIVE', 'DEVICE', 'STATE', 'ACTIVE-PATH', 
#            'SLAVE', 'FILENAME'
#            ]
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--fields', '-f', choices=values, nargs='+', default=values)
#    parser.add_argument('--strip-headers',action='store_true',  default=False)
#
#    args = parser.parse_args()
#    fields = args.fields
#
#    # args from command line (-f ... )
#    for i in connections_show(*args.fields, strip_headers=args.strip_headers):
#        print(i)
#
    print(find_ipvanish_connections())
    print(active_connections())
    #conn_down('ipvanish-sjc')
    #conn_up('ipvanish-sjc')
    #remove_ipv_connection('ipvanish-RS-Belgrade-beg-c02')
    add_vpn_connection('ipvanish-RS-Belgrade-beg-c03.ovpn')

