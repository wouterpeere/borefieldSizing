"""
This document contains all the code to run create the figures of (Peere W., 2023).
The code is created and should be work with GHEtool v2.2.0. Further compatibility is not guaranteed.
"""

from GHEtool import Borefield, HourlyGeothermalLoad, SingleUTube, DoubleUTube, GroundTemperatureGradient, FluidData

import matplotlib.pyplot as plt
import numpy as np
import pygfunction as gt

import copy
import itertools


# set parameters
glycol_single_lam = FluidData(0.2, 0.5, 1021.7, 3919, 0.0033)
glycol_double_lam = FluidData(0.225, 0.5, 1021.7, 3919, 0.0033)
glycol_single_tur = FluidData(0.36, 0.5, 1021.7, 3919, 0.0033)
glycol_double_tur = FluidData(0.45, 0.5, 1021.7, 3919, 0.0033)

singe_u_pipe_good = SingleUTube(2, 0.016, 0.02, 0.4, 0.04)
double_u_pipe_good = DoubleUTube(2, 0.013, 0.016, 0.4, 0.045)
singe_u_pipe_bad = SingleUTube(1.5, 0.016, 0.02, 0.4, 0.04)
double_u_pipe_bad = DoubleUTube(1.5, 0.013, 0.016, 0.4, 0.045)

fluid_pipes_single = list(zip([glycol_single_lam, glycol_single_tur], [singe_u_pipe_bad, singe_u_pipe_good]))
fluid_pipes_double = list(zip([glycol_double_lam, glycol_double_tur], [double_u_pipe_bad, double_u_pipe_good]))
fluid_pipes = fluid_pipes_single + fluid_pipes_double


office_load = HourlyGeothermalLoad()
auditorium_load = HourlyGeothermalLoad()
residential_load = HourlyGeothermalLoad()
office_load.load_hourly_profile('office.csv', header=True, separator=";", col_cooling=0, col_heating=1)
auditorium_load.load_hourly_profile('auditorium.csv', header=True, separator=";", col_cooling=0, col_heating=1)
residential_load.load_hourly_profile('residential.csv', header=True, separator=";", col_cooling=1, col_heating=0)
loads = [auditorium_load, office_load, residential_load]

# convert to geothermal load using a SCOP of 5
SCOP = 5
factor = 1 - 1/SCOP
for load in loads:
    load.hourly_heating_load = load.hourly_heating_load * factor

ground_low_cond_low_gradient = GroundTemperatureGradient(1.5, 10, gradient=2)
ground_high_cond_low_gradient = GroundTemperatureGradient(2.5, 10, gradient=2)
ground_low_cond_high_gradient = GroundTemperatureGradient(1.5, 10, gradient=3)
ground_high_cond_high_gradient = GroundTemperatureGradient(2.5, 10, gradient=3)
grounds = [ground_low_cond_low_gradient, ground_high_cond_low_gradient,
           ground_low_cond_high_gradient, ground_high_cond_high_gradient]

temp_limits = [(17, 3), (25, 3), (17, 1), (25, 1)]

auditorium_field = gt.boreholes.rectangle_field(6, 6, 6, 6, 150, 0.75, 0.07)
office_field = gt.boreholes.rectangle_field(20, 10, 6, 6, 150, 0.75, 0.07)
residential_field = gt.boreholes.rectangle_field(5, 8, 6, 6, 150, 0.75, 0.07)

ROT = 0.030  # rule of thumb kW/m


def figure_1_2() -> None:
    """
    This function creates Figure 1 and 2 from the article.

    Returns
    -------
    None
    """

    # initialise arrays
    cool, heat, ref = np.empty(3), np.empty(3), np.empty(3)

    # iterate over the different buildings and size the borefield
    for idx, (field, load) in enumerate(zip([auditorium_field, office_field, residential_field],
                                            [auditorium_load, office_load, residential_load])):

        borefield = Borefield(borefield=field, load=load)
        borefield.set_ground_parameters(ground_high_cond_low_gradient)
        borefield.set_max_ground_temperature(17)
        borefield.set_min_ground_temperature(3)
        borefield.set_fluid_parameters(glycol_double_tur)
        borefield.set_pipe_parameters(double_u_pipe_good)
        ref[idx] = (borefield.size(L4_sizing=True) * borefield.number_of_boreholes)

        # calculate the size according to the rule of thumb
        cool[idx] = (load.max_peak_cooling / ROT)
        heat[idx] = (load.max_peak_heating / ROT)

    # Figure 1 for the total required borehole length
    barWidth = 0.25

    plt.figure()

    cool_br = np.arange(3)
    heat_br = [x + barWidth for x in cool_br]
    ref_br = [x + barWidth for x in heat_br]

    plt.bar(cool_br, cool, width=barWidth, label='Rule of thumb cooling')
    plt.bar(heat_br, heat, width=barWidth, label='Rule of thumb heating')
    plt.bar(ref_br, ref, width=barWidth, label='GHEtool (Reference)')

    plt.xticks([r + barWidth for r in range(3)], ['Auditorium', 'Office', 'Residential'])
    plt.ylabel('Total borehole length [m]')
    plt.title('Total borehole length for different buildings')
    plt.legend()

    # Figure 2 for relative over- and undersizing
    # calculate over- and undersizing
    rel_cool = (cool - ref) / ref * 100  # %
    rel_heat = (heat - ref) / ref * 100  # %

    plt.figure()

    cool_br = np.arange(3)
    heat_br = [x + barWidth for x in cool_br]

    plt.bar(cool_br, rel_cool, width=barWidth, label='Rule of thumb cooling')
    plt.bar(heat_br, rel_heat, width=barWidth, label='Rule of thumb heating')

    plt.xticks([r + barWidth for r in range(3)], ['Auditorium', 'Office', 'Residential'])
    plt.ylabel('Relative over- and undersizing w.r.t. GHEtool [%]')
    plt.title('Influence of the building load/type\non the required borehole length')
    plt.ylim((-100, 150))
    plt.legend()
    plt.grid(axis='y')
    plt.show()


