import click
from ipvanish import get_countries

def list_countries():
    get_countries()

print(list_countries())
