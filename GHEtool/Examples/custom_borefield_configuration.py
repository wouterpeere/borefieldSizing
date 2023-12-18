"""
This file gives an example on how to work with a custom borefield within GHEtool using pygfunction.

When working on a custom borefield configuration, one needs to import this configuration into the GHEtool.
Based on the pygfunction, one creates his custom borefield and gives it as an argument to the class initiater Borefield of GHEtool.

You also need a custom g-function file for interpolation. This can also be given as an argument to the class initiater as _custom_gfunction.
This custom variable, must contain gfunctions for all time steps in Borefield.DEFAULT_TIME_ARRAY, and should be structured as follows:
{"Time":Borefield.DEFAULT_TIME_ARRAY,"Data":[[Depth1,[Gfunc1,Gfunc2 ...]],[Depth2,[Gfunc1, Gfunc2 ...]]]}.

However, one can use the function 'create_custom_dataset' when a custom borefield is given. This will make the required dataset for the optimisation.
 """

import numpy as np
import pygfunction as gt

# import all the relevant functions
from GHEtool import *


def custom_borefield_configuration():
    # set the relevant ground data for the calculations
    data = GroundConstantTemperature(3, 10)

    # Monthly loading values
    peak_cooling = np.array([0., 0, 3.4, 6.9, 13., 18., 21., 50., 16., 3.7, 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([60., 42., 10., 5., 0., 0., 0., 0., 4.4, 8.5, 19., 36.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 30 * 10 ** 3  # kWh
    annual_cooling_load = 16 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    borefield.set_ground_parameters(data)
    borefield.Rb = 0.2

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    # create custom borefield based on pygfunction
    custom_field = gt.boreholes.L_shaped_field(N_1=4, N_2=5, B_1=5., B_2=5., H=100., D=4, r_b=0.05)

    # set the custom borefield (so the number of boreholes is correct)
    borefield.set_borefield(custom_field)
    borefield.create_custom_dataset()

    # size borefield
    depth = borefield.size()
    print("The borehole depth is: ", depth, "m")

    # print imbalance
    print("The borefield imbalance is: ", borefield.load.imbalance, "kWh/y. (A negative imbalance means the the field is heat extraction dominated so it cools down year after year.)") # print imbalance

    # plot temperature profile for the calculated depth
    borefield.print_temperature_profile(legend=True)

    # plot temperature profile for a fixed depth
    borefield.print_temperature_profile_fixed_depth(depth=75, legend=False)

    # print gives the array of monthly temperatures for peak cooling without showing the plot
    borefield.calculate_temperatures(depth=90)
    print("Result array for cooling peaks")
    print(borefield.results.peak_cooling)


if __name__ == "__main__":  # pragma: no cover
    custom_borefield_configuration()
