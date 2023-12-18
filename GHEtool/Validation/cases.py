"""
This document contains checks to see whether or not adaptations to the code still comply with some specific cases.
It also shows the difference between the original L2 sizing methode (Peere et al., 2021) and a more general L3 one.

This document contains 4 different cases referring to the paper: Peere, W., Picard, D., Cupeiro Figueroa, I., Boydens, W., and Helsen, L. Validated combined first and last year borefield sizing methodology. In Proceedings of International Building Simulation Conference 2021 (2021). Brugge (Belgium), 1-3 September 2021.

"""

import numpy as np
import pygfunction as gt

from GHEtool import Borefield, GroundConstantTemperature, MonthlyGeothermalLoadAbsolute

# relevant borefield data for the calculations
data = GroundConstantTemperature(3.5,  # conductivity of the soil (W/mK)
                                 10)   # Ground temperature at infinity (degrees C)

borefield_gt = gt.boreholes.rectangle_field(10, 12, 6.5, 6.5, 100, 4, 0.075)


def load_case(number):
    """This function returns the values for one of the four cases."""

    if number == 1:
        # case 1
        # limited in the first year by cooling
        monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 300 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 150 * 10 ** 3  # kWh
        peak_cooling = np.array([0., 0., 22., 44., 83., 117., 134., 150., 100., 23., 0., 0.])
        peak_heating = np.zeros(12)

    elif number == 2:
        # case 2
        # limited in the last year by cooling
        monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, .117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 160 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 240 * 10 ** 3  # kWh
        peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
        peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])

    elif number == 3:
        # case 3
        # limited in the first year by heating
        monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, .117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 160 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 240 * 10 ** 3  # kWh
        peak_cooling = np.zeros(12)
        peak_heating = np.array([300.0, 266.25, 191.25, 103.125, 0.0, 0.0, 0.0, 0.0, 75.75, 159.375, 223.125, 255.0])

    else:
        # case 4
        # limited in the last year by heating
        monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
        monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
        monthly_load_heating = monthly_load_heating_percentage * 300 * 10 ** 3  # kWh
        monthly_load_cooling = monthly_load_cooling_percentage * 150 * 10 ** 3  # kWh
        peak_cooling = np.array([0., 0., 22., 44., 83., 117., 134., 150., 100., 23., 0., 0.])
        peak_heating = np.array([300., 268., 191., 103., 75., 0., 0., 38., 76., 160., 224., 255.])

    return monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling


def check_cases():

    """
    This function checks whether the borefield sizing gives the correct (i.e. validated) results for the 4 cases.
    If not, an assertion error is raised.
    NOTE: these values differ slightly from the values in the mentioned paper. This is due to the fact that GHEtool uses slightly different precalculated data.
    """

    correct_answers_L2 = (56.75, 117.23, 66.94, 91.32)
    correct_answers_L3 = (56.77, 118.74, 66.47, 91.24)

    for i in (1, 2, 3, 4):
        borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(i)))

        borefield.set_ground_parameters(data)
        borefield.set_borefield(borefield_gt)
        borefield.Rb = 0.2

        # set temperature boundaries
        borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
        borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

        borefield.size(100, L2_sizing=True)
        print(f'correct answer L2: {correct_answers_L2[i-1]}; calculated answer L2: {round(borefield.H,2)}; error: '
              f'{round(abs(1 - borefield.H / correct_answers_L2[i - 1]) * 100, 4)} %')
        assert np.isclose(borefield.H, correct_answers_L2[i-1], rtol=0.001)

        borefield.size(100, L3_sizing=True)
        print(f'correct answer L3: {correct_answers_L3[i - 1]}; calculated answer L3: {round(borefield.H, 2)}; error: '
              f'{round(abs(1 - borefield.H / correct_answers_L3[i - 1]) * 100, 4)} %')
        assert np.isclose(borefield.H, correct_answers_L3[i-1], rtol=0.001)


def check_custom_datafile():
    """
    This function checks whether the borefield sizing gives the correct (i.e. validated) results for the 4 cases given the custom datafile.
    If not, an assertion error is raised.
    """

    # create custom datafile

    correct_answers = (56.75, 117.23, 66.94, 91.32)

    custom_field = gt.boreholes.rectangle_field(N_1=12, N_2=10, B_1=6.5, B_2=6.5, H=110., D=4, r_b=0.075)

    for i in (1, 2, 3, 4):
        borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(i)))

        borefield.set_ground_parameters(data)
        borefield.set_borefield(custom_field)
        borefield.Rb = 0.2

        # set temperature boundaries
        borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
        borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

        borefield.size(100, L3_sizing=True)
        print(f'correct answer: {correct_answers[i-1]}; calculated '
              f'answer: {round(borefield.H,2)}; error: '
              f'{round(abs(1-borefield.H/correct_answers[i - 1])*100,4)} %')


if __name__ == "__main__":   # pragma: no cover
    check_cases()  # check different cases
    check_custom_datafile()  # check if the custom datafile is correct
