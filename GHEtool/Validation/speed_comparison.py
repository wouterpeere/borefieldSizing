"""
This document compares the speed of the L2 sizing method of (Peere et al., 2021) with and without the precalculated gfunction data.
This is done for two fields with different sizes. It shows that, specifically for the larger fields, the precalculated data is way faster.
"""

import time

import pygfunction as gt

from GHEtool import Borefield, GroundConstantTemperature, MonthlyGeothermalLoadAbsolute


def test_64_boreholes():
    data = GroundConstantTemperature(3, 10)
    borefield_64 = gt.boreholes.rectangle_field(8, 8, 6, 6, 110, 1, 0.075)

    # monthly loading values
    peak_cooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]  # Peak cooling in kW
    peak_heating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10 ** 3  # kWh
    annual_cooling_load = 160 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144]
    monthly_load_cooling_percentage = [0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025]

    # resulting load per month
    monthly_load_heating = list(map(lambda x: x * annual_heating_load, monthly_load_heating_percentage))  # kWh
    monthly_load_cooling = list(map(lambda x: x * annual_cooling_load, monthly_load_cooling_percentage))  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_64)
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    # precalculate
    borefield.create_custom_dataset()

    # size borefield
    t1 = time.time()
    depth_precalculated = borefield.size()
    t1_end = time.time()

    # delete precalculated data
    borefield.custom_gfunction.delete_custom_gfunction()

    ### size without the precalculation
    t2 = time.time()
    depth_calculated = borefield.size()
    t2_end = time.time()

    print("With precalculated data, the sizing took", round(t1_end - t1, 3), "s for 64 boreholes.")
    print("Without the precalculated data, the sizing took", round(t2_end - t2, 3), "s for 64 boreholes.")
    print("The difference in accuracy between the two results is",
          round((depth_calculated - depth_precalculated) / depth_calculated * 100, 3), "%.")


def test_10_boreholes():
    data = GroundConstantTemperature(3, 10)
    borefield_10 = gt.boreholes.rectangle_field(2, 5, 6, 6, 110, 1, 0.075)

    # monthly loading values
    peak_cooling = [0., 0, 3., 9., 13., 20., 43., 30., 16., 7., 0., 0.]  # Peak cooling in kW
    peak_heating = [16., 14, 10., 5., 0., 0., 0., 0., 4, 8., 19., 13.]  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 16 * 10 ** 3  # kWh
    annual_cooling_load = 24 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_heating_load_percentage = [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144]
    monthly_load_cooling_percentage = [0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025]

    # resulting load per month
    monthly_load_heating = list(map(lambda x: x * annual_heating_load, monthly_heating_load_percentage))  # kWh
    monthly_load_cooling = list(map(lambda x: x * annual_cooling_load, monthly_load_cooling_percentage))  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_10)
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    # precalculate
    borefield.create_custom_dataset()

    # size borefield
    t1 = time.time()
    depth_precalculated = borefield.size()
    t1_end = time.time()

    # delete precalculated data
    borefield.custom_gfunction.delete_custom_gfunction()

    ### size without the precalculation
    t2 = time.time()
    depth_calculated = borefield.size()
    t2_end = time.time()

    print("With precalculated data, the sizing took", round(t1_end - t1, 3), "s for 10 boreholes.")
    print("Without the precalculated data, the sizing took", round(t2_end - t2, 3), "s for 10 boreholes.")
    print("The difference in accuracy between the two results is",
          round((depth_calculated-depth_precalculated) / depth_calculated * 100, 3), "%.\n")


if __name__ == "__main__":  # pragma: no cover

    test_10_boreholes()
    test_64_boreholes()
