"""
This document contains the TestMethodClass used for testing the GHEtool methods.
"""
from GHEtool import Borefield
from typing import List
import copy

import numpy as np


class SizingObject:

    def __init__(self, borefield, L2_output=None, L3_output=None, L4_output=None,
                 quadrant: int = None, error_L2=None, error_L3=None, error_L4=None, name: str = ""):
        self.borefield: Borefield = copy.deepcopy(borefield)
        self.L2_output = L2_output
        self.L3_output = L3_output
        self.L4_output = L4_output
        self.quadrant = quadrant
        self.error_L2 = error_L2
        self.error_L3 = error_L3
        self.error_L4 = error_L4
        self.name = name


class OptimiseLoadProfileObject:

    def __init__(self, borefield: Borefield, load, depth: float, SCOP: float, SEER: float, percentage_heating: float,
                 percentage_cooling: float, peak_heating_geo: float, peak_cooling_geo: float, peak_heating_ext: float,
                 peak_cooling_ext: float, name: str = ""):
        self.borefield = copy.deepcopy(borefield)
        self.load = copy.deepcopy(load)
        self.depth = depth
        self.SCOP = SCOP
        self.SEER = SEER
        self.percentage_heating = percentage_heating
        self.percentage_cooling = percentage_cooling
        self.peak_heating_geo = peak_heating_geo
        self.peak_cooling_geo = peak_cooling_geo
        self.peak_heating_ext = peak_heating_ext
        self.peak_cooling_ext = peak_cooling_ext
        self.name = name

    def test(self):  # pragma: no cover
        self.borefield.optimise_load_profile(self.load, self.depth, self.SCOP, self.SEER)
        assert np.isclose(self.borefield._percentage_heating, self.percentage_heating)
        assert np.isclose(self.borefield._percentage_cooling, self.percentage_cooling)
        assert np.isclose(self.borefield.load.max_peak_heating, self.peak_heating_geo)
        assert np.isclose(self.borefield.load.max_peak_cooling, self.peak_cooling_geo)
        assert np.isclose(self.borefield._external_load.max_peak_heating, self.peak_heating_ext)
        assert np.isclose(self.borefield._external_load.max_peak_cooling, self.peak_cooling_ext)


class TestMethodClass():

    def __init__(self):
        self.list_of_test_objects: List[SizingObject | OptimiseLoadProfileObject] = []

    def add(self, object: SizingObject | OptimiseLoadProfileObject) -> None:
        self.list_of_test_objects.append(object)

    @property
    def names_L2(self) -> list:
        list_of_names = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L2_output is None and i.error_L2 is None:
                continue
            if i.name != '':
                list_of_names.append(i.name)
                continue
            list_of_names.append(f'case {_}')  # pragma: no cover
        return list_of_names

    @property
    def names_L3(self) -> list:
        list_of_names = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L3_output is None and i.error_L3 is None:
                continue
            if i.name != '':
                list_of_names.append(i.name)
                continue
            list_of_names.append(f'case {_}')  # pragma: no cover
        return list_of_names

    @property
    def names_L4(self) -> list:
        list_of_names = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L4_output is None and i.error_L4 is None:
                continue
            if i.name != '':
                list_of_names.append(i.name)
                continue
            list_of_names.append(f'case {_}')  # pragma: no cover
        return list_of_names

    @property
    def names_optimise_load_profile(self) -> list:
        list_of_names = []
        for _, i in enumerate(self.list_of_test_objects):
            if isinstance(i, SizingObject):
                continue
            if i.name != '':
                list_of_names.append(i.name)
                continue
            list_of_names.append(f'case {_}')  # pragma: no cover
        return list_of_names

    @property
    def L2_sizing_input(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L2_output is not None or i.error_L2 is not None:
                temp.append(copy.deepcopy(i.borefield))
        return temp

    @property
    def L2_sizing_output(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L2_output is not None or i.error_L2 is not None:
                temp.append((i.L2_output if i.L2_output is not None else i.error_L2, i.quadrant))
        return temp

    @property
    def L3_sizing_input(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L3_output is not None or i.error_L3 is not None:
                temp.append(copy.deepcopy(i.borefield))
        return temp

    @property
    def L3_sizing_output(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L3_output is not None or i.error_L3 is not None:
                temp.append((i.L3_output if i.L3_output is not None else i.error_L3, i.quadrant))
        return temp

    @property
    def L4_sizing_input(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L4_output is not None or i.error_L4 is not None:
                temp.append(copy.deepcopy(i.borefield))
        return temp

    @property
    def L4_sizing_output(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if not isinstance(i, SizingObject):
                continue
            if i.L4_output is not None or i.error_L4 is not None:
                temp.append((i.L4_output if i.L4_output is not None else i.error_L4, i.quadrant))
        return temp

    @property
    def optimise_load_profile_input(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if isinstance(i, SizingObject):
                continue
            temp.append((copy.deepcopy(i.borefield), copy.deepcopy(i.load), i.depth, i.SCOP, i.SEER))
        return temp

    @property
    def optimise_load_profile_output(self) -> list:
        temp = []
        for _, i in enumerate(self.list_of_test_objects):
            if isinstance(i, SizingObject):
                continue
            temp.append((i.percentage_heating, i.percentage_cooling, i.peak_heating_geo, i.peak_cooling_geo,
                         i.peak_heating_ext, i.peak_cooling_ext))
        return temp