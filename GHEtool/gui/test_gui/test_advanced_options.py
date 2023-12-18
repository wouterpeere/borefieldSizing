"""
Test to see if the advanced options work as expected
"""
import sys
from pathlib import Path

from ScenarioGUI import load_config

from GHEtool.gui.test_gui.starting_closing_tests import close_tests, start_tests

load_config(Path(__file__).parent.joinpath("gui_config.ini"))

sys.setrecursionlimit(1500)


def test_advanced_options(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    gs = main_window.gui_structure
    gs.option_source_ground_temperature.set_value(0)
    gs.option_method_rb_calc.set_value(0)

    assert gs.category_advanced_options.is_hidden()
    gs.option_advanced_options.set_value(1)
    assert not gs.category_advanced_options.is_hidden()
    gs.aim_req_depth.widget.click()

    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.result_text_depth.label.text() == 'Depth: 115.13 m'

    gs.option_atol.set_value(25)
    gs.option_rtol.set_value(20)
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    main_window.display_results()
    assert gs.result_text_depth.label.text() == 'Depth: 115.15 m'
    close_tests(main_window, qtbot)
