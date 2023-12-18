import os
from pathlib import Path
from sys import setrecursionlimit

import numpy as np
from GHEtool import FOLDER
from GHEtool.gui.data_2_borefield_func import data_2_borefield
from GHEtool.gui.gui_structure import load_data_GUI
from ScenarioGUI.gui_classes.gui_structure_classes import ListBox
from pytest import raises

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

setrecursionlimit(1500)

from ScenarioGUI import load_config

load_config(Path(__file__).parent.joinpath("gui_config.ini"))


def test_language(qtbot):
    """
    test if the language is changed correctly
    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    from GHEtool.gui.translation_csv_to_py import main

    main()

    # init gui window
    main_window = start_tests(qtbot)

    for idx, action in enumerate(main_window.menu_language.actions()):
        action.trigger()
        assert main_window.gui_structure.option_language.get_value()[0] == idx

    main_window.menu_language.actions()[0].trigger()
    close_tests(main_window, qtbot)


def test_wrong_results_shown(qtbot):
    """
    test if results are shown correctly.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.show()
    main_window.gui_structure.option_method_rb_calc.set_value(0)
    main_window.gui_structure.option_decimal_csv.set_value(0)
    main_window.gui_structure.option_seperator_csv.set_value(0)

    main_window.gui_structure.option_filename.set_value(f'{FOLDER}/Examples/hourly_profile.csv')
    assert main_window.gui_structure.option_cooling_column.get_value()[0] == 1
    assert main_window.gui_structure.option_column.get_value() == 1
    main_window.gui_structure.option_decimal_csv.set_value(1)
    main_window.gui_structure.option_seperator_csv.set_value(1)
    main_window.gui_structure.fun_update_combo_box_data_file(f'{FOLDER}/Examples/hourly_profile.csv')
    assert main_window.status_bar.label.text() == 'Please make sure the seperator and decimal point are different.'
    main_window.gui_structure.option_decimal_csv.set_value(0)
    main_window.gui_structure.option_seperator_csv.set_value(0)
    main_window.gui_structure.option_column.set_value(1)
    main_window.gui_structure.option_cooling_column.set_value(1)

    main_window.gui_structure.aim_optimize.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert not main_window.gui_structure.hourly_figure_temperature_profile.is_hidden()
    assert main_window.gui_structure.result_Rb_calculated.is_hidden()
    assert not main_window.gui_structure.figure_load_duration.is_hidden()
    main_window.gui_structure.page_aim.button.click()
    main_window.gui_structure.page_result.button.click()

    main_window.gui_structure.option_method_rb_calc.set_value(1)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert not main_window.gui_structure.hourly_figure_temperature_profile.is_hidden()
    assert not main_window.gui_structure.result_Rb_calculated.is_hidden()

    main_window.add_scenario()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert not main_window.gui_structure.hourly_figure_temperature_profile.is_hidden()
    assert not main_window.gui_structure.result_Rb_calculated.is_hidden()
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    assert not main_window.gui_structure.hourly_figure_temperature_profile.is_hidden()
    assert not main_window.gui_structure.result_Rb_calculated.is_hidden()
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert not main_window.gui_structure.hourly_figure_temperature_profile.is_hidden()
    assert not main_window.gui_structure.result_Rb_calculated.is_hidden()
    close_tests(main_window, qtbot)


def test_wrong_results_shown_2(qtbot):
    """
    test if results are shown correctly.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.add_scenario()
    assert main_window.gui_structure.option_temperature_profile_hourly.get_value() < 1
    assert main_window.gui_structure.option_method_size_depth.get_value() < 1
    if not main_window.gui_structure.aim_temp_profile.is_checked():  # pragma: no cover
        main_window.gui_structure.aim_temp_profile.widget.click()
    main_window.save_scenario()
    ds = main_window.list_ds[-1]
    assert ds.option_temperature_profile_hourly < 1
    assert ds.option_method_size_depth < 1
    assert ds.aim_temp_profile
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.display_results()
    assert main_window.gui_structure.hourly_figure_temperature_profile.is_hidden()

    main_window._save_to_data("hello/not_there.GHEtool")
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[main_window.gui_structure.option_language.get_value()[0]]
    close_tests(main_window, qtbot)


def test_backward_compatibility(qtbot):
    """
    test if the GUI is importing old files correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    import numpy as np
    from GHEtool import FOLDER
    # check results None works
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    main_window.load_backup()
    assert main_window.list_ds[0].results is None
    main_window._load_from_data("no_file")
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[0]
    close_tests(main_window, qtbot)

    # init gui window
    main_window_old = start_tests(qtbot)

    # test cannot load old data
    assert not main_window_old._load_from_data(f'{FOLDER}/gui/test_gui/test_file_version_2_1_0.GHEtool')

    assert main_window_old._load_from_data(f'{FOLDER}/gui/test_gui/test_file_version_2_1_1.GHEtool')
    # init gui window
    main_window_new = start_tests(qtbot)
    assert main_window_new._load_from_data(f'{FOLDER}/gui/test_gui/test_file_version_2_2_0.GHEtool')
    # check if the imported values are the same
    for ds_old, ds_new in zip(main_window_old.list_ds, main_window_new.list_ds):
        ds_new.borefield_file = ds_old.borefield_file
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), int) and isinstance(getattr(ds_new, option), list):  # pragma: no cover
                # listboxes are saved differently from v2.2.0 onwards
                assert getattr(ds_old, option) == getattr(ds_new, option)[0]
                continue
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    # init gui window
    close_tests(main_window_new, qtbot)
    close_tests(main_window_old, qtbot)
    main_window_new = start_tests(qtbot)
    main_window_new._load_from_data(f'{FOLDER}/gui/test_gui/test_file_version_999_1_1.GHEtool')
    assert main_window_new.status_bar.label.text() == main_window_new.translations.cannot_load_new_version[0]
    close_tests(main_window_new, qtbot)


