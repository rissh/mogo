# mogo/cli.py
import typer
from pathlib import Path
import os, re

app = typer.Typer()

@app.command()
def hello():
    """
    A simple hello world command to test the CLI.
    """
    typer.echo("Hello from Mogo!")

@app.command()
def list(
    direct: bool = typer.Option(False, "--direct", help="List only direct dependencies"),
    indirect: bool = typer.Option(False, "--indirect", help="List only indirect dependencies"),
    count: bool = typer.Option(False, "--count", help="Show the count of dependencies instead of listing them")
):
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

    # Determine which dependencies to process
    if not direct and not indirect:
        dependencies = direct_dependencies + indirect_dependencies
        dependency_type = "Dependencies"
    elif direct:
        dependencies = direct_dependencies
        dependency_type = "Direct dependencies"
    elif indirect:
        dependencies = indirect_dependencies
        dependency_type = "Indirect dependencies"

    # Display count or list of dependencies
    if count:
        typer.echo(f"{dependency_type} count: {len(dependencies)}")
    else:
        typer.echo(f"{dependency_type} found in go.mod:")
        for dep in dependencies:
            typer.echo(f"  {dep}")

@app.command()
def find(package: str):
    """
    Find and display details of a package or matching packages in the go.mod file.
    Allows partial matching of package names.
    """
    go_mod_path = Path.cwd() / "go.mod"
    
    if not go_mod_path.exists():
        typer.echo("Error: go.mod file not found in the current directory!")
        raise typer.Exit(code=1)

    with go_mod_path.open() as file:
        lines = file.readlines()

    # Initialize variables to store dependencies
    direct_dependencies = []
    indirect_dependencies = []

    # Read through the file and classify dependencies
    for line in lines:
        line = line.strip()

        # Skip non-dependency lines
        if line.startswith("module ") or line.startswith("go "):
            continue
        if line.startswith("require "):
            continue
        if "require (" in line or ")" in line:
            continue
        
        # Classify dependencies into direct and indirect
        if "// indirect" in line:
            indirect_dependencies.append(line)
        else:
            direct_dependencies.append(line)

    # Function to search for packages in both direct and indirect dependencies
    def find_packages(dependencies, package_name):
        matching_packages = []
        for dep in dependencies:
            if re.search(package_name, dep, re.IGNORECASE):  # Case-insensitive match
                matching_packages.append(dep)
        return matching_packages

    # Search in both direct and indirect dependencies
    direct_matches = find_packages(direct_dependencies, package)
    indirect_matches = find_packages(indirect_dependencies, package)

    # Combine all matching packages
    all_matches = direct_matches + indirect_matches

    if all_matches:
        typer.echo(f"Dependency found:")
        for match in all_matches:
            # Extract package name and version
            parts = match.split()
            package_name = parts[0]
            version = parts[1]
            # Determine the type (Direct or Indirect)
            if match in direct_matches:
                dep_type = "Direct"
            else:
                dep_type = "Indirect"
            # Print the details
            typer.echo(f"Package: {package_name}")
            typer.echo(f"Version: {version}")
            typer.echo(f"Type: {dep_type}")
    else:
        typer.echo(f"Dependency '{package}' not found in go.mod.")




if __name__ == "__main__":
    app()
