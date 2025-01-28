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
def list(direct: bool = typer.Option(False, "--direct", help="List only direct dependencies"),
         indirect: bool = typer.Option(False, "--indirect", help="List only indirect dependencies")):
    """
    List dependencies in the go.mod file. Supports filtering by direct and indirect dependencies.
    """
    go_mod_path = Path.cwd() / "go.mod"
    
    if not go_mod_path.exists():
        typer.echo("Error: go.mod file not found in the current directory!")
        raise typer.Exit(code=1)

    with go_mod_path.open() as file:
        lines = file.readlines()
    
    dependencies = []
    direct_dependencies = []
    indirect_dependencies = []

    for line in lines:
        line = line.strip()

        # Skip non-dependency lines
        if line.startswith("module ") or line.startswith("go "):
            continue
        if line.startswith("require "):
            continue
        if "require (" in line or ")" in line:
            continue
        
        # Classify dependencies
        if line:
            if "// indirect" in line:
                indirect_dependencies.append(line)
            else:
                direct_dependencies.append(line)

    # Default behavior: show all dependencies
    if not direct and not indirect:
        dependencies = direct_dependencies + indirect_dependencies
        typer.echo("Dependencies found in go.mod:")
    elif direct:
        dependencies = direct_dependencies
        typer.echo("Direct dependencies found in go.mod:")
    elif indirect:
        dependencies = indirect_dependencies
        typer.echo("Indirect dependencies found in go.mod:")

    for dep in dependencies:
        typer.echo(f"  {dep}")



if __name__ == "__main__":
    app()
