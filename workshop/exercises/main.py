"""Entry point — `python -m exercises.main`."""

import typer

from exercises import client
from exercises.server import serve

app = typer.Typer(help="gRPC Chat Workshop CLI")

app.add_typer(client.app, name="client")


@app.command()
def server(
    port: int = typer.Option(50051, "--port", "-p", help="gRPC port"),
    metrics_port: int = typer.Option(
        8000, "--metrics-port", help="Prometheus metrics port"
    ),
) -> None:
    """Start the gRPC chat server."""
    serve(port=port, metrics_port=metrics_port)


if __name__ == "__main__":
    app()
