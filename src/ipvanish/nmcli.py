from argparse import Namespace
import subprocess
import os
from pathlib import Path

cmd_base = ['nmcli', '--color', 'no']

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
        obj = dict(zip(headers, c))
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



def add_vpn_connection(cfg_filepath: Path):
    if not cfg_filepath.exists():
        print(f"No such file: {cfg_filepath}")
        return False
    current_connections = connections_show('NAME', strip_headers=True)

    cmd = ["nmcli", "con", "import", "type", "vpn", "file", str(cfg_filepath.absolute())]
    result = subprocess.run(cmd, capture_Coutput=True, encoding='utf-8')
    stdout = result.stdout.split("\n")
    if result.stderr != '':
        print(f"Something wnet worng: {result.stderr}")
        print(f"stdout: {result.stdout}")
        



if __name__ == '__main__':
    import argparse
    # EXAMPLE USAGE
    # python3 nmcli -f NAME UUID --strip-headers

    values = [
            'NAME', 'UUID', 'TYPE', 'TIMESTAMP', 'TIMESTAMP-REAL',
            'AUTOCONNECT', 'AUTOCONNECT-PRIORITY', 'READONLY', 
            'DBUS-PATH', 'ACTIVE', 'DEVICE', 'STATE', 'ACTIVE-PATH', 
            'SLAVE', 'FILENAME'
            ]
    parser = argparse.ArgumentParser()
    parser.add_argument('--fields', '-f', choices=values, nargs='+', default=values)
    parser.add_argument('--strip-headers',action='store_true',  default=False)

    args = parser.parse_args()
    fields = args.fields

    # args from command line (-f ... )
    for i in connections_show(*args.fields, strip_headers=args.strip_headers):
        print(i)


