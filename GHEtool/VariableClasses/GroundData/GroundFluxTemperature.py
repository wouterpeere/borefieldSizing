from GHEtool.VariableClasses.GroundData._GroundData import _GroundData


class GroundFluxTemperature(_GroundData):

    __slots__ = _GroundData.__slots__ + ('flux',)

    def __init__(self, k_s: float = None,
                 T_g: float = None,
                 volumetric_heat_capacity: float = 2.4 * 10**6,
                 flux: float = 0.06):
        """

        Parameters
        ----------
        k_s : float
            Ground thermal conductivity [W/mK]
        T_g : float
            Surface ground temperature [deg C]
        volumetric_heat_capacity : float
            The volumetric heat capacity of the ground [J/m3K]
        flux : float
            The geothermal heat flux [W/m2]
        """
        super().__init__(k_s=k_s, volumetric_heat_capacity=volumetric_heat_capacity)
        self.flux = flux
        self.Tg = T_g
        self.variable_Tg = True

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
        return self.Tg + H * self.flux / self.k_s / 2

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
        return temperature_diff * 2 * self.k_s / self.flux
