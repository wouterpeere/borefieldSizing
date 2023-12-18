"""
This document contains the information for the BaseClass.
This class is used as a super class for different variable classes.
"""
from __future__ import annotations
from typing import List

import numpy as np
from numpy import ndarray
from pygfunction.boreholes import Borehole
from importlib import import_module


class BaseClass:
    """
    This class contains basic functionality of different classes within GHEtool.
    It contains the code to generate a dictionary from the class (in order to be able to export to JSON),
    to load a class based on a dictionary and to check whether or not all attributes differ from None.

    This class should only be altered whenever a highly general method should be implemented.
    """
    def to_dict(self) -> dict:
        """
        This function converts the class variables to a dictionary so it can be saved in a JSON format.
        Currently, it can handle np.ndarray, list, set, str, int, float, tuple,
        pygfunction.Borehole and classes within GHEtool.

        Returns
        -------
        dict
            Dictionary with all the attributes of the class
        """

        # get all variables in class
        if hasattr(self, "__slots__"):
            variables: List[str] = list(self.__slots__)
        else:
            variables: List[str] = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        # initiate dictionary
        dictionary: dict = {"__module__": f"{type(self).__module__}", "__name__":  f"{type(self).__name__}"}

        # populate dictionary
        for key in variables:
            value = getattr(self, key)

            if value is None:
                dictionary[key] = "None"
                continue

            if isinstance(value, (int, bool, float, str)):
                dictionary[key] = value
                continue

            if isinstance(value, tuple):
                dictionary[key] = {"value": list(value), "type": "tuple"}
                continue

            if isinstance(value, np.ndarray):
                dictionary[key] = {"value": value.tolist(), "type": "np.ndarray"}
                continue

            if isinstance(value, set):
                dictionary[key] = {"value": list(value), "type": "set"}
                continue

            if isinstance(value, list):
                if np.any(value) and isinstance(value[0], Borehole):
                    # pygfunction object
                    dictionary[key] = {"value": [{key: value for key, value in borehole.__dict__.items()
                                                  if key != "_is_tilted"}
                                                 for borehole in value],
                                       "type": "pygfunction.Borehole"}
                    continue
                dictionary[key] = value

            if isinstance(value, dict):
                # note that this can cause problems whenever self.key contains values that or not int, bool, float or str
                dictionary[key] = value
                continue

            # for all self-defined classes
            if hasattr(value, "to_dict"):
                dictionary[key] = value.to_dict()

        return dictionary

    def from_dict(self, dictionary: dict) -> None:
        """
        This function converts the dictionary values to the class attributes.
        Currently, it can handle np.ndarray, list, set, str, int, float, tuple, pygfunction.Borehole
        and classes within GHEtool.

        Parameters
        ----------
        dictionary
            Dictionary with all the attributes of the class

        Returns
        -------
        None
        """
        if hasattr(self, "__slots__"):
            variables: List[str] = list(self.__slots__)
        else:
            variables: List[str] = [key for key, value in dictionary.items() if not key.startswith("__")]

        for key, value in dictionary.items():

            if key not in variables:
                continue

            if value == "None":
                setattr(self, key, None)
                continue

            if isinstance(value, (int, bool, float, str, list)):
                setattr(self, key, value)
                continue

            if isinstance(value, dict):
                # note that this can mean that the value is a dictionary, or it is a np.ndarray, set or tuple
                keys = value.keys()
                # for all self-defined classes
                if "__module__" in keys:
                    class_dict = getattr(import_module(value["__module__"]), value["__name__"])
                    setattr(self, key, class_dict.__new__(class_dict))
                    getattr(self, key).from_dict(value)
                    continue

                if len(keys) == 2 and "type" in keys and "value" in keys:
                    var_type = value["type"]
                    _value = value["value"]

                    if var_type == "set":
                        setattr(self, key, set(_value))
                        continue
                    if var_type == "np.ndarray":
                        setattr(self, key, np.array(_value))
                        continue
                    if var_type == "tuple":
                        setattr(self, key, tuple(_value))
                        continue
                    if var_type == "pygfunction.Borehole":
                        borefield = [Borehole(H=borehole["H"],
                                              D=borehole["D"],
                                              r_b=borehole["r_b"],
                                              x=borehole["x"],
                                              y=borehole["y"],
                                              tilt=borehole["tilt"],
                                              orientation=borehole["orientation"])
                                     for borehole in _value]
                        setattr(self, key, borefield)
                        continue
                # normal dictionary
                setattr(self, key, value)

    def check_values(self) -> bool:
        """
        This functions checks if the class attributes differ from None.

        Returns
        -------
        bool
            True if all values are correct. False otherwise
        """
        # get all variables in class
        if hasattr(self, "__slots__"):
            variables: List[str] = list(self.__slots__)
        else:
            variables: List[str] = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        return all(getattr(self, var) is not None for var in variables)


class UnsolvableDueToTemperatureGradient(Exception):
    """
    This Exception occurs when there is an unsizeble borefield due to incompatibility between 1) peak cooling,
    which requires a deeper borefield and 2) a temperature gradient, which causes a higher ground temperature when
    the field is drilled deeper. This leads to unsizeble solutions.
    """
    def __init__(self):
        super().__init__('No solution can be found due to the temperature gradient. Please increase the field size.')


class MaximumNumberOfIterations(RuntimeError):
    """
    This Error occurs when the maximum number of interation is reacted.
    """
    def __init__(self, iter: int):
        super().__init__(f'The maximum number of iterations {iter} is crossed. There is no size convergence.')
