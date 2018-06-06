
import os
import json

from click.testing import CliRunner
from fio_area.scripts.cli import area


def make_feature_collection(data):
    """Return a feature collection."""
    return {
        "type": "FeatureCollection",
        "features": data
    }


def test_cli_default():
    """Shoult return a geojson with area property."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures/sample.geojson')
    expected = os.path.join(os.path.dirname(__file__), 'expected/esri54009.json')
    with open(expected, 'r') as f:
        exp = json.loads(f.read())

    runner = CliRunner()
    result = runner.invoke(area, [path])
    res = make_feature_collection(list(map(json.loads, result.output.splitlines())))
    assert res == exp
    assert result.exit_code == 0


def test_cli_summary():
    """Shoult return a geojson with area property."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures/sample.geojson')
    expected = {
        "min": 294402748285.0502,
        "max": 850337428101.8224,
        "mean": 603326626751.0883,
        "sum": 3619959760506.5293,
        "std": 197308285092.32553
    }

    runner = CliRunner()
    result = runner.invoke(area, [path, '--summary'])
    assert json.loads(result.output) == expected
    assert result.exit_code == 0


def test_cli_ESRI():
    """Shoult work as espected when CRS code is in capital letters."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures/sample.geojson')
    expected = os.path.join(os.path.dirname(__file__), 'expected/esri54009.json')
    with open(expected, 'r') as f:
        exp = json.loads(f.read())

    runner = CliRunner()
    result = runner.invoke(area, [path, '--calc-crs', 'ESRI:54009'])
    res = make_feature_collection(list(map(json.loads, result.output.splitlines())))
    assert res == exp
    assert result.exit_code == 0


def test_cli_epsg3857():
    """Shoult return a geojson with area property."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures/sample.geojson')
    expected = os.path.join(os.path.dirname(__file__), 'expected/epsg3857.json')
    with open(expected, 'r') as f:
        exp = json.loads(f.read())

    runner = CliRunner()
    result = runner.invoke(area, [path, '--calc-crs', 'epsg:3857'])
    res = make_feature_collection(list(map(json.loads, result.output.splitlines())))
    assert res == exp
    assert result.exit_code == 0
