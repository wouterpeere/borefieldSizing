from GHEtool.VariableClasses.GroundData._GroundData import _GroundData


class GroundTemperatureGradient(_GroundData):

    __slots__ = _GroundData.__slots__ + ('gradient',)

    def __init__(self, k_s: float = None,
                 T_g: float = None,
                 volumetric_heat_capacity: float = 2.4 * 10**6,
                 gradient: float = 3.0):
        """

        Parameters
        ----------
        k_s : float
            Ground thermal conductivity [W/mK]
        T_g : float
            Surface ground temperature [deg C]
        volumetric_heat_capacity : float
            The volumetric heat capacity of the ground [J/m3K]
        gradient : float
            The geothermal temperature gradient [K/100m]
        """
        super().__init__(k_s=k_s, volumetric_heat_capacity=volumetric_heat_capacity)
        self.gradient = gradient
        self.Tg = T_g

    def calculate_Tg(self, H: float) -> float:
        """
        This function gives back the ground temperature at a depth H.

        Parameters
        ----------
        H : float
            Depth at which the temperature should be calculated [m]

        Returns
        -------
        Tg : float
            Ground temperature [deg C]
        """
        # geothermal gradient is equal to the geothermal heat flux divided by the thermal conductivity
        # avg ground temperature is (Tg + gradient + Tg) / 2 = Tg + gradient / 2
        # divide by 100 since the gradient is in K/100m
        return self.Tg + H * self.gradient / 2 / 100

    def calculate_delta_H(self, temperature_diff: float) -> float:
        """
        This function calculates the difference in depth for a given difference in temperature.

        Parameters
        ----------
        temperature_diff : float
            Difference in temperature [deg C]

        Returns
        -------
        float
            Difference in depth [m]
        """
        return temperature_diff * 2 * 100 / self.gradient