def test_datastorage(qtbot):
    """
    tests the datastorage
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    main_window.add_scenario()
    assert main_window.list_ds[0] != 2
    assert main_window.list_ds[0] == main_window.list_ds[1]
    val_old = main_window.list_ds[1].option_depth
    main_window.list_ds[1].option_depth = 1
    assert main_window.list_ds[1] != main_window.list_ds[0]
    main_window.list_ds[1].option_depth = val_old
    assert main_window.list_ds[0] == main_window.list_ds[1]
    main_window.list_ds[1].list_options_aims.append('no_real_option')
    assert main_window.list_ds[1] != main_window.list_ds[0]
    close_tests(main_window, qtbot)


def test_no_valid_value(qtbot) -> None:
    """
    test no valid value

    Parameters
    ----------
    qtbot: qtbot
        qtbot
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    gs = main_window.gui_structure
    gs.aim_req_depth.widget.click() if not gs.aim_req_depth.widget.isChecked() else None
    gs.option_method_size_depth.set_value(2)
    gs.option_filename.widget.setText("")
    assert not main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    main_window.start_multiple_scenarios_calculation()
    close_tests(main_window, qtbot)


def test_value_error(qtbot) -> None:
    """
    test value error caption

    Parameters
    ----------
    qtbot: qtbot
        qtbot
    """
    # init gui window
    main_window = start_tests(qtbot)
    gs = main_window.gui_structure

    gs.aim_temp_profile.widget.click() if not gs.aim_temp_profile.widget.isChecked() else None
    gs.option_depth.widget.setMinimum(-500)
    gs.option_depth.minimal_value = -500
    gs.option_depth.set_value(-100)
    main_window.save_scenario()
    borefield, func = data_2_borefield(main_window.list_ds[-1])
    with raises(ValueError) as err:
        func()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    for figure in main_window.gui_structure.list_of_result_figures:
        assert figure[0].is_hidden()

    main_window.check_results()
    assert f'{main_window.list_ds[-1].debug_message}' == f'{err.value}' 
    close_tests(main_window, qtbot)

def test_load_data_gui_errors():
    """
    test the load gui errors.
    """
    with raises(FileNotFoundError):
        load_data_GUI("", 0, 'Heating', 'Cooling', 'Heating', ';', '.', 1)
    with raises(FileNotFoundError):
        load_data_GUI("no_existing_file.csv", 0, 'Heating', 'Cooling', 'Heating', ';', '.', 1)
    with raises(ValueError):
        load_data_GUI("no_existing_file.csv", 0, 'Heating', 'Heating', 'Heating', ';', '.', 1)
    with raises(ValueError):
        load_data_GUI(FOLDER.joinpath("Examples/hourly_profile.csv"), 0, "Heating", "Cooling", "Heating", ",", ".", 1, False)


