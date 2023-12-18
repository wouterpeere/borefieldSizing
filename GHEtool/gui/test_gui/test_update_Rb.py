"""
Test to see if the Rb* is calculated on the go
"""
import sys
from pathlib import Path

from ScenarioGUI import load_config

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

load_config(Path(__file__).parent.joinpath("gui_config.ini"))

sys.setrecursionlimit(1500)


def test_pipe_right_options_shown(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(0)
    assert gs.category_pipe_data.is_hidden()
    gs.option_method_rb_calc.set_value(1)
    gs.page_borehole_resistance.button.click()
    assert not gs.option_U_pipe_or_coaxial_pipe.is_hidden()
    assert not gs.option_pipe_inner_radius.is_hidden()
    assert not gs.option_pipe_outer_radius.is_hidden()
    assert not gs.option_pipe_conductivity.is_hidden()
    assert not gs.option_pipe_distance.is_hidden()
    assert not gs.option_pipe_number.is_hidden()
    assert not gs.option_pipe_roughness.is_hidden()
    assert not gs.option_pipe_borehole_radius_2.is_hidden()
    assert not gs.option_pipe_grout_conductivity.is_hidden()
    assert gs.option_pipe_coaxial_inner_inner.is_hidden()
    assert gs.option_pipe_coaxial_inner_outer.is_hidden()
    assert gs.option_pipe_coaxial_outer_inner.is_hidden()
    assert gs.option_pipe_coaxial_outer_outer.is_hidden()

    gs.option_U_pipe_or_coaxial_pipe.set_value(1)
    assert gs.option_pipe_inner_radius.is_hidden()
    assert gs.option_pipe_outer_radius.is_hidden()
    assert not gs.option_pipe_conductivity.is_hidden()
    assert gs.option_pipe_distance.is_hidden()
    assert gs.option_pipe_number.is_hidden()
    assert not gs.option_pipe_grout_conductivity.is_hidden()
    assert not gs.option_pipe_roughness.is_hidden()
    assert not gs.option_pipe_borehole_radius_2.is_hidden()
    assert not gs.option_pipe_coaxial_inner_inner.is_hidden()
    assert not gs.option_pipe_coaxial_inner_outer.is_hidden()
    assert not gs.option_pipe_coaxial_outer_inner.is_hidden()
    assert not gs.option_pipe_coaxial_outer_outer.is_hidden()
    close_tests(main_window, qtbot)


def test_Rb_calculated_when_value_changed_U_pipe(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(0)
    assert gs.category_pipe_data.is_hidden()
    gs.option_method_rb_calc.set_value(1)
    gs.page_borehole_resistance.button.click()
    assert not gs.category_pipe_data.is_hidden()

    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0579 mK/W'
    gs.option_conductivity.set_value(2.5)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.058 mK/W'
    gs.option_depth.set_value(160)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0686 mK/W'
    gs.option_fluid_conductivity.set_value(0.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0684 mK/W'
    gs.option_fluid_density.set_value(2000)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0684 mK/W'
    gs.option_fluid_capacity.set_value(4000)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.07 mK/W'
    gs.option_fluid_viscosity.set_value(0.002)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.071 mK/W'
    gs.option_fluid_mass_flow.set_value(0.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.065 mK/W'
    gs.option_pipe_number.set_value(1)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0839 mK/W'
    gs.option_pipe_grout_conductivity.set_value(1.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0806 mK/W'
    gs.option_pipe_conductivity.set_value(0.44)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0798 mK/W'
    gs.option_pipe_inner_radius.set_value(0.021)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0709 mK/W'
    gs.option_pipe_outer_radius.set_value(0.023)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0769 mK/W'
    gs.option_pipe_borehole_radius_2.set_value(0.076)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0783 mK/W'
    gs.option_pipe_distance.set_value(0.041)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.077 mK/W'
    gs.option_pipe_roughness.set_value(0.00002)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0769 mK/W'
    close_tests(main_window, qtbot)


def test_Rb_calculated_when_value_changed_coaxial(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(0)
    assert gs.category_pipe_data.is_hidden()

    gs.option_method_rb_calc.set_value(1)
    gs.page_borehole_resistance.button.click()
    assert not gs.pipe_thermal_resistance.is_hidden()
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0579 mK/W'
    gs.option_U_pipe_or_coaxial_pipe.set_value(1)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0984 mK/W'
    gs.option_depth.set_value(160)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1116 mK/W'
    gs.option_fluid_conductivity.set_value(0.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1109 mK/W'
    gs.option_fluid_density.set_value(2000)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1109 mK/W'
    gs.option_fluid_capacity.set_value(4000)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.113 mK/W'
    gs.option_fluid_viscosity.set_value(0.002)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1516 mK/W'
    gs.option_fluid_mass_flow.set_value(0.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1197 mK/W'
    gs.option_pipe_grout_conductivity.set_value(1.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1177 mK/W'
    gs.option_pipe_conductivity.set_value(0.44)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1159 mK/W'

    gs.option_pipe_coaxial_inner_inner.set_value(0.022)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1195 mK/W'
    gs.option_pipe_coaxial_inner_outer.set_value(0.026)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1185 mK/W'
    gs.option_pipe_coaxial_outer_inner.set_value(0.052)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1032 mK/W'
    gs.option_pipe_coaxial_outer_outer.set_value(0.06)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1253 mK/W'

    gs.option_pipe_borehole_radius_2.set_value(0.076)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1266 mK/W'
    gs.option_pipe_roughness.set_value(0.00002)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.1265 mK/W'

    import pygfunction as gt
    k_g = 1.0  # Grout thermal conductivity [W/m.K]
    k_p = 0.4  # Pipe thermal conductivity [W/m.K]
    r_in_in = 0.0221  # Inside pipe inner radius [m]
    r_in_out = 0.025  # Inside pipe outer radius [m]
    r_out_in = 0.0487  # Outer pipe inside radius [m]
    r_out_out = 0.055  # Outer pipe outside radius [m]
    # init gui window
    close_tests(main_window, qtbot)
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(1)
    gs.page_borehole_resistance.button.click()
    gs.option_U_pipe_or_coaxial_pipe.set_value(1)
    fluid = gt.media.Fluid('MPG', 20.)
    gs.option_fluid_conductivity.set_value(fluid.k)
    gs.option_fluid_density.set_value(fluid.rho)
    gs.option_fluid_capacity.set_value(fluid.cp)
    gs.option_fluid_viscosity.set_value(fluid.mu)
    gs.option_fluid_mass_flow.set_value(0.5)
    gs.option_pipe_grout_conductivity.set_value(k_g)
    gs.option_pipe_conductivity.set_value(k_p)

    gs.option_pipe_coaxial_inner_inner.set_value(r_in_in)
    gs.option_pipe_coaxial_inner_outer.set_value(r_in_out)
    gs.option_pipe_coaxial_outer_inner.set_value(r_out_in)
    gs.option_pipe_coaxial_outer_outer.set_value(r_out_out)
    gs.option_pipe_borehole_radius_2.set_value(0.075)

    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.1737 mK/W'
    close_tests(main_window, qtbot)


def test_correct_fluid_options_shown(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(0)

    assert gs.category_fluid_data.is_hidden()
    gs.option_method_rb_calc.set_value(1)
    assert not gs.category_fluid_data.is_hidden()
    assert not gs.option_fluid_capacity.is_hidden()
    assert not gs.option_fluid_conductivity.is_hidden()
    assert not gs.option_fluid_density.is_hidden()
    assert not gs.option_fluid_viscosity.is_hidden()
    assert not gs.option_fluid_selector.is_hidden()
    assert not gs.option_fluid_mass_flow.is_hidden()
    assert gs.option_glycol_selector.is_hidden()
    assert gs.option_glycol_percentage.is_hidden()
    assert gs.option_fluid_ref_temp.is_hidden()

    gs.option_fluid_selector.set_value(1)
    assert not gs.category_fluid_data.is_hidden()
    assert gs.option_fluid_capacity.is_hidden()
    assert gs.option_fluid_conductivity.is_hidden()
    assert gs.option_fluid_density.is_hidden()
    assert gs.option_fluid_viscosity.is_hidden()
    assert not gs.option_fluid_selector.is_hidden()
    assert not gs.option_fluid_mass_flow.is_hidden()
    assert not gs.option_glycol_selector.is_hidden()
    assert not gs.option_glycol_percentage.is_hidden()
    assert not gs.option_fluid_ref_temp.is_hidden()

    gs.option_fluid_selector.set_value(0)
    gs.page_borehole_resistance.button.click()
    assert not gs.pipe_thermal_resistance.is_hidden()
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0579 mK/W'
    gs.option_fluid_selector.set_value(1)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0621 mK/W'
    gs.option_glycol_percentage.set_value(10)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0595 mK/W'
    gs.option_fluid_ref_temp.set_value(15)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0591 mK/W'
    gs.option_glycol_selector.set_value(1)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0593 mK/W'
    gs.option_glycol_percentage.set_value(20)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0627 mK/W'
    gs.option_fluid_ref_temp.set_value(10)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0681 mK/W'
    close_tests(main_window, qtbot)
