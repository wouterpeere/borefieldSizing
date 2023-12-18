# test if model can be imported
import copy
from math import isclose
import matplotlib.pyplot as plt

import numpy as np
import pygfunction as gt
import pytest

from GHEtool import *
from GHEtool.VariableClasses.BaseClass import UnsolvableDueToTemperatureGradient

data = GroundConstantTemperature(3, 10)
data_ground_flux = GroundFluxTemperature(3, 10)

fluidData = FluidData(0.2, 0.568, 998, 4180, 1e-3)
pipeData = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05)

borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 4, 0.075)


def load_case(number):
    """This function returns the values for one of the four cases."""
    if number == 1:
        # case 1
        # limited in the first year by cooling
        monthly_load_heating_percentage = np.array(
            [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 300 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 150 * 10 ** 3  # kWh
        peak_cooling = np.array([0., 0., 22., 44., 83., 117., 134., 150., 100., 23., 0., 0.])
        peak_heating = np.zeros(12)

    elif number == 2:
        # case 2
        # limited in the last year by cooling
        monthly_load_heating_percentage = np.array(
            [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, .117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 160 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 240 * 10 ** 3  # kWh
        peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
        peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])

    else:
        # case 4
        # limited in the last year by heating
        monthly_load_heating_percentage = np.array(
            [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 300 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 150 * 10 ** 3  # kWh
        peak_cooling = np.array([0., 0., 22., 44., 83., 117., 134., 150., 100., 23., 0., 0.])
        peak_heating = np.array([300., 268., 191., 103., 75., 0., 0., 38., 76., 160., 224., 255.])

    return monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling


def test_different_heating_cooling_peaks():
    # Monthly loading values
    peakCooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]  # Peak cooling in kW
    peakHeating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]  # Peak heating in kW

    # annual heating and cooling load
    annualHeatingLoad = 300 * 10 ** 3  # kWh
    annualCoolingLoad = 160 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthlyLoadHeatingPercentage = [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144]
    monthlyLoadCoolingPercentage = [0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025]

    # resulting load per month
    monthlyLoadHeating = list(map(lambda x: x * annualHeatingLoad, monthlyLoadHeatingPercentage))  # kWh
    monthlyLoadCooling = list(map(lambda x: x * annualCoolingLoad, monthlyLoadCoolingPercentage))  # kWh

    load = MonthlyGeothermalLoadAbsolute(monthlyLoadHeating, monthlyLoadCooling, peakHeating, peakCooling)
    borefield = Borefield(load=load)

    borefield.set_ground_parameters(data)
    borefield.set_borefield(copy.copy(borefield_gt))
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature
    borefield.set_length_peak_cooling(8)
    assert borefield.load.peak_cooling_duration == 8 * 3600
    assert borefield.load.peak_heating_duration == 6 * 3600
    assert np.isclose(borefield.size(), 94.05270927679376)
    assert borefield.load.peak_cooling_duration == 8 * 3600
    assert borefield.load.peak_heating_duration == 6 * 3600


def test_stuck_in_loop():
    borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(4)))

    borefield.set_ground_parameters(data)
    borefield.set_borefield(copy.copy(borefield_gt))
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature
    borefield.calculation_setup(max_nb_of_iterations=500)

    borefield.size()
    borefield.set_length_peak_cooling(8)
    borefield.set_length_peak_heating(8)
    assert borefield.load.peak_cooling_duration == 8 * 3600
    assert borefield.load.peak_heating_duration == 8 * 3600
    borefield.size()
    assert np.isclose(borefield.size(), 100.91784885721547)
    borefield.set_length_peak_heating(7)
    assert np.isclose(borefield.size(), 100.15133835697398)


def test_different_results_with_other_peak_lengths():
    borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(4)))

    borefield.set_ground_parameters(data)
    borefield.set_borefield(copy.copy(borefield_gt))

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    borefield.set_length_peak(2)
    init_length_L2 = borefield.size_L2()
    borefield.set_length_peak_heating(8)
    borefield.set_length_peak_cooling(8)
    new_length_L2 = borefield.size_L2()

    assert new_length_L2 > init_length_L2


def test_reset_temp_profiles_when_loaded(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(1)))

    borefield.set_ground_parameters(data)
    borefield.set_borefield(copy.copy(borefield_gt))

    borefield.calculate_temperatures()
    Tmax = borefield.results.peak_cooling.copy()
    Tmin = borefield.results.peak_heating.copy()

    monthlyLoadCooling, monthlyLoadHeating, peakCooling, peakHeating = load_case(2)
    borefield.set_baseload_cooling(monthlyLoadCooling)
    borefield.set_baseload_heating(monthlyLoadHeating)
    borefield.set_peak_heating(peakHeating)
    borefield.set_peak_cooling(peakCooling)

    borefield.print_temperature_profile()

    assert not np.array_equal(Tmax, borefield.results.peak_heating)
    assert not np.array_equal(Tmin, borefield.results.peak_cooling)


def test_no_possible_solution():
    borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(4)))

    borefield.set_ground_parameters(data_ground_flux)
    borefield.set_borefield(copy.copy(borefield_gt))

    # limited by cooling
    borefield.set_max_avg_fluid_temperature(14)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(3)  # minimum temperature
    borefield.size()

    # limited by heating, but no problem for cooling
    borefield.set_max_avg_fluid_temperature(15)
    borefield.set_min_avg_fluid_temperature(2)
    borefield.set_baseload_heating(borefield.load.baseload_heating * 5)
    borefield.size()

    # limited by heating, but problem for cooling --> no solution
    borefield.set_max_avg_fluid_temperature(14)
    borefield.set_min_avg_fluid_temperature(2)
    borefield.set_baseload_heating(borefield.load.baseload_heating * 5)
    try:
        borefield.size(L3_sizing=True)
        assert False  # pragma: no cover
    except UnsolvableDueToTemperatureGradient:
        assert True


def test_problem_with_gfunction_calc_obj():
    # GroundData for an initial field of 11 x 11
    data = GroundConstantTemperature(3, 10)
    borefield_gt = gt.boreholes.rectangle_field(11, 11, 6, 6, 110, 1, 0.075)

    # Monthly loading values
    peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 150 * 10 ** 3  # kWh
    annual_cooling_load = 400 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array(
        [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # create the borefield object
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)
    borefield = Borefield(load=load)

    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_gt)
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    # size borefield
    assert np.isclose(borefield.size(), 190.2116676694166)

    # borefield of 6x20
    data = GroundConstantTemperature(3, 10)
    borefield_gt = gt.boreholes.rectangle_field(6, 20, 6, 6, 110, 1, 0.075)

    # set ground parameters to borefield
    borefield.set_borefield(borefield_gt)
    borefield.set_ground_parameters(data)

    # set Rb
    borefield.Rb = 0.2

    # size borefield
    assert np.isclose(borefield.size(), 186.50968468475781)
