import pytest

import numpy as np

from GHEtool import FOLDER
from GHEtool.VariableClasses import HourlyGeothermalLoad, HourlyGeothermalLoadMultiYear, MonthlyGeothermalLoadAbsolute


def test_load_hourly_data():
    load = HourlyGeothermalLoad()
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    load1 = HourlyGeothermalLoad()
    load1.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"), col_heating=1, col_cooling=0)
    assert np.array_equal(load.hourly_cooling_load, load1.hourly_heating_load)
    assert np.array_equal(load.hourly_heating_load, load1.hourly_cooling_load)
    load2 = HourlyGeothermalLoad()
    load2.load_hourly_profile(FOLDER.joinpath("test/methods/hourly_data/hourly_profile_without_header.csv"), header=False)
    assert np.array_equal(load.hourly_cooling_load, load2.hourly_cooling_load)
    assert np.array_equal(load.hourly_heating_load, load2.hourly_heating_load)


def test_checks():
    load = HourlyGeothermalLoad()
    assert not load._check_input(2)
    assert not load._check_input(np.ones(8759))
    assert not load._check_input(-1*np.ones(8760))
    assert load._check_input([1]*8760)
    assert load._check_input(np.ones(8760))


def test_imbalance():
    load = HourlyGeothermalLoad(np.ones(8760)*10, np.ones(8760))
    assert load.imbalance == -78840
    load = HourlyGeothermalLoad(np.ones(8760), np.ones(8760)*10)
    assert load.imbalance == 78840


def test_resample_to_monthly():
    load = HourlyGeothermalLoad()
    peak, baseload = load.resample_to_monthly(np.tile(np.linspace(0, 729, 730), 12))
    assert np.array_equal(peak, np.ones(12)*729)
    assert np.array_equal(baseload, np.ones(12)*266085)
    load.all_months_equal = False
    peak, baseload = load.resample_to_monthly(np.tile(np.linspace(0, 729, 730), 12))
    assert np.array_equal(peak, np.array([729., 685., 729., 729., 729., 729., 729., 729., 729., 729., 729., 729.]))
    assert np.array_equal(baseload, np.array([266176., 234864., 275780., 259140., 275836., 259100.,
                                              275892., 276088., 258920., 276144., 258880., 276200.]))


def test_baseload_heating():
    load = HourlyGeothermalLoad()
    assert np.array_equal(load.baseload_heating, np.zeros(12))
    load.hourly_heating_load = np.repeat(np.linspace(0, 11, 12), 730)
    assert np.array_equal(load.baseload_heating, np.linspace(0, 11, 12)*730)
    assert np.array_equal(load.baseload_heating / 730, load.baseload_heating_power)
    assert np.array_equal(load.baseload_heating_power, load.peak_heating)


def test_baseload_cooling():
    load = HourlyGeothermalLoad()
    assert np.array_equal(load.baseload_cooling, np.zeros(12))
    load.hourly_cooling_load = np.repeat(np.linspace(0, 11, 12), 730)
    assert np.array_equal(load.baseload_cooling, np.linspace(0, 11, 12) * 730)
    assert np.array_equal(load.baseload_cooling / 730, load.baseload_cooling_power)
    assert np.array_equal(load.baseload_cooling_power, load.peak_cooling)


def test_peak_heating():
    load = HourlyGeothermalLoad()
    assert np.array_equal(load.peak_heating, np.zeros(12))
    load.hourly_heating_load = np.repeat(np.linspace(0, 11, 12), 730)
    assert np.array_equal(load.peak_heating, np.linspace(0, 11, 12))
    load.hourly_heating_load = np.repeat(np.linspace(1, 12, 12), 730)
    assert np.array_equal(load.peak_heating, np.linspace(1, 12, 12))


def test_peak_cooling():
    load = HourlyGeothermalLoad()
    assert np.array_equal(load.peak_cooling, np.zeros(12))
    load.hourly_cooling_load = np.repeat(np.linspace(0, 11, 12), 730)
    assert np.array_equal(load.peak_cooling, np.linspace(0, 11, 12))
    load.hourly_cooling_load = np.repeat(np.linspace(1, 12, 12), 730)
    assert np.array_equal(load.peak_cooling, np.linspace(1, 12, 12))


def test_load_simulation_period():
    load = HourlyGeothermalLoad()
    load.hourly_heating_load = np.linspace(0, 8759, 8760)
    assert np.array_equal(load.hourly_heating_load_simulation_period,
                          np.tile(np.linspace(0, 8759, 8760), load.simulation_period))
    load.hourly_cooling_load = np.linspace(50, 8759, 8760)
    assert np.array_equal(load.hourly_cooling_load_simulation_period,
                          np.tile(np.linspace(50, 8759, 8760), load.simulation_period))
    assert np.array_equal(load.hourly_load_simulation_period,
                          np.tile(-np.linspace(0, 8759, 8760)+np.linspace(50, 8759, 8760), load.simulation_period))


