from GHEtool import FOLDER
from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests


def test_results_DHW(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    gs = main_window.gui_structure
    gs.option_source_ground_temperature.set_value(0)
    gs.option_method_rb_calc.set_value(0)

    gs.aim_optimize.widget.click()
    main_window.gui_structure.option_decimal_csv.set_value(0)
    main_window.gui_structure.option_seperator_csv.set_value(0)

    main_window.gui_structure.option_filename.set_value(f'{FOLDER}/Examples/hourly_profile.csv')
    main_window.gui_structure.fun_update_combo_box_data_file(f'{FOLDER}/Examples/hourly_profile.csv')
    main_window.gui_structure.option_column.set_value(1)
    main_window.gui_structure.option_cooling_column.set_value(1)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.results_heating_load.label.text() == "Heating load on the borefield: 530633.0 kWh"

    gs.aim_temp_profile.widget.click()
    gs.geo_load.set_value(0)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.64 °C'
    assert gs.min_temp.label.text() == 'The minimum average fluid temperature is 3.15 °C'

    gs.option_include_dhw.set_value(1)
    gs.DHW.set_value(8760)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 16.59 °C'
    assert gs.min_temp.label.text() == 'The minimum average fluid temperature is 2.8 °C'

    gs.geo_load.set_value(1)
    gs.option_include_dhw.set_value(0)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 18.53 °C'
    assert gs.min_temp.label.text() == 'The minimum average fluid temperature is 8.79 °C'

    gs.option_include_dhw.set_value(1)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 18.5 °C'
    assert gs.min_temp.label.text() == 'The minimum average fluid temperature is 8.55 °C'

    gs.option_temperature_profile_hourly.set_value(1)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 29.77 °C'
    assert gs.min_temp.label.text() == 'The minimum average fluid temperature is -2.87 °C'

    gs.option_include_dhw.set_value(0)

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.max_temp.label.text() == 'The maximum average fluid temperature is 29.81 °C'
    assert gs.min_temp.label.text() == 'The minimum average fluid temperature is -2.64 °C'

    gs.option_include_dhw.set_value(1)

    # check again optimize that it is not changed
    gs.aim_optimize.widget.click()

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()

    assert gs.results_heating_load.label.text() == "Heating load on the borefield: 530633.0 kWh"

    close_tests(main_window, qtbot)

