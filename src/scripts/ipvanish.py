import click

from ipvanish import get_city_servers, get_countries, get_country_cities

from .cli_helpers import column_print

@click.group()
def main():
    return


@click.command()
def get_ctry():
    c = get_countries()
    testlist = ['asdf']
    c = list(c) + testlist
    print(c)
    d = []
    hm = []
    for i in c:
        d.append('green')
    for j in zip(c,d):
        hm.append(j)
    print(hm)
    column_print(hm)

@click.command()
def get_servers():
    get_city_servers()

@click.command()
def yo():
    click.secho("Hello world!", fg='blue')
    

main.add_command(yo, name='hi')
main.add_command(get_servers, name='srv')
main.add_command(get_ctry, name='ctry')

if __name__ == '__main__':
    main()