def test_set_hourly_values():
    load = HourlyGeothermalLoad()
    try:
        load.set_hourly_heating(np.ones(10))
        assert False   # pragma: no cover
    except ValueError:
        assert True
    try:
        load.set_hourly_cooling(np.ones(10))
        assert False   # pragma: no cover
    except ValueError:
        assert True

### continue for multi year
def test_checks_multiyear():
    load = HourlyGeothermalLoadMultiYear()
    assert not load._check_input(2)
    assert not load._check_input(np.ones(8759))
    assert not load._check_input(-1*np.ones(8760))
    assert load._check_input([1]*8760)
    assert load._check_input(np.ones(8760))
    assert load._check_input(np.ones(8760 * 3))
    assert not load._check_input(np.ones(9000))


def test_set_hourly_load_multi_year():
    load = HourlyGeothermalLoadMultiYear()
    load.hourly_heating_load = np.linspace(0, 8759*2+1, 8760*2)
    assert len(load._hourly_heating_load) == 8760*2
    assert len(load.hourly_heating_load) == 8760
    assert load.simulation_period == 2
    assert np.array_equal(load.hourly_heating_load, np.linspace(0 + 8760/2, 8759 + 8760/2, 8760))
    assert np.array_equal(load.hourly_heating_load_simulation_period, load._hourly_heating_load)
    load.hourly_cooling_load = np.linspace(0, 8759 * 2 + 1, 8760 * 2)
    assert len(load._hourly_cooling_load) == 8760 * 2
    assert len(load.hourly_cooling_load) == 8760
    assert load.simulation_period == 2
    assert np.array_equal(load.hourly_cooling_load, np.linspace(0 + 8760 / 2, 8759 + 8760 / 2, 8760))
    assert np.array_equal(load.hourly_cooling_load_simulation_period, load._hourly_cooling_load)
    load._hourly_cooling_load = load._hourly_cooling_load - 20
    assert np.array_equal(load.hourly_load_simulation_period, load._hourly_cooling_load-load._hourly_heating_load)


def test_imbalance_multi_year():
    load = HourlyGeothermalLoad(np.ones(8760)*10, np.ones(8760))
    assert load.imbalance == -78840
    load = HourlyGeothermalLoad(np.ones(8760), np.ones(8760)*10)
    assert load.imbalance == 78840


def test_set_hourly_values_multi_year():
    load = HourlyGeothermalLoadMultiYear()
    try:
        load.set_hourly_heating(np.ones(10))
        assert False   # pragma: no cover
    except ValueError:
        assert True
    try:
        load.set_hourly_cooling(np.ones(10))
        assert False   # pragma: no cover
    except ValueError:
        assert True


def test_dhw():
    load = HourlyGeothermalLoad()
    assert load.dhw == 0.
    load.add_dhw(1000)
    assert load.dhw == 1000.
    load.dhw = 200
    assert load.dhw == 200.
    try:
        load.add_dhw('test')
        assert False  # pragma: no cover
    except ValueError:
        assert True
    try:
        load.add_dhw(-10)
        assert False  # pragma: no cover
    except ValueError:
        assert True

    load.dhw = 8760*10
    assert np.array_equal(np.full(12, 10), load.peak_heating)
    assert np.array_equal(np.full(8760, 10), load.hourly_heating_load)
    assert load.max_peak_heating == 10
    assert np.array_equal(np.full(8760, 10), load.hourly_heating_load)
    assert np.array_equal(np.full(12, 8760*10/12), load.baseload_heating)
    assert load.imbalance == -8760*10


def test_eq():
    profile_1 = HourlyGeothermalLoad()
    profile_2 = MonthlyGeothermalLoadAbsolute()
    assert not profile_1 == profile_2
    assert profile_1 == profile_1

    profile_2 = HourlyGeothermalLoad()
    assert profile_1 == profile_2

    profile_1.simulation_period = 55
    assert profile_1 != profile_2

    profile_1.hourly_cooling_load = np.linspace(0, 10000, 8760)
    profile_2.simulation_period = 55
    assert profile_1 != profile_2

    profile_2.hourly_cooling_load = np.linspace(0, 10000, 8760)
    assert profile_1 == profile_2

    profile_1.hourly_heating_load = np.linspace(0, 8759, 8760)
    assert profile_1 != profile_2

    profile_2.hourly_heating_load = np.linspace(0, 8759, 8760)
    assert profile_1 == profile_2
