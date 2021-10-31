import json
import click
from collections import defaultdict

from ipvanish import get_city_servers, get_countries, get_country_cities, get_countries_status

from .cli_helpers import column_print, column_print_plainjane, center, title_block

example_secho_list = [
        # as in key => status
        { 'name': 'NZ', 'stats': {'fg': 'green', 'bg': ''} },
        { 'name': 'US', 'stats': {'fg': 'red', 'bg': 'blue'} },
        { 'name': 'UK', 'stats': {'fg': 'green', 'bg': ''} },
]

@click.group()
def list_():
    return


@click.command()
def get_ctry():
    banner = " Available Countries "
    title_block(banner)
    print()
    c = get_countries()
    column_print_plainjane(c)

@click.command()
@click.option('--country')
def cities_in_country(country):
    l = get_country_cities(country)
    color = 'blue'
    d = []
    banner = f" Cities in {country} "
    title_block(banner)
    print()
    for i in l:
        d.append({'name': i, 'stats': {'fg': color}})
    column_print(d)

@click.command()
@click.option('--country')
@click.option('--city')
def get_servers(city):
    get_city_servers(city)

main.add_command(get_servers, name='srv')
main.add_command(get_ctry, name='ctry')
main.add_command(get_status, name='stat')
main.add_command(cities_in_country, name='list_cities')

if __name__ == '__main__':
    list_()
