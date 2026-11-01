import pytest
matplotlib = pytest.importorskip("matplotlib")
from pathlib import Path
from scripts.charts import football_field, dcf_sensitivity_heatmap
from scripts.valuation import dcf_sensitivity


def test_football_field_chart_is_created(tmp_path):
    path=Path(football_field({"DCF":{"Bear":30,"Base":42,"Bull":55}},42.5,str(tmp_path/"football.png")))
    assert path.is_file() and path.stat().st_size > 1000


def test_sensitivity_heatmap_is_created(tmp_path):
    data=dcf_sensitivity([100,110,120],[.08,.10],[.02,.03],0,10)
    path=Path(dcf_sensitivity_heatmap(data,str(tmp_path/"heatmap.png")))
    assert path.is_file() and path.stat().st_size > 1000
