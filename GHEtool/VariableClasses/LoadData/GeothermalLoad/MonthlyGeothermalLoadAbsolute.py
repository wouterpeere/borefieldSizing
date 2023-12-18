import numpy as np

from typing import Union
from GHEtool.VariableClasses.LoadData._LoadData import _LoadData
from GHEtool.logger.ghe_logger import ghe_logger


class MonthlyGeothermalLoadAbsolute(_LoadData):
    """
    This class contains all the information for geothermal load data with a monthly resolution and absolute input.
    This means that the inputs are both in kWh/month and kW/month.
    """

    __slots__ = tuple(_LoadData.__slots__) + ('_baseload_heating', '_baseload_cooling',
                                              '_peak_heating', '_peak_cooling')

    def __init__(self, baseload_heating: Union[np.ndarray, list, tuple] = np.zeros(12),
                 baseload_cooling: Union[np.ndarray, list, tuple] = np.zeros(12),
                 peak_heating: Union[np.ndarray, list, tuple] = np.zeros(12),
                 peak_cooling: Union[np.ndarray, list, tuple] = np.zeros(12),
                 simulation_period: int = 20,
                 dhw: float = 0.):
        """

        Parameters
        ----------
        baseload_heating : np.ndarray, list, tuple
            Baseload heating values [kWh/month]
        baseload_cooling : np.ndarray, list, tuple
            Baseload cooling values [kWh/month]
        peak_heating : np.ndarray, list, tuple
            Peak heating values [kW/month]
        peak_cooling : np.ndarray, list, tuple
            Peak cooling values [kW/month]
        simulation_period : int
            Length of the simulation period in years
        dhw : float
            Yearly consumption of domestic hot water [kWh/year]
        """

        super().__init__(hourly_resolution=False, simulation_period=simulation_period)

        # initiate variables
        self._baseload_heating: np.ndarray = np.zeros(12)
        self._baseload_cooling: np.ndarray = np.zeros(12)
        self._peak_heating: np.ndarray = np.zeros(12)
        self._peak_cooling: np.ndarray = np.zeros(12)

        # set variables
        self.baseload_heating = baseload_heating
        self.baseload_cooling = baseload_cooling
        self.peak_heating = peak_heating
        self.peak_cooling = peak_cooling
        self.dhw = dhw

    def _check_input(self, input: Union[np.ndarray, list, tuple]) -> bool:
        """
        This function checks whether the input is valid or not.
        The input is correct if and only if:
        1) the input is a np.ndarray, list or tuple
        2) the length of the input is 12
        3) the input does not contain any negative values.

        Parameters
        ----------
        input : np.ndarray, list or tuple

        Returns
        -------
        bool
            True if the inputs are valid
        """
        if not isinstance(input, (np.ndarray, list, tuple)):
            ghe_logger.error("The load should be of type np.ndarray, list or tuple.")
            return False
        if not len(input) == 12:
            ghe_logger.error("The length of the load should be 12.")
            return False
        if np.min(input) < 0:
            ghe_logger.error("No value in the load can be smaller than zero.")
            return False
        return True

    @property
    def baseload_cooling(self) -> np.ndarray:
        """
        This function returns the baseload cooling in kWh/month.

        Returns
        -------
        baseload cooling : np.ndarray
            Baseload cooling values [kWh/month] for one year, so the length of the array is 12
        """
        return self._baseload_cooling

    @baseload_cooling.setter
    def baseload_cooling(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the baseload cooling [kWh/month] after it has been checked.
        If the baseload cooling gives a higher average power than the peak power,
        this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Baseload cooling [kWh/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._baseload_cooling = np.array(load)
            return
        raise ValueError

    def set_baseload_cooling(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the baseload cooling [kWh/month] after it has been checked.
        If the baseload cooling gives a higher average power than the peak power,
        this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Baseload cooling [kWh/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        self.baseload_cooling = load

    @property
    def baseload_heating(self) -> np.ndarray:
        """
        This function returns the baseload heating in kWh/month (incl. DHW).

        Returns
        -------
        baseload heating : np.ndarray
            Baseload heating values (incl. DHW) [kWh/month] for one year, so the length of the array is 12
        """
        return self._baseload_heating + self.dhw / 8760 * self.UPM

    @baseload_heating.setter
    def baseload_heating(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the baseload heating [kWh/month] after it has been checked.
        If the baseload heating gives a higher average power than the peak power,
        this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Baseload heating [kWh/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._baseload_heating = np.array(load)
            return
        raise ValueError

    def set_baseload_heating(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the baseload heating [kWh/month] after it has been checked.
        If the baseload heating gives a higher average power than the peak power,
        this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Baseload heating [kWh/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        self.baseload_heating = np.array(load)

    @property
    def peak_cooling(self) -> np.ndarray:
        """
        This function returns the peak cooling load in kW/month.

        Returns
        -------
        peak cooling : np.ndarray
            Peak cooling values for one year, so the length of the array is 12
        """
        return np.maximum(self._peak_cooling, self.baseload_cooling_power)

    @peak_cooling.setter
    def peak_cooling(self, load) -> None:
        """
        This function sets the peak cooling load [kW/month] after it has been checked.
        If the baseload cooling gives a higher average power, this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Peak cooling load [kW/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._peak_cooling = np.array(load)
            return
        raise ValueError

    def set_peak_cooling(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the peak cooling load [kW/month] after it has been checked.
        If the baseload cooling gives a higher average power, this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Peak cooling load [kW/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        self.peak_cooling = np.array(load)

    @property
    def peak_heating(self) -> np.ndarray:
        """
        This function returns the peak heating load in kW/month.

        Returns
        -------
        peak heating : np.ndarray
            Peak heating values for one year, so the length of the array is 12
        """
        return np.maximum(np.array(self._peak_heating) + self.dhw_power, self.baseload_heating_power)

    @peak_heating.setter
    def peak_heating(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the peak heating load [kW/month] after it has been checked.
        If the baseload heating gives a higher average power, this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Peak heating load [kW/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._peak_heating = np.array(load)
            return
        raise ValueError

    def set_peak_heating(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the peak heating load [kW/month] after it has been checked.
        If the baseload heating gives a higher average power, this is taken as the peak power in that month.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Peak heating load [kW/month]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 12, the input is not of the correct type, or it contains negative
            values
        """
        self.peak_heating = np.array(load)

    def __eq__(self, other) -> bool:
        if not isinstance(other, MonthlyGeothermalLoadAbsolute):
            return False
        if not np.array_equal(self.baseload_heating, other.baseload_heating):
            return False
        if not np.array_equal(self.baseload_cooling, other.baseload_cooling):
            return False
        if not np.array_equal(self.peak_heating, other.peak_heating):
            return False
        if not np.array_equal(self.peak_cooling, other.peak_cooling):
            return False
        if not self.simulation_period == other.simulation_period:
            return False
        return True