def figure_3() -> None:
    """
    This function creates the third figure from the article.

    Returns
    -------
    None
    """

    # initialise loads
    cool, heat, ref = np.empty(4), np.empty(4), np.empty(4)

    # iterate over all flow type-pipe combinations
    field, load = auditorium_field, auditorium_load
    for idx, (fluid, pipe) in enumerate(zip([glycol_double_lam, glycol_double_tur, glycol_single_lam, glycol_single_tur],
                           [double_u_pipe_good, double_u_pipe_good, singe_u_pipe_good, singe_u_pipe_good])):
        borefield = Borefield(borefield=field, load=load)
        borefield.set_ground_parameters(ground_high_cond_low_gradient)
        borefield.set_max_ground_temperature(17)
        borefield.set_min_ground_temperature(3)
        borefield.set_fluid_parameters(fluid)
        borefield.set_pipe_parameters(pipe)
        ref[idx] = (borefield.size(L4_sizing=True) * borefield.number_of_boreholes)

        # size according to the rule of thumb
        cool[idx] = (load.max_peak_cooling / ROT)
        heat[idx] = (load.max_peak_heating / ROT)

    # Figure 3
    barWidth = 0.25

    # calculate relative over- and undersizing
    rel_cool = (cool - ref) / ref * 100  # %
    rel_heat = (heat - ref) / ref * 100  # %

    plt.figure()

    cool_br = np.arange(4)
    heat_br = [x + barWidth for x in cool_br]

    plt.bar(cool_br, rel_cool, width=barWidth, label='Rule of thumb cooling')
    plt.bar(heat_br, rel_heat, width=barWidth, label='Rule of thumb heating')

    plt.xticks([r + barWidth for r in range(4)], ['Double U-pipe\nLaminar flow', 'Double U-pipe\nTurbulent flow',
                                                  'Single U-pipe\nLaminar flow', 'Single U-pipe\nTurbulent flow'])
    plt.ylabel('Relative over- and undersizing w.r.t. GHEtool[%]')
    plt.title('Influence of borehole design parameters\non the required borehole length for the auditorium')
    plt.legend()
    plt.grid(axis='y')
    plt.show()


def figure_4() -> None:
    """
    This function creates Figure 4 from the article.

    Returns
    -------
    None
    """

    # initialise arrays
    cool, heat, ref = np.empty(4), np.empty(4), np.empty(4)

    # iterate over the temperature limits
    field, load = auditorium_field, auditorium_load
    for idx, (max, min) in enumerate(temp_limits):
        borefield = Borefield(borefield=field, load=load)
        borefield.set_ground_parameters(ground_high_cond_low_gradient)
        borefield.set_max_ground_temperature(max)
        borefield.set_min_ground_temperature(min)
        borefield.set_fluid_parameters(glycol_double_tur)
        borefield.set_pipe_parameters(double_u_pipe_good)
        ref[idx] = (borefield.size(L4_sizing=True) * borefield.number_of_boreholes)

        # size according to the rule of thumb
        cool[idx] = (load.max_peak_cooling / ROT)
        heat[idx] = (load.max_peak_heating / ROT)

    # Figure 4
    barWidth = 0.25

    # calculate relative over- and undersizing
    rel_cool = (cool - ref) / ref * 100  # %
    rel_heat = (heat - ref) / ref * 100  # %

    plt.figure()

    cool_br = np.arange(4)
    heat_br = [x + barWidth for x in cool_br]

    plt.bar(cool_br, rel_cool, width=barWidth, label='Rule of thumb cooling')
    plt.bar(heat_br, rel_heat, width=barWidth, label='Rule of thumb heating')

    plt.xticks([r + barWidth for r in range(4)], ['Max 17\nMin 3', 'Max 25\nMin 3',
                                                  'Max 17\nMin 1', 'Max 25\nMin 1'])
    plt.ylabel('Relative over- and undersizing w.r.t. GHEtool[%]')
    plt.title('Influence of average fluid temperature limits\non the required borehole length for the auditorium')
    plt.ylim((-100, 400))
    plt.legend()
    plt.grid(axis='y')
    plt.show()


