import json
import click
from collections import defaultdict

from ipvanish import get_city_servers, get_countries, get_country_cities, get_countries_status, city_abv_pair

from .cli_helpers import column_print, column_print_plainjane, center, title_block

example_secho_list = [
        # as in key => status
        { 'name': 'NZ', 'stats': {'fg': 'green', 'bg': ''} },
        { 'name': 'US', 'stats': {'fg': 'red', 'bg': 'blue'} },
        { 'name': 'UK', 'stats': {'fg': 'green', 'bg': ''} },
]

@click.group()
def main():
    return


@click.command()
def get_ctry():
    banner = " Available Countries "
    title_block(banner)
    print()
    c = get_countries()
    column_print_plainjane(c)

@click.command()
def get_status():
    banner = " Server stats "
    title_block(banner)
    print()
    column_print(example_secho_list)

@click.command()
@click.option('--country')
def cities_in_country(country):
    l = get_country_cities(country)
    color = 'blue'
    d = []
    #banner = f" Cities in {country} "
    #title_block(banner)
    print()
    pairs = city_abv_pair()
    pairs = [x for x in sorted(pairs, key=lambda pair: pairs[0]) ]
    #print(len(pairs))
    for p in pairs:
        d.append({'name': f"{p[0]} ({p[1]})", 'stats': {'fg': color}})
#        print(p)
#        print(p[0])
#        print(p[1])
#    return
    print(d)
    column_print(d)

@click.command()
def get_servers():
    get_city_servers()

@click.command()
def yo():
    click.secho("Hello world!", fg='blue')
    

main.add_command(yo, name='hi')
main.add_command(get_servers, name='srv')
main.add_command(get_ctry, name='ctry')
main.add_command(get_status, name='stat')
main.add_command(cities_in_country, name='list_cities')

if __name__ == '__main__':
    main()
