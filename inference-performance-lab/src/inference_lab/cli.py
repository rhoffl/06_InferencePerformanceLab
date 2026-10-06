import asyncio
from pathlib import Path
import typer
from .runner import run_experiment

app = typer.Typer(help="Reproducible inference performance laboratory")

@app.command()
def run(config: str, output_dir: str = "results"):
    """Run one versioned experiment matrix."""
    path = asyncio.run(run_experiment(config, output_dir)); typer.echo(path)

@app.command()
def list_results(output_dir: str = "results"):
    for path in sorted(Path(output_dir).glob("*.jsonl")): typer.echo(path)

