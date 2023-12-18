import abc
from abc import ABC
from typing import Union

import numpy as np

from GHEtool.VariableClasses.BaseClass import BaseClass


class _LoadData(BaseClass, ABC):
    """
    This class contains information w.r.t. load data for the borefield sizing.
    """
    __slots__ = 'hourly_resolution', 'simulation_period', '_peak_heating_duration', '_peak_cooling_duration', 'tm',\
                '_all_months_equal', '_dhw_yearly'

    AVG_UPM: float = 730.  # number of hours per month
    DEFAULT_LENGTH_PEAK: int = 6  # hours
    DEFAULT_SIMULATION_PERIOD: int = 20  # years

    def __init__(self, hourly_resolution: bool, simulation_period: int = DEFAULT_SIMULATION_PERIOD):
        """

        Parameters
        ----------
        hourly_resolution : bool
            True if the load class uses an hourly resolution
        simulation_period : int
            Length of the simulation period in years
        """
        self.hourly_resolution: bool = hourly_resolution
        self.simulation_period: int = simulation_period
        self._peak_cooling_duration: int = _LoadData.DEFAULT_LENGTH_PEAK
        self._peak_heating_duration: int = _LoadData.DEFAULT_LENGTH_PEAK
        self.tm: int = _LoadData.AVG_UPM * 3600  # time in a month in seconds
        self._all_months_equal: bool = True  # true if it is assumed that all months are of the same length
        self._dhw_yearly: float = 0.

    @property
    def all_months_equal(self) -> bool:
        """
        Returns the attribute all months are equal

        Returns
        -------
        bool
            True if the months are assumed to be of equal length (i.e. 730 hours/month).
            False if the correct number of hours is used.
        """
        return self._all_months_equal

    @all_months_equal.setter
    def all_months_equal(self, bool: bool) -> None:
        """
        Sets the all_months_equal attribute.

        Parameters
        ----------
        bool : bool
            True if the months are assumed to be of equal length (i.e. 730 hours/month).
            False if the correct number of hours is used.

        Returns
        -------
        None
        """
        self._all_months_equal = bool

    @property
    def UPM(self) -> np.ndarray:
        """
        Depending on whether all months are assumed to have equal length, the UPM are either constant
        or vary during the year.

        Returns
        -------
        Hours per month : np.ndarray
        """
        if self.all_months_equal:
            # every month has equal length
            return np.ones(12) * _LoadData.AVG_UPM
        else:
            return np.array([744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744])

    @abc.abstractmethod
    def _check_input(self, input: Union[np.ndarray, list, tuple]) -> bool:
        """
        This function checks whether the input is valid or not.

        Parameters
        ----------
        input : np.ndarray, list, tuple
            Thermal load input

        Returns
        -------
        bool
            True if the input is correct for the load class
        """

    @abc.abstractmethod
    def peak_heating(self) -> np.ndarray:
        """
        This function returns the peak heating load in kW/month.

        Returns
        -------
        peak heating : np.ndarray
        """

    @abc.abstractmethod
    def peak_cooling(self) -> np.ndarray:
        """
        This function returns the peak cooling load in kW/month.

        Returns
        -------
        peak cooling : np.ndarray
        """

    @abc.abstractmethod
    def baseload_heating(self) -> np.ndarray:
        """
        This function returns the baseload heating in kWh/month.

        Returns
        -------
        baseload heating : np.ndarray
        """

    @property
    def baseload_heating_power(self) -> np.ndarray:
        """
        This function returns the baseload heating in kW avg/month.

        Returns
        -------
        baseload heating : np.ndarray
        """
        return np.divide(self.baseload_heating, self.UPM)

    @abc.abstractmethod
    def baseload_cooling(self) -> np.ndarray:
        """
        This function returns the baseload cooling in kWh/month.

        Returns
        -------
        baseload cooling : np.ndarray
        """

    @property
    def baseload_cooling_power(self) -> np.ndarray:
        """
        This function returns the baseload cooling in kW avg/month.

        Returns
        -------
        baseload cooling : np.ndarray
        """
        return np.divide(self.baseload_cooling, self.UPM)

    @property
    def yearly_heating_load(self) -> float:
        """
        This function returns the yearly heating load in kWh/year.

        Returns
        -------
        float
            Yearly heating load kWh/year
        """
        return np.sum(self.baseload_heating)

    @property
    def yearly_cooling_load(self) -> float:
        """
        This function returns the yearly cooling load in kWh/year.

        Returns
        -------
        float
            Yearly cooling load kWh/year
        """
        return np.sum(self.baseload_cooling)

    @property
    def baseload_heating_simulation_period(self) -> np.ndarray:
        """
        This function returns the baseload heating in kWh/month for a whole simulation period.

        Returns
        -------
        baseload heating : np.ndarray
            baseload heating for the whole simulation period
        """
        return np.tile(self.baseload_heating, self.simulation_period)

    @property
    def baseload_cooling_simulation_period(self) -> np.ndarray:
        """
        This function returns the baseload cooling in kWh/month for a whole simulation period.

        Returns
        -------
        baseload cooling : np.ndarray
            baseload cooling for the whole simulation period
        """
        return np.tile(self.baseload_cooling, self.simulation_period)

    @property
    def peak_heating_simulation_period(self) -> np.ndarray:
        """
        This function returns the peak heating in kW/month for a whole simulation period.

        Returns
        -------
        peak heating : np.ndarray
            peak heating for the whole simulation period
        """
        return np.tile(self.peak_heating, self.simulation_period)

    @property
    def peak_cooling_simulation_period(self) -> np.ndarray:
        """
        This function returns the peak cooling in kW/month for a whole simulation period.

        Returns
        -------
        peak cooling : np.ndarray
            peak cooling for the whole simulation period
        """
        return np.tile(self.peak_cooling, self.simulation_period)

    @property
    def baseload_heating_power_simulation_period(self) -> np.ndarray:
        """
        This function returns the avergae heating power in kW avg/month for a whole simulation period.

        Returns
        -------
        average heating power : np.ndarray
            average heating power for the whole simulation period
        """
        return np.tile(self.baseload_heating_power, self.simulation_period)

    @property
    def baseload_cooling_power_simulation_period(self) -> np.ndarray:
        """
        This function returns the average cooling power in kW avg/month for a whole simulation period.

        Returns
        -------
        average cooling power : np.ndarray
            average cooling for the whole simulation period
        """
        return np.tile(self.baseload_cooling_power, self.simulation_period)

    @property
    def imbalance(self) -> float:
        """
        This function calculates the ground imbalance.
        A positive imbalance means that the field is injection dominated, i.e. it heats up every year.

        Returns
        -------
        imbalance : float
        """
        return self.yearly_cooling_load - self.yearly_heating_load

    @property
    def monthly_average_load(self) -> np.ndarray:
        """
        This function calculates the average monthly load in kW.

        Returns
        -------
        monthly average load : np.ndarray
        """
        return self.baseload_cooling_power - self.baseload_heating_power

    @property
    def monthly_average_load_simulation_period(self) -> np.ndarray:
        """
        This function calculates the average monthly load in kW for the whole simulation period.

        Returns
        -------
        monthly average load : np.ndarray
        """
        return np.tile(self.monthly_average_load, self.simulation_period)

    @property
    def peak_heating_duration(self) -> float:
        """
        Length of the peak in heating.

        Returns
        -------
        Length peak in heating [s]
        """
        return self._peak_heating_duration * 3600

    @peak_heating_duration.setter
    def peak_heating_duration(self, duration: float) -> None:
        """
        This function sets the duration of the peak in heating.

        Parameters
        ----------
        duration : float
            Duration of the peak in hours

        Returns
        -------
        None
        """
        self._peak_heating_duration = duration

    @property
    def peak_cooling_duration(self) -> float:
        """
        Duration of the peak in cooling.

        Returns
        -------
        Duration of the peak in cooling [s]
        """
        return self._peak_cooling_duration * 3600

    @peak_cooling_duration.setter
    def peak_cooling_duration(self, duration: float) -> None:
        """
        This function sets the duration of the peak in cooling.

        Parameters
        ----------
        duration : float
            Duration of the peak in hours

        Returns
        -------
        None
        """
        self._peak_cooling_duration = duration

    @property
    def peak_duration(self) -> None:
        """
        Dummy object to set the length peak for both heating and cooling.

        Returns
        -------
        None
        """
        return

    @peak_duration.setter
    def peak_duration(self, duration: float) -> None:
        """
        This sets the duration of both the heating and cooling peak.

        Parameters
        ----------
        duration : float
            Duration in hours

        Returns
        -------
        None
        """
        self.peak_heating_duration = duration
        self.peak_cooling_duration = duration

    @property
    def ty(self) -> float:
        """
        Simulation period in seconds.

        Returns
        -------
        Simulation period in seconds
        """
        return self.simulation_period * 8760 * 3600

    @property
    def time_L3(self) -> np.ndarray:
        """
        Time for L3 sizing, i.e. an array with monthly the cumulative seconds that have passed.
        [744, 1416 ...] * 3600

        Returns
        -------
        Times for the L3 sizing : np.ndarray
        """
        return np.cumsum(np.tile(self.UPM, self.simulation_period) * 3600)

    @property
    def time_L4(self) -> np.ndarray:
        """
        Times for the L4 sizing, i.e. an array with hourly the cumulative seconds that have passed.
        [1, 2, 3, 4 ...] * 3600

        Returns
        -------
        Times for the L4 sizing : np.ndarray
        """
        # set the time constant for the L4 sizing
        time_L4 = 3600 * np.arange(1, 8760 * self.simulation_period + 1, dtype=np.float16)
        if np.isinf(time_L4).any():
            # 16 bit is not enough, go to 32
            time_L4 = 3600 * np.arange(1, 8760 * self.simulation_period + 1, dtype=np.float32)
        return time_L4

    @staticmethod
    def get_month_index(peak_load, avg_load) -> int:
        """
        This function calculates and returns the month index (i.e. the index of the month
        in which the field should be sized). It does so by taking 1) the month with the highest peak load.
        2) if all the peak loads are the same, it takes the month with the highest average load
        3) if all average loads are the same, it takes the last month

        Parameters
        ----------
        peak_load : np.ndarray
            array with the peak loads [kW]
        avg_load : np.ndarray
            array with the monthly average loads [kW]

        Returns
        -------
        month_index : int
            0 = jan, 1 = feb ...
        """
        # check if all peak loads are equal
        if not np.all(peak_load == peak_load[0]):
            return np.where(peak_load == np.max(peak_load))[0][-1]

        # if the average load is not constant, the month with the highest average load is chosen
        # if it is constant, the last month is returned
        return np.where(avg_load == np.max(avg_load))[0][-1]

    def _calculate_last_year_params(self, HC: bool) -> tuple:
        """
        This function calculates the parameters for the sizing based on the last year of operation.
        This is needed for the L2 sizing.

        Parameters
        ----------
        HC : bool
            True if the borefield is limited by extraction load

        Returns
        -------
        th, qh, qm, qa : float
            Peak length [s], peak load [W], corresponding monthly load [W], yearly imbalance [W]
        """

        # convert imbalance to Watt
        qa = self.imbalance / 8760. * 1000

        if HC:
            # limited by extraction load

            # set length peak
            th = self.peak_heating_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self.peak_heating, self.baseload_heating_power)
            qm = self.monthly_average_load[month_index] * 1000.
            qh = self.max_peak_heating * 1000.

            # correct signs
            qm = -qm
            qa = -qa

        else:
            # limited by injection load

            # set length peak
            th = self.peak_cooling_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self.peak_cooling, self.baseload_cooling_power)
            qm = self.monthly_average_load[month_index] * 1000.
            qh = self.max_peak_cooling * 1000.

        return th, qh, qm, qa

    def _calculate_first_year_params(self, HC: bool) -> tuple:
        """
        This function calculates the parameters for the sizing based on the first year of operation.
        This is needed for the L2 sizing.

        Parameters
        ----------
        HC : bool
            True if the borefield is limited by extraction load

        Returns
        -------
        th, tpm, tcm, qh, qpm, qcm : float
            Peak duration [s], cumulative time passed at the start of the month [s],
            cumulative time passed at the end of the month [s], peak load [W],
            average cumulative load of the past months [W avg],
            average load of the current month [W avg]
        """

        if HC:
            # limited by extraction load

            # set peak length
            th = self.peak_heating_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self.peak_heating, self.baseload_heating_power)
            qh = self.max_peak_heating * 1000.

            qm = self.monthly_average_load[month_index] * 1000.

            if month_index < 1:
                qpm = 0
            else:
                qpm = np.sum(self.monthly_average_load[:month_index]) * 1000 / (month_index + 1)

            qm = -qm
        else:
            # limited by injection

            # set peak length
            th = self.peak_cooling_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self.peak_cooling, self.baseload_cooling_power)
            qh = self.max_peak_cooling * 1000.

            qm = self.monthly_average_load[month_index] * 1000.
            if month_index < 1:
                qpm = 0
            else:
                qpm = np.sum(self.monthly_average_load[:month_index]) * 1000 / (month_index + 1)

        tcm = self.time_L3[month_index]
        tpm = self.time_L3[month_index - 1] if month_index > 0 else 0

        return th, tpm, tcm, qh, qpm, qm

    @property
    def max_peak_cooling(self) -> float:
        """
        This returns the max peak cooling in kW.

        Returns
        -------
        max peak cooling : float
        """
        return np.max(self.peak_cooling)

    @property
    def max_peak_heating(self) -> float:
        """
        This returns the max peak heating in kW.

        Returns
        -------
        max peak heating : float
        """
        return np.max(self.peak_heating)

    def add_dhw(self, dhw: float) -> None:
        """
        This function adds the domestic hot water (dhw).
        An error is raies is the dhw is not positive.

        Parameters
        ----------
        dhw : float
            Yearly consumption of domestic hot water [kWh/year]

        Returns
        -------
        None
        """
        self.dhw = dhw

    @property
    def dhw(self) -> float:
        """
        This function returns the yearly domestic hot water consumption.

        Returns
        -------
        dhw : float
            Yearly domestic hot water consumption [kWh/year]
        """
        return self._dhw_yearly

    @dhw.setter
    def dhw(self, dhw: float) -> None:
        """
        This function adds the domestic hot water (dhw).
        An error is raies is the dhw is not positive.

        Parameters
        ----------
        dhw : float
            Yearly consumption of domestic hot water [kWh/year]

        Returns
        -------
        None
        """
        if not isinstance(dhw, (float, int)):
            raise ValueError('Please fill in a number for the domestic hot water.')
        if not dhw >= 0:
            raise ValueError(f'Please fill in a positive value for the domestic hot water instead of {dhw}.')
        self._dhw_yearly = dhw

    @property
    def dhw_power(self) -> float:
        """
        This function returns the power related to the dhw production.

        Returns
        -------
        dhw power : float
        """
        return self._dhw_yearly / 8760