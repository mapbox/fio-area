"""fio-area cli."""

import json

import click
import cligj

import numpy as np

from fio_area.utils import _area_adder, _poly_filter


@click.command()
@click.option("--summary", "-s", is_flag=True, help="Output summary statistics only")
@click.option(
    "--calc-crs",
    type=str,
    default="esri:54009",
    help="Projection to calculate area in [DEFAULT=esri:54009]",
)
@click.pass_context
@cligj.features_in_arg
@cligj.sequence_opt
def area(ctx, features, summary, calc_crs, sequence):
    features = _poly_filter(features)

    calc_crs = calc_crs.lower()
    features, sums = zip(*[[f, a] for f, a in _area_adder(features, calc_crs)])

    if summary:
        stats = [np.min, np.max, np.mean, np.sum, np.std]
        snames = ["min", "max", "mean", "sum", "std"]
        sums = np.array(sums)
        click.echo(json.dumps({s: f(sums) for s, f in zip(snames, stats)}))
    else:
        for f in features:
            click.echo(json.dumps(f))