def test_file_import_errors(qtbot):
    from pandas import DataFrame, Series, date_range, read_csv, to_datetime
    # init gui window
    main_window = start_tests(qtbot)
    g_s = main_window.gui_structure
    g_s.option_filename.set_value("")
    main_window.gui_structure.fun_display_data()
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[0]

    g_s.option_filename.set_value(f'{FOLDER.joinpath("Examples/hourly_profile.csv")}')
    g_s.fun_update_combo_box_data_file(f'{FOLDER.joinpath("Examples/hourly_profile.csv")}')
    g_s.option_single_column.widget.addItem('No Existing Column')
    g_s.option_single_column.set_value(-1)
    g_s.option_column.set_value(0)
    main_window.gui_structure.fun_display_data()
    assert main_window.status_bar.label.text() == main_window.translations.ColumnError[0]
    g_s.option_single_column.set_value(0)
    g_s.option_heating_column.set_value(0)
    g_s.option_cooling_column.set_value(1)
    g_s.option_filename.set_value(f'{FOLDER.joinpath("Examples/hourly_profile_wrong.csv")}')
    main_window.gui_structure.fun_display_data()
    assert main_window.status_bar.label.text() == main_window.translations.ValueError[0]

    g_s.option_filename.set_value(f'{FOLDER.joinpath("Examples/hourly_profile.csv")}')
    g_s.fun_update_combo_box_data_file(f'{FOLDER.joinpath("Examples/hourly_profile.csv")}')
    g_s.option_column.set_value(1)
    g_s.option_single_column.set_value(0)
    g_s.option_heating_column.set_value(0)
    g_s.option_cooling_column.set_value(1)
    data = read_csv(FOLDER.joinpath("Examples/hourly_profile.csv"), sep=";", decimal=".")
    data_new = DataFrame()
    start = to_datetime("2019-01-01 00:00:00")
    end = to_datetime("2019-12-31 23:59:00")
    # add date column
    data_new["Date"] = Series(date_range(start, end, freq="1H"))
    data_new = data_new.set_index("Date")
    data_new["Heating Load"] = data["Heating"].to_numpy()
    data_new["Cooling Load"] = data["Cooling"].to_numpy()
    data_new["Heating peak"] = data["Heating"].to_numpy()
    data_new["Cooling peak"] = data["Cooling"].to_numpy()
    data_new = data_new.resample("M").agg({"Heating Load": "sum", "Cooling Load": "sum", "Heating peak": "max", "Cooling peak": "max"})
    main_window.gui_structure.fun_display_data()
    assert np.isclose(data_new["Heating peak"][0], g_s.option_hp_jan.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][1], g_s.option_hp_feb.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][2], g_s.option_hp_mar.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][3], g_s.option_hp_apr.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][4], g_s.option_hp_may.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][5], g_s.option_hp_jun.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][6], g_s.option_hp_jul.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][7], g_s.option_hp_aug.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][8], g_s.option_hp_sep.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][9], g_s.option_hp_oct.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][10], g_s.option_hp_nov.get_value(), atol=0.01)
    assert np.isclose(data_new["Heating peak"][11], g_s.option_hp_dec.get_value(), atol=0.01)

    assert np.isclose(data_new["Cooling peak"][0], g_s.option_cp_jan.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][1], g_s.option_cp_feb.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][2], g_s.option_cp_mar.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][3], g_s.option_cp_apr.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][4], g_s.option_cp_may.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][5], g_s.option_cp_jun.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][6], g_s.option_cp_jul.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][7], g_s.option_cp_aug.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][8], g_s.option_cp_sep.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][9], g_s.option_cp_oct.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][10], g_s.option_cp_nov.get_value(), atol=0.01)
    assert np.isclose(data_new["Cooling peak"][11], g_s.option_cp_dec.get_value(), atol=0.01)

    assert np.isclose(data_new["Heating Load"][0], g_s.option_hl_jan.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][1], g_s.option_hl_feb.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][2], g_s.option_hl_mar.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][3], g_s.option_hl_apr.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][4], g_s.option_hl_may.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][5], g_s.option_hl_jun.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][6], g_s.option_hl_jul.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][7], g_s.option_hl_aug.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][8], g_s.option_hl_sep.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][9], g_s.option_hl_oct.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][10], g_s.option_hl_nov.get_value(), atol=1)
    assert np.isclose(data_new["Heating Load"][11], g_s.option_hl_dec.get_value(), atol=1)

    assert np.isclose(data_new["Cooling Load"][0], g_s.option_cl_jan.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][1], g_s.option_cl_feb.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][2], g_s.option_cl_mar.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][3], g_s.option_cl_apr.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][4], g_s.option_cl_may.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][5], g_s.option_cl_jun.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][6], g_s.option_cl_jul.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][7], g_s.option_cl_aug.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][8], g_s.option_cl_sep.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][9], g_s.option_cl_oct.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][10], g_s.option_cl_nov.get_value(), atol=1)
    assert np.isclose(data_new["Cooling Load"][11], g_s.option_cl_dec.get_value(), atol=1)
    
    close_tests(main_window, qtbot)


