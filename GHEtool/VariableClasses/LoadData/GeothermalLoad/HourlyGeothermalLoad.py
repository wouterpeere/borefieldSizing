import numpy as np
import pandas as pd

from typing import Union, Tuple
from GHEtool.VariableClasses.LoadData._LoadData import _LoadData
from GHEtool.logger import ghe_logger


class HourlyGeothermalLoad(_LoadData):
    """
    This class contains all the information for geothermal load data with a monthly resolution and absolute input.
    This means that the inputs are both in kWh/month and kW/month.
    """

    __slots__ = tuple(_LoadData.__slots__) + ('_heating_load', '_cooling_load')

    # define parameters for conversion to monthly loads
    START = pd.to_datetime("2019-01-01 00:00:00")
    END = pd.to_datetime("2019-12-31 23:59:00")
    HOURS_SERIES = pd.Series(pd.date_range(START, END, freq="1H"))

    def __init__(self, heating_load: Union[np.ndarray, list, tuple] = np.zeros(8760),
                 cooling_load: Union[np.ndarray, list, tuple] = np.zeros(8760),
                 simulation_period: int = 20,
                 dhw: float = 0.):
        """

        Parameters
        ----------
        heating_load : np.ndarray, list, tuple
            Heating load [kWh/h]
        cooling_load : np.ndarray, list, tuple
            Cooling load [kWh/h]
        simulation_period : int
            Length of the simulation period in years
        dhw : float
            Yearly consumption of domestic hot water [kWh/year]
        """

        super().__init__(hourly_resolution=True, simulation_period=simulation_period)

        # initiate variables
        self._hourly_heating_load: np.ndarray = np.zeros(8760)
        self._hourly_cooling_load: np.ndarray = np.zeros(8760)

        # set variables
        self.hourly_heating_load = heating_load
        self.hourly_cooling_load = cooling_load
        self.dhw = dhw

    def _check_input(self, input: Union[np.ndarray, list, tuple]) -> bool:
        """
        This function checks whether the input is valid or not.
        The input is correct if and only if:
        1) the input is a np.ndarray, list or tuple
        2) the length of the input is 8760
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
        if not len(input) == 8760:
            ghe_logger.error("The length of the load should be 12.")
            return False
        if np.min(input) < 0:
            ghe_logger.error("No value in the load can be smaller than zero.")
            return False
        return True

    @property
    def hourly_heating_load(self) -> np.ndarray:
        """
        This function returns the hourly heating load in kWh/h including DHW.

        Returns
        -------
        hourly heating : np.ndarray
            Hourly heating values (incl. DHW) [kWh/h] for one year, so the length of the array is 8760
        """
        return self._hourly_heating_load + self.dhw / 8760

    @hourly_heating_load.setter
    def hourly_heating_load(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the hourly heating load [kWh/h] after it has been checked.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Hourly heating [kWh/h]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 8760, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._hourly_heating_load = load
            return
        raise ValueError

    def set_hourly_heating(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the hourly heating load [kWh/h] after it has been checked.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Hourly heating [kWh/h]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 8760, the input is not of the correct type, or it contains negative
            values
        """
        self.hourly_heating_load = load

    @property
    def hourly_cooling_load(self) -> np.ndarray:
        """
        This function returns the hourly cooling load in kWh/h.

        Returns
        -------
        hourly cooling : np.ndarray
            Hourly cooling values [kWh/h] for one year, so the length of the array is 8760
        """
        return self._hourly_cooling_load

    @hourly_cooling_load.setter
    def hourly_cooling_load(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the hourly cooling load [kWh/h] after it has been checked.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Hourly cooling [kWh/h]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 8760, the input is not of the correct type, or it contains negative
            values
        """
        if self._check_input(load):
            self._hourly_cooling_load = load
            return
        raise ValueError

    def set_hourly_cooling(self, load: Union[np.ndarray, list, tuple]) -> None:
        """
        This function sets the hourly cooling load [kWh/h] after it has been checked.

        Parameters
        ----------
        load : np.ndarray, list or tuple
            Hourly cooling [kWh/h]

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When either the length is not 8760, the input is not of the correct type, or it contains negative
            values
        """
        self.hourly_cooling_load = load

    @property
    def imbalance(self) -> float:
        """
        This function calculates the ground imbalance.
        A positive imbalance means that the field is injection dominated, i.e. it heats up every year.

        Returns
        -------
        imbalance : float
        """
        return np.sum(self.hourly_cooling_load - self.hourly_heating_load)

    def resample_to_monthly(self, hourly_load: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        This function resamples an hourly_load to monthly peaks (kW/month) and baseloads (kWh/month).

        Parameters
        ----------
        hourly_load : np.ndarray
            Hourly loads in kWh/h

        Returns
        -------
        peak loads [kW], monthly average loads [kWh/month] : np.ndarray, np.ndarray
        """
        # create dataframe
        df = pd.DataFrame(hourly_load, index=HourlyGeothermalLoad.HOURS_SERIES, columns=['load'])

        if self.all_months_equal:
            return np.max(np.array_split(hourly_load, 12), axis=1), np.sum(np.array_split(hourly_load, 12), axis=1)

        # resample
        return np.array(df.resample('M').agg({'load': 'max'})['load']),\
            np.array(df.resample('M').agg({'load': 'sum'})['load'])


    @property
    def baseload_cooling(self) -> np.ndarray:
        """
        This function returns the baseload cooling in kWh/month.

        Returns
        -------
        baseload cooling : np.ndarray
            Baseload cooling values [kWh/month] for one year, so the length of the array is 12
        """
        return self.resample_to_monthly(self.hourly_cooling_load)[1]

    @property
    def baseload_heating(self) -> np.ndarray:
        """
        This function returns the baseload heating in kWh/month.

        Returns
        -------
        baseload heating : np.ndarray
            Baseload heating values [kWh/month] for one year, so the length of the array is 12
        """
        return self.resample_to_monthly(self.hourly_heating_load)[1]

    @property
    def peak_cooling(self) -> np.ndarray:
        """
        This function returns the peak cooling load in kW/month.

        Returns
        -------
        peak cooling : np.ndarray
            Peak cooling values for one year, so the length of the array is 12
        """
        return self.resample_to_monthly(self.hourly_cooling_load)[0]

    @property
    def peak_heating(self) -> np.ndarray:
        """
        This function returns the peak heating load in kW/month.

        Returns
        -------
        peak heating : np.ndarray
            Peak heating values for one year, so the length of the array is 12
        """
        return self.resample_to_monthly(self.hourly_heating_load)[0]

    @property
    def hourly_cooling_load_simulation_period(self) -> np.ndarray:
        """
        This function returns the hourly cooling in kWh/h for a whole simulation period.

        Returns
        -------
        hourly cooling : np.ndarray
            hourly cooling for the whole simulation period
        """
        return np.tile(self.hourly_cooling_load, self.simulation_period)

    @property
    def hourly_load_simulation_period(self) -> np.ndarray:
        """
        This function calculates the resulting hourly load in kW for the whole simulation period.

        Returns
        -------
        resulting hourly load : np.ndarray
        """
        return self.hourly_cooling_load_simulation_period - self.hourly_heating_load_simulation_period

    @property
    def hourly_heating_load_simulation_period(self) -> np.ndarray:
        """
        This function returns the hourly heating in kWh/h for a whole simulation period.

        Returns
        -------
        hourly heating : np.ndarray
            hourly heating for the whole simulation period
        """
        return np.tile(self.hourly_heating_load, self.simulation_period)

    def load_hourly_profile(self, file_path: str, header: bool = True, separator: str = ";",
                            decimal_seperator: str = ".", col_heating: int = 0, col_cooling: int = 1) -> None:
        """
        This function loads in an hourly load profile [kW].

        Parameters
        ----------
        file_path : str
            Path to the hourly load file
        header : bool
            True if this file contains a header row
        separator : str
            Symbol used in the file to separate the columns
        decimal_seperator : str
            Symbol used for the decimal number separation
        col_heating : int
            Column index for heating
        col_cooling : int
            Column index for cooling

        Returns
        -------
        None
        """
        if header:
            header: int = 0
        else:
            header = None

        # TODO implement single column
        # if col_heating == col_cooling:
        #     ghe_logger.info('Only one column with data selected. Load will be splitted into heating and cooling load.')

        # import data
        df = pd.read_csv(file_path, sep=separator, header=header, decimal=decimal_seperator)

        # set data
        self.hourly_heating_load = np.array(df.iloc[:, col_heating])
        self.hourly_cooling_load = np.array(df.iloc[:, col_cooling])

        ghe_logger.info("Hourly profile loaded!")

    def __eq__(self, other) -> bool:
        if not isinstance(other, HourlyGeothermalLoad):
            return False
        if not np.array_equal(self.hourly_cooling_load, other.hourly_cooling_load):
            return False
        if not np.array_equal(self.hourly_heating_load, other.hourly_heating_load):
            return False
        if not self.simulation_period == other.simulation_period:
            return False
        return True
