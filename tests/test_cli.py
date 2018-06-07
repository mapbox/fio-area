
import os
import json

from pytest import approx

from click.testing import CliRunner
from fio_area.scripts.cli import area


def make_feature_collection(data):
    """Return a feature collection."""
    return {"type": "FeatureCollection", "features": data}


def test_cli_default():
    """Shoult return a geojson with area property."""
    path = os.path.join(os.path.dirname(__file__), "fixtures/sample.geojson")
    expected = os.path.join(os.path.dirname(__file__), "expected/esri54009.json")
    with open(expected, "r") as f:
        exp = json.loads(f.read())

    runner = CliRunner()
    result = runner.invoke(area, [path])
    assert result.exit_code == 0

    for e_feat, res_feat in zip(
        exp["features"], map(json.loads, result.output.splitlines())
    ):
        assert e_feat["properties"] == approx(res_feat["properties"])
        assert e_feat["geometry"] == res_feat["geometry"]


def test_cli_summary():
    """Shoult return a geojson with area property."""
    path = os.path.join(os.path.dirname(__file__), "fixtures/sample.geojson")
    expected = {
        "min": 294482961341.2758,
        "max": 850713020250.7839,
        "mean": 603329112176.4628,
        "sum": 3619974673058.7764,
        "std": 197484273024.1649,
    }

    runner = CliRunner()
    result = runner.invoke(area, [path, "--summary"])
    assert approx(json.loads(result.output)) == expected
    assert result.exit_code == 0


def test_cli_ESRI():
    """Shoult work as espected when CRS code is in capital letters."""
    path = os.path.join(os.path.dirname(__file__), "fixtures/sample.geojson")
    expected = os.path.join(os.path.dirname(__file__), "expected/esri54009.json")
    with open(expected, "r") as f:
        exp = json.loads(f.read())

    runner = CliRunner()
    result = runner.invoke(area, [path, "--calc-crs", "ESRI:54009"])
    assert result.exit_code == 0

    for e_feat, res_feat in zip(
        exp["features"], map(json.loads, result.output.splitlines())
    ):
        assert e_feat["properties"] == approx(res_feat["properties"])
        assert e_feat["geometry"] == res_feat["geometry"]


def test_cli_epsg3857():
    """Shoult return a geojson with area property."""
    path = os.path.join(os.path.dirname(__file__), "fixtures/sample.geojson")
    expected = os.path.join(os.path.dirname(__file__), "expected/epsg3857.json")
    with open(expected, "r") as f:
        exp = json.loads(f.read())

    runner = CliRunner()
    result = runner.invoke(area, [path, "--calc-crs", "epsg:3857"])
    assert result.exit_code == 0

    for e_feat, res_feat in zip(
        exp["features"], map(json.loads, result.output.splitlines())
    ):
        assert e_feat["properties"] == approx(res_feat["properties"])
        assert e_feat["geometry"] == res_feat["geometry"]