def test_load_data_GUI():
    from GHEtool.gui.gui_structure import load_data_GUI
    from pandas import DataFrame, Series, date_range, read_csv, to_datetime
    calc_data = load_data_GUI(FOLDER.joinpath("Examples/hourly_profile.csv"), 0, "Heating", "Cooling", "Heating", ";", ".", 1, False)
    data = read_csv(FOLDER.joinpath("Examples/hourly_profile.csv"), sep=";", decimal=".")
    data_new = DataFrame()
    start = to_datetime("2019-01-01 00:00:00")
    end = to_datetime("2019-12-31 23:59:00")
    # add date column
    data_new["Date"] = Series(date_range(start, end, freq="1H"))
    data_new = data_new.set_index("Date")
    data_new["Heating Load"] = data["Heating"].to_numpy()
    data_new["Cooling Load"] = np.zeros(8760)
    data_new["Heating peak"] = data["Heating"].to_numpy()
    data_new["Cooling peak"] = np.zeros(8760)
    data_one = data_new.resample("M").agg({"Heating Load": "sum", "Cooling Load": "sum", "Heating peak": "max", "Cooling peak": "max"})
    assert np.allclose(data_one["Heating peak"], calc_data[0])
    assert np.allclose(data_one["Cooling peak"], calc_data[1])
    assert np.allclose(data_one["Heating Load"], calc_data[2])
    assert np.allclose(data_one["Cooling Load"], calc_data[3])
    calc_data = load_data_GUI(FOLDER.joinpath("Examples/hourly_profile.csv"), 1, "Heating", "Cooling", "Heating", ";", ".", 1, False)
    data_new["Heating Load"] = data["Heating"].to_numpy()
    data_new["Cooling Load"] = data["Cooling"].to_numpy()
    data_new["Heating peak"] = data["Heating"].to_numpy()
    data_new["Cooling peak"] = data["Cooling"].to_numpy()
    data_two = data_new.resample("M").agg({"Heating Load": "sum", "Cooling Load": "sum", "Heating peak": "max", "Cooling peak": "max"})
    assert np.allclose(data_two["Heating peak"], calc_data[0])
    assert np.allclose(data_two["Cooling peak"], calc_data[1])
    assert np.allclose(data_two["Heating Load"], calc_data[2])
    assert np.allclose(data_two["Cooling Load"], calc_data[3])
    calc_data = load_data_GUI(FOLDER.joinpath("Examples/hourly_profile.csv"), 1, "Heating", "Cooling", "Heating", ";", ".", 1, True)
    assert np.allclose(data["Heating"], calc_data[0])
    assert np.allclose(data["Cooling"], calc_data[1])


def test_bug_when_opening_scenarios_which_have_autosave_enabled(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.gui_structure.option_auto_saving.set_value(1)
    main_window.add_scenario()
    main_window.add_scenario()
    main_window.gui_structure.aim_req_depth.widget.click()

    ds_old = main_window.list_ds[0]

    filename_1 = main_window.default_path.joinpath("try_open1.GHEtool")
    filename_2 = main_window.default_path.joinpath("try_open2.GHEtool")
    main_window._save_to_data(filename_1)
    main_window.gui_structure.aim_optimize.widget.click()
    assert main_window.gui_structure.aim_optimize.is_checked()
    main_window._save_to_data(filename_2)
    assert main_window._load_from_data(filename_1)
    assert not main_window.list_ds[-1].aim_optimize
    assert not main_window.gui_structure.aim_optimize.is_checked()
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    ds_new = main_window.list_ds[0]
    for option in ds_new.list_options_aims:
        if isinstance(option, ListBox):
            pass  # pragma: no cover
        if isinstance(getattr(ds_old, option), (int, float)):
            assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
            continue
        if isinstance(getattr(ds_old, option), (str, bool)):
            assert getattr(ds_old, option) == getattr(ds_new, option)
            continue
    os.remove(filename_1)
    os.remove(filename_2)
    close_tests(main_window, qtbot)


def test_start_after_crash(qtbot):
    """
    tests if the gui can start after a crash when an * is present in the scenario's.

    Parameters
    ----------
    qtbot

    Returns
    -------
    None
    """
    from GHEtool import FOLDER

    # init gui window
    main_window_old = start_tests(qtbot)
    main_window_old._load_from_data(f'{FOLDER}/gui/test_gui/test_after_crash.GHEtool')
    close_tests(main_window_old, qtbot)


def test_gui_filename_errors(qtbot):
    """
    test if all gui values are set and get correctly.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)

    main_window.gui_structure.fun_update_combo_box_data_file("")
    main_window.gui_structure.fun_update_combo_box_data_file("C:/test.GHEtool")

    try:
        load_data_GUI("", 1, "Heating", "Cooling", "Combined", 5, 6, 7)
    except FileNotFoundError:
        assert True
    try:
        load_data_GUI("C:/test.GHEtool", 1, "Heating", "Cooling", "Combined", ";", ",", 7)
    except FileNotFoundError:
        assert True
    try:
        load_data_GUI(f'{FOLDER}/Examples/hourly_profile.csv', 1, "Heating", "Cooling", "", ";", ",", 1)
    except ValueError:
        assert True
        
    close_tests(main_window, qtbot)
