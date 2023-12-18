import pytest

from GHEtool import *

import pygfunction as gt


def test_fluid_data():
    data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    assert data.mfr == 0.2
    assert data.k_f == 0.568
    assert data.rho == 998
    assert data.Cp == 4180
    assert data.mu == 1e-3


def test_fluid_data_equal():
    data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    data2 = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    assert data == data2


def test_fluid_data_unequal():
    data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    data2 = FluidData(0.2, 0.567, 998, 4180, 1e-3)
    assert data != data2


def test_unequal_cross():
    data_fluid = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    data_ground = GroundConstantTemperature(3, 10)
    assert data_ground != data_fluid
    assert data_fluid != data_ground


def test_empty_variable_classes():
    fluid_data = FluidData()
    assert not fluid_data.check_values()


def test_set_mfr():
    data_fluid = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    data_fluid.set_mass_flow_rate(10)
    assert data_fluid.mfr == 10


def test_import_fluid_from_pygfunction():
    data_fluid = FluidData()
    data_fluid.set_mass_flow_rate(0.2)
    test_data = gt.media.Fluid('MPG', 20)
    data_fluid.import_fluid_from_pygfunction(test_data)
    assert data_fluid.mu == test_data.mu
    assert data_fluid.rho == test_data.rho
    assert data_fluid.Cp == test_data.cp
    assert data_fluid.k_f == test_data.k