def figure_5_6() -> None:
    def calc() -> list:
        size_per_field = []
        for idx, (field, load) in enumerate(zip([auditorium_field, office_field, residential_field],
                                                    [auditorium_load, office_load, residential_load])):
            sizes = []
            for ground in grounds:
                for fluid, pipe in fluid_pipes:
                    for temp_limit in temp_limits:
                        for sim_period in (20, 40):
                            try:
                                borefield = Borefield(load=load)
                                borefield.borefield = copy.copy(field)
                                borefield.set_ground_parameters(ground)
                                borefield.simulation_period = sim_period
                                borefield.set_pipe_parameters(pipe)
                                borefield.set_fluid_parameters(fluid)
                                borefield.set_min_ground_temperature(temp_limit[1])
                                borefield.set_max_ground_temperature(temp_limit[0])
                                print(borefield.size())
                                sizes.append(borefield.H * borefield.number_of_boreholes)
                            except RuntimeError:
                                print('Error')
            size_per_field.append(sizes)
        return size_per_field

    # calculate the sizings for each building
    size_per_field = calc()

    # Figure 5
    fig = plt.figure()

    # Creating plot
    plt.boxplot(size_per_field, positions=range(3))

    # Create scatter
    x, y = np.empty(0), np.empty(0)
    for i in range(3):
        y = np.concatenate((y, np.array(size_per_field[i])))
        # Add some random "jitter" to the x-axis
        x = np.concatenate((x, np.random.normal(i, 0.04, size=len(size_per_field[i]))))

    plt.plot(x, y, 'r.', alpha=0.2, label='Individual sizings')

    # add sizing based on rule of thumb
    plt.arrow(0.4, auditorium_load.max_peak_cooling/ROT, -0.2, 0, length_includes_head=True, head_width=500, head_length=0.04, color="#377eb8", label='Rule of thumb cooling')  # cooling
    plt.arrow(0.4, auditorium_load.max_peak_heating/ROT, -0.2, 0, length_includes_head=True, head_width=500, head_length=0.04, color="#ff7f00", label='Rule of thumb heating')
    plt.arrow(1.4, office_load.max_peak_cooling/ROT, -0.2, 0, length_includes_head=True, head_width=500, head_length=0.04, color="#377eb8")  # cooling
    plt.arrow(1.4, office_load.max_peak_heating/ROT, -0.2, 0, length_includes_head=True, head_width=500, head_length=0.04, color="#ff7f00")
    plt.arrow(2.4, residential_load.max_peak_cooling/ROT, -0.2, 0, length_includes_head=True, head_width=500, head_length=0.04, color="#377eb8")  # cooling
    plt.arrow(2.4, residential_load.max_peak_heating/ROT, -0.2, 0, length_includes_head=True, head_width=500, head_length=0.04, color="#ff7f00")

    # labels
    plt.ylabel('Total required borehole length [m]')
    plt.xticks([r for r in range(3)], ['Auditorium', 'Office', 'Residential'])
    plt.legend()
    plt.title('Variation in total required borehole length')
    plt.show()

    # Figure 6
    specific_extraction = [0, 0, 0]

    # list of all the peak values for different buildings in both heating and cooling
    peak = [(auditorium_load.max_peak_heating, auditorium_load.max_peak_cooling),
            (office_load.max_peak_heating, office_load.max_peak_cooling),
            (residential_load.max_peak_heating, residential_load.max_peak_cooling)]

    # calculate specific heat extraction for both heating and cooling
    for i, val in enumerate(size_per_field):
        specific_extraction[i] = val / peak[i][0] + val / peak[i][1]

    plt.figure()
    # Creating plot
    plt.boxplot(specific_extraction, positions=range(3))

    # Create scatter
    x, y = np.empty(0), np.empty(0)
    for i in range(3):
        y = np.concatenate((y, np.array(specific_extraction[i])))
        # Add some random "jitter" to the x-axis
        x = np.concatenate((x, np.random.normal(i, 0.04, size=len(specific_extraction[i]))))

    plt.plot(x, y, 'r.', alpha=0.2, label='Individual sizings')

    # figure layout
    plt.ylabel('Specific heat extraction [W/m]')
    plt.xticks([r for r in range(3)], ['Auditorium', 'Office', 'Residential'])
    plt.legend()
    plt.title('Variation in rule of thumb parameter')
    plt.show()


if __name__ == '__main__':
    figure_1_2()
    figure_3()
    figure_4()
    figure_5_6()
