"""
This document is an example of how the borefield configuration can influence the total borehole length and hence the cost of the borefield.
"""

# import all the relevant functions
from GHEtool import GroundConstantTemperature, Borefield, MonthlyGeothermalLoadAbsolute
import numpy as np
import pygfunction as gt


def effect_borefield_configuration():
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
    monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage   # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage   # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_gt)
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)   # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)    # minimum temperature

    # size borefield
    depth = borefield.size()
    print("The borehole depth is:", depth, "m for a 11x11 field")
    print("The total length is:", int(depth * 11 * 11), "m")
    print("------------------------")


    # borefield of 6x20
    data = GroundConstantTemperature(3, 10)
    borefield_gt = gt.boreholes.rectangle_field(6, 20, 6, 6, 110, 1, 0.075)

    # set ground parameters to borefield
    borefield.set_borefield(borefield_gt)
    borefield.set_ground_parameters(data)

    # set Rb
    borefield.Rb = 0.2

    # size borefield
    depth6_20 = borefield.size()
    print("The borehole depth is:", depth6_20, "m for a 6x20 field")
    print("The total length is:", int(depth6_20 * 6 * 20), "m")
    print("The second field is hence", -int(depth6_20 * 6 * 20) + int(depth * 11 * 11), "m shorter")

    borefield.print_temperature_profile()


if __name__ == "__main__":   # pragma: no cover
    effect_borefield_configuration()
