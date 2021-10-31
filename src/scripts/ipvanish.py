import json
import click
from click import echo, style
from collections import defaultdict

from ipvanish import ConfigurationSet, get_city_servers, get_country_cities, get_countries_status, city_abv_pair

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
    config = ConfigurationSet()
    banner = " Available Countries "
    title_block(banner)
    print()
    c = config.countries
    column_print_plainjane(c)

# TODO add number of servers next to city name
@click.command()
def get_all_cities():
    config = ConfigurationSet()
    color='yellow'
    d = []
    banner = f" All Cities "
    title_block(banner)
    print()
    for i,c in enumerate(config.countries):
        click.echo(f"{i}) ", nl=None)
        click.secho(f"{c} ({len(config.abvXcountry[c])}) ", fg='blue', nl=None)
        click.secho(f"{', '.join(config.abvXcountry[c])}", fg='green')
        
#    pairs = city_abv_pair()
#    pairs = [x for x in sorted(pairs, key=lambda pair: pairs[0]) ]
#    for p in pairs:
#        #d.append({'name': f"{p[0]} ({p[1]})", 'stats': {'fg': color}})
#        d.append({'name': f"{p[1]}", 'stats': {'fg': color}})
#    column_print(d)


@click.command()
def get_status():
    banner = " Server stats "
    title_block(banner)
    print()
    column_print(example_secho_list)


# TODO make option mandatory
@click.command()
@click.option('--country')
def get_cities(country):
    config = ConfigurationSet()
    if country in config.cityXcountry.keys():
        city_countries = sorted(list(config.cityXcountry[country]))
    else:
        click.secho(f"No such country '{country}'", fg='red')
        return

    color = 'blue'
    d = []
    banner = f" Cities in {country} "
    title_block(banner)
    print()
    for c in city_countries:
        d.append({'name': c, 'stats': {'fg': color}})
    column_print(d)

# TODO
# TODO make option mandatory
@click.command()
@click.option('--city')
def get_servers(city):
    config = ConfigurationSet()



@click.command()
def yo():
    click.secho("Hello world!", fg='blue')
    

main.add_command(yo, name='hi')
main.add_command(get_servers, name='srv*')
main.add_command(get_ctry, name='ctry')
main.add_command(get_status, name='stat*')
main.add_command(get_cities, name='list_cities')
main.add_command(get_all_cities, name='all')

if __name__ == '__main__':
    main()