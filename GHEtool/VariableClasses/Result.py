"""
This file implements a Result class for temperature profiles.
"""
import numpy as np


class Results:
    """
    Class which contains the temperatures of the fluid and borehole wall.
    """
    def __init__(self,
                 borehole_wall_temp: np.ndarray = np.array([]),
                 peak_heating: np.ndarray = np.array([]),
                 peak_cooling: np.ndarray = np.array([]),
                 monthly_heating: np.ndarray = np.array([]),
                 monthly_cooling: np.ndarray = np.array([])):
        """

        Parameters
        ----------
        borehole_wall_temp : np.ndarray
            Borehole wall temperature [deg C]
        peak_heating : np.ndarray
            Average fluid temperature in peak heating [deg C]
        peak_cooling : np.ndarray
            Average fluid temperature in peak cooling [deg C]
        monthly_heating : np.ndarray
            Average temperature due to average monthly heating [deg C]
        monthly_cooling : np.ndarray
            Average temperature due to average monthly cooling [deg C]
        """
        self._peak_heating = peak_heating
        self._peak_cooling = peak_cooling
        self._monthly_heating = monthly_heating
        self._monthly_cooling = monthly_cooling
        self._Tb = borehole_wall_temp

    @property
    def peak_heating(self) -> np.ndarray:
        return self._peak_heating

    @property
    def peak_cooling(self) -> np.ndarray:
        return self._peak_cooling

    @property
    def monthly_heating(self) -> np.ndarray:
        return self._monthly_heating

    @property
    def monthly_cooling(self) -> np.ndarray:
        return self._monthly_cooling

    @property
    def Tb(self) -> np.ndarray:
        return self._Tb
