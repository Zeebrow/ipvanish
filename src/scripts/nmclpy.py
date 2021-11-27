import json
import click
from click import echo, style

from ipvanish import get_ovpn_config_dir

from .cli_helpers import column_print, column_print_plainjane, center, title_block


@click.group()
def main():
    return


@click.command()
def conn_show():
    pass

main.add_command("show", conn_show)

if __name__ == '__main__':
    main()
