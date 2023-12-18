"""
This document contains the CalculationSetup class.
This class contains all the relevant settings for the sizing options
"""
import copy

import numpy as np

from GHEtool.VariableClasses.BaseClass import BaseClass


class CalculationSetup(BaseClass):
    """
    This class contains all the settings related to the GHEtool methods.
    """

    __slots__ = '_L2_sizing', '_L3_sizing', '_L4_sizing', 'quadrant_sizing', '_backup', \
                'atol', 'rtol', 'max_nb_of_iterations', 'interpolate_gfunctions', 'H_init',\
                'use_precalculated_dataset', 'deep_sizing', 'force_deep_sizing'

    def __init__(self, quadrant_sizing: int = 0,
                 L2_sizing: bool = None, L3_sizing: bool = None, L4_sizing: bool = None,
                 atol: float = 0.05, rtol: float = 0.005, max_nb_of_iterations: int = 40,
                 interpolate_gfunctions: bool = None, H_init: float = 100.,
                 use_precalculated_dataset: bool = True, deep_sizing: bool = False,
                 force_deep_sizing: bool = False):
        """

        Parameters
        ----------
        quadrant_sizing : int
            Differs from 0 when a sizing in a certain quadrant is desired.
            Quadrants are developed by (Peere et al., 2021) [#PeereBS]_, [#PeereThesis]_
        L2_sizing : bool
            True if a sizing with the L2 method is needed
        L3_sizing : bool
            True if a sizing with the L3 method is needed
        L4_sizing : bool
            True if a sizing with the L4 method is needed
        atol : float
            Absolute tolerance between two consecutive depths in the sizing method,
            below which the iteration is stopped. False means that this tolerance is ignored.
        rtol : float
            Relative tolerance between two consecutive depths in the sizing method,
             below which the iteration is stopped. False means that this tolerance is ignored.
        max_nb_of_iterations : int
            Max number of iterations after which the iteration is stopped.
        interpolate_gfunctions : bool
            True if the g-functions may be interpolated. This can lead to some problems with time-invariant results,
            for if you run a sizing twice, the second time the algorithm can interpolate, so it (can) converge(s) to
            a slightly different result.
        H_init : float
            The initial depth for the different methods.
        use_precalculated_dataset : bool
            True if a precalculated dataset of g-function should be used.
        deep_sizing : bool
            When using a temperature gradient, sometimes the iterative algorithm will get stuck in a loop, returning
            an unsolvable error due to the maximum number of iterations. However, it can be that there is a solution
            anyways. By using another approach for sizing with a variable ground temperature, a solution can be found,
            however this method is slower. If deep_sizing is True, whenever an unsolvable error is returned, the
            sizing is done again with this other methodology.
        force_deep_sizing : bool
            True when deep_sizing should be done always

        References
        ----------
        .. [#PeereBS] Peere, W., Picard, D., Cupeiro Figueroa, I., Boydens, W., and Helsen, L. (2021) Validated combined first and last year borefield sizing methodology. In Proceedings of International Building Simulation Conference 2021. Brugge (Belgium), 1-3 September 2021. https://doi.org/10.26868/25222708.2021.30180
        .. [#PeereThesis] Peere, W. (2020) Methode voor economische optimalisatie van geothermische verwarmings- en koelsystemen. Master thesis, Department of Mechanical Engineering, KU Leuven, Belgium.

        """
        # define sizing options
        self._L2_sizing: bool = True
        self._L3_sizing: bool = False
        self._L4_sizing: bool = False
        self.quadrant_sizing: int = 0
        self.atol: float = atol
        self.rtol: float = rtol
        self.max_nb_of_iterations: int = max_nb_of_iterations
        self.interpolate_gfunctions: bool = interpolate_gfunctions
        self.H_init: float = H_init
        self.use_precalculated_dataset: bool = use_precalculated_dataset
        self.deep_sizing: bool = deep_sizing
        self.force_deep_sizing: bool = force_deep_sizing

        self._backup: CalculationSetup = None

        # set the variables in this class by passing down the values given in this function
        self._set_sizing_setup(kwargs=locals())

    def update_variables(self, **kwargs) -> None:
        """
        This function updates the variables in the current class.

        Parameters
        ----------
        kwargs
            Keyword arguments with all the variables that need to be changed with the corresponding new values

        Returns
        -------
        None
        """
        self._set_sizing_setup(kwargs)

    def _set_sizing_setup(self, kwargs) -> None:
        """
        This method sets all the variables in the SizingSetup class.
        This is done by looping over all the keywords in the kwargs and setting the corresponding variables
        in this class to the value in the kwargs.
        W.r.t. the sizing methodology, it is checked whether this can be set.

        Parameters
        ----------
        kwargs
            All the keyword arguments of the init class or all the variables in the class itself.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When there is a problematic value like two sizing methods or a quadrant not in (0, 4)
        """
        variables = self.__slots__
        sizing_vars = set(["L2_sizing", "L3_sizing", "L4_sizing"])

        # set value for sizing method
        # Lx_sizing is for the initialisation of the class
        # _Lx_sizing is for the case a backup is set
        L2_sizing = kwargs.get("L2_sizing") if "L2_sizing" in kwargs else kwargs.get("_L2_sizing")
        L3_sizing = kwargs.get("L3_sizing") if "L3_sizing" in kwargs else kwargs.get("_L3_sizing")
        L4_sizing = kwargs.get("L4_sizing") if "L4_sizing" in kwargs else kwargs.get("_L4_sizing")

        self._check_and_set_sizing(L2_sizing, L3_sizing, L4_sizing)

        # set all the other class variables
        for key, val in kwargs.items():
            if key in variables and key not in sizing_vars:
                if val is not None:
                    if key == "quadrant_sizing" and val not in (0, 1, 2, 3, 4):
                        raise ValueError(f'The quadrant {val} does not exist!')
                    self.__setattr__(key, val)
            elif key != 'self' and key not in sizing_vars:
                raise ValueError(f'The variable {key} is not a valid options!')

    def _check_and_set_sizing(self, L2_sizing: bool, L3_sizing: bool, L4_sizing: bool) -> None:
        """
        This function checks whether the sizing method can be set (i.e. a unique method is requested)
        and sets the according variable to True.

        Parameters
        ----------
        L2_sizing : bool
            True if a sizing with the L2 method is needed
        L3_sizing : bool
            True if a sizing with the L3 method is needed
        L4_sizing : bool
            True if a sizing with the L4 method is needed

        Returns
        -------
        None

        Raises
        ------
        ValueError
            This function raises a value error when more than 1 sizing methodology is set to True
        """
        # check if just one sizing is given
        if np.sum([L2_sizing if L2_sizing is not None else 0, L3_sizing if L3_sizing is not None else 0,
                   L4_sizing if L4_sizing is not None else 0]) > 1:
            raise ValueError("Please check if just one sizing method is chosen!")

        self._set_sizing(L2_sizing, L3_sizing, L4_sizing)

    def _set_sizing(self, L2_sizing: bool = False, L3_sizing: bool = False, L4_sizing: bool = False) -> None:
        """
        This function sets the sizing method.

        Parameters
        ----------
        L2_sizing : bool
            True if a sizing with the L2 method is needed
        L3_sizing : bool
            True if a sizing with the L3 method is needed
        L4_sizing : bool
            True if a sizing with the L4 method is needed

        Returns
        -------
        None
        """

        if not (L2_sizing or L3_sizing or L4_sizing):
            Warning("No sizing method is set to true, so nothing has changed.")

        # save sizing
        if L2_sizing:
            self._L2_sizing = L2_sizing
            self._L3_sizing = False
            self._L4_sizing = False
        if L3_sizing:
            self._L3_sizing = L3_sizing
            self._L2_sizing = False
            self._L4_sizing = False
        if L4_sizing:
            self._L4_sizing = L4_sizing
            self._L2_sizing = False
            self._L3_sizing = False

    @property
    def L2_sizing(self) -> bool:
        return self._L2_sizing

    @L2_sizing.setter
    def L2_sizing(self, L2_sizing) -> None:
        self._set_sizing(L2_sizing=L2_sizing)

    @property
    def L3_sizing(self) -> bool:
        return self._L3_sizing

    @L3_sizing.setter
    def L3_sizing(self, L3_sizing) -> None:
        self._set_sizing(L3_sizing=L3_sizing)

    @property
    def L4_sizing(self) -> bool:
        return self._L4_sizing

    @L4_sizing.setter
    def L4_sizing(self, L4_sizing) -> None:
        self._set_sizing(L4_sizing=L4_sizing)

    def make_backup(self) -> None:
        """
        This function sets the backup variable of the class.
        This is done by making a copy of the current class.

        Returns
        -------
        None
        """
        self._backup = copy.copy(self)

    def restore_backup(self) -> None:
        """
        This function restores the class to a previous backup using the self.backup variable.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            A value error is raised when this function is called before a backup has been made
        """
        if self._backup is None:
            raise ValueError("No backup has been made.")

        kwargs = {}
        for var in self.__slots__:
            kwargs[var] = self._backup.__getattribute__(var)
        self._set_sizing_setup(kwargs)

    def __eq__(self, other):
        if not isinstance(other, CalculationSetup):
            return False
        for i in self.__slots__:
            if i == '_backup':
                continue
            if getattr(self, i) != getattr(other, i):
                return False
        return True
