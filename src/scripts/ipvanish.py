import click


@click.group()
def main():
    return

@click.command()
def yo():
    click.secho("Hello world!", fg='blue')
    

main.add_command(yo, name='hi')

if __name__ == '__main__':
    main()
