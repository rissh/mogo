# mogo/cli.py
import typer

app = typer.Typer()

@app.command()
def hello():
    """
    A simple hello world command to test the CLI.
    """
    typer.echo("Hello from Mogo!")

if __name__ == "__main__":
    app()
