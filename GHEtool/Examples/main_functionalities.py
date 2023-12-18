"""
This file contains all the main functionalities of GHEtool being:
    * sizing of the borefield
    * sizing of the borefield for a specific quadrant
    * plotting the temperature evolution
    * plotting the temperature evolution for a specific depth
    * printing the array of the temperature
"""

import numpy as np

# import all the relevant functions
from GHEtool import Borefield, FluidData, DoubleUTube, GroundConstantTemperature, MonthlyGeothermalLoadAbsolute


def main_functionalities():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,             # conductivity of the soil (W/mK)
                                     10,            # Ground temperature at infinity (degrees C)
                                     2.4 * 10**6)   # ground volumetric heat capacity (J/m3K)

    # monthly loading values
    peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10 ** 3  # kWh
    annual_cooling_load = 160 * 10 ** 3  # kWh

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

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    borefield.create_rectangular_borefield(10, 12, 6, 6, 100, 4, 0.075)

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)   # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)    # minimum temperature

    # size borefield
    depth = borefield.size()
    print("The borehole depth is: ", depth, "m")

    # print imbalance
    print("The borefield imbalance is: ", borefield._borefield_load.imbalance, "kWh/y. (A negative imbalance means the the field is heat extraction dominated so it cools down year after year.)") # print imbalance

    # plot temperature profile for the calculated depth
    borefield.print_temperature_profile(legend=True)

    # plot temperature profile for a fixed depth
    borefield.print_temperature_profile_fixed_depth(depth=75, legend=False)

    # print gives the array of monthly temperatures for peak cooling without showing the plot
    borefield.calculate_temperatures(depth=90)
    print("Result array for cooling peaks")
    print(borefield.results.peak_cooling)
    print("---------------------------------------------")

    # size the borefield for quadrant 3
    # for more information about borefield quadrants, see (Peere et al., 2021)
    depth = borefield.size(quadrant_sizing=3)
    print("The borehole depth is: ", str(round(depth, 2)), "m for a sizing in quadrant 3")
    # plot temperature profile for the calculated depth
    borefield.print_temperature_profile(legend=True)

    # size with a dynamic Rb* value
    # note that the original Rb* value will be overwritten!

    # this requires pipe and fluid data
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    pipe_data = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)

    # disable the use of constant_Rb with the setup, in order to plot the profile correctly
    # when it is given as an argument to the size function, it will size correctly, but the plot will be with
    # constant Rb* since it has not been changed in the setup function
    borefield.calculation_setup(use_constant_Rb=False)
    depth = borefield.size()
    print("The borehole depth is: ", str(round(depth, 2)), "m for a sizing with dynamic Rb*.")
    borefield.print_temperature_profile(legend=True)


if __name__ == "__main__":  # pragma: no cover
    main_functionalities()
