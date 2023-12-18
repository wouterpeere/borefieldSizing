from pathlib import Path
from sys import setrecursionlimit

import PySide6.QtWidgets as QtW

from GHEtool import Borefield
from GHEtool.gui.gui_classes.gui_combine_window import MainWindow
from GHEtool.gui.gui_classes.translation_class import Translations
from GHEtool.gui.gui_structure import GUI
from GHEtool.gui.data_2_borefield_func import data_2_borefield
from GHEtool import FOLDER
from GHEtool.gui.data_2_borefield_func import _create_monthly_loads_peaks
from GHEtool.gui.gui_structure import load_data_GUI
from ScenarioGUI import load_config

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

load_config(Path(__file__).parent.joinpath("gui_config.ini"))

setrecursionlimit(1500)


def test_correct_columns_hourly_data(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.gui_structure.option_method_rb_calc.set_value(0)
    main_window.gui_structure.option_decimal_csv.set_value(0)
    main_window.gui_structure.option_seperator_csv.set_value(0)
    main_window.gui_structure.option_source_ground_temperature.set_value(0)

    main_window.gui_structure.option_filename.set_value(f'{FOLDER}/Examples/hourly_profile.csv')
    main_window.gui_structure.option_column.set_value(1)
    main_window.gui_structure.option_cooling_column.set_value(0)
    main_window.gui_structure.option_heating_column.set_value(1)

    main_window.save_scenario()

    main_window.add_scenario()
    main_window.save_scenario()
    filename_1 = main_window.default_path.joinpath("try_open2.GHEtool")
    main_window._save_to_data(filename_1)

    close_tests(main_window, qtbot)

    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=Borefield,
                             data_2_results_function=data_2_borefield)

    gs = main_window.gui_structure
    assert gs.option_cooling_column.get_value() == (0, 'Heating')
    assert gs.option_heating_column.get_value() == (1, 'Cooling')

    main_window.change_scenario(1)
    assert gs.option_cooling_column.get_value() == (0, 'Heating')
    assert gs.option_heating_column.get_value() == (1, 'Cooling')
