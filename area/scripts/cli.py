import click
import cligj
import json

from supermercado import super_utils

from area import addArea

@click.command(short_help="Say hi")
@click.pass_context
@cligj.features_in_arg
@cligj.sequence_opt
def area(ctx, features, sequence):
    features = [f for f in super_utils.filter_polygons(features)]

    for f in features:
        click.echo(json.dumps({
            "type": "Feature",
            "properties": addArea(f),
            "geometry": f['geometry']
        }))
