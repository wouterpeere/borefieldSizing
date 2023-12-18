"""
test that the results are correctly calculated
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from GHEtool import Borefield, FOLDER, FluidData, GroundConstantTemperature, GroundFluxTemperature, GroundTemperatureGradient, MonthlyGeothermalLoadAbsolute, MultipleUTube
from GHEtool.gui.data_2_borefield_func import data_2_borefield
from GHEtool.gui.gui_structure import GuiStructure
from ScenarioGUI import load_config
import pygfunction as gt

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

load_config(Path(__file__).parent.joinpath("gui_config.ini"))

sys.setrecursionlimit(1500)


def round_down(value: float, decimal: int) -> float:
    """
    round the value down considering the decimal nuber
    Parameters
    ----------
    value: float
        value to be rounded
    decimal : int
        decimal number
    Returns
    -------
        down rounded value
    """
    return int(value * 10 ** decimal) / (10 ** decimal)


def create_borefield(g_s: GuiStructure) -> Borefield:
    """
    create borefield from Gui structure
    Parameters
    ----------
    g_s GuiStructure:
        gui structure

    Returns
    -------
        borefield with data from g_s
    """
    borefield = Borefield()

    borefield.set_max_avg_fluid_temperature(g_s.option_max_temp.get_value())
    borefield.set_min_avg_fluid_temperature(g_s.option_min_temp.get_value())

    g_d = GroundConstantTemperature(g_s.option_conductivity.get_value(), g_s.option_ground_temp.get_value(), g_s.option_heat_capacity.get_value() * 1000)
    borefield.set_ground_parameters(g_d)
    borefield.set_Rb(g_s.option_constant_rb.get_value())

    borefield.create_rectangular_borefield(g_s.option_width.get_value(), g_s.option_length.get_value(), g_s.option_spacing_width.get_value(),
                                           g_s.option_spacing_width.get_value(), g_s.option_depth.get_value(), g_s.option_pipe_depth.get_value(),
                                           g_s.option_pipe_borehole_radius.get_value())

    hl = [g_s.option_hl_jan.get_value(), g_s.option_hl_feb.get_value(), g_s.option_hl_mar.get_value(), g_s.option_hl_apr.get_value(),
          g_s.option_hl_may.get_value(), g_s.option_hl_jun.get_value(), g_s.option_hl_jul.get_value(), g_s.option_hl_aug.get_value(),
          g_s.option_hl_sep.get_value(), g_s.option_hl_oct.get_value(), g_s.option_hl_nov.get_value(), g_s.option_hl_dec.get_value()]

    cl = [g_s.option_cl_jan.get_value(), g_s.option_cl_feb.get_value(), g_s.option_cl_mar.get_value(), g_s.option_cl_apr.get_value(),
          g_s.option_cl_may.get_value(), g_s.option_cl_jun.get_value(), g_s.option_cl_jul.get_value(), g_s.option_cl_aug.get_value(),
          g_s.option_cl_sep.get_value(), g_s.option_cl_oct.get_value(), g_s.option_cl_nov.get_value(), g_s.option_cl_dec.get_value()]

    hp = [g_s.option_hp_jan.get_value(), g_s.option_hp_feb.get_value(), g_s.option_hp_mar.get_value(), g_s.option_hp_apr.get_value(),
          g_s.option_hp_may.get_value(), g_s.option_hp_jun.get_value(), g_s.option_hp_jul.get_value(), g_s.option_hp_aug.get_value(),
          g_s.option_hp_sep.get_value(), g_s.option_hp_oct.get_value(), g_s.option_hp_nov.get_value(), g_s.option_hp_dec.get_value()]

    cp = [g_s.option_cp_jan.get_value(), g_s.option_cp_feb.get_value(), g_s.option_cp_mar.get_value(), g_s.option_cp_apr.get_value(),
          g_s.option_cp_may.get_value(), g_s.option_cp_jun.get_value(), g_s.option_cp_jul.get_value(), g_s.option_cp_aug.get_value(),
          g_s.option_cp_sep.get_value(), g_s.option_cp_oct.get_value(), g_s.option_cp_nov.get_value(), g_s.option_cp_dec.get_value()]

    load = MonthlyGeothermalLoadAbsolute(hl, cl, hp, cp)

    load.peak_heating_duration = g_s.option_len_peak_heating.get_value()
    load.peak_cooling_duration = g_s.option_len_peak_cooling.get_value()

    borefield.load = load
    borefield.simulation_period = g_s.option_simu_period.get_value()

    return borefield


def test_temp_profile_ground_data(qtbot):
    # depth: float = 100
    # k_s: float = 5
    # heat_cap: float = 2000
    # ground_temp: float = 12.
    # init gui window
    main_window = start_tests(qtbot)

    main_window.save_scenario()

    k_s = round_down(main_window.gui_structure.option_conductivity.get_value() * 1.5, 3)
    heat_cap = round_down(main_window.gui_structure.option_heat_capacity.get_value() * 1.5, 1)
    depth = round_down(main_window.gui_structure.option_depth.get_value() * 1.5, 2)
    ground_temp = round_down(main_window.gui_structure.option_ground_temp.get_value() * 1.5, 2)
    r_b = round_down(main_window.gui_structure.option_constant_rb.get_value() * 1.5, 4)

    gs = main_window.gui_structure
    gs.option_temperature_profile_hourly.set_value(0)

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

    borefield = create_borefield(gs)

    gs.option_conductivity.set_value(k_s)
    gs.option_heat_capacity.set_value(heat_cap)
    gs.option_ground_temp.set_value(ground_temp)
    gs.option_depth.set_value(depth)
    gs.option_source_ground_temperature.set_value(0)
    gs.option_constant_rb.set_value(r_b)

    gd = GroundConstantTemperature(k_s, ground_temp, heat_cap * 1_000)
    borefield.set_ground_parameters(gd)
    borefield.set_Rb(r_b)

    main_window.save_scenario()

    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert borefield_gui.ground_data == borefield.ground_data
    assert borefield_gui.borehole._Rb == borefield.borehole._Rb
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (depth, )
    assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_temp_profile_temp_gradient(qtbot):
    # depth: float = 100
    # k_s: float = 5
    # heat_cap: float = 2000
    # ground_temp: float = 12.
    # init gui window
    main_window = start_tests(qtbot)

    main_window.save_scenario()
    main_window.add_scenario()

    gs = main_window.gui_structure
    gs.option_temperature_profile_hourly.set_value(0)

    k_s = gs.option_conductivity.get_value()
    depth = gs.option_depth.get_value()

    gradient = round_down(main_window.gui_structure.option_temp_gradient.get_value() * 1.5, 3)
    ground_temp = round_down(main_window.gui_structure.option_temp_gradient.get_value() * 1.5, 2)

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

    borefield = create_borefield(gs)

    gs.option_temp_gradient.set_value(gradient)
    gs.option_source_ground_temperature.set_value(2)
    gs.option_flux_gradient.set_value(1)
    gs.option_ground_temp_gradient.set_value(ground_temp)
    main_window.save_scenario()

    gd = GroundTemperatureGradient(k_s, ground_temp, borefield.ground_data.volumetric_heat_capacity, gradient)
    borefield.set_ground_parameters(gd)

    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert np.isclose(borefield_gui.ground_data.gradient, borefield.ground_data.gradient)
    assert np.isclose(borefield_gui.ground_data.Tg, borefield.ground_data.Tg)
    assert np.isclose(borefield_gui._Tg(150), gd.calculate_Tg(150))
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (depth,)
    assert func.keywords == {}

    flux = round_down(gradient * k_s / 100, 2)

    gs.option_temp_gradient.set_value(gradient)
    gs.option_flux_gradient.set_value(0)
    gs.option_ground_heat_flux.set_value(flux)
    main_window.save_scenario()

    gd = GroundFluxTemperature(k_s, ground_temp, borefield.ground_data.volumetric_heat_capacity, flux)
    borefield.set_ground_parameters(gd)

    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert np.isclose(borefield_gui.ground_data.flux, borefield.ground_data.flux)
    assert np.isclose(borefield_gui.ground_data.Tg, borefield.ground_data.Tg)
    assert np.isclose(borefield_gui._Tg(150), gd.calculate_Tg(150))
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (depth,)
    assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_borefield_shapes(qtbot):
    tilt = 0
    # init gui window
    main_window = start_tests(qtbot)

    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.aim_rect.widget.click() if not main_window.gui_structure.aim_rect.widget.isChecked() else None
    main_window.gui_structure.option_tilted.set_value(tilt)
    main_window.gui_structure.option_spacing_length.set_value(main_window.gui_structure.option_spacing_width.get_value() + 1)
    main_window.gui_structure.update_borefield()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    boreholes = gt.boreholes.rectangle_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_width + 1, ds.option_depth,
                                              ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt / 360 * 2 * np.pi)
    def check_borefield(borefield_1: list[gt.boreholes], borefield_2: list[gt.boreholes]):
        for borehole_1, borehole_2 in zip(borefield_1, borefield_2):
            assert np.isclose(borehole_1.H, borehole_2.H)
            assert np.isclose(borehole_1.D, borehole_2.D)
            assert np.isclose(borehole_1.r_b, borehole_2.r_b)
            assert np.isclose(borehole_1.x, borehole_2.x)
            assert np.isclose(borehole_1.y, borehole_2.y)
            assert np.isclose(borehole_1.tilt, borehole_2.tilt)
            assert np.isclose(borehole_1.orientation, borehole_2.orientation)

    check_borefield(borefield_gui.borefield, boreholes)
    qtbot.wait(10)
    main_window.gui_structure.aim_Box_shaped.widget.click()
    main_window.gui_structure.update_borefield()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    boreholes = gt.boreholes.box_shaped_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_width + 1, ds.option_depth,
                                              ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt / 360 * 2 * np.pi)
    check_borefield(borefield_gui.borefield, boreholes)
    qtbot.wait(10)
    main_window.gui_structure.aim_L_shaped.widget.click()
    main_window.gui_structure.update_borefield()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    boreholes = gt.boreholes.L_shaped_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_width + 1, ds.option_depth,
                                              ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt / 360 * 2 * np.pi)
    check_borefield(borefield_gui.borefield, boreholes)
    qtbot.wait(10)
    main_window.gui_structure.aim_U_shaped.widget.click()
    main_window.gui_structure.update_borefield()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    boreholes = gt.boreholes.U_shaped_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_width + 1, ds.option_depth,
                                              ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt / 360 * 2 * np.pi)
    check_borefield(borefield_gui.borefield, boreholes)
    qtbot.wait(10)
    main_window.gui_structure.aim_circle.widget.click()
    main_window.gui_structure.update_borefield()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    boreholes = gt.boreholes.circle_field(ds.option_number_circle_boreholes, ds.option_borefield_radius, ds.option_depth,
                                              ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt / 360 * 2 * np.pi)
    check_borefield(borefield_gui.borefield, boreholes)
    qtbot.wait(10)

    main_window.gui_structure.aim_custom.widget.click()
    values = [(x, y, H, D, r_b) for x, y, H, D, r_b in [(0,0,100,5,0.075), (0,9,110,2,0.06), (9,0,90,3,0.08), (9,9,150,6,0.07)]]
    main_window.gui_structure.custom_borefield.set_value(values)
    main_window.gui_structure.update_borefield()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    boreholes = [gt.boreholes.Borehole(H, D, r_b, x=x, y=y) for x, y, H, D, r_b in values]
    check_borefield(borefield_gui.borefield, boreholes)
    qtbot.wait(10)
    close_tests(main_window, qtbot)


def test_import_borefield_data(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    main_window.gui_structure.borefield_file.set_value("file")
    main_window.gui_structure.import_borefield.button.click()
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[main_window.gui_structure.option_language.get_value()[0]]

    main_window.gui_structure.aim_custom.widget.click()
    file = f"{FOLDER.joinpath('gui/test_gui/borefield_data.csv')}"
    main_window.gui_structure.borefield_file.set_value(file)
    main_window.gui_structure.option_seperator_borefield.set_value(1)
    main_window.gui_structure.option_decimal_borefield.set_value(0)
    main_window.gui_structure.import_borefield.button.click()
    main_window.save_scenario()
    data = pd.read_csv(file)
    for li_1, li_2 in zip(data.values, main_window.gui_structure.custom_borefield.get_value()):
        assert np.allclose(li_1, li_2)

    main_window.gui_structure.custom_borefield.set_value([(0, 0 ,10, 4, 0.05)])

    file = f"{FOLDER.joinpath('gui/test_gui/borefield_data.txt')}"
    main_window.gui_structure.borefield_file.set_value(file)
    main_window.gui_structure.option_seperator_borefield.set_value(2)
    main_window.gui_structure.option_decimal_borefield.set_value(1)
    main_window.gui_structure.import_borefield.button.click()
    for li_1, li_2 in zip(data.values, main_window.gui_structure.custom_borefield.get_value()):
        assert np.allclose(li_1, li_2)

    qtbot.wait(10)
    close_tests(main_window, qtbot)


def test_temp_profile_pipe_data(qtbot):
    # depth: float = 100
    # k_s: float = 5
    # heat_cap: float = 2000
    # ground_temp: float = 12.
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    main_window.add_scenario()

    gs = main_window.gui_structure

    depth = gs.option_depth.get_value()
    gs.option_pipe_borehole_radius.set_value(0.5)

    conduct_grout = round_down(gs.option_pipe_grout_conductivity.get_value() * 1.5, 3)
    conduct_pipe = round_down(gs.option_pipe_conductivity.get_value() * 1.5, 3)
    inner_pipe = round_down(gs.option_pipe_inner_radius.get_value() * 1.5, 4)
    dis = round_down(0.5 - (inner_pipe + 0.02 * 1.5) - 0.02, 4)
    outer_pipe = round_down(inner_pipe + 0.02 * 1.5 - 0.02, 4)
    roughness = round_down(gs.option_pipe_roughness.get_value() * 1.5, 7)

    pipe_data = MultipleUTube(conduct_grout, inner_pipe, outer_pipe, conduct_pipe, dis, main_window.gui_structure.option_pipe_number.get_value() + 2, roughness)
    fluid_data = FluidData(gs.option_fluid_mass_flow.get_value(), gs.option_fluid_conductivity.get_value(), gs.option_fluid_density.get_value(),
                           gs.option_fluid_capacity.get_value(), gs.option_fluid_viscosity.get_value())

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

    borefield = create_borefield(gs)

    gs.option_pipe_grout_conductivity.set_value(conduct_grout)
    gs.option_pipe_distance.set_value(dis)
    gs.option_pipe_number.set_value(main_window.gui_structure.option_pipe_number.get_value() + 2)
    gs.option_pipe_outer_radius.set_value(outer_pipe)
    gs.option_pipe_inner_radius.set_value(inner_pipe)
    gs.option_pipe_conductivity.set_value(conduct_pipe)
    gs.option_pipe_roughness.set_value(roughness)
    gs.option_method_rb_calc.set_value(1)

    while not np.isclose(gs.option_pipe_distance.get_value(), dis):
        gs.option_pipe_distance.set_value(dis)  # pragma: no cover

    borefield.set_pipe_parameters(pipe_data)
    borefield.set_fluid_parameters(fluid_data)

    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert borefield_gui.borehole.pipe_data == borefield.borehole.pipe_data
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (depth,)
    assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_temp_profile_fluid_data(qtbot):
    # depth: float = 100
    # k_s: float = 5
    # heat_cap: float = 2000
    # ground_temp: float = 12.
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    main_window.add_scenario()

    gs = main_window.gui_structure

    depth = gs.option_depth.get_value()

    conduct = round_down(gs.option_fluid_conductivity.get_value() * 1.5, 3)
    density = round_down(gs.option_fluid_density.get_value() * 1.5, 1)
    heat_cap = round_down(gs.option_fluid_capacity.get_value() * 1.5, 1)
    viscosity = round_down(gs.option_fluid_viscosity.get_value() * 1.5, 6)
    flow_rate = round_down(gs.option_fluid_mass_flow.get_value() * 1.5, 3)

    pipe_data = MultipleUTube(gs.option_pipe_grout_conductivity.get_value(), gs.option_pipe_inner_radius.get_value(), gs.option_pipe_outer_radius.get_value(),
                              gs.option_pipe_conductivity.get_value(), gs.option_pipe_distance.get_value(), gs.option_pipe_number.get_value(), gs.option_pipe_roughness.get_value())
    fluid_data = FluidData(flow_rate, conduct, density, heat_cap, viscosity)

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

    borefield = create_borefield(gs)

    gs.option_fluid_mass_flow.set_value(flow_rate)
    gs.option_fluid_conductivity.set_value(conduct)
    gs.option_fluid_density.set_value(density)
    gs.option_fluid_capacity.set_value(heat_cap)
    gs.option_fluid_viscosity.set_value(viscosity)
    gs.option_method_rb_calc.set_value(1)

    borefield.set_pipe_parameters(pipe_data)
    borefield.set_fluid_parameters(fluid_data)

    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert borefield_gui.borehole.fluid_data == borefield.borehole.fluid_data
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (depth,)
    assert func.keywords == {}
    close_tests(main_window, qtbot)

def test_temp_profile_borefield_data(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    main_window.save_scenario()
    main_window.add_scenario()
    gs = main_window.gui_structure

    spacing = round_down(gs.option_spacing_width.get_value() * 1.5, 2)
    radius = round_down(gs.option_pipe_borehole_radius.get_value() * 1.5, 4)
    burial_depth = round_down(gs.option_pipe_depth.get_value() * 1.5, 1)
    width = gs.option_width.get_value() + 2
    length = gs.option_length.get_value() + 2

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

    borefield = create_borefield(gs)

    main_window.gui_structure.aim_rect.widget.click() if not main_window.gui_structure.aim_rect.widget.isChecked() else None
    gs.option_width.set_value(width)
    gs.option_length.set_value(length)
    gs.option_spacing_width.set_value(spacing)
    gs.option_spacing_length.set_value(spacing)
    gs.option_pipe_depth.set_value(burial_depth)
    gs.option_pipe_borehole_radius.set_value(radius)

    boreholes = gt.boreholes.rectangle_field(width, length, spacing, spacing, gs.option_depth.get_value(), burial_depth, radius,
                                             tilt=gs.option_tilted.get_value() / 360 * 2 * np.pi)
    borefield.set_borefield(boreholes)

    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert borefield_gui.borefield[0].__str__() == borefield.borefield[0].__str__()
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (gs.option_depth.get_value(),)
    assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_sizing_L2_L3_min_max(qtbot) -> None:
    # init gui window
    main_window = start_tests(qtbot)

    gs = main_window.gui_structure
    gs.option_source_ground_temperature.set_value(0)

    for L2 in [0, 1]:
        min_temp = round_down(gs.option_min_temp.get_value() - 2, 2)
        ground_temp = round_down(gs.option_ground_temp.get_value() * 1.12, 2)
        max_temp = round_down(gs.option_max_temp.get_value() + 2, 2)
        main_window.save_scenario()
        main_window.add_scenario()

        gs.aim_req_depth.widget.click() if not gs.aim_req_depth.widget.isChecked() else None
        gs.option_method_size_depth.set_value(0 if L2 else 1)

        borefield = create_borefield(gs)

        borefield.ground_data.Tg = ground_temp
        borefield.set_max_avg_fluid_temperature(max_temp)
        borefield.set_min_avg_fluid_temperature(min_temp)

        gs.option_max_temp.set_value(max_temp)
        gs.option_min_temp.set_value(min_temp)
        gs.option_ground_temp.set_value(ground_temp)

        main_window.save_scenario()

        main_window.save_scenario()
        ds = main_window.list_ds[-1]
        borefield_gui, func = data_2_borefield(ds)
        assert borefield_gui.ground_data.Tg == borefield.ground_data.Tg
        assert borefield_gui.Tf_max == borefield.Tf_max
        assert borefield_gui.Tf_min == borefield.Tf_min
        assert borefield_gui._calculation_setup.L2_sizing == L2
        assert borefield_gui._calculation_setup.L3_sizing != L2
        assert func.func == borefield_gui.size
        assert func.args == ()
        assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_temp_profile_period_peak_length(qtbot) -> None:
    # init gui window
    main_window = start_tests(qtbot)

    main_window.save_scenario()
    main_window.add_scenario()

    gs = main_window.gui_structure

    peak_heating = round_down(gs.option_len_peak_heating.get_value() * 1.5, 2)
    peak_cooling = round_down(gs.option_len_peak_cooling.get_value() * 1.4, 2)
    period = gs.option_simu_period.get_value() + 10

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

    borefield = create_borefield(gs)
    borefield.load.simulation_period = period
    borefield.load.peak_heating_duration = peak_heating
    borefield.load.peak_cooling_duration = peak_cooling

    gs.option_len_peak_heating.set_value(peak_heating)
    gs.option_len_peak_cooling.set_value(peak_cooling)
    gs.option_simu_period.set_value(period)

    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    borefield_gui, func = data_2_borefield(ds)
    assert borefield_gui.load.peak_cooling_duration == borefield.load.peak_cooling_duration
    assert borefield_gui.load.peak_heating_duration == borefield.load.peak_heating_duration
    assert func.func == borefield_gui.calculate_temperatures
    assert func.args == (gs.option_depth.get_value(), )
    assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_temp_profile_heating_data(qtbot) -> None:
    # init gui window
    main_window = start_tests(qtbot)

    factor = 1.12
    for delay in range(1, 10):
        main_window.save_scenario()
        main_window.add_scenario()

        heat_peak = [142, 102, 55, 0, 0, 0, 0, 40.4, 85, 119, 136, 160]

        heat_load = [44_400, 37_500, 29_700, 19_200, 0, 0, 0, 18_300, 26_100, 35_100, 43_200, 46_500]

        heat_load = np.array([round_down(heat_load[i] * factor, 0) for i in range(-delay, 12 - delay)])
        heat_peak = np.array([round_down(heat_peak[i] * factor, 3) for i in range(-delay, 12 - delay)])

        gs = main_window.gui_structure

        gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None

        borefield = create_borefield(gs)
        borefield.set_baseload_heating(heat_load)
        borefield.set_peak_heating(heat_peak)

        for option, value in zip([gs.option_hl_jan, gs.option_hl_feb, gs.option_hl_mar, gs.option_hl_apr, gs.option_hl_may, gs.option_hl_jun, gs.option_hl_jul,
                                  gs.option_hl_aug, gs.option_hl_sep, gs.option_hl_oct, gs.option_hl_nov, gs.option_hl_dec], heat_load):
            option.set_value(value)

        for option, value in zip([gs.option_hp_jan, gs.option_hp_feb, gs.option_hp_mar, gs.option_hp_apr, gs.option_hp_may, gs.option_hp_jun, gs.option_hp_jul,
                                  gs.option_hp_aug, gs.option_hp_sep, gs.option_hp_oct, gs.option_hp_nov, gs.option_hp_dec], heat_peak):
            option.set_value(value)

        main_window.save_scenario()
        ds = main_window.list_ds[-1]
        borefield_gui, func = data_2_borefield(ds)
        assert np.allclose(borefield_gui.load.baseload_heating, borefield.load.baseload_heating)
        assert np.allclose(borefield_gui.load.baseload_cooling, borefield.load.baseload_cooling)
        assert np.allclose(borefield_gui.load.peak_heating, borefield.load.peak_heating)
        assert np.allclose(borefield_gui.load.peak_cooling, borefield.load.peak_cooling)
        assert func.func == borefield_gui.calculate_temperatures
        assert func.args == (gs.option_depth.get_value(),)
        assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_temp_profile_cooling_data(qtbot) -> None:
    """
    test cooling data

    Parameters
    ----------
    qtbot: qtbot
        qtbot
    delay: int
        change within the year
    factor: float
        factor to scale profile

    """
    # init gui window
    main_window = start_tests(qtbot)

    cool_peak = [0, 0, 34, 69, 133, 187, 213, 240, 160, 37, 0, 0]

    cool_load = [4_000, 8_000, 8_000, 8_000, 12_000, 16_000, 32_000, 32_000, 16_000, 12_000, 8_000, 4_000]

    factor = 1.154
    for delay in range(1, 10):
        main_window.save_scenario()
        main_window.add_scenario()

        cool_load = np.array([round_down(cool_load[i] * factor, 0) for i in range(-delay, 12 - delay)])
        cool_peak = np.array([round_down(cool_peak[i] * factor, 3) for i in range(-delay, 12 - delay)])

        g_s = main_window.gui_structure

        if not g_s.aim_temp_profile.widget.isChecked():  # pragma: no cover
            g_s.aim_temp_profile.widget.click()

        borefield = create_borefield(g_s)
        borefield.set_baseload_cooling(cool_load)
        borefield.set_peak_cooling(cool_peak)

        for option, value in zip([g_s.option_cl_jan, g_s.option_cl_feb, g_s.option_cl_mar, g_s.option_cl_apr, g_s.option_cl_may, g_s.option_cl_jun, g_s.option_cl_jul,
                                  g_s.option_cl_aug, g_s.option_cl_sep, g_s.option_cl_oct, g_s.option_cl_nov, g_s.option_cl_dec], cool_load):
            option.set_value(value)

        for option, value in zip([g_s.option_cp_jan, g_s.option_cp_feb, g_s.option_cp_mar, g_s.option_cp_apr, g_s.option_cp_may, g_s.option_cp_jun, g_s.option_cp_jul,
                                  g_s.option_cp_aug, g_s.option_cp_sep, g_s.option_cp_oct, g_s.option_cp_nov, g_s.option_cp_dec], cool_peak):
            option.set_value(value)

        main_window.save_scenario()
        d_s = main_window.list_ds[-1]
        borefield_gui, func = data_2_borefield(d_s)
        assert np.allclose(borefield_gui.load.baseload_heating, borefield.load.baseload_heating)
        assert np.allclose(borefield_gui.load.baseload_cooling, borefield.load.baseload_cooling)
        assert np.allclose(borefield_gui.load.peak_heating, borefield.load.peak_heating)
        assert np.allclose(borefield_gui.load.peak_cooling, borefield.load.peak_cooling)
        assert func.func == borefield_gui.calculate_temperatures
        assert func.args == (g_s.option_depth.get_value(),)
        assert func.keywords == {}
    close_tests(main_window, qtbot)


def test_coaxial_and_gradient(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    gs = main_window.gui_structure
    gs.option_source_ground_temperature.set_value(2)

    gs.option_method_rb_calc.set_value(1)
    gs.option_U_pipe_or_coaxial_pipe.set_value(1)
    gs.option_flux_gradient.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.result_Rb_calculated.label.text() == 'Equivalent borehole thermal resistance: 0.0984 mK/W'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.55 °C'

    gs.option_flux_gradient.set_value(0)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.result_Rb_calculated.label.text() == 'Equivalent borehole thermal resistance: 0.0984 mK/W'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 17.05 °C'
    close_tests(main_window, qtbot)


def test_ground_selector(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(0)

    gs.option_source_ground_temperature.set_value(2)
    gs.option_flux_gradient.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.results_ground_temperature.label.text() == 'Average ground temperature: 11.5 °C'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.14 °C'

    gs.option_source_ground_temperature.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.results_ground_temperature.label.text() == 'Average ground temperature: 12.17 °C'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.81 °C'

    gs.option_ground_database.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.results_ground_temperature.label.text() == 'Average ground temperature: 13.07 °C'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 17.71 °C'
    close_tests(main_window, qtbot)


def test_fluid_selector(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    gs = main_window.gui_structure
    gs.option_source_ground_temperature.set_value(0)

    gs.option_method_rb_calc.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.result_Rb_calculated.label.text() == 'Equivalent borehole thermal resistance: 0.0579 mK/W'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.15 °C'

    gs.option_fluid_selector.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.result_Rb_calculated.label.text() == 'Equivalent borehole thermal resistance: 0.0621 mK/W'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.25 °C'

    gs.option_glycol_selector.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.result_Rb_calculated.label.text() == 'Equivalent borehole thermal resistance: 0.0681 mK/W'
    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.38 °C'
    close_tests(main_window, qtbot)
