from GHEtool import *
import numpy as np
import pygfunction as gt
import time
import os, contextlib

from GHEtool.Examples.main_functionalities import main_functionalities
from GHEtool.Examples.sizing_with_Rb_calculation import sizing_with_Rb
from GHEtool.Examples.effect_of_borehole_configuration import effect_borefield_configuration
from GHEtool import HourlyGeothermalLoad

# disable the plot function by monkey patching over it
Borefield._plot_temperature_profile = lambda *args, **kwargs: None


# disable the print outputs
def supress_stdout(func):
    def wrapper(*a, **ka):
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                return func(*a, **ka)
    return wrapper


@supress_stdout
def run_without_messages(callable) -> None:
    """
    This function runs the callable without messages.

    Parameters
    ----------
    callable : Callable
        Function to be called

    Returns
    -------
    None
    """
    callable()


def optimise_load_profile() -> None:
    """
    This is a benchmark for the optimise load profile method.

    Returns
    -------
    None
    """
    # initiate ground data
    data = GroundData(3, 10, 0.2)

    # initiate pygfunction borefield model
    borefield_gt = gt.boreholes.rectangle_field(10, 10, 6, 6, 110, 1, 0.075)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(data)

    # set pygfunction borefield
    borefield.set_borefield(borefield_gt)

    # load the hourly profile
    load = HourlyGeothermalLoad()
    load.load_hourly_profile("hourly_profile.csv", header=True, separator=";")
    borefield.load = load

    # optimise the load for a 10x10 field (see data above) and a fixed depth of 150m.
    borefield.optimise_load_profile(depth=150, print_results=False)


def size_L2() -> None:
    """
    This is a benchmark for the L2 sizing method.

    Returns
    -------
    None
    """
    number_of_iterations = 5
    max_value_cooling = 700
    max_value_heating = 800

    monthly_load_cooling_array = np.empty((number_of_iterations, 12))
    monthly_load_heating_array = np.empty((number_of_iterations, 12))
    peak_load_cooling_array = np.empty((number_of_iterations, 12))
    peak_load_heating_array = np.empty((number_of_iterations, 12))

    # populate arrays with random values
    for i in range(number_of_iterations):
        for j in range(12):
            monthly_load_cooling_array[i, j] = np.random.randint(0, max_value_cooling)
            monthly_load_heating_array[i, j] = np.random.randint(0, max_value_heating)
            peak_load_cooling_array[i, j] = np.random.randint(monthly_load_cooling_array[i, j], max_value_cooling)
            peak_load_heating_array[i, j] = np.random.randint(monthly_load_heating_array[i, j], max_value_heating)

    # initiate borefield model
    data = GroundData(3, 10, 0.2)
    borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 1, 0.075)

    # Monthly loading values
    peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10 ** 3  # kWh
    annual_cooling_load = 160 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array(
        [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # create the borefield object
    borefield = Borefield(simulation_period=20,
                          peak_heating=peak_heating,
                          peak_cooling=peak_cooling,
                          baseload_heating=monthly_load_heating,
                          baseload_cooling=monthly_load_cooling)
    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_gt)

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    # size according to L2 method
    for i in range(number_of_iterations):
        borefield.set_baseload_cooling(monthly_load_cooling_array[i])
        borefield.set_baseload_heating(monthly_load_heating_array[i])
        borefield.set_peak_cooling(peak_load_cooling_array[i])
        borefield.set_peak_heating(peak_load_heating_array[i])
        borefield.size(100, L2_sizing=True)


def size_L3() -> None:
    """
    This is a benchmark for the L3 sizing method.

    Returns
    -------
    None
    """
    number_of_iterations = 5
    max_value_cooling = 700
    max_value_heating = 800

    monthly_load_cooling_array = np.empty((number_of_iterations, 12))
    monthly_load_heating_array = np.empty((number_of_iterations, 12))
    peak_load_cooling_array = np.empty((number_of_iterations, 12))
    peak_load_heating_array = np.empty((number_of_iterations, 12))

    # populate arrays with random values
    for i in range(number_of_iterations):
        for j in range(12):
            monthly_load_cooling_array[i, j] = np.random.randint(0, max_value_cooling)
            monthly_load_heating_array[i, j] = np.random.randint(0, max_value_heating)
            peak_load_cooling_array[i, j] = np.random.randint(monthly_load_cooling_array[i, j], max_value_cooling)
            peak_load_heating_array[i, j] = np.random.randint(monthly_load_heating_array[i, j], max_value_heating)

    # initiate borefield model
    data = GroundData(3, 10, 0.2)
    borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 1, 0.075)

    # Monthly loading values
    peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10 ** 3  # kWh
    annual_cooling_load = 160 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array(
        [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # create the borefield object
    borefield = Borefield(simulation_period=20,
                          peak_heating=peak_heating,
                          peak_cooling=peak_cooling,
                          baseload_heating=monthly_load_heating,
                          baseload_cooling=monthly_load_cooling)
    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_gt)

    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

    # size according to L3 method
    for i in range(number_of_iterations):
        borefield.set_baseload_cooling(monthly_load_cooling_array[i])
        borefield.set_baseload_heating(monthly_load_heating_array[i])
        borefield.set_peak_cooling(peak_load_cooling_array[i])
        borefield.set_peak_heating(peak_load_heating_array[i])
        borefield.size(100, L3_sizing=True)


def size_L4() -> None:
    """
    This is a benchmark for the L4 sizing method.

    Returns
    -------
    None
    """
    # initiate ground data
    data = GroundData(3, 10, 0.2)

    # initiate pygfunction borefield model
    borefield_gt = gt.boreholes.rectangle_field(10, 10, 6, 6, 110, 1, 0.075)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(data)

    # set pygfunction borefield
    borefield.set_borefield(borefield_gt)

    # load the hourly profile
    load = HourlyGeothermalLoad()
    load.load_hourly_profile("hourly_profile.csv", header=True, separator=";")
    borefield.load = load

    borefield.size(L4_sizing=True)


def benchmark(callable, name: str) -> None:
    """
    This function calls the callable five times and outputs the time needed to run the callable.

    Parameters
    ----------
    callable : Callable
        Function to be called
    name : str
        Name of the function

    Returns
    -------
    None
    """
    diff, diff_without = 0., 0.

    for i in range(5):
        GFunction.DEFAULT_STORE_PREVIOUS_VALUES = True

        start_time = time.time()
        run_without_messages(callable)
        end_time = time.time()
        diff = diff * i/(i+1) + (end_time - start_time)/(i+1)

        GFunction.DEFAULT_STORE_PREVIOUS_VALUES = False

        start_time_without = time.time()
        run_without_messages(callable)
        end_time_without = time.time()
        diff_without = diff_without * i/(i+1) + (end_time_without - start_time_without)/(i+1)

    print(f'{name} took  {round(diff_without, 2)} ms in v2.1.0 and '
          f'{round(diff, 2)} ms in v2.1.1. This is an improvement of {round((diff_without-diff)/diff*100)}%.')


# run examples
benchmark(main_functionalities, "Main functionalities")
benchmark(optimise_load_profile, "Optimise load profile")
benchmark(sizing_with_Rb, "Sizing with Rb calculation")
benchmark(effect_borefield_configuration, "Effect borehole configuration")

# run benchmark sizing methods
benchmark(size_L2, "Sizing with L2 method")
benchmark(size_L3, "Sizing with L3 method")
benchmark(size_L4, "Sizing with L4 (hourly) method")
