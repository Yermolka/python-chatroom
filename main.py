import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-u', '--username', required=True, type=str)
@click.option('-p', '--password', required=True, type=str)
def run_client(username: str, password: str):
    import client
    client.run(username, password)

@cli.command()
def run_server():
    import server
    server.run()

if __name__ == '__main__':
    cli()