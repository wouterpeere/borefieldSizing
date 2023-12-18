"""
This file contains all the code for the borefield calculations.
"""
from __future__ import annotations

import copy
import warnings
from math import pi
from pathlib import Path
from typing import Tuple
import logging

import matplotlib.pyplot as plt
import numpy as np
import pygfunction as gt
from scipy.signal import convolve
from warnings import warn

from GHEtool.VariableClasses import FluidData, Borehole, GroundConstantTemperature, Results
from GHEtool.VariableClasses import CustomGFunction, load_custom_gfunction, GFunction, CalculationSetup
from GHEtool.VariableClasses.LoadData import *
from GHEtool.VariableClasses.LoadData import _LoadData
from GHEtool.VariableClasses.PipeData import _PipeData
from GHEtool.VariableClasses.BaseClass import BaseClass, UnsolvableDueToTemperatureGradient, MaximumNumberOfIterations
from GHEtool.VariableClasses.GroundData._GroundData import _GroundData
from GHEtool.borefield_configurations.CircleField import CircleField
from GHEtool.borefield_configurations.L_field import LField
from GHEtool.borefield_configurations.U_field import UField
from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration
from GHEtool.borefield_configurations.box_field import BoxField
from GHEtool.borefield_configurations.rectangular_field import RectangularField
from GHEtool.borefield_configurations.undefined_borefield import UndefinedBorefield
from GHEtool.logger.ghe_logger import ghe_logger


