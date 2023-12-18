import matplotlib.pyplot as plt
import pytest


def test_validation_cases(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    from GHEtool.Validation.cases import check_cases, check_custom_datafile
    check_cases()
    check_custom_datafile()


@pytest.mark.slow
def test_sizing_method_comparison(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    from GHEtool.Validation.sizing_method_comparison import sizing_method_comparison
    sizing_method_comparison()


@pytest.mark.slow
def test_speed_comparison():
    from GHEtool.Validation.speed_comparison import test_10_boreholes, test_64_boreholes
    test_10_boreholes()
    test_64_boreholes()


@pytest.mark.slow
def test_compare_L2_L3_L4(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    from GHEtool.Validation.sizing_method_comparison_L2_L3_L4 import compare
    compare()


@pytest.mark.slow
def test_effective_borehole_thermal_resistance(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    from GHEtool.Validation.validation_effective_borehole_thermal_resistance import validate
    validate()


@pytest.mark.slow
def test_validate_deep_sizing(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    from GHEtool.Validation.validate_deep_sizing import validate
    validate()
