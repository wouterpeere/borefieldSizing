import os
from pathlib import Path
from sys import setrecursionlimit

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

setrecursionlimit(1500)

from ScenarioGUI import load_config

load_config(Path(__file__).parent.joinpath("gui_config.ini"))


def test_wrong_file_save_location(qtbot):
    from GHEtool import FOLDER

    main_window = start_tests(qtbot)
    main_window._save_to_data(f'{FOLDER}/gui/test_gui/temp.GHEtool')
    close_tests(main_window, qtbot)
    os.replace(f'{FOLDER}/gui/test_gui/temp.GHEtool', f'{FOLDER}/gui/test_gui/temp2.GHEtool')
    main_window = start_tests(qtbot)
    main_window.filename = (f'{FOLDER}/gui/test_gui/temp2.GHEtool', 0)
    main_window.fun_load_known_filename()
    main_window.fun_save()
    close_tests(main_window, qtbot)
    assert not os.path.exists(f'{FOLDER}/gui/test_gui/temp.GHEtool')
    assert os.path.exists(f'{FOLDER}/gui/test_gui/temp2.GHEtool')
