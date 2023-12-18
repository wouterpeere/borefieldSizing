from pathlib import Path
from sys import setrecursionlimit

import numpy as np

from GHEtool import FOLDER
from GHEtool.gui.data_2_borefield_func import _create_monthly_loads_peaks
from GHEtool.gui.gui_structure import load_data_GUI
from ScenarioGUI import load_config

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

load_config(Path(__file__).parent.joinpath("gui_config.ini"))

setrecursionlimit(1500)


def test_building_load(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.gui_structure.option_method_rb_calc.set_value(0)
    main_window.gui_structure.option_decimal_csv.set_value(0)
    main_window.gui_structure.option_seperator_csv.set_value(0)
    main_window.gui_structure.option_source_ground_temperature.set_value(0)

    main_window.gui_structure.option_filename.set_value(f'{FOLDER}/Examples/hourly_profile.csv')
    main_window.gui_structure.fun_update_combo_box_data_file(f'{FOLDER}/Examples/hourly_profile.csv')
    main_window.gui_structure.option_column.set_value(1)
    main_window.gui_structure.option_cooling_column.set_value(1)

    # load data
    main_window.save_scenario()
    peak_heating, peak_cooling = load_data_GUI(
        filename=main_window.list_ds[0].option_filename,
        thermal_demand=main_window.list_ds[0].option_column,
        heating_load_column=main_window.list_ds[0].option_heating_column_text,
        cooling_load_column=main_window.list_ds[0].option_cooling_column_text,
        combined=main_window.list_ds[0].option_single_column_text,
        sep=";" if main_window.list_ds[0].option_seperator_csv == 0 else ",",
        dec="." if main_window.list_ds[0].option_decimal_csv == 0 else ",",
        fac=1, hourly=True)

    # set optimize load profile
    main_window.gui_structure.aim_optimize.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    # check if the data is the same, because optimize load profile needs the building, not the ground data
    assert np.allclose(main_window.list_ds[0].results._building_load.hourly_cooling_load, peak_cooling)
    assert np.allclose(main_window.list_ds[0].results._building_load.hourly_heating_load, peak_heating)
    assert main_window.list_ds[0].results._building_load.simulation_period == 40

    # check if the resultTexts are correct
    gs = main_window.gui_structure
    main_window.display_results()

    assert gs.results_heating_load.label.text() == "Heating load on the borefield: 530633.0 kWh"
    assert gs.results_heating_peak_geo.label.text() == "with a peak of: 274.35 kW"
    assert gs.results_heating_load_percentage.label.text() == "This is 82.52 % of the heating load"
    assert gs.results_heating_ext.label.text() == "Heating load external: 112385.0 kWh"
    assert gs.results_heating_peak.label.text() == "with a peak of: 261.69 kW"
    assert gs.results_cooling_load.label.text() == "Cooling load on the borefield: 172688.0 kWh"
    assert gs.results_cooling_peak_geo.label.text() == "with a peak of: 120.17 kW"
    assert gs.results_cooling_load_percentage.label.text() == "This is 64.5 % of the cooling load"
    assert gs.results_cooling_ext.label.text() == "Cooling load external: 95056.0 kWh"
    assert gs.results_cooling_peak.label.text() == "with a peak of: 556.25 kW"

    # calculate with geothermal load
    main_window.gui_structure.aim_temp_profile.widget.click()
    main_window.gui_structure.geo_load.set_value(0)
    main_window.save_scenario()
    without_SCOP, without_SEER, without_SCOP_avg, without_SEER_avg = _create_monthly_loads_peaks(main_window.list_ds[-1])

    # calculate with building load
    main_window.gui_structure.geo_load.set_value(1)
    main_window.save_scenario()

    with_SCOP, with_SEER, with_SCOP_avg, with_SEER_avg = _create_monthly_loads_peaks(main_window.list_ds[-1])

    # check loads
    assert np.array_equal(with_SCOP, (1 - 1/4) * without_SCOP)
    assert np.array_equal(with_SEER, (1 + 1/3) * without_SEER)
    assert np.array_equal(with_SCOP_avg, (1 - 1 / 4) * without_SCOP_avg)
    assert np.array_equal(with_SEER_avg, (1 + 1 / 3) * without_SEER_avg)

    main_window.gui_structure.option_temperature_profile_hourly.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    # # check if the data is the same
    assert np.allclose(main_window.list_ds[0].results.load.hourly_cooling_load / (1 + 1/3), peak_cooling)
    assert np.allclose(main_window.list_ds[0].results.load.hourly_heating_load / (1 - 1/4), peak_heating)
    close_tests(main_window, qtbot)
