# -*- coding: utf-8 -*-
# 
# Copyright (c) 2023~2999 - Cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

from pathlib import Path
from typing import Annotated, Optional
import sys
import json

import typer

from .core import json_to_efurowitem, write_efu_to

app = typer.Typer()

@app.command()
def main(
        prefix: str = None,
        source: Annotated[Optional[Path], typer.Option(exists=True, readable=True)] = None,
        output: Annotated[Optional[Path], typer.Option(writable=True)] = None,
    ):

    if source is None:
        if sys.stdin.isatty():
            typer.echo('No source specified.', err=True)
            raise typer.Exit(1)
        json_content = json.loads(sys.stdin.read())
    else:
        json_content = json.loads(source.read_text())

    if prefix is None:
        if source is None or output is None:
            typer.echo('No prefix specified.', err=True)
            raise typer.Exit(2)
        prefix = (source or output).stem
    assert prefix

    items = [json_to_efurowitem(x, prefix) for x in json_content['Contents']]

    if output is None:
        write_efu_to(sys.stdout, items)
    else:
        with output.open('w', newline='') as fp_out:
            write_efu_to(fp_out, items)
