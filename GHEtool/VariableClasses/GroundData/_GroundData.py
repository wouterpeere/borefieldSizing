import abc
from abc import ABC
from GHEtool.VariableClasses.BaseClass import BaseClass


class _GroundData(BaseClass, ABC):
    """
    Contains information regarding the ground data of the borefield.
    """

    __slots__ = 'k_s', 'volumetric_heat_capacity', 'alpha', 'variable_Tg', 'Tg'

    def __init__(self, k_s: float = None,
                 volumetric_heat_capacity: float = 2.4 * 10**6):
        """

        Parameters
        ----------
        k_s : float
            Ground thermal conductivity [W/mK]
        volumetric_heat_capacity : float
            The volumetric heat capacity of the ground [J/m3K]
        """

        self.k_s = k_s  # W/mK
        self.volumetric_heat_capacity = volumetric_heat_capacity  # J/m3K
        self.variable_Tg: bool = False
        self.Tg: float = 10
        if self.volumetric_heat_capacity is None or self.k_s is None:
            self.alpha = None
        else:
            self.alpha = self.k_s / self.volumetric_heat_capacity  # m2/s

    @abc.abstractmethod
    def calculate_Tg(self, H: float) -> float:
        """
        This function gives back the ground temperature

        Parameters
        ----------
        H : float
            Depth of the borefield [m]

        Returns
        -------
        Tg : float
            Ground temperature [deg C]
        """

    @abc.abstractmethod
    def calculate_delta_H(self, temperature_diff: float) -> float:
        """
        This function calculates the difference in depth for a given difference in temperature.

        Parameters
        ----------
        temperature_diff : float
            Difference in temperature [deg C]

        Returns
        -------
        Difference in depth [m] : float
        """

    def max_depth(self, max_temp: float) -> float:
        """
        This function returns the maximum depth, based on the maximum temperature.
        The maximum is the depth where the ground temperature equals the maximum temperature limit.

        Parameters
        ----------
        max_temp : float
            Maximum temperature [deg C]

        Returns
        -------
        Depth : float
            Maximum depth [m]
        """
        return self.calculate_delta_H(max_temp-self.Tg)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for i in self.__slots__:
            if getattr(self, i) != getattr(other, i):
                return False
        return True