class Borefield(BaseClass):
    """Main borefield class"""
    UPM: float = 730.  # number of hours per month
    THRESHOLD_BOREHOLE_DEPTH: float = 0.05  # threshold for iteration
    MAX_SIMULATION_PERIOD: int = 100  # maximal value for simulation

    # define default values
    DEFAULT_INVESTMENT: list = [35, 0]  # 35 EUR/m
    DEFAULT_LENGTH_PEAK: int = 6  # hours
    THRESHOLD_DEPTH_ERROR: int = 10000  # m

    HOURLY_LOAD_ARRAY: np.ndarray = np.arange(0, 8761, UPM).astype(np.uint32)

    __slots__ = 'H', 'borehole', \
        'number_of_boreholes', '_borefield', 'cost_investment', \
        'Tf_max', 'Tf_min', 'limiting_quadrant', \
        'Tf', \
        '_ground_data', '_borefield_load', \
        'options_pygfunction', \
        'THRESHOLD_WARNING_SHALLOW_FIELD', \
        'gui', 'D', 'r_b', 'gfunction_calculation_object', \
        '_calculation_setup', \
        '_secundary_borefield_load', '_building_load', '_external_load'

    def __init__(self, peak_heating: np.ndarray | list = None,
                 peak_cooling: np.ndarray | list = None,
                 baseload_heating: np.ndarray | list = None,
                 baseload_cooling: np.ndarray | list = None,
                 borefield: BorefieldConfiguration | None=None,
                 custom_gfunction: CustomGFunction = None,
                 gui: bool = False,
                 load: _LoadData = None):
        """

        Parameters
        ----------
        peak_heating : list, numpy array
            Monthly peak heating values [kW]
        peak_cooling : list, numpy array
            Monthly peak cooling values [kW]
        baseload_heating : list, numpy array
            Monthly baseload heating values [kWh]
        baseload_cooling : list, numpy array
            Monthly baseload heating values [kWh]
        borefield : pygfunction borehole/borefield object
            Set the borefield for which the calculations will be carried out
        custom_gfunction : CustomGFunction
            Custom gfunction dataset
        gui : bool
            True if the Borefield object is created by the GUI. This should not be used in the code version
            of GHEtool itself.

        Examples
        --------

        monthly peak values [kW]

        >>> peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])
        >>> peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])

        annual heating and cooling load [kWh]

        >>> annual_heating_load = 300 * 10 ** 3
        >>> annual_cooling_load = 160 * 10 ** 3

        percentage of annual load per month (15.5% for January ...)

        >>> monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
        >>> monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

        resulting load per month [kWh]

        >>> monthly_load_heating = annual_heating_load * monthly_load_heating_percentage
        >>> monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage

        create the borefield object

        >>> borefield = Borefield()

        set the load

        >>> load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)
        >>> borefield.load = load

        """

        # initiate vars
        LIST_OF_ZEROS = np.zeros(12)
        if baseload_cooling is None:
            baseload_cooling: np.ndarray = LIST_OF_ZEROS
        if baseload_heating is None:
            baseload_heating: np.ndarray = LIST_OF_ZEROS
        if peak_cooling is None:
            peak_cooling: np.ndarray = LIST_OF_ZEROS
        if peak_heating is None:
            peak_heating: np.ndarray = LIST_OF_ZEROS

        self.limiting_quadrant: int = 0  # parameter that tells in which quadrant the field is limited
        # m hereafter one needs to chance to fewer boreholes with more depth, because the calculations are no longer
        # that accurate.
        self.THRESHOLD_WARNING_SHALLOW_FIELD: int = 50

        self.custom_gfunction: CustomGFunction = custom_gfunction
        self.gfunction_calculation_object: GFunction = GFunction()

        ## params w.r.t. pygfunction
        self.options_pygfunction: dict = {"method": "equivalent"}

        # initialize variables for temperature plotting
        self.results = Results()

        # initiate ground parameters
        self.H = 0.  # borehole depth m
        self.number_of_boreholes = 0  # number of total boreholes #
        self._ground_data: _GroundData = GroundConstantTemperature()
        self.D: float = 0.  # buried depth of the borehole [m]
        self.r_b: float = 0.  # borehole radius [m]

        # initiate fluid parameters
        self.Tf: float = 0.  # temperature of the fluid
        self.Tf_max: float = 16.  # maximum temperature of the fluid
        self.Tf_min: float = 0.  # minimum temperature of the fluid

        # initiale borehole
        self.borehole = Borehole()

        # initiate different sizing
        self._calculation_setup: CalculationSetup = CalculationSetup()
        self.calculation_setup()

        # check if the GHEtool is used by the gui i
        self.gui = gui

        # load on the geothermal borefield, used in calculations
        self._borefield_load = MonthlyGeothermalLoadAbsolute()
        # geothermal load, but converted to a secundary demand in optimise_load_profile
        self._secundary_borefield_load: HourlyGeothermalLoad = HourlyGeothermalLoad()
        # secundary load of the building, used in optimise_load_profile
        self._building_load: HourlyGeothermalLoad = HourlyGeothermalLoad()

        if load is not None:
            self.load = load
        else:
            self.load = MonthlyGeothermalLoadAbsolute(baseload_heating, baseload_cooling,
                                                      peak_heating, peak_cooling)

        # set investment cost
        self.cost_investment: list = Borefield.DEFAULT_INVESTMENT

        # set a custom borefield
        self.borefield: BorefieldConfiguration | None = borefield

        ghe_logger.main_info("Borefield object has been created.")

    @staticmethod
    def activate_logger() -> None:
        """
        This function activates the logging.

        Returns
        -------
        None
        """
        ghe_logger.setLevel("MAIN_INFO")

    @staticmethod
    def deactivate_logger() -> None:
        """
        This function deactivates the logging.

        Returns
        -------
        None
        """
        ghe_logger.setLevel(logging.INFO)

    def _set_number_of_boreholes(self) -> None:
        """
        This functions sets the number of boreholes based on the length of the borefield attribute.

        Returns
        -------
        None
        """
        self.number_of_boreholes = len(self.borefield.li_boreholes) if self.borefield is not None else 0

    def set_borefield(self, borefield: list[gt.boreholes.Borehole] = None) -> None:
        """
        This function set the borefield object. When None is given, the borefield will be deleted.

        Parameters
        ----------
        borefield : List[pygfunction.boreholes.Borehole]
            Borefield created with the pygfunction package

        Returns
        -------
        None
        """
        self.borefield = borefield

    def create_rectangular_borefield(self, N_1: int, N_2: int, B_1: float, B_2: float, H: float, D: float = 1,
                                     r_b: float = 0.075) -> RectangularField:
        """
        This function creates a rectangular borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        N_1 : int
            Number of boreholes in the x direction
        N_2 : int
            Number of boreholes in the y direction
        B_1 : float
            Distance between adjacent boreholes in the x direction [m]
        B_2 : float
            Distance between adjacent boreholes in the y direction [m]
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]

        Returns
        -------
        pygfunction borefield object
        """
        borefield = RectangularField(N_1, N_2, B_1, B_2, H, D, r_b)
        self.borefield = borefield
        return borefield

    def create_box_borefield(self, N_1: int, N_2: int, B_1: float, B_2: float, H: float, D: float = 1,
                                     r_b: float = 0.075) -> BoxField:
        """
        This function creates a box shaped borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        N_1 : int
            Number of boreholes in the x direction
        N_2 : int
            Number of boreholes in the y direction
        B_1 : float
            Distance between adjacent boreholes in the x direction [m]
        B_2 : float
            Distance between adjacent boreholes in the y direction [m]
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]

        Returns
        -------
        pygfunction borefield object
        """
        borefield = BoxField(N_1, N_2, B_1, B_2, H, D, r_b)
        self.borefield = borefield
        return borefield

    def create_L_shaped_borefield(self, N_1: int, N_2: int, B_1: float, B_2: float, H: float, D: float = 1,
                                     r_b: float = 0.075) -> LField:
        """
        This function creates a L shaped borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        N_1 : int
            Number of boreholes in the x direction
        N_2 : int
            Number of boreholes in the y direction
        B_1 : float
            Distance between adjacent boreholes in the x direction [m]
        B_2 : float
            Distance between adjacent boreholes in the y direction [m]
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]

        Returns
        -------
        pygfunction borefield object
        """
        borefield = LField(N_1, N_2, B_1, B_2, H, D, r_b)
        self.borefield = borefield
        return borefield

    def create_U_shaped_borefield(self, N_1: int, N_2: int, B_1: float, B_2: float, H: float, D: float = 1,
                                     r_b: float = 0.075) -> UField:
        """
        This function creates a U shaped borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        x-> y^
        o    o
        o    o
        o    o
        oooooo
        -> N_1 = 6, N_2 =4

        Parameters
        ----------
        N_1 : int
            Number of boreholes in the x direction
        N_2 : int
            Number of boreholes in the y direction
        B_1 : float
            Distance between adjacent boreholes in the x direction [m]
        B_2 : float
            Distance between adjacent boreholes in the y direction [m]
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]

        Returns
        -------
            UField
        """
        borefield = UField(N_1, N_2, B_1, B_2, H, D, r_b)
        self.borefield = borefield
        return borefield

    def create_circular_borefield(self, N: int, radius_center_2_boreholes: float, H: float, D: float = 1, r_b: float = 0.075) -> CircleField:
        """
        This function creates a circular borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        N : int
            Number of boreholes in the borefield
        radius_center_2_boreholes : float
            radius form center to boreholes
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]

        Returns
        -------
            CircleField
        """
        borefield = CircleField(N, radius_center_2_boreholes, H, D, r_b)
        self.set_borefield(borefield)
        return borefield

    def create_start_config(self) -> list[tuple]:
        config = self._borefield.create_start_config()
        self.borefield = self._borefield
        return config

    def update_config(self, n_min: int) -> list[tuple]:
        config = self._borefield.update_config(n_min)
        self.borefield = self._borefield
        return config

    def check_config(self, config: tuple) -> bool:
        self._borefield.reset_from_config(config)
        self.borefield = self._borefield
        self.calculate_temperatures(self._borefield.depth_max)
        return np.max(self.results_peak_cooling - self.Tf_max) < 0 and np.min(self.results_peak_heating - self.Tf_min) > 0

    @property
    def borefield(self):
        """
        Returns the hidden _borefield variable.

        Returns
        -------
        Hidden _borefield object
        """
        return self._borefield

    @borefield.setter
    def borefield(self, borefield: BorefieldConfiguration | list[gt.boreholes.Borehole] | None = None) -> None:
        """
        This function sets the borefield configuration. When no input is given, the borefield variable will be deleted.

        Parameters
        ----------
        borefield : List[pygfunction.boreholes.Borehole]
            Borefield created with the pygfunction package

        Returns
        -------
        None
        """
        if borefield is None:
            del self.borefield
            return
        if isinstance(borefield, list):
            borefield = UndefinedBorefield(borefield)
        self._borefield: BorefieldConfiguration = borefield
        self._set_number_of_boreholes()
        self.D = borefield.D
        self.r_b = borefield.r_b
        self.H = borefield.H
        self.gfunction_calculation_object.remove_previous_data()

    @borefield.deleter
    def borefield(self):
        """
        This function deletes the hidden _borefield object.
        It also sets the number of boreholes to zero

        Returns
        -------
        None
        """
        self._borefield = None
        self._set_number_of_boreholes()
        self.gfunction_calculation_object.remove_previous_data()
        self.custom_gfunction = None

    def _update_borefield_depth(self, H: float = None) -> None:
        """
        This function updates the borehole depth.

        Parameters
        ----------
        H : float
            Borehole depth.

        Returns
        -------
        None
        """
        H = H if H is not None else self.H

        if self._borefield.H == H:
            # the borefield is already at the correct depth
            return

        for bor in self._borefield.li_boreholes:
            bor.H = H

    def load_custom_gfunction(self, location: str) -> None:
        """
        This function loads the custom gfunction.

        Parameters
        ----------
        location : str
            Path to the location of the custom gfunction file

        Returns
        -------
        None
        """

        self.custom_gfunction = load_custom_gfunction(location)
        ghe_logger.main_info("Custom g-function has been loaded.")

    def set_investment_cost(self, investment_cost: list = None) -> None:
        """
        This function sets the investment cost. This is linear with respect to the total field length.
        If None, the default is set.

        Parameters
        ----------
        investment_cost : list
            1D array of polynomial coefficients (including coefficients equal to zero) from highest degree to the constant term

        Returns
        -------
        None
        """
        if investment_cost is None:
            investment_cost = Borefield.DEFAULT_INVESTMENT
        self.cost_investment: list = investment_cost

    def set_length_peak(self, length: float = DEFAULT_LENGTH_PEAK) -> None:
        """
        This function sets the length of the peak.

        Parameters
        ----------
        length : float
            Length of the peak [hours]

        Returns
        -------
        None
        """
        self._borefield_load.peak_duration = length

    def set_length_peak_heating(self, length: float = DEFAULT_LENGTH_PEAK) -> None:
        """
        This function sets the length of the heating peak.

        Parameters
        ----------
        length : float
            Length of the peak [hours]

        Returns
        -------
        None
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.peak_heating_duration = length

    def set_length_peak_cooling(self, length: float = DEFAULT_LENGTH_PEAK) -> None:
        """
        This function sets the length of the cooling peak.

        Parameters
        ----------
        length : float
            Length of the peak [hours]

        Returns
        -------
        None
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.peak_cooling_duration = length

    def set_simulation_period(self, simulation_period: int) -> None:
        """
        This function sets the simulation period and updates the time constants.

        Parameters
        ----------
        simulation_period : int
            Simulation period [years]

        Returns
        -------
        None
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.simulation_period = simulation_period

    def set_load(self, load: _LoadData) -> None:
        """
        This function sets the _load attribute.

        Parameters
        ----------
        load : _LoadData
            Load data object

        Returns
        -------
        None
        """
        self.load = load

    @property
    def load(self) -> _LoadData | HourlyGeothermalLoad | MonthlyGeothermalLoadAbsolute:
        """
        This returns the LoadData object.

        Returns
        -------
        Load data: LoadData
        """
        return self._borefield_load

    @load.setter
    def load(self, load: _LoadData) -> None:
        """
        This function sets the _load attribute.

        Parameters
        ----------
        load : _LoadData
            Load data object

        Returns
        -------
        None
        """
        self._borefield_load = load
        self._delete_calculated_temperatures()

    @property
    def simulation_period(self) -> int:
        """
        This returns the simulation period from the LoadData object.

        Returns
        -------
        Simulation period [years] : int
        """
        return self.load.simulation_period

    @simulation_period.setter
    def simulation_period(self, simulation_period: float) -> None:
        """
        This function sets the simulation period.

        Parameters
        ----------
        simulation_period : float
            Simulation period in years

        Returns
        -------
        None
        """
        self._borefield_load.simulation_period = simulation_period

    @property
    def Rb(self) -> float:
        """
        This function returns the equivalent borehole thermal resistance.

        Returns
        -------
        Rb : float
            Equivalent borehole thermal resistance [mK/W]
        """
        return self.borehole.get_Rb(self.H, self.D, self.r_b, self.ground_data.k_s)

    @Rb.setter
    def Rb(self, Rb: float) -> None:
        """
        This function sets the constant equivalent borehole thermal resistance.

        Parameters
        ----------
        Rb : float
            Equivalent borehole thermal resistance [mk/W]

        Returns
        -------
        None
        """
        self.set_Rb(Rb)

    @property
    def ground_data(self) -> _GroundData:
        """"
        This function returns the ground data.

        Returns
        -------
        ground data : GroundData

        """
        return self._ground_data

    @ground_data.setter
    def ground_data(self, data: _GroundData) -> None:
        """
        This function sets the relevant ground parameters.

        Parameters
        ----------
        data : GroundData
            All the relevant ground data

        Returns
        -------
        None
        """
        # Ground properties
        self._ground_data = data

        # new ground data implies that a new g-function should be loaded
        self.custom_gfunction = None

        # the stored gfunction data should be deleted
        self.gfunction_calculation_object.remove_previous_data()

    def set_ground_parameters(self, data: _GroundData) -> None:
        """
        This function sets the relevant ground parameters.

        Parameters
        ----------
        data : GroundData
            All the relevant ground data

        Returns
        -------
        None
        """

        # Ground properties
        self.ground_data = data

    def set_fluid_parameters(self, data: FluidData) -> None:
        """
        This function sets the fluid parameters.

        Parameters
        ----------
        data : FluidData
            All the relevant fluid data

        Returns
        -------
        None
        """
        self.borehole.fluid_data = data

    def set_pipe_parameters(self, data: _PipeData) -> None:
        """
        This function sets the pipe parameters.

        Parameters
        ----------
        data : PipeData
            All the relevant pipe parameters

        Returns
        -------
        None
        """
        self.borehole.pipe_data = data

    def set_Rb(self, Rb: float) -> None:
        """
        This function sets the constant equivalent borehole thermal resistance.

        Parameters
        ----------
        Rb : float
            Equivalent borehole thermal resistance (mK/W)

        Returns
        -------
        None
        """
        self.borehole.Rb = Rb

    def set_max_avg_fluid_temperature(self, temp: float) -> None:
        """
        This functions sets the maximal average fluid temperature to temp.

        Parameters
        ----------
        temp : float
            Maximal average fluid temperature [deg C]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When the maximal average fluid temperature is lower than the minimal average fluid temperature
        """
        if temp <= self.Tf_min:
            raise ValueError(f'The maximum average fluid temperature {temp} is lower than the minimum average fluid temperature {self.Tf_min}')
        self.Tf_max: float = temp

    def set_max_ground_temperature(self, temp: float) -> None:  # pragma: no cover
        DeprecationWarning('This function will be depreciated in v2.2.1. Please use the correct set_max_avg_fluid_temperature() function')
        self.set_max_avg_fluid_temperature(temp)

    def set_min_avg_fluid_temperature(self, temp: float) -> None:
        """
        This functions sets the minimal average fluid temperature to temp.

        Parameters
        ----------
        temp : float
            Minimal average fluid temperature [deg C]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When the maximal average temperature is lower than the minimal average temperature
        """
        if temp >= self.Tf_max:
            raise ValueError(f'The minimum average fluid temperature {temp} is lower than the maximum average fluid temperature {self.Tf_max}')
        self.Tf_min: float = temp

    def set_min_ground_temperature(self, temp: float) -> None:  # pragma: no cover
        DeprecationWarning('This function will be depreciated in v2.2.1. Please use the correct set_min_avg_fluid_temperature() function')
        self.set_min_avg_fluid_temperature(temp)

    def _Tg(self, H: float = None) -> float:
        """
        This function gives back the ground temperature.

        Parameters
        ----------
        H : float
            Depth of the field at which the temperature is to be evaluated

        Returns
        -------
        Temperature of the ground : float
        """
        # check if specific depth is given
        if H is None:
            H = self.H

        return self.ground_data.calculate_Tg(H)

    def _check_convergence(self, new_depth: float, old_depth: float, iter: int) -> bool:
        """
        This function checks, with the absolute and relative tolerance, if the depth is converged.
        This is the case if both criteria are met. Raises MaximumNumberOfIterations error if the max number of iterations is crossed.

        Parameters
        ----------
        new_depth : float
            Depth from the current interation [m]
        old_depth : float
            Depth from the previous iteration [m]
        iter : int
            Current number of iteration

        Returns
        -------
        bool
            True if the depth is converged

        Raises
        ------
        MaximumNumberOfIterations
            MaximumNumberOfIterations if the max number of iterations is crossed
        """
        if iter + 1 > self._calculation_setup.max_nb_of_iterations:
            raise MaximumNumberOfIterations(self._calculation_setup.max_nb_of_iterations)

        if old_depth == 0:
            return False
        test_a_tol = abs(new_depth - old_depth) <= self._calculation_setup.atol if self._calculation_setup.atol != False else True
        test_rtol = abs(
            new_depth - old_depth) / old_depth <= self._calculation_setup.rtol if self._calculation_setup.rtol != False else True

        return test_a_tol and test_rtol

    def _Ahmadfard(self, th: float, qh: float, qm: float, qa: float) -> float:
        """
        This function sizes the field based on the last year of operation, i.e. quadrants 2 and 4.

        It uses the methodology developed by (Ahmadfard and Bernier, 2019) [#Ahmadfard2019]_.
        The concept of borefield quadrants is developed by (Peere et al., 2020) [#PeereBS]_ [#PeereThesis]_.

        Parameters
        ----------
        th : float
            Peak duration [s]
        qh : float
            Peak load [W]
        qm : float
            Monthly average load [W]
        qa : float
            Yearly imbalance load [W]

        Returns
        -------
        H : float
            Required borehole depth [m]

        References
        ----------
        .. [#Ahmadfard2019] Ahmadfard M. and Bernier M., A review of vertical ground heat exchanger sizing tools including an inter-model comparison,
        Renewable and Sustainable Energy Reviews, Volume 110, 2019, Pages 247-265, ISSN 1364-0321, https://doi.org/10.1016/j.rser.2019.04.045
        .. [#PeereBS] Peere, W., Picard, D., Cupeiro Figueroa, I., Boydens, W., and Helsen, L. (2021) Validated combined first and last year borefield sizing methodology. In Proceedings of International Building Simulation Conference 2021. Brugge (Belgium), 1-3 September 2021. https://doi.org/10.26868/25222708.2021.30180
        .. [#PeereThesis] Peere, W. (2020) Methode voor economische optimalisatie van geothermische verwarmings- en koelsystemen. Master thesis, Department of Mechanical Engineering, KU Leuven, Belgium.
        """
        # initiate iteration
        H_prev = 0
        # set minimal depth to 50 m
        self.H = 50 if self.H < 1 else self.H

        time = np.array([th, th + self.load.tm, self.load.ty + self.load.tm + th])
        # Iterates as long as there is no convergence
        # (convergence if difference between depth in iterations is smaller than THRESHOLD_BOREHOLE_DEPTH)
        i = 0
        while not self._check_convergence(self.H, H_prev, i):
            # calculate the required g-function values
            gfunct_uniform_T = self.gfunction(time, max(1, self.H))
            # calculate the thermal resistances
            Ra = (gfunct_uniform_T[2] - gfunct_uniform_T[1]) / (2 * pi * self.ground_data.k_s)
            Rm = (gfunct_uniform_T[1] - gfunct_uniform_T[0]) / (2 * pi * self.ground_data.k_s)
            Rd = (gfunct_uniform_T[0]) / (2 * pi * self.ground_data.k_s)
            # calculate the total borehole length
            L = (qa * Ra + qm * Rm + qh * Rd + qh * self.Rb) / abs(self.Tf - self._Tg())
            # updating the depth values
            H_prev = self.H
            self.H = L / self.number_of_boreholes
            i += 1

        return self.H

    def _Carcel(self, th: float, tcm: float, qh: float, qpm: float, qm: float) -> float:
        """
        This function sizes the field based on the first year of operation, i.e. quadrants 1 and 3.

        It uses the methodology developed by (Monzo et al., 2016) [#Monzo]_ and adapted by (Peere et al., 2021) [#PeereBS]_.
        The concept of borefield quadrants is developed by (Peere et al., 2021) [#PeereBS]_, [#PeereThesis]_.

        Returns
        -------
        H : float
            Required borehole depth [m]

        References
        ----------
        .. [#Monzo] Monzo, P., M. Bernier, J. Acuna, and P. Mogensen. (2016). A monthly based bore field sizing methodology with applications to optimum borehole spacing. ASHRAE Transactions 122, 111–126.
        .. [#PeereBS] Peere, W., Picard, D., Cupeiro Figueroa, I., Boydens, W., and Helsen, L. (2021) Validated combined first and last year borefield sizing methodology. In Proceedings of International Building Simulation Conference 2021. Brugge (Belgium), 1-3 September 2021. https://doi.org/10.26868/25222708.2021.30180
        .. [#PeereThesis] Peere, W. (2020) Methode voor economische optimalisatie van geothermische verwarmings- en koelsystemen. Master thesis, Department of Mechanical Engineering, KU Leuven, Belgium.
        """

        # initiate iteration
        H_prev = 0
        time_steps = [th, th + self.load.tm, tcm + th]
        if self.H < 1:
            self.H = 50

        # Iterates as long as there is no convergence
        # (convergence if difference between depth in iterations is smaller than THRESHOLD_BOREHOLE_DEPTH)
        i = 0
        while not self._check_convergence(self.H, H_prev, i):
            # get the g-function values
            gfunc_uniform_T = self.gfunction(time_steps, max(1, self.H))

            # calculate the thermal resistances
            Rpm = (gfunc_uniform_T[2] - gfunc_uniform_T[1]) / (2 * pi * self.ground_data.k_s)
            Rcm = (gfunc_uniform_T[1] - gfunc_uniform_T[0]) / (2 * pi * self.ground_data.k_s)
            Rh = (gfunc_uniform_T[0]) / (2 * pi * self.ground_data.k_s)

            # calculate the total length
            L = (qh * self.Rb + qh * Rh + qm * Rcm + qpm * Rpm) / abs(self.Tf - self._Tg())

            # updating the depth values
            H_prev = self.H
            self.H = L / self.number_of_boreholes
            i += 1
        return self.H

    def calculation_setup(self, calculation_setup: CalculationSetup = None, use_constant_Rb: bool = None, **kwargs) -> None:
        """
        This function sets the options for the sizing function.

        * The L2 sizing is the one explained in (Peere et al., 2021) [#PeereBS]_ and is the quickest method (it uses 3 pulses)

        * The L3 sizing is a more general approach which is slower but more accurate (it uses 24 pulses/year)

        * The L4 sizing is the most exact one, since it uses hourly data (8760 pulses/year)

        Parameters
        ----------
        calculation_setup : CalculationSetup
            An instance of the CalculationSetup class. When this argument differs from None, all the other parameters are
            set based on this calculation_setup
        use_constant_Rb : bool
            True if a constant borehole equivalent resistance (Rb*) value should be used
        kwargs
            Dictionary with all the other options that can be set within GHEtool. For a complete list,
            see the documentation in the CalculationSetup class.

        Returns
        -------
        None

        References
        ----------
        .. [#PeereBS] Peere, W., Picard, D., Cupeiro Figueroa, I., Boydens, W., and Helsen, L. (2021) Validated combined first and last year borefield sizing methodology. In Proceedings of International Building Simulation Conference 2021. Brugge (Belgium), 1-3 September 2021. https://doi.org/10.26868/25222708.2021.30180
        .. [#PeereThesis] Peere, W. (2020) Methode voor economische optimalisatie van geothermische verwarmings- en koelsystemen. Master thesis, Department of Mechanical Engineering, KU Leuven, Belgium.
        """

        # if calculation_setup is not None, then the sizing setup is set directly
        if calculation_setup is not None:
            self._calculation_setup = calculation_setup
            return

        self._calculation_setup.update_variables(**kwargs)

        if not use_constant_Rb is None:
            self.borehole.use_constant_Rb = use_constant_Rb

    def size(self, H_init: float = None, use_constant_Rb: bool = None, L2_sizing: bool = None,
             L3_sizing: bool = None, L4_sizing: bool = None, quadrant_sizing: int = None, **kwargs) -> float:
        """
        This function sets the options for the sizing function.

        * The L2 sizing is the one explained in (Peere et al., 2021) [#PeereBS]_ and is the quickest method (it uses 3 pulses)

        * The L3 sizing is a more general approach which is slower but more accurate (it uses 24 pulses/year)

        * The L4 sizing is the most exact one, since it uses hourly data (8760 pulses/year)

        Please note that the changes sizing setup changes here are not saved! Use self.setupSizing for this.

        Parameters
        ----------
        H_init : float
            Initial depth for the iteration. If None, the default H_init is chosen.
        use_constant_Rb : bool
            True if a constant borehole equivalent resistance (Rb*) value should be used
        L2_sizing : bool
            True if a sizing with the L2 method is needed
        L3_sizing : bool
            True if a sizing with the L3 method is needed
        L4_sizing : bool
            True if a sizing with the L4 method is needed
        quadrant_sizing : int
            Differs from 0 when a sizing in a certain quadrant is desired.
            Quadrants are developed by (Peere et al., 2021) [#PeereBS]_, [#PeereThesis]_
        kwargs : dict
            Dictionary with all the other options that can be set within GHEtool. For a complete list,
            see the documentation in the CalculationSetup class.

        Returns
        -------
        borehole depth : float

        Raises
        ------
        ValueError
            ValueError when no ground data is provided
        """
        # check ground data
        if not self.ground_data.check_values():
            raise ValueError("Please provide ground data.")

        # make backup of initial parameter states
        self._calculation_setup.make_backup()
        use_constant_Rb_backup = self.borehole.use_constant_Rb

        # run the sizing setup
        self._calculation_setup.update_variables(H_init=H_init, L2_sizing=L2_sizing, L3_sizing=L3_sizing,
                                                 L4_sizing=L4_sizing,
                                                 quadrant_sizing=quadrant_sizing)
        self._calculation_setup.update_variables(**kwargs)

        if not use_constant_Rb is None:
            self.borehole.use_constant_Rb = use_constant_Rb

        # sizes according to the correct algorithm
        if self._calculation_setup.L2_sizing:
            depth = self.size_L2(H_init, self._calculation_setup.quadrant_sizing)
        if self._calculation_setup.L3_sizing:
            depth = self.size_L3(H_init, self._calculation_setup.quadrant_sizing)
        if self._calculation_setup.L4_sizing:
            depth = self.size_L4(H_init, self._calculation_setup.quadrant_sizing)

        # reset initial parameters
        self._calculation_setup.restore_backup()
        self.borehole.use_constant_Rb = use_constant_Rb_backup

        # check if the field is not shallow
        if depth < self.THRESHOLD_WARNING_SHALLOW_FIELD:
            ghe_logger.warning(f"The field has a calculated depth of {round(depth, 2)}"
                               f"m which is lower than the proposed minimum "
                               f"of {self.THRESHOLD_WARNING_SHALLOW_FIELD} m. "
                               f"Please change your configuration accordingly to have a not so shallow field.")

        ghe_logger.info("The borefield has been sized.")
        return depth

    def _select_size(self, size_max_temp: float, size_min_temp: float, hourly: bool = False) -> float:
        """
        This function selects the correct size based on a size for the minimum and maximum temperature.
        When no temperature gradient is taken into account, this is just the maximum value of the two.
        When there is a temperature gradient and the sizing for the minimum temperature is higher than the sizing
        for the max temperature, it is checked if this sizing does not cross the maximum temperature limit.
        If it does, an error is returned.

        Parameters
        ----------
        size_max_temp : float
            Sizing according to the quadrants limited by the maximum temperature [m]
        size_min_temp : float
            Sizing according to the quadrants limited by the minimum temperature [m]
        hourly : bool
            True if the sizing was hourly

        Returns
        -------
        depth : float
            Required borehole depth [m]

        Raises
        ------
        UnsolvableDueToTemperatureGradient
            Error when no solution can be found
        """
        # return the max of both sizes when no temperature gradient is used
        if not self.ground_data.variable_Tg:
            return max(size_max_temp, size_min_temp)

        if size_max_temp > size_min_temp:
            # no problem, since the field is already sized by the maximum temperature
            return size_max_temp

        # check if sizing by the minimum temperature (quadrant 3/4) does not cross the temperature boundary
        self.calculate_temperatures(size_min_temp, hourly=hourly)
        if np.max(self.results.peak_cooling) <= self.Tf_max:
            return size_min_temp
        raise UnsolvableDueToTemperatureGradient

    def size_L2(self, H_init: float = None, quadrant_sizing: int = 0) -> float:
        """
        This function sizes the  of the given configuration according to the methodology explained in
        (Peere et al., 2021) [#PeereBS]_, which is a L2 method. When quadrant sizing is other than 0, it sizes the field based on
        the asked quadrant. It returns the borefield depth.

        Parameters
        ----------
        H_init : float
            Initial depth from where to start the iteration [m]
        quadrant_sizing : int
            If a quadrant is given the sizing is performed for this quadrant else for the relevant

        Returns
        -------
        H : float
            Required depth of the borefield [m]

        Raises
        ------
        ValueError
            ValueError when no ground data is provided or quadrant is not in range.
        """
        # check ground data
        if not self.ground_data.check_values():
            raise ValueError("Please provide ground data.")
        # check quadrants
        if not quadrant_sizing in range(0, 5):
            raise ValueError(f'Quadrant {quadrant_sizing} does not exist.')

        # initiate with a given depth
        self.H: float = H_init if H_init is not None else self._calculation_setup.H_init

        def size_quadrant1():
            th, _, tcm, qh, qpm, qm = self.load._calculate_first_year_params(False)  # calculate parameters
            self.Tf = self.Tf_max
            return self._Carcel(th, tcm, qh, qpm, qm)  # size

        def size_quadrant2():
            th, qh, qm, qa = self.load._calculate_last_year_params(False)  # calculate parameters
            self.Tf = self.Tf_max
            return self._Ahmadfard(th, qh, qm, qa)  # size

        def size_quadrant3():
            th, _, tcm, qh, qpm, qm = self.load._calculate_first_year_params(True)  # calculate parameters
            self.Tf = self.Tf_min
            return self._Carcel(th, tcm, qh, qpm, qm)  # size

        def size_quadrant4():
            th, qh, qm, qa = self.load._calculate_last_year_params(True)  # calculate parameters
            self.Tf = self.Tf_min
            return self._Ahmadfard(th, qh, qm, qa)  # size

        if quadrant_sizing != 0:
            # size according to a specific quadrant
            if quadrant_sizing == 1:
                self.H = size_quadrant1()
            elif quadrant_sizing == 2:
                self.H = size_quadrant2()
            elif quadrant_sizing == 3:
                self.H = size_quadrant3()
            else:
                self.H = size_quadrant4()
            self.limiting_quadrant = quadrant_sizing
        else:
            # size according to the biggest quadrant
            # determine which quadrants are relevant
            if self.load.imbalance <= 0:
                # extraction dominated, so quadrants 1 and 4 are relevant
                if self.load.max_peak_cooling != 0:
                    quadrant1 = size_quadrant1()
                else:
                    quadrant1 = 0
                quadrant4 = size_quadrant4()

                self.H = self._select_size(quadrant1, quadrant4)

                if quadrant1 == self.H:
                    self.limiting_quadrant = 1
                else:
                    self.limiting_quadrant = 4
            else:
                # injection dominated, so quadrants 2 and 3 are relevant
                quadrant2 = size_quadrant2()
                if self.load.max_peak_heating != 0:
                    quadrant3 = size_quadrant3()
                else:
                    quadrant3 = 0

                self.H = self._select_size(quadrant2, quadrant3)

                if quadrant2 == self.H:
                    self.limiting_quadrant = 2
                else:
                    self.limiting_quadrant = 3

        return self.H

    def size_L3(self, H_init: float = None, quadrant_sizing: int = 0) -> float:
        """
        This function sizes the borefield based on a monthly (L3) method.

        Parameters
        ----------
        H_init : float
            Initial depth from where to start the iteration [m]
        quadrant_sizing : int
            If a quadrant is given the sizing is performed for this quadrant else for the relevant

        Returns
        -------
        H : float
            Required depth of the borefield [m]

        Raises
        ------
         ValueError
            ValueError when no ground data is provided or quadrant is not in range.
        UnsolvableDueToTemperatureGradient
            Error when the field cannot be sized.
        """
        # check ground data
        if not self.ground_data.check_values():
            raise ValueError("Please provide ground data.")
        # check quadrants
        if not quadrant_sizing in range(0, 5):
            raise ValueError(f'Quadrant {quadrant_sizing} does not exist.')

        # initiate with a given depth
        self.H: float = H_init if H_init is not None else self._calculation_setup.H_init

        if quadrant_sizing != 0:
            # size according to a specific quadrant
            self.H, _ = self._size_based_on_temperature_profile(quadrant_sizing)
            return self.H
        else:
            try:
                max_temp, sized = self._size_based_on_temperature_profile(10, deep_sizing=self._calculation_setup.force_deep_sizing)
            except MaximumNumberOfIterations as e:
                # no convergence with normal method, but perhaps with deep_sizing enabled
                if self._calculation_setup.deep_sizing and self.ground_data.variable_Tg:
                    max_temp, sized = self._size_based_on_temperature_profile(10, deep_sizing=True)
                else:
                    raise e
            if sized:
                # already correct size
                self.H = max_temp
                if self.load.imbalance <= 0:
                    self.limiting_quadrant = 1
                else:
                    self.limiting_quadrant = 2
                return max_temp
            min_temp, sized = self._size_based_on_temperature_profile(20)
            if sized:
                self.H = min_temp
                if self.load.imbalance <= 0:
                    self.limiting_quadrant = 4
                else:
                    self.limiting_quadrant = 3
                return min_temp
            raise UnsolvableDueToTemperatureGradient

    def size_L4(self, H_init: float = None, quadrant_sizing: int = 0) -> float:
        """
        This function sizes the borefield based on an hourly (L4) sizing methodology.

        Parameters
        ----------
        H_init : float
            Initial depth from where to start the iteration [m]
        quadrant_sizing : int
            If a quadrant is given the sizing is performed for this quadrant else for the relevant

        Returns
        -------
        H : float
            Required depth of the borefield [m]

        Raises
        ------
        ValueError
           ValueError when no ground data is provided or quadrant is not in range.
        UnsolvableDueToTemperatureGradient
           When the field cannot be sized due to the temperature gradient.
        """
        # check ground data
        if not self.ground_data.check_values():
            raise ValueError("Please provide ground data.")
        # check quadrants
        if not quadrant_sizing in range(0, 5):
            raise ValueError(f'Quadrant {quadrant_sizing} does not exist.')

        # check if hourly data is given
        if not self.load.hourly_resolution:
            raise ValueError("There is no hourly resolution available!")

        # initiate with a given depth
        self.H: float = H_init if H_init is not None else self._calculation_setup.H_init

        if quadrant_sizing != 0:
            # size according to a specific quadrant
            self.H, _ = self._size_based_on_temperature_profile(quadrant_sizing, hourly=True)
            return self.H
        else:
            try:
                max_temp, sized = self._size_based_on_temperature_profile(10, hourly=True, deep_sizing=self._calculation_setup.force_deep_sizing) if np.any(self.load.hourly_cooling_load) else (0, False)
            except MaximumNumberOfIterations as e:
                # no convergence with normal method, but perhaps with deep_sizing enabled
                if self._calculation_setup.deep_sizing and self.ground_data.variable_Tg:
                    max_temp, sized = self._size_based_on_temperature_profile(10, hourly=True, deep_sizing=True) if np.any(self.load.hourly_cooling_load) else (0, False)
                else:
                    raise e
            if sized:
                # already correct size
                self.H = max_temp
                if self.load.imbalance <= 0:
                    self.limiting_quadrant = 1
                else:
                    self.limiting_quadrant = 2
                return max_temp
            min_temp, sized = self._size_based_on_temperature_profile(20, hourly=True) if np.any(self.load.hourly_heating_load) else (0, False)
            if sized:
                if self.load.imbalance <= 0:
                    self.limiting_quadrant = 4
                else:
                    self.limiting_quadrant = 3
                self.H = min_temp
                return min_temp
            raise UnsolvableDueToTemperatureGradient

    def calculate_next_depth_deep_sizing(self, current_depth: float) -> float:
        """
        This method is a slower but more robust way of calculating the next depth in the sizing iteration when the
        borefield is sized for the maximum fluid temperature when there is a non-constant ground temperature.
        The method is based (as can be seen in its corresponding validation document) on the assumption that the
        difference between the maximum temperature in peak cooling and the average undisturbed ground temperature
        is irreversily proportional to the depth. In this way, given this difference in temperature and the current
        depth, a new depth can be calculated.

        Parameters
        ----------
        current_depth : float
            The current depth of the borefield [m]

        Returns
        -------
        float
            New depth of the borefield [m]
        """
        # diff between the max temperature in peak cooling and the avg undisturbed ground temperature at current_depth
        delta_temp = np.max(self.results.peak_cooling - self.ground_data.calculate_Tg(current_depth))

        # calculate the maximum temperature difference between the temperature limit and the ground temperature
        # at current_depth
        delta_wrt_max = self.Tf_max - self.ground_data.calculate_Tg(current_depth)

        # delta_t1/H1 ~ delta_t2/H2
        # H2 = delta_t2/delta_t1*current_depth
        rel_diff = delta_wrt_max/delta_temp
        new_depth = current_depth/rel_diff

        return new_depth

    def _size_based_on_temperature_profile(self, quadrant: int, hourly: bool = False, deep_sizing: bool = False) -> (float, bool):
        """
        This function sizes based on the temperature profile.
        It sizes for a specific quadrant and can both size with a monthly or an hourly resolution.

        Parameters
        ----------
        quadrant : int
            Differs from 0 when a sizing in a certain quadrant is desired.
            Quadrants are developed by (Peere et al., 2021) [#PeereBS]_, [#PeereThesis]_
        hourly : bool
            True if an hourly resolution should be used
        deep_sizing : bool
            True if the slower method should be used for the sizing, which is robuster.

        Returns
        -------
        Depth : float
            Required depth of the borefield [m]
        Sized : bool
            True if the required depth also satisfies the other temperature constraint [m]
        """
        # initiate iteration
        H_prev = 0

        if self.H < 1:
            self.H = 50

        # define loads for sizing
        # it only calculates the first and the last year, so the sizing is less computationally expensive
        # loads_short = self.load.hourly_cooling_load - self.load.hourly_heating_load if hourly else self.load.monthly_average_load
        # loads_short_rev = loads_short[::-1]
        # loads_long = np.tile(loads_short, 2)
        #
        # # initialise the results array
        # results = np.zeros(loads_short.size * 2)

        if deep_sizing:
            # set borefield to minimal depth
            self.H = 20

        # Iterates as long as there is no convergence
        # (convergence if difference between depth in iterations is smaller than THRESHOLD_BOREHOLE_DEPTH)
        i = 0
        while not self._check_convergence(self.H, H_prev, i):

            if hourly:
                # # calculate g-values
                # g_values = self.gfunction(self.load.time_L4, self.H)
                #
                # # calculation of needed differences of the g-function values. These are the weight factors
                # # in the calculation of Tb.
                # g_value_differences = np.diff(g_values, prepend=0)
                #
                # # convolution to get the monthly results
                # results[:8760] = convolve(loads_short * 1000, g_value_differences[:8760])[:8760]
                #
                # g_sum_n1 = g_value_differences[:8760 * (self.simulation_period - 1)].reshape(self.simulation_period - 1,
                #                                                                              8760).sum(axis=0)
                # g_sum = g_sum_n1 + g_value_differences[8760 * (self.simulation_period - 1):]
                # g_sum_n2 = np.concatenate((np.array([0]), g_sum_n1[::-1]))[:-1]
                #
                # results[8760:] = convolve(loads_short * 1000, g_sum)[:8760] + convolve(loads_short_rev * 1000,
                #                                                                        g_sum_n2)[:8760][::-1]
                #
                # # calculation the borehole wall temperature for every month i
                # Tb = results / (2 * pi * self.ground_data.k_s) / (self.H * self.number_of_boreholes) + self._Tg(self.H)
                #
                # self.Tb = Tb
                # # now the Tf will be calculated based on
                # # Tf = Tb + Q * R_b
                # temperature_result = Tb + loads_long * 1000 * (self.Rb / self.number_of_boreholes / self.H)
                # # reset other variables
                # self.results.peak_heating = temperature_result
                # self.results.peak_cooling = temperature_result
                self._calculate_temperature_profile(self.H, hourly=True)

            else:
                # # calculate g-values
                # g_values = self.gfunction(self.load.time_L3, self.H)
                #
                # # the g-function value of the peak with length_peak hours
                # g_value_peak_cooling = self.gfunction(self.load.peak_cooling_duration, self.H)[0]
                # if self.load.peak_cooling_duration == self.load.peak_heating_duration:
                #     g_value_peak_heating = g_value_peak_cooling
                # else:
                #     g_value_peak_heating = self.gfunction(self.load.peak_heating_duration, self.H)[0]
                #
                # # calculation of needed differences of the g-function values. These are the weight factors in
                # # the calculation of Tb.
                # g_value_differences = np.diff(g_values, prepend=0)
                #
                # # convolution to get the monthly results
                # results[:12] = convolve(loads_short * 1000, g_value_differences[:12])[:12]
                #
                # g_sum_n1 = g_value_differences[:12 * (self.load.simulation_period - 1)]\
                #     .reshape(self.load.simulation_period - 1, 12).sum(axis=0)
                # g_sum = g_sum_n1 + g_value_differences[12 * (self.load.simulation_period - 1):]
                # g_sum_n2 = np.concatenate((np.array([0]), g_sum_n1[::-1]))[:-1]
                #
                # results[12:] = convolve(loads_short * 1000, g_sum)[:12]\
                #                + convolve(loads_short_rev * 1000, g_sum_n2)[:12][::-1]
                #
                # # calculation the borehole wall temperature for every month i
                # Tb = results / (2 * pi * self.ground_data.k_s) / (self.H * self.number_of_boreholes) + self._Tg(self.H)
                #
                # self.Tb = Tb
                # # now the Tf will be calculated based on
                # # Tf = Tb + Q * R_b
                # results_month_cooling = Tb + np.tile(self.load.baseload_cooling_power, 2) * 1000 \
                #                         * (self.Rb / self.number_of_boreholes / self.H)
                # results_month_heating = Tb - np.tile(self.load.baseload_heating_power, 2) * 1000 \
                #                         * (self.Rb / self.number_of_boreholes / self.H)
                #
                # # extra summation if the g-function value for the peak is included
                # results_peak_cooling = results_month_cooling +\
                #                        np.tile(self.load.peak_cooling - self.load.baseload_cooling_power, 2) * 1000 *\
                #                        (g_value_peak_cooling / self.ground_data.k_s / 2 / pi + self.Rb) / self.number_of_boreholes / self.H
                # results_peak_heating = results_month_heating - np.tile(self.load.peak_heating - self.load.baseload_heating_power, 2) * 1000 \
                #                        * (g_value_peak_heating / self.ground_data.k_s / 2 / pi + self.Rb)\
                #                        / self.number_of_boreholes / self.H
                #
                # # save temperatures under variable
                # self.results.peak_heating = results_peak_heating
                # self.results.peak_cooling = results_peak_cooling
                self._calculate_temperature_profile(self.H, hourly=False)
            H_prev = self.H
            if not deep_sizing:
                if quadrant == 1:
                    # maximum temperature
                    # convert back to required length
                    self.H = (np.max(self.results.peak_cooling[:8760 if hourly else 12]) - self._Tg()) / (self.Tf_max - self._Tg()) * H_prev
                elif quadrant == 2:
                    # maximum temperature
                    # convert back to required length
                    self.H = (np.max(self.results.peak_cooling[-8760 if hourly else -12:]) - self._Tg()) / (self.Tf_max - self._Tg()) * H_prev
                elif quadrant == 3:
                    # minimum temperature
                    # convert back to required length
                    self.H = (np.min(self.results.peak_heating[:8760 if hourly else 12]) - self._Tg()) / (self.Tf_min - self._Tg()) * H_prev
                elif quadrant == 4:
                    # minimum temperature
                    # convert back to required length
                    self.H = (np.min(self.results.peak_heating[-8760 if hourly else -12:]) - self._Tg()) / (self.Tf_min - self._Tg()) * H_prev
                elif quadrant == 10:
                    # over all years
                    # maximum temperature
                    # convert back to required length
                    self.H = (np.max(self.results.peak_cooling) - self._Tg()) / (self.Tf_max - self._Tg()) * H_prev
                elif quadrant == 20:
                    # over all years
                    # minimum temperature
                    # convert back to required length
                    self.H = (np.min(self.results.peak_heating) - self._Tg()) / (self.Tf_min - self._Tg()) * H_prev
            elif self.ground_data.variable_Tg:
                # for when the temperature gradient is active and it is cooling
                self.H = self.calculate_next_depth_deep_sizing(H_prev)
            if self.H < 0:
                return 0, False

            i += 1

        return self.H, (np.max(self.results.peak_cooling) <= self.Tf_max + 0.05 or
                        (quadrant == 10 or quadrant == 1 or quadrant == 2))\
                       and (np.min(self.results.peak_heating) >= self.Tf_min - 0.05 or
                            (quadrant == 20 or quadrant == 3 or quadrant == 4))

    def set_baseload_heating(self, baseload: np.ndarray | list) -> None:
        """
        This function defines the baseload in heating both in an energy as in an average power perspective.

        Parameters
        ----------
        baseload : np.ndarray, list
            Baseload heating per month [kWh]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            ValueError when the baseload is no list or np.ndarray
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.baseload_heating = baseload
        self._delete_calculated_temperatures()

    def set_baseload_cooling(self, baseload: np.array | list) -> None:
        """
        This function defines the baseload in cooling both in an energy as in an average power perspective.

        Parameters
        ----------
        baseload : np.ndarray, list
            Baseload cooling per month [kWh]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            ValueError when the baseload is no list or np.ndarray
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.baseload_cooling = baseload
        self._delete_calculated_temperatures()

    def set_peak_heating(self, peak_load: np.ndarray | list) -> None:
        """
        This function sets the peak heating to peak load heating.

        Parameters
        ----------
        peak_load : np.ndarray, list
            Peak load of heating per month [kW]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            ValueError when the peak_load is no list or np.ndarray
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.peak_heating = peak_load
        self._delete_calculated_temperatures()

    def set_peak_cooling(self, peak_load: np.ndarray | list) -> None:
        """
        This function sets the peak cooling to peak load cooling.

        Parameters
        ----------
        peak_load : np.ndarray, list
            Peak load of cooling per month [kW]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            ValueError when the peak_load is no list or np.ndarray
        """
        warn("This function will be depreciated in v2.2.1", DeprecationWarning, stacklevel=2)
        self._borefield_load.peak_cooling = peak_load
        self._delete_calculated_temperatures()

    @property
    def investment_cost(self) -> float:
        """
        This function calculates the investment cost based on a cost profile linear to the total borehole length.

        Returns
        -------
        float
            Investment cost
        """
        return np.polyval(self.cost_investment, self.H * self.number_of_boreholes)

    def calculate_temperatures(self, depth: float = None, hourly: bool = False) -> None:
        """
        Calculate all the temperatures without plotting the figure. When depth is given, it calculates it for a given
        depth.

        Parameters
        ----------
        depth : float
            Depth for which the temperature profile should be calculated for [m]
        hourly : bool
            True when the temperatures should be calculated based on hourly data

        Returns
        -------
        None
        """
        self._calculate_temperature_profile(H=depth, hourly=hourly)

    def print_temperature_profile(self, legend: bool = True, plot_hourly: bool = False) -> None:
        """
        This function plots the temperature profile for the calculated depth.
        It uses the available temperature profile data.

        Parameters
        ----------
        legend : bool
            True if the legend should be printed
        plot_hourly : bool
            True if the temperature profile printed should be based on the hourly load profile.

        Returns
        -------
        fig, ax
            If the borefield object is part of the GUI, it returns the figure object
        """
        # calculate temperature profile
        self._calculate_temperature_profile(hourly=plot_hourly)

        return self._plot_temperature_profile(legend=legend, plot_hourly=plot_hourly)

    def print_temperature_profile_fixed_depth(self, depth: float, legend: bool = True, plot_hourly: bool = False):
        """
        This function plots the temperature profile for a fixed depth.
        It uses the already calculated temperature profile data, if available.

        Parameters
        ----------
        depth : float
            Depth at which the temperature profile should be shown
        legend : bool
            True if the legend should be printed
        plot_hourly : bool
            True if the temperature profile printed should be based on the hourly load profile.

        Returns
        -------
        fig, ax
            If the borefield object is part of the GUI, it returns the figure object
        """
        # calculate temperature profile
        self._calculate_temperature_profile(H=depth, hourly=plot_hourly)

        return self._plot_temperature_profile(legend=legend, plot_hourly=plot_hourly)

    def _plot_temperature_profile(self, legend: bool = True, plot_hourly: bool = False) -> Tuple[plt.Figure, plt.Axes]:
        """
        This function plots the temperature profile.
        If the Borefield object exists as part of the GUI, than the figure is returned,
        otherwise it is shown.

        Parameters
        ----------
        legend : bool
            True if the legend should be printed
        plot_hourly : bool
            True if the temperature profile printed should be based on the hourly load profile.

        Returns
        -------
        fig, ax
            If the borefield object is part of the GUI, it returns the figure object
        """

        # make a time array
        if plot_hourly:
            time_array = self.load.time_L4 / 12 / 3600 / 730
        else:
            time_array = self.load.time_L3 / 12 / 730. / 3600.

        # plt.rc('figure')
        # create new figure and axes if it not already exits otherwise clear it.
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # set axes labelsv
        ax.set_xlabel(r'Time (year)')
        ax.set_ylabel(r'Temperature ($^\circ C$)')
        ax.yaxis.label.set_color(plt.rcParams["axes.labelcolor"])
        ax.xaxis.label.set_color(plt.rcParams["axes.labelcolor"])

        # plot Temperatures
        ax.step(time_array, self.results.Tb, 'k-', where="post", lw=1.5, label="Tb")

        if plot_hourly:
            ax.step(time_array, self.results.peak_cooling, 'b-', where="post", lw=1, label='Tf')
        else:
            ax.step(time_array, self.results.peak_cooling, 'b-', where="post", lw=1.5, label='Tf peak cooling')
            ax.step(time_array, self.results.peak_heating, 'r-', where="post", lw=1.5, label='Tf peak heating')

            ax.step(time_array, self.results.monthly_cooling, color='b', linestyle="dashed", where="post", lw=1.5,
                    label='Tf base cooling')
            ax.step(time_array, self.results.monthly_heating, color='r', linestyle="dashed", where="post", lw=1.5,
                    label='Tf base heating')

        # define temperature bounds
        ax.hlines(self.Tf_min, 0, self.simulation_period, colors='r', linestyles='dashed', label='', lw=1)
        ax.hlines(self.Tf_max, 0, self.simulation_period, colors='b', linestyles='dashed', label='', lw=1)
        ax.set_xticks(range(0, self.simulation_period + 1, 2))

        # Plot legend
        if legend:
            ax.legend()
        ax.set_xlim(left=0, right=self.simulation_period)
        # show figure if not in gui mode
        if not self.gui:
            plt.show()
        return fig, ax

    def _delete_calculated_temperatures(self) -> None:
        """
        This function deletes all the calculated temperatures.

        Returns
        -------
        None
        """
        self.results = Results()
        self._building_load = HourlyGeothermalLoad()
        self._secundary_borefield_load = HourlyGeothermalLoad()
        ghe_logger.info("Deleted all stored temperatures from previous calculations.")

    def _calculate_temperature_profile(self, H: float = None, hourly: bool = False) -> None:
        """
        This function calculates the evolution in the fluid temperature and borehole wall temperature.

        Parameters
        ----------
        H : float
            Depth at which the temperatures should be evaluated [m]. If None, than the current depth is taken.
        hourly : bool
            True if the temperature evolution should be calculated on an hourly basis.

        Returns
        -------
        None
        """

        # set Rb* value
        Rb = self.borehole.get_Rb(H if H is not None else self.H, self.D, self.r_b, self.ground_data.k_s)
        H = H if H is not None else self.H

        if not hourly:
            # self.g-function is a function that uses the precalculated data to interpolate the correct values of the
            # g-function. This dataset is checked over and over again and is correct
            g_values = self.gfunction(self.load.time_L3, H)

            # the g-function value of the peak with length_peak hours
            g_value_peak_cooling = self.gfunction(self.load.peak_cooling_duration, H)[0]
            if self.load.peak_cooling_duration == self.load.peak_heating_duration:
                g_value_peak_heating = g_value_peak_cooling
            else:
                g_value_peak_heating = self.gfunction(self.load.peak_heating_duration, H)[0]

            # calculation of needed differences of the g-function values. These are the weight factors in the calculation
            # of Tb.
            g_value_differences = np.diff(g_values, prepend=0)

            # convolution to get the monthly results
            results = convolve(self.load.monthly_average_load_simulation_period * 1000,
                               g_value_differences)[:12 * self.simulation_period]

            # calculation the borehole wall temperature for every month i
            Tb = results / (2 * pi * self.ground_data.k_s) / (H * self.number_of_boreholes) + self._Tg(H)

            # now the Tf will be calculated based on
            # Tf = Tb + Q * R_b
            results_month_cooling = Tb + self.load.baseload_cooling_power_simulation_period * 1000 \
                                    * (Rb / self.number_of_boreholes / H)
            results_month_heating = Tb - self.load.baseload_heating_power_simulation_period * 1000 \
                                    * (Rb / self.number_of_boreholes / H)

            # extra summation if the g-function value for the peak is included
            results_peak_cooling = results_month_cooling + (
                    self.load.peak_cooling_simulation_period - self.load.baseload_cooling_power_simulation_period) * 1000 \
                                   * (
                                           g_value_peak_cooling / self.ground_data.k_s / 2 / pi + Rb) / self.number_of_boreholes / H
            results_peak_heating = results_month_heating - (
                    self.load.peak_heating_simulation_period - self.load.baseload_heating_power_simulation_period) * 1000 \
                                   * (
                                           g_value_peak_heating / self.ground_data.k_s / 2 / pi + Rb) / self.number_of_boreholes / H

            # save temperatures under variable
            self.results = Results(borehole_wall_temp=Tb,
                                   peak_heating=results_peak_heating,
                                   peak_cooling=results_peak_cooling,
                                   monthly_heating=results_month_heating,
                                   monthly_cooling=results_month_cooling)

        if hourly:
            # check for hourly data if this is requested
            if not self.load.hourly_resolution:
                raise ValueError("There is no hourly resolution available!")

            hourly_load = self.load.hourly_load_simulation_period

            # self.g-function is a function that uses the precalculated data to interpolate the correct values of the
            # g-function. This dataset is checked over and over again and is correct
            g_values = self.gfunction(self.load.time_L4, H)

            # calculation of needed differences of the g-function values. These are the weight factors in the calculation
            # of Tb.
            g_value_differences = np.diff(g_values, prepend=0)

            # convolution to get the monthly results
            results = convolve(hourly_load * 1000, g_value_differences)[:len(hourly_load)]

            # calculation the borehole wall temperature for every month i
            Tb = results / (2 * pi * self.ground_data.k_s) / (H * self.number_of_boreholes) + self._Tg(H)

            # now the Tf will be calculated based on
            # Tf = Tb + Q * R_b
            temperature_result = Tb + hourly_load * 1000 * (Rb / self.number_of_boreholes / H)

            # reset other variables
            self.results = Results(borehole_wall_temp=Tb,
                                   peak_heating=temperature_result,
                                   peak_cooling=temperature_result)

    def set_options_gfunction_calculation(self, options: dict) -> None:
        """
        This function sets the options for the gfunction calculation of pygfunction.
        This dictionary is directly passed through to the gFunction class of pygfunction.
        For more information, please visit the documentation of pygfunction.

        Parameters
        ----------
        options : dict
            Dictionary with options for the gFunction class of pygfunction

        Returns
        -------
        None
        """
        self.gfunction_calculation_object.set_options_gfunction_calculation(options)

    def gfunction(self, time_value: list | float | np.ndarray, H: float = None) -> np.ndarray:
        """
        This function returns the gfunction value.
        It can do so by either calculating the gfunctions just-in-time or by interpolating from a
        loaded custom data file.

        Parameters
        ----------
        time_value : list, float, np.ndarray
            Time value(s) in seconds at which the gfunctions should be calculated
        H : float
            Depth [m] at which the gfunctions should be calculated.
            If no depth is given, the current depth is taken.

        Returns
        -------
        gvalue : np.ndarray
            1D array with the g-values for all the requested time_value(s)
        """
        if H is None:
            H = self.H
        # when using a variable ground temperature, sometimes no solution can be found
        if not isinstance(self.ground_data, GroundConstantTemperature) and H > Borefield.THRESHOLD_DEPTH_ERROR:
            raise UnsolvableDueToTemperatureGradient

        def jit_gfunction_calculation() -> np.ndarray:
            """
            This function calculates the gfunction just-in-time.

            Returns
            -------
            gvalues : np.ndarray
                1D array with the g-values for the requested time intervals
            """
            # set the correct depth of the borefield
            self._update_borefield_depth(H=H)
            return self.gfunction_calculation_object.calculate(time_value, self.borefield.li_boreholes, self.ground_data.alpha,
                                                               interpolate=self._calculation_setup.interpolate_gfunctions)


        ## 1 bypass any possible precalculated g-functions
        # if calculate is False, then the gfunctions are calculated jit
        if not self._calculation_setup.use_precalculated_dataset:
            return jit_gfunction_calculation()

        ## 2 use precalculated g-functions when available
        if self.custom_gfunction is not None:
            # there is precalculated data available
            # check if the requested values can be calculated using the custom_gfunction
            if self.custom_gfunction.within_range(time_value, H):
                return self.custom_gfunction.calculate_gfunction(time_value, H)

        ## 3 calculate g-function jit
        return jit_gfunction_calculation()

    def create_custom_dataset(self, time_array: list | np.ndarray = None,
                              depth_array: list | np.ndarray = None,
                              options: dict = {}) -> None:
        """
        This function makes a datafile for a given custom borefield and sets it for the borefield object.
        It automatically sets this datafile in the current borefield object so it can be used as a source for
        the interpolation of g-values.

        Parameters
        ----------
        time_array : list, np.array
            Time values (in seconds) used for the calculation of the datafile
        depth_array : list, np.array
            List or arrays of depths for which the datafile should be created
        options : dict
            Options for the g-function calculation (check pygfunction.gfunction.gFunction() for more information)

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When no borefield or ground data is set
        """

        try:
            self.borefield.li_boreholes[0]
        except TypeError:
            raise ValueError("No borefield is set for which the gfunctions should be calculated")
        try:
            self.ground_data.alpha
        except AttributeError:
            raise ValueError("No ground data is set for which the gfunctions should be calculated")

        self.custom_gfunction = CustomGFunction(time_array, depth_array, options)
        self.custom_gfunction.create_custom_dataset(self.borefield.li_boreholes, self.ground_data.alpha)

    @property
    def Re(self) -> float:
        """
        Reynolds number.

        Returns
        -------
        float
            Reynolds number
        """
        return self.borehole.Re

    def optimise_load_profile(self, building_load: HourlyGeothermalLoad, depth: float = None, SCOP: float = 10 ** 6,
                              SEER: float = 10 ** 6, print_results: bool = False, temperature_threshold: float = 0.05) -> None:
        """
        This function optimises the load based on the given borefield and the given hourly load.
        (When the load is not geothermal, the SCOP and SEER are used to convert it to a geothermal load.)
        It does so based on a load-duration curve. The temperatures of the borefield are calculated on a monthly
        basis, even though we have hourly data, for an hourly calculation of the temperatures
        would take a very long time.

        Parameters
        ----------
        building_load : _LoadData
            Load data used for the optimisation
        depth : float
            Depth of the boreholes in the borefield [m]
        SCOP : float
            SCOP of the geothermal system (needed to convert hourly building load to geothermal load)
        SEER : float
            SEER of the geothermal system (needed to convert hourly building load to geothermal load)
        print_results : bool
            True when the results of this optimisation are to be printed in the terminal
        temperature_threshold : float
            The maximum allowed temperature difference between the maximum and minimum fluid temperatures and their
            respective limits. The lower this threshold, the longer the convergence will take.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            ValueError if no hourly load is given or the threshold is negative
        """

        ## Explain variables
        # load --> primary, geothermal load
        # _building_load --> secundary, building load
        # _secundary_borefield_load --> secundary, geothermal load

        # check if hourly load is given
        if not building_load.hourly_resolution:
            raise ValueError("No hourly load was given!")

        # check if threshold is positive
        if temperature_threshold < 0:
            raise ValueError(f'The temperature threshold is {temperature_threshold}, but it cannot be below 0!')

        # set depth
        if depth is None:
            depth = self.H

        # since the depth does not change, the Rb* value is constant
        # set to use a constant Rb* value but save the initial parameters
        Rb_backup = self.borehole.Rb
        use_constant_Rb_backup = self.borehole.use_constant_Rb
        self.Rb = self.borehole.get_Rb(depth, self.D, self.r_b, self.ground_data.k_s)

        # load hourly heating and cooling load and convert it to geothermal loads
        primary_geothermal_load = HourlyGeothermalLoad(simulation_period=building_load.simulation_period)
        primary_geothermal_load.set_hourly_cooling(building_load.hourly_cooling_load.copy() * (1 + 1 / SEER))
        primary_geothermal_load.set_hourly_heating(building_load.hourly_heating_load.copy() * (1 - 1 / SCOP))

        # set geothermal load
        self.load = copy.deepcopy(primary_geothermal_load)

        # set initial peak loads
        init_peak_heating: float = self.load.max_peak_heating
        init_peak_cooling: float = self.load.max_peak_cooling

        # peak loads for iteration
        peak_heat_load_geo: float = init_peak_heating
        peak_cool_load_geo: float = init_peak_cooling

        # set iteration criteria
        cool_ok, heat_ok = False, False

        while not cool_ok or not heat_ok:
            # limit the primary geothermal heating and cooling load to peak_heat_load_geo and peak_cool_load_geo
            self.load.set_hourly_cooling(np.minimum(peak_cool_load_geo, primary_geothermal_load.hourly_cooling_load))
            self.load.set_hourly_heating(np.minimum(peak_heat_load_geo, primary_geothermal_load.hourly_heating_load))

            # calculate temperature profile, just for the results
            self.calculate_temperatures(depth=depth)

            # deviation from minimum temperature
            if abs(min(self.results.peak_heating) - self.Tf_min) > temperature_threshold:

                # check if it goes below the threshold
                if min(self.results.peak_heating) < self.Tf_min:
                    peak_heat_load_geo = max(0.1,
                                             peak_heat_load_geo - 1 * max(1, 10 * (self.Tf_min - min(self.results.peak_heating))))
                else:
                    peak_heat_load_geo = min(init_peak_heating, peak_heat_load_geo * 1.01)
                    if peak_heat_load_geo == init_peak_heating:
                        heat_ok = True
            else:
                heat_ok = True

            # deviation from maximum temperature
            if abs(np.max(self.results.peak_cooling) - self.Tf_max) > temperature_threshold:

                # check if it goes above the threshold
                if np.max(self.results.peak_cooling) > self.Tf_max:
                    peak_cool_load_geo = max(0.1,
                                             peak_cool_load_geo - 1 * max(1, 10 * (-self.Tf_max + np.max(self.results.peak_cooling))))
                else:
                    peak_cool_load_geo = min(init_peak_cooling, peak_cool_load_geo * 1.01)
                    if peak_cool_load_geo == init_peak_cooling:
                        cool_ok = True
            else:
                cool_ok = True

        # calculate the resulting secundary hourly profile that can be put on the borefield
        self._secundary_borefield_load = HourlyGeothermalLoad(simulation_period=building_load.simulation_period)
        self._secundary_borefield_load.set_hourly_cooling(self.load.hourly_cooling_load / (1 + 1 / SEER))
        self._secundary_borefield_load.set_hourly_heating(self.load.hourly_heating_load / (1 - 1 / SCOP))

        # set building load
        self._building_load = building_load

        # calculate external load
        self._external_load = HourlyGeothermalLoad(simulation_period=building_load.simulation_period)
        self._external_load.set_hourly_heating(np.maximum(0, building_load.hourly_heating_load -
                                                          self._secundary_borefield_load.hourly_heating_load))
        self._external_load.set_hourly_cooling(np.maximum(0, building_load.hourly_cooling_load -
                                                          self._secundary_borefield_load.hourly_cooling_load))

        # restore the initial parameters
        self.Rb = Rb_backup
        self.borehole.use_constant_Rb = use_constant_Rb_backup

        if print_results:
            # print results
            print("The peak load heating is: ", f'{self._secundary_borefield_load.max_peak_heating:.0f}',
                  "kW, leading to",
                  f'{np.sum(self._secundary_borefield_load.hourly_heating_load):.0f}', "kWh of heating.")
            print("This is", f'{self._percentage_heating:.0f}',
                  "% of the total heating load.")
            print("Another", f'{np.sum(self._external_load.hourly_heating_load):.0f}',
                  "kWh of heating should come from another source, with a peak of",
                  f'{self._external_load.max_peak_heating:.0f}', "kW.")
            print("------------------------------------------")
            print("The peak load cooling is: ", f'{self._secundary_borefield_load.max_peak_cooling:.0f}',
                  "kW, leading to",
                  f'{np.sum(self._secundary_borefield_load.hourly_cooling_load):.0f}', "kWh of cooling.")
            print("This is", f'{self._percentage_cooling:.0f}',
                  "% of the total cooling load.")
            print("Another", f'{np.sum(self._external_load.hourly_cooling_load):.0f}',
                  "kWh of cooling should come from another source, with a peak of",
                  f'{self._external_load.max_peak_cooling:.0f}', "kW.")

            # plot results
            self.print_temperature_profile_fixed_depth(depth=depth)

    @property
    def _percentage_heating(self) -> float:
        """
        This function returns the percentage of heating load that can be done geothermally.

        Returns
        -------
        float
            Percentage of heating load that can be done geothermally.
        """
        return np.sum(self._secundary_borefield_load.hourly_heating_load) / \
            np.sum(self._building_load.hourly_heating_load) * 100

    @property
    def _percentage_cooling(self) -> float:
        """
        This function returns the percentage of cooling load that can be done geothermally.

        Returns
        -------
        float
            Percentage of cooling load that can be done geothermally.
        """
        return np.sum(self._secundary_borefield_load.hourly_cooling_load) / \
            np.sum(self._building_load.hourly_cooling_load) * 100

    def calculate_quadrant(self) -> int:
        """
        This function returns the borefield quadrant (as defined by Peere et al., 2021 [#PeereEtAl]_)
        based on the calculated temperature profile.
        If there is no limiting quadrant, None is returned.\n
        Quadrant 1 is limited in the first year by the maximum temperature\n
        Quadrant 2 is limited in the last year by the maximum temperature\n
        Quadrant 3 is limited in the first year by the minimum temperature\n
        Quadrant 4 is limited in the last year by the maximum temperature

        Returns
        ----------
        quadrant : int
            The quadrant which limits the borefield

        References
        ----------
        .. [#PeereEtAl] Peere, W., Picard, D., Cupeiro Figueroa, I., Boydens, W., and Helsen, L. (2021) Validated combined first and last year borefield sizing methodology. In Proceedings of International Building Simulation Conference 2021. Brugge (Belgium), 1-3 September 2021. https://doi.org/10.26868/25222708.2021.30180
        """

        # calculate temperatures if they are not calculated
        if not np.any(self.results.peak_heating):
            ghe_logger.warning('There are not yet temperatures calculated, hence there is no limiting quadrant.'
                               'The temperature is calculated now, based on monthly values.')
            self.calculate_temperatures()

        # calculate max/min fluid temperatures
        max_temp = np.max(self.results.peak_cooling)
        min_temp = np.min(self.results.peak_heating)

        # calculate temperature difference w.r.t. the limits
        DT_max = - self.Tf_max + max_temp + 1000  # + 1000 to have no problems with negative temperatures
        DT_min = self.Tf_min - min_temp + 1000

        # if the temperature limit is not crossed, return None
        if self.Tf_max - 0.1 > max_temp and self.Tf_min + 0.1 < min_temp:
            return

        # True if heating/extraction dominated
        if self.load.imbalance < 0:
            # either quadrant 1 or 4
            if DT_min > DT_max:
                # limited by minimum temperature
                return 4
            return 1

        # quadrant 2 or 3
        if DT_min > DT_max:
            # limited by minimum temperature
            return 3
        return 2

    def plot_load_duration(self, legend: bool = False) -> Tuple[plt.Figure, plt.Axes]:
        """
        This function makes a load-duration curve from the hourly values.

        Parameters
        ----------
        legend : bool
            True if the figure should have a legend

        Returns
        ----------
        Tuple
            plt.Figure, plt.Axes
        """
        # check if there are hourly values
        if not self.load.hourly_resolution:
            raise ValueError("There is no hourly resolution available!")

        # sort heating and cooling load
        heating = self.load.hourly_heating_load.copy()
        heating[::-1].sort()

        cooling = self.load.hourly_cooling_load.copy()
        cooling.sort()
        cooling = cooling * (-1)
        # create new figure and axes if it not already exits otherwise clear it.
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # add sorted loads to plot
        ax.step(np.arange(0, 8760, 1), heating, 'r-', label="Heating")
        ax.step(np.arange(0, 8760, 1), cooling, 'b-', label="Cooling")
        # create 0 line
        ax.hlines(0, 0, 8759, color="black")
        # add labels
        ax.set_xlabel("Time [hours]")
        ax.set_ylabel("Power [kW]")
        # set x limits to 8760
        ax.set_xlim(0, 8760)
        # plot legend if wanted
        if legend:
            ax.legend()  #
        # show plt if not in gui
        if not self.gui:
            plt.show()
        return fig, ax

    def _plot_load_duration(self, legend: bool = False) -> Tuple[plt.Figure, plt.Axes]:
        """
        This function makes a load-duration curve from the hourly values.

        Parameters
        ----------
        legend : bool
            True if the figure should have a legend

        Returns
        ----------
        Tuple
            plt.Figure, plt.Axes
        """

        load = self._secundary_borefield_load if self._secundary_borefield_load != HourlyGeothermalLoad() else self.load

        # sort heating and cooling load
        heating = load.hourly_heating_load.copy()
        heating[::-1].sort()

        cooling = load.hourly_cooling_load.copy()
        cooling.sort()
        cooling = cooling * (-1)
        # create new figure and axes if it not already exits otherwise clear it.
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # add sorted loads to plot
        ax.step(np.arange(0, 8760, 1), heating, 'r-', label="Heating")
        ax.step(np.arange(0, 8760, 1), cooling, 'b-', label="Cooling")
        # create 0 line
        ax.hlines(0, 0, 8759, color="black")
        # add labels
        ax.set_xlabel("Time [hours]")
        ax.set_ylabel("Power [kW]")
        # set x limits to 8760
        ax.set_xlim(0, 8760)
        # plot legend if wanted
        if legend:
            ax.legend()  # pragma: no cover
        # show plt if not in gui
        if not self.gui:
            plt.show()  # pragma: no cover
        return fig, ax
