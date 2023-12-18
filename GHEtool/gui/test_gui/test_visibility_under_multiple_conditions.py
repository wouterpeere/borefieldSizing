"""
Test to see if the Rb* is calculated on the go
"""
import sys
from pathlib import Path

import numpy as np

from GHEtool import FOLDER
from ScenarioGUI import load_config

from GHEtool.gui.test_gui.starting_closing_tests import start_tests, close_tests

load_config(Path(__file__).parent.joinpath("gui_config.ini"))

sys.setrecursionlimit(1500)


def setup(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_method_rb_calc.set_value(0)
    gs.option_source_ground_temperature.set_value(0)
    return main_window, gs


def test_visibility_hourly_profile(qtbot):

    main_window, gs = setup(qtbot)
    assert not gs.option_temperature_profile_hourly.is_hidden()
    assert gs.option_method_size_depth.is_hidden()
    main_window.save_scenario()

    main_window.add_scenario()
    assert not gs.option_temperature_profile_hourly.is_hidden()
    assert gs.option_method_size_depth.is_hidden()
    gs.aim_req_depth.widget.click()

    assert gs.option_temperature_profile_hourly.is_hidden()
    assert not gs.option_method_size_depth.is_hidden()
    main_window.save_scenario()
    main_window.change_scenario(0)
    assert not gs.option_temperature_profile_hourly.is_hidden()
    assert gs.option_method_size_depth.is_hidden()
    close_tests(main_window, qtbot)


def test_visibility_non_constant_temperature(qtbot):

    main_window, gs = setup(qtbot)

    def check(value: int):
        assert not gs.option_source_ground_temperature.is_hidden()
        if value == 0:
            assert not gs.option_ground_temp.is_hidden()
            assert gs.option_ground_temp_gradient.is_hidden()
            assert gs.option_ground_heat_flux.is_hidden()
            assert gs.option_temp_gradient.is_hidden()
            assert gs.option_ground_database.is_hidden()
            assert gs.hint_ground_database.is_hidden()
            assert gs.hint_ground_flux_database.is_hidden()
            return
        if value == 1:
            assert gs.option_ground_temp.is_hidden()
            assert gs.option_ground_temp_gradient.is_hidden()
            assert gs.option_ground_heat_flux.is_hidden()
            assert gs.option_temp_gradient.is_hidden()
            assert not gs.option_ground_database.is_hidden()
            assert not gs.hint_ground_database.is_hidden()
            assert not gs.hint_ground_flux_database.is_hidden()
            return
        if value == 2:
            assert gs.option_ground_temp.is_hidden()
            assert not gs.option_ground_temp_gradient.is_hidden()
            assert not gs.option_ground_heat_flux.is_hidden()
            assert gs.option_temp_gradient.is_hidden()
            assert gs.option_ground_database.is_hidden()
            assert gs.hint_ground_database.is_hidden()
            assert gs.hint_ground_flux_database.is_hidden()
            return

        assert gs.option_ground_temp.is_hidden()
        assert not gs.option_ground_temp_gradient.is_hidden()
        assert gs.option_ground_heat_flux.is_hidden()
        assert not gs.option_temp_gradient.is_hidden()
        assert gs.option_ground_database.is_hidden()
        assert gs.hint_ground_database.is_hidden()
        assert gs.hint_ground_flux_database.is_hidden()
        return

    check(0)
    main_window.save_scenario()

    main_window.add_scenario()
    gs.option_source_ground_temperature.set_value(1)
    check(1)
    main_window.save_scenario()

    main_window.add_scenario()
    gs.option_source_ground_temperature.set_value(2)
    check(2)
    main_window.save_scenario()

    main_window.add_scenario()
    gs.option_flux_gradient.set_value(1)
    check(3)

    main_window.save_scenario()

    main_window.change_scenario(0)
    check(0)

    main_window.change_scenario(1)
    assert gs.hint_ground_database.label.text() == "The ground temperature at the selected location is: 9.5 °C"
    assert gs.hint_ground_flux_database.label.text() == "The geothermal heat flux at the selected location is: 0.08 W/m²"
    gs.option_ground_database.set_value(1)
    assert gs.hint_ground_database.label.text() == "The ground temperature at the selected location is: 10.4 °C"
    assert gs.hint_ground_flux_database.label.text() == "The geothermal heat flux at the selected location is: 0.08 W/m²"
    check(1)
    main_window.save_scenario()
    main_window.change_scenario(2)
    check(2)
    main_window.change_scenario(3)
    check(3)
    close_tests(main_window, qtbot)


def test_visibility_peak_length(qtbot):

    main_window, gs = setup(qtbot)

    def visible():
        assert not gs.option_len_peak_heating.is_hidden()
        assert not gs.option_len_peak_cooling.is_hidden()

    def invisible():
        assert gs.option_len_peak_heating.is_hidden()
        assert gs.option_len_peak_cooling.is_hidden()

    visible()
    main_window.gui_structure.option_filename.set_value(f'{FOLDER}/Examples/hourly_profile.csv')

    gs.option_temperature_profile_hourly.set_value(1)
    invisible()
    gs.aim_req_depth.widget.click()
    visible()
    gs.option_method_size_depth.set_value(2)
    invisible()
    gs.aim_optimize.widget.click()
    visible()

    main_window.save_scenario()
    main_window.add_scenario()
    visible()
    gs.aim_temp_profile.widget.click()
    invisible()
    main_window.save_scenario()

    main_window.change_scenario(0)
    visible()
    main_window.change_scenario(1)
    invisible()
    close_tests(main_window, qtbot)


def test_visibility_rb(qtbot):

    main_window, gs = setup(qtbot)

    assert not gs.category_constant_rb.is_hidden()
    assert gs.category_fluid_data.is_hidden()
    assert gs.category_pipe_data.is_hidden()
    main_window.save_scenario()

    main_window.add_scenario()
    gs.option_method_rb_calc.set_value(1)
    assert gs.category_constant_rb.is_hidden()
    assert not gs.category_fluid_data.is_hidden()
    assert not gs.category_pipe_data.is_hidden()
    main_window.save_scenario()

    main_window.change_scenario(0)
    assert not gs.category_constant_rb.is_hidden()
    assert gs.category_fluid_data.is_hidden()
    assert gs.category_pipe_data.is_hidden()
    close_tests(main_window, qtbot)


def test_visibility_rb_autosave(qtbot):
    main_window, gs = setup(qtbot)

    main_window.save_scenario()  # needed in ScenarioGUI v0.3.0.2 due to a bug (issue 144)
    gs.option_auto_saving.set_value(1)
    gs.option_method_rb_calc.set_value(0)

    assert not gs.category_constant_rb.is_hidden()
    assert gs.category_fluid_data.is_hidden()
    assert gs.category_pipe_data.is_hidden()

    main_window.add_scenario()
    gs.option_method_rb_calc.set_value(1)
    assert gs.category_constant_rb.is_hidden()
    assert not gs.category_fluid_data.is_hidden()
    assert not gs.category_pipe_data.is_hidden()

    main_window.change_scenario(0)
    assert not gs.category_constant_rb.is_hidden()
    assert gs.category_fluid_data.is_hidden()
    assert gs.category_pipe_data.is_hidden()
    close_tests(main_window, qtbot)


def test_visibility_pipe_options(qtbot):

    main_window, gs = setup(qtbot)
    gs.option_auto_saving.set_value(1)

    gs.option_method_rb_calc.set_value(1)
    assert gs.option_pipe_coaxial_inner_inner.is_hidden()
    assert gs.option_pipe_coaxial_inner_outer.is_hidden()
    assert gs.option_pipe_coaxial_outer_inner.is_hidden()
    assert gs.option_pipe_coaxial_outer_outer.is_hidden()
    assert not gs.option_pipe_inner_radius.is_hidden()
    assert not gs.option_pipe_outer_radius.is_hidden()
    assert not gs.option_pipe_number.is_hidden()
    assert not gs.option_pipe_distance.is_hidden()

    gs.option_U_pipe_or_coaxial_pipe.set_value(1)
    assert not gs.option_pipe_coaxial_inner_inner.is_hidden()
    assert not gs.option_pipe_coaxial_inner_outer.is_hidden()
    assert not gs.option_pipe_coaxial_outer_inner.is_hidden()
    assert not gs.option_pipe_coaxial_outer_outer.is_hidden()
    assert gs.option_pipe_inner_radius.is_hidden()
    assert gs.option_pipe_outer_radius.is_hidden()
    assert gs.option_pipe_number.is_hidden()
    assert gs.option_pipe_distance.is_hidden()

    main_window.add_scenario()
    gs.option_U_pipe_or_coaxial_pipe.set_value(0)
    assert gs.option_pipe_coaxial_inner_inner.is_hidden()
    assert gs.option_pipe_coaxial_inner_outer.is_hidden()
    assert gs.option_pipe_coaxial_outer_inner.is_hidden()
    assert gs.option_pipe_coaxial_outer_outer.is_hidden()
    assert not gs.option_pipe_inner_radius.is_hidden()
    assert not gs.option_pipe_outer_radius.is_hidden()
    assert not gs.option_pipe_number.is_hidden()
    assert not gs.option_pipe_distance.is_hidden()

    main_window.add_scenario()
    gs.option_method_rb_calc.set_value(0)
    assert gs.category_pipe_data.is_hidden()

    main_window.change_scenario(0)
    assert not gs.option_pipe_coaxial_inner_inner.is_hidden()
    assert not gs.option_pipe_coaxial_inner_outer.is_hidden()
    assert not gs.option_pipe_coaxial_outer_inner.is_hidden()
    assert not gs.option_pipe_coaxial_outer_outer.is_hidden()
    assert gs.option_pipe_inner_radius.is_hidden()
    assert gs.option_pipe_outer_radius.is_hidden()
    assert gs.option_pipe_number.is_hidden()
    assert gs.option_pipe_distance.is_hidden()
    close_tests(main_window, qtbot)


def test_visibility_load(qtbot):

    main_window, gs = setup(qtbot)
    gs.option_auto_saving.set_value(1)

    def visible():
        assert not gs.button_load_csv.is_hidden()
        assert not gs.hint_press_load.is_hidden()
        assert not gs.category_th_demand.is_hidden()

    def invisible():
        assert gs.button_load_csv.is_hidden()
        assert gs.hint_press_load.is_hidden()
        assert gs.category_th_demand.is_hidden()

    assert gs.option_heating_column.is_hidden()
    assert gs.option_cooling_column.is_hidden()
    assert not gs.option_single_column.is_hidden()
    gs.option_column.set_value(1)
    assert not gs.option_heating_column.is_hidden()
    assert not gs.option_cooling_column.is_hidden()
    assert gs.option_single_column.is_hidden()

    visible()
    gs.option_temperature_profile_hourly.set_value(1)
    invisible()
    gs.option_temperature_profile_hourly.set_value(0)
    visible()
    gs.aim_req_depth.widget.click()
    visible()
    gs.option_method_size_depth.set_value(2)
    invisible()
    gs.aim_temp_profile.widget.click()
    visible()
    gs.aim_optimize.widget.click()
    invisible()
    gs.aim_req_depth.widget.click()
    invisible()
    close_tests(main_window, qtbot)


def test_visibility_SCOP(qtbot):

    main_window, gs = setup(qtbot)

    def visible():
        assert not gs.SCOP.is_hidden()
        assert not gs.SEER.is_hidden()

    def invisible():
        assert gs.SCOP.is_hidden()
        assert gs.SEER.is_hidden()

    gs.option_include_dhw.set_value(1)

    invisible()
    gs.geo_load.set_value(1)
    visible()
    main_window.save_scenario()

    main_window.add_scenario()
    visible()
    gs.geo_load.set_value(0)
    invisible()

    gs.aim_optimize.widget.click()
    visible()
    gs.aim_temp_profile.widget.click()
    main_window.save_scenario()
    main_window.change_scenario(0)
    visible()
    close_tests(main_window, qtbot)


def test_visibility_dhw(qtbot):

    main_window, gs = setup(qtbot)

    assert not gs.option_include_dhw.is_hidden()
    assert gs.DHW.is_hidden()
    assert gs.SCOP_DHW.is_hidden()

    gs.option_include_dhw.set_value(1)
    assert not gs.DHW.is_hidden()
    assert gs.SCOP_DHW.is_hidden()

    gs.geo_load.set_value(1)
    assert not gs.DHW.is_hidden()
    assert not gs.SCOP_DHW.is_hidden()

    gs.aim_optimize.widget.click()
    assert gs.DHW.is_hidden()
    assert gs.SCOP_DHW.is_hidden()
    close_tests(main_window, qtbot)


def test_visibility_on_result_page(qtbot):
    """
    This function tests options on the result page for their visibility.
    This is done by creating multiple scenario's, calculating all of them and then checking the visibility.

    These scenarios are:
    1) default
    2) default + flux
    3) default + gradient
    4) default + pipe
    5) default + hourly
    6) default + size depth
    7) default + size depth (hourly)
    8) optimize

    """
    main_window, gs = setup(qtbot)

    gs.option_filename.set_value(f'{FOLDER}/Examples/hourly_profile.csv')

    # scenario 2
    main_window.save_scenario()
    main_window.add_scenario()
    gs.option_source_ground_temperature.set_value(2)
    # scenario 3
    main_window.save_scenario()
    main_window.add_scenario()
    gs.option_flux_gradient.set_value(1)
    # scenario 4
    main_window.save_scenario()
    main_window.add_scenario()
    gs.option_source_ground_temperature.set_value(0)
    gs.option_method_rb_calc.set_value(1)
    # scenario 5
    main_window.save_scenario()
    main_window.add_scenario()
    gs.option_method_rb_calc.set_value(0)
    gs.option_temperature_profile_hourly.set_value(1)
    # scenario 6
    main_window.save_scenario()
    main_window.add_scenario()
    gs.aim_req_depth.widget.click()
    # scenario 7
    main_window.save_scenario()
    main_window.add_scenario()
    gs.option_method_size_depth.set_value(2)
    # scenario 8
    main_window.save_scenario()
    main_window.add_scenario()
    gs.option_method_size_depth.set_value(0)
    gs.aim_optimize.widget.click()

    main_window.start_multiple_scenarios_calculation()
    # thread = main_window.threads[-1]
    _ = [thread.run() for thread in main_window.threads]
    # assert thread.calculated
    qtbot.wait(10000)

    list_options_optimize_load_profile = [gs.results_heating_ext, gs.results_heating_peak_geo,
                                          gs.results_heating_load_percentage, gs.results_heating_load,
                                          gs.results_heating_peak, gs.results_cooling_ext,
                                          gs.results_cooling_load_percentage, gs.results_cooling_load,
                                          gs.results_cooling_peak, gs.results_cooling_peak_geo]

    # go over all the scenario's and check correct visibility
    # scenario 1
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert gs.result_text_depth.is_hidden()
    assert gs.results_ground_temperature.is_hidden()
    assert gs.hourly_figure_temperature_profile.is_hidden()
    assert gs.figure_load_duration.is_hidden()
    assert not gs.max_temp.is_hidden()
    assert not gs.min_temp.is_hidden()
    assert gs.max_temp.label.text() == "The maximum average fluid temperature is 16.64 °C"
    assert gs.min_temp.label.text() == "The minimum average fluid temperature is 3.15 °C"

    # scenario 2
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert gs.result_text_depth.is_hidden()
    assert gs.hourly_figure_temperature_profile.is_hidden()
    assert gs.figure_load_duration.is_hidden()
    assert not gs.max_temp.is_hidden()
    assert not gs.min_temp.is_hidden()
    assert gs.max_temp.label.text() == "The maximum average fluid temperature is 16.64 °C"
    assert gs.min_temp.label.text() == "The minimum average fluid temperature is 3.15 °C"
    assert not gs.results_ground_temperature.is_hidden()
    assert gs.results_ground_temperature.label.text() == "Average ground temperature: 12.0 °C"

    # scenario 3
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(2))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert gs.result_text_depth.is_hidden()
    assert gs.hourly_figure_temperature_profile.is_hidden()
    assert gs.figure_load_duration.is_hidden()
    assert not gs.max_temp.is_hidden()
    assert not gs.min_temp.is_hidden()
    assert gs.max_temp.label.text() == "The maximum average fluid temperature is 16.14 °C"
    assert gs.min_temp.label.text() == "The minimum average fluid temperature is 2.65 °C"
    assert not gs.results_ground_temperature.is_hidden()
    assert gs.results_ground_temperature.label.text() == "Average ground temperature: 11.5 °C"

    # scenario 4
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(3))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_text_depth.is_hidden()
    assert gs.hourly_figure_temperature_profile.is_hidden()
    assert gs.figure_load_duration.is_hidden()
    assert not gs.max_temp.is_hidden()
    assert not gs.min_temp.is_hidden()
    assert gs.max_temp.label.text() == "The maximum average fluid temperature is 16.15 °C"
    assert gs.min_temp.label.text() == "The minimum average fluid temperature is 3.47 °C"
    assert gs.results_ground_temperature.is_hidden()
    assert gs.result_Rb_calculated.label.text() == "Equivalent borehole thermal resistance: 0.0579 mK/W"
    assert gs.result_Reynolds.label.text() == "Reynolds number: 7958.0 "

    # scenario 5
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(4))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert gs.result_text_depth.is_hidden()
    assert not gs.hourly_figure_temperature_profile.is_hidden()
    assert not gs.figure_load_duration.is_hidden()
    assert not gs.max_temp.is_hidden()
    assert not gs.min_temp.is_hidden()
    assert gs.max_temp.label.text() == "The maximum average fluid temperature is 24.82 °C"
    assert gs.min_temp.label.text() == "The minimum average fluid temperature is -14.93 °C"
    assert gs.results_ground_temperature.is_hidden()

    # scenario 6
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(5))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert not gs.result_text_depth.is_hidden()
    assert gs.result_text_depth.label.text() == "Depth: 317.61 m"
    assert gs.hourly_figure_temperature_profile.is_hidden()
    assert gs.figure_load_duration.is_hidden()
    assert gs.max_temp.is_hidden()
    assert gs.min_temp.is_hidden()
    assert gs.results_ground_temperature.is_hidden()

    # scenario 7
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(6))
    main_window.display_results()
    assert np.all([option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert not gs.result_text_depth.is_hidden()
    assert gs.result_text_depth.label.text() == "Depth: 323.5 m"
    assert not gs.hourly_figure_temperature_profile.is_hidden()
    assert not gs.figure_load_duration.is_hidden()
    assert gs.max_temp.is_hidden()
    assert gs.min_temp.is_hidden()
    assert gs.results_ground_temperature.is_hidden()

    # scenario 8
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(7))
    main_window.display_results()
    assert np.all([not option.is_hidden() for option in list_options_optimize_load_profile])
    assert gs.result_Rb_calculated.is_hidden()
    assert gs.result_Reynolds.is_hidden()
    assert gs.result_text_depth.is_hidden()
    assert not gs.hourly_figure_temperature_profile.is_hidden()
    assert not gs.figure_load_duration.is_hidden()
    assert gs.max_temp.is_hidden()
    assert gs.min_temp.is_hidden()
    assert gs.results_ground_temperature.is_hidden()
    close_tests(main_window, qtbot)
