"""
This file contains an example on how GHEtool can be used to size a borefield
using a combination of active and passive cooling.
This example is based on the work of Coninx and De Nies, 2021.
Coninx, M., De Nies, J. (2022). Cost-efficient Cooling of Buildings by means of Borefields
with Active and Passive Cooling. Master thesis, Department of Mechanical Engineering, KU Leuven, Belgium.
It is also published as: Coninx, M., De Nies, J., Hermans, L., Peere, W., Boydens, W., Helsen, L. (2024).
Cost-efficient cooling of buildings by means of geothermal borefields with active and passive cooling.
Applied Energy, 355, Art. No. 122261, https://doi.org/10.1016/j.apenergy.2023.122261.
"""

from GHEtool import Borefield, GroundConstantTemperature, HourlyGeothermalLoadMultiYear

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skopt import gp_minimize


def active_passive_cooling(location='Active_passive_example.csv'):

    # load data
    columnNames = ['HeatingSpace', 'HeatingAHU', 'CoolingSpace', 'CoolingAHU']
    df = pd.read_csv(location, names=columnNames, header=0)
    heating_data = df.HeatingSpace + df.HeatingAHU
    cooling_data = df.CoolingSpace + df.CoolingAHU

    # variable COP and EER data
    COP = [0.122, 4.365]  # ax+b
    EER = [-3.916, 17,901]  # ax+b
    threshold_active_cooling = 16

    # set simulation period
    SIMULATION_PERIOD: int = 50
    heating_building: np.ndarray = np.tile(np.array(heating_data), SIMULATION_PERIOD)
    cooling_building: np.ndarray = np.tile(np.array(cooling_data), SIMULATION_PERIOD)

    def update_load_COP(temp_profile: np.ndarray,
                    COP:np.ndarray,
                    load_profile: np.ndarray) -> np.ndarray:
        """
        This function updates the geothermal load for heating based on a variable COP

        Parameters
        ----------
        temp_profile : np.ndarray
            Temperature profile of the fluid
        COP : np.ndarray
            Variable COP i.f.o. temperature
        load_profile : np.ndarray
            Heating load of the building

        Returns
        -------
        Geothermal heating load : np.ndarray
        """
        COP_array = temp_profile * COP[0] + COP[1]
        return load_profile * (1 - 1/COP_array)


    def update_load_EER(temp_profile: np.ndarray,
                        EER: np.ndarray,
                        threshold_active_cooling: float,
                        load_profile: np.ndarray) -> np.ndarray:
        """
        This function updates the geothermal load for cooling based on a threshold for active/passive cooling,
        and a variable EER.

        Parameters
        ----------
        temp_profile : np.ndarray
            Temperature profile of the fluid
        EER : np.ndarray
            Variable EER i.f.o. temperature
        threshold_active_cooling : float
            Threshold of the temperature above which active cooling is needed
        load_profile : np.ndarray
            Cooling load of the building

        Returns
        -------
        Geothermal cooling load : np.ndarray
        """
        EER_array = temp_profile * EER[0] + EER[1]
        passive: np.ndarray = temp_profile < threshold_active_cooling
        active = np.invert(passive)
        return active * load_profile * (1 + 1/EER_array) + passive * load_profile


    costs = {"C_elec": 0.2159,      #  electricity cost (EUR/kWh)
             "C_borefield": 35,     #  inv cost per m borefield (EUR/m)
             "DR": 0.0011,          #  discount rate(-)
             "sim_period": SIMULATION_PERIOD}


    def calculate_costs(borefield: Borefield, heating_building: np.ndarray, heating_geothermal: np.ndarray,
                        cooling_building: np.ndarray, cooling_geothermal: np.ndarray, costs: dict) -> tuple:
        """
        This function calculates the relevant costs for the borefield.

        Parameters
        ----------
        borefield : Borefield
            Borefield object
        heating_building : np.ndarray
            Heating demand for the building
        heating_geothermal : np.ndarray
            Heating demand coming from the ground
        cooling_building : np.ndarray
            Cooling demand for the building
        cooling_geothermal : np.ndarray
            Cooling demand coming from the ground
        costs : dict
            Dictionary with investment cost for borefield/m, electricity cost, annual discount rate

        Returns
        -------
        investment cost borefield, operational cost heating, operational cost cooling, total operational cost:
            float, float, float, float
        """
        # calculate investment cost
        investment_borefield = costs["C_borefield"] * borefield.H * borefield.number_of_boreholes

        # calculate working costs
        elec_heating = heating_building - heating_geothermal
        elec_cooling = cooling_geothermal - cooling_building

        discounted_cooling_cost = []
        discounted_heating_cost = []
        for i in range(SIMULATION_PERIOD):
            tempc = costs["C_elec"] * (elec_cooling[730 * 12 * i:730 * 12 * (i + 1)])
            tempc = tempc * (1 / (1 + costs["DR"])) ** (i + 1)

            temph = costs["C_elec"] * (elec_heating[730 * 12 * i:730 * 12 * (i + 1)])
            temph = temph * (1 / (1 + costs["DR"])) ** (i + 1)
            discounted_cooling_cost.append(tempc)
            discounted_heating_cost.append(temph)
        cost_cooling = np.sum(discounted_cooling_cost)
        cost_heating = np.sum(discounted_heating_cost)

        return investment_borefield, cost_heating, cost_cooling, cost_heating+cost_cooling

    borefield = Borefield()
    borefield.simulation_period = SIMULATION_PERIOD
    borefield.set_max_avg_fluid_temperature(17)

    borefield.create_rectangular_borefield(12, 12, 6, 6, 100)
    borefield.set_ground_parameters(GroundConstantTemperature(2.1, 11))
    borefield.Rb = 0.12

    ### PASSIVE COOLING
    depths = [0.9, 0]

    # set initial loads
    cooling_ground = cooling_building.copy()
    heating_ground = heating_building.copy()

    while abs(depths[0] - depths[1]) > 0.1:
        # set loads
        load = HourlyGeothermalLoadMultiYear()
        load.hourly_heating_load = heating_ground
        load.hourly_cooling_load = cooling_ground
        borefield.load = load

        # size borefield
        depth_passive = borefield.size_L4()
        depths.insert(0, depth_passive)

        # get temperature profile
        temp_profile = borefield.results.peak_heating

        # recalculate heating load
        heating_ground = update_load_COP(temp_profile, COP, heating_building)


    ### ACTIVE COOLING
    depths = [0.9, 0]

    # set initial loads
    cooling_ground = cooling_building.copy()
    heating_ground = heating_building.copy()

    borefield.set_max_avg_fluid_temperature(25)
    while abs(depths[0] - depths[1]) > 0.1:
        # set loads
        load = HourlyGeothermalLoadMultiYear()
        load.hourly_heating_load = heating_ground
        load.hourly_cooling_load = cooling_ground
        borefield.load = load

        # size borefield
        depth_active = borefield.size_L4()
        depths.insert(0, depth_active)

        # get temperature profile
        temp_profile = borefield.results.peak_heating

        # recalculate heating load
        heating_ground = update_load_COP(temp_profile, COP, heating_building)
        cooling_ground = update_load_EER(temp_profile, EER, 16, cooling_building)


    ### RUN OPTIMISATION

    # initialise parameters
    operational_costs = []
    operational_costs_cooling = []
    operational_costs_heating = []
    investment_costs = []
    total_costs = []
    depths = []


    def f(depth: list) -> float:
        """
        Optimisation function.

        Parameters
        ----------
        depth : list
            List with one element: the depth of the borefield in mm

        Returns
        -------
        total_cost : float
        """
        # convert to meters
        depth = depth[0] / 1000
        borefield._update_borefield_depth(depth)
        borefield.H = depth
        depths.append(depth)

        # initialise
        heating_ground = heating_building.copy()
        cooling_ground = cooling_building.copy()

        heating_ground_prev = np.zeros(len(heating_ground))
        cooling_ground_prev = np.zeros(len(cooling_ground))

        # iterate until convergence in the load
        while np.sum(cooling_ground + heating_ground - heating_ground_prev - cooling_ground_prev) > 100:
            # set loads
            load = HourlyGeothermalLoadMultiYear()
            load.hourly_heating_load = heating_ground
            load.hourly_cooling_load = cooling_ground
            borefield.load = load

            # get temperature profile
            borefield.calculate_temperatures(depth, hourly=True)
            temp_profile = borefield.results.peak_heating

            # set previous loads
            heating_ground_prev = heating_ground.copy()
            cooling_ground_prev = cooling_ground.copy()

            # recalculate heating load
            heating_ground = update_load_COP(temp_profile, COP, heating_building)
            cooling_ground = update_load_EER(temp_profile, EER, 16, cooling_building)

        # calculate costs
        investment, cost_heating, cost_cooling, operational_cost = calculate_costs(borefield,
                                                                                 heating_building, heating_ground,
                                                                                 cooling_building, cooling_ground,
                                                                                 costs)
        total_costs.append(investment + operational_cost)
        operational_costs.append(operational_cost)
        operational_costs_cooling.append(cost_cooling)
        operational_costs_heating.append(cost_heating)
        investment_costs.append(investment)
        return investment + operational_cost

    # add boundaries to figure
    # multiply with 1000 for numerical stability
    f([depth_active * 10 ** 3])
    f([depth_passive * 10 ** 3])

    res = gp_minimize(f,  # the function to minimize
                      [(depth_active * 10 ** 3, depth_passive * 10 ** 3)],  # the bounds on each dimension of x
                      acq_func="EI",  # the acquisition function
                      n_calls=30,  # the number of evaluations of f
                      initial_point_generator="lhs",
                      n_random_starts=15,  # the number of random initialization points
                      # noise=0,       # the noise level (optional)
                      random_state=1234)  # the random seed

    # plot figures
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(depths, [x/1000 for x in total_costs], marker = 'o', label = "TC")
    ax1.plot(depths, [x/1000 for x in investment_costs], marker = 'o', label="IC")
    ax1.plot(depths, [x/1000 for x in operational_costs], marker = 'o', label="OC")
    ax1.plot(depths, [x/1000 for x in operational_costs_cooling], marker='o', label="OCc")
    ax1.plot(depths, [x/1000 for x in operational_costs_heating], marker='o', label="OCh")
    ax1.set_xlabel(r'Depth (m)', fontsize=14)
    ax1.set_ylabel(r'Costs ($k€$)', fontsize=14)
    ax1.legend(loc='lower left', ncol=3)
    ax1.tick_params(labelsize=14)
    plt.show()


if __name__ == "__main__":  # pragma: no cover
    active_passive_cooling()
