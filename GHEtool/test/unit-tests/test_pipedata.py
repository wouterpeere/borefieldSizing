"""
This file contains the test for the pipedata
"""

from GHEtool.VariableClasses.PipeData import *
from GHEtool.VariableClasses import FluidData
import matplotlib.pyplot as plt
import numpy as np
import pygfunction as gt


### Test U-pipes
def test_empty_class():
    assert not SingleUTube().check_values()
    assert not DoubleUTube().check_values()
    assert not MultipleUTube().check_values()


def test_axissym():
    single = SingleUTube(1, 0.016, 0.02, 2, 0.02)
    double = DoubleUTube(1, 0.016, 0.02, 2, 0.02)
    np.testing.assert_array_almost_equal(single._axis_symmetrical_pipe, [(-0.02, 2.4492935982947064e-18), (0.02, -4.898587196589413e-18)])
    np.testing.assert_array_almost_equal(double._axis_symmetrical_pipe, [(-0.02, 2.4492935982947064e-18), (0.02, -4.898587196589413e-18), (-3.673940397442059e-18, -0.02), (6.123233995736766e-18, 0.02)])
    np.testing.assert_array_almost_equal(single._axis_symmetrical_pipe, MultipleUTube(1, 0.16, 0.02, 2, 0.02, 1)._axis_symmetrical_pipe)
    np.testing.assert_array_almost_equal(double._axis_symmetrical_pipe, MultipleUTube(1, 0.16, 0.02, 2, 0.02, 2)._axis_symmetrical_pipe)


def test_calculate_thermal_resistance():
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    single = SingleUTube(1, 0.016, 0.02, 2, 0.02)
    double = DoubleUTube(1, 0.016, 0.02, 2, 0.02)
    Us = MultipleUTube(1, 0.016, 0.02, 2, 0.02, 1)
    Ud = MultipleUTube(1, 0.016, 0.02, 2, 0.02, 2)

    single.calculate_resistances(fluid_data)
    double.calculate_resistances(fluid_data)
    Us.calculate_resistances(fluid_data)
    Ud.calculate_resistances(fluid_data)
    assert np.isclose(single.R_p, 0.017757199605368243)
    assert np.isclose(single.R_f, 0.008698002460890118)
    assert np.isclose(double.R_p, 0.017757199605368243)
    assert np.isclose(double.R_f, 0.017963387333190542)
    assert np.allclose((single.R_f, single.R_p), (Us.R_f, Us.R_p))
    assert np.allclose((double.R_f, double.R_p), (Ud.R_f, Ud.R_p))


def test_equivalent_borehole_resistance_U_tubes():
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    single = SingleUTube(1, 0.016, 0.02, 2, 0.04)
    double = DoubleUTube(1, 0.016, 0.02, 2, 0.04)
    single.calculate_resistances(fluid_data)
    double.calculate_resistances(fluid_data)
    borehole = gt.boreholes.Borehole(100, 1, 0.07, 0, 0)
    pipe = single.pipe_model(fluid_data, 2, borehole)
    assert np.isclose(pipe.effective_borehole_thermal_resistance(0.1, 4180), 0.13637413925456277)
    pipe = double.pipe_model(fluid_data, 2, borehole)
    assert np.isclose(pipe.effective_borehole_thermal_resistance(0.2, 4180), 0.09065168435087693)


def test_draw_internals(monkeypatch):
    pipe = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05)
    monkeypatch.setattr(plt, 'show', lambda: None)
    pipe.draw_borehole_internal(0.075)
    assert pipe.R_f == 0
    assert pipe.R_p == 0
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    pipe.calculate_resistances(fluid_data)
    pipe.draw_borehole_internal(0.075)


def test_pipe_data():
    data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 2)
    assert data.k_g == 1
    assert data.r_in == 0.015
    assert data.r_out == 0.02
    assert data.k_p == 0.4
    assert data.D_s == 0.05
    assert data.number_of_pipes == 2


def test_pipe_data_equal():
    data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 2)
    data2 = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 2)
    assert data == data2


def test_pipe_data_unequal():
    data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 2)
    data2 = MultipleUTube(1, 0.016, 0.02, 0.4, 0.05, 2)
    assert data != data2


