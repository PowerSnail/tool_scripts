#!/usr/bin/env python3
import typer
import pathlib


def main(name: str, ext: str):
    if not ext.startswith("."):
        ext = "." + ext
    typer.echo(pathlib.Path(name).with_suffix(ext))


if __name__ == "__main__":
    typer.run(main)

