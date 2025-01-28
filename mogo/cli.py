# mogo/cli.py
import typer
from pathlib import Path
import os

app = typer.Typer()

@app.command()
def hello():
    """
    A simple hello world command to test the CLI.
    """
    typer.echo("Hello from Mogo!")

@app.command()
def list():
    """
    List all dependencies from the go.mod file.
    """
    # Path to go.mod file
    go_mod_file = Path(__file__).parent / "go.mod"
    
    if not go_mod_file.exists():
        typer.echo("Error: go.mod file not found in the current directory!")
        return
    
    # Read the go.mod file
    with go_mod_file.open("r") as file:
        lines = file.readlines()
    
    # Extract dependencies from the 'require' block
    in_require_block = False
    dependencies = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("require ("):
            in_require_block = True
            continue
        elif line == ")":
            in_require_block = False
            continue
        
        if in_require_block:
            dependencies.append(line)
        elif line.startswith("require"):  # Single-line require
            dependencies.append(line.replace("require", "").strip())
    
    # Print dependencies
    if dependencies:
        typer.echo("Dependencies found in go.mod:")
        for dep in dependencies:
            typer.echo(f"  {dep}")
    else:
        typer.echo("No dependencies found in go.mod.")

if __name__ == "__main__":
    app()