### Test Coaxial pipes
k_g = 1.0           # Grout thermal conductivity [W/m.K]
k_p = 0.4           # Pipe thermal conductivity [W/m.K]
r_in_in = 0.0221    # Inside pipe inner radius [m]
r_in_out = 0.025    # Inside pipe outer radius [m]
r_out_in = 0.0487   # Outer pipe inside radius [m]
r_out_out = 0.055   # Outer pipe outside radius [m]


def test_empty_coaxial():
    assert not CoaxialPipe().check_values()


def test_draw_coaxial_internals(monkeypatch):
    pipe = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g)
    monkeypatch.setattr(plt, 'show', lambda: None)
    pipe.draw_borehole_internal(0.075)
    assert pipe.R_ff == 0
    assert pipe.R_fp == 0
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    pipe.calculate_resistances(fluid_data)
    pipe.draw_borehole_internal(0.075)


def test_calculate_resistance_coaxial():
    pipe = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    fluid = gt.media.Fluid('MPG', 20.)
    fluid = FluidData(0.5, fluid.k, fluid.rho, fluid.cp, fluid.mu)
    pipe.calculate_resistances(fluid)
    assert np.isclose(pipe.R_fp, 0.11803503887356001)
    assert np.isclose(pipe.R_ff, 0.16491519753761458)
    pipe = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=False)
    fluid = gt.media.Fluid('MPG', 20.)
    fluid = FluidData(0.5, fluid.k, fluid.rho, fluid.cp, fluid.mu)
    pipe.calculate_resistances(fluid)
    assert np.isclose(pipe.R_fp, 0.11803503887356001)
    assert np.isclose(pipe.R_ff, 0.16491519753761458)


def test_calculate_borehole_equivalent_resistance_coaxial():
    pipe = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    fluid = gt.media.Fluid('MPG', 20.)
    fluid = FluidData(0.5, fluid.k, fluid.rho, fluid.cp, fluid.mu)
    borehole = gt.boreholes.Borehole(100, 1, 0.075, 0, 0)
    pipe.calculate_resistances(fluid)
    model = pipe.pipe_model(fluid, 2, borehole)
    assert np.isclose(model.effective_borehole_thermal_resistance(0.5, 4180), 0.17312532151975354)
    pipe = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=False)
    fluid = gt.media.Fluid('MPG', 20.)
    fluid = FluidData(0.5, fluid.k, fluid.rho, fluid.cp, fluid.mu)
    pipe.calculate_resistances(fluid)
    model = pipe.pipe_model(fluid, 2, borehole)
    assert np.isclose(model.effective_borehole_thermal_resistance(0.5, 4180), 0.17312532151975354)

    # pygfunction itself
    is_inner_inlet = True
    for i in range(1, 12, 2):
        pipe_ghe = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=False)
        fluid = gt.media.Fluid('MPG', 20.)
        fluid = FluidData(0.5, fluid.k, fluid.rho, fluid.cp, fluid.mu)
        pipe_ghe.calculate_resistances(fluid)
        pipe = gt.pipes.Coaxial(pos=(0., 0.),
                         r_in=np.array([r_out_in, r_in_in]) if is_inner_inlet else
                         np.array([r_in_in, r_out_in]),
                         r_out=np.array([r_out_out, r_in_out]) if is_inner_inlet else
                         np.array([r_in_out, r_out_out]),
                         borehole=borehole, k_s=i, k_g=k_g, R_ff=pipe_ghe.R_ff, R_fp=pipe_ghe.R_fp, J=2)


def test_pipe_data_equal_coaxial():
    data = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    data2 = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    assert data == data2


def test_pipe_data_unequal_coaxial():
    data = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    data2 = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=False)
    assert data != data2


def test_pipe_data_unequal_cross():
    data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 2)
    data2 = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    assert data != data2
    assert data2 != data


def test_reynolds_number():
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 2)
    assert np.isclose(data.Re(fluid_data=fluid_data), 4244.131815783876)
    data = CoaxialPipe(r_in_in, r_in_out, r_out_in, r_out_out, k_p, k_g, is_inner_inlet=True)
    assert np.isclose(data.Re(fluid_data=fluid_data), 1727.5977540504243)
