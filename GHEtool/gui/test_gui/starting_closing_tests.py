import random
from os import remove
from os.path import exists
from pathlib import Path

from ScenarioGUI.gui_classes.gui_structure_classes import ResultFigure
from ScenarioGUI import load_config
from matplotlib import pyplot as plt
import ScenarioGUI.global_settings as globs
import PySide6.QtWidgets as QtW

from GHEtool import Borefield
from GHEtool.gui.gui_classes.gui_combine_window import MainWindow
from GHEtool.gui.gui_classes.translation_class import Translations
from GHEtool.gui.gui_structure import GUI
from GHEtool.gui.data_2_borefield_func import data_2_borefield

load_config(Path(__file__).absolute().parent.joinpath("./gui_config.ini"))
MainWindow.TEST_MODE = True


def start_tests(qtbot) -> MainWindow:
    _backup_filename: str = f"backup.{globs.FILE_EXTENSION}BackUp"
    default_path: Path = Path(Path.home(), f"Documents/{globs.GUI_NAME}")
    backup_file: Path = Path(default_path, _backup_filename)
    pm_error = False
    if exists(backup_file):  # pragma: no cover
        try:
            remove(backup_file)
        except PermissionError:
            pm_error = True
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=Borefield, data_2_results_function=data_2_borefield)
    if pm_error:  # pragma: no cover
        main_window.backup_file = Path(f"{main_window.backup_file}".replace("backup", f"backup{random.randint(0,1000)}"))
    return main_window


def close_tests(main_window: MainWindow, qtbot) -> None:
    [ds.close_figures() for ds in main_window.list_ds]
    [plt.close(cat.fig) for cat in main_window.gui_structure.page_result.list_categories if isinstance(cat, ResultFigure)]
    if main_window.saving_threads:  # pragma: no cover
        _ = [thread.terminate() for thread in main_window.saving_threads if not thread.isRunning()]
        if any([not thread.calculated for thread in main_window.saving_threads]):
            qtbot.wait(1000)
            _ = [thread.func() for thread in main_window.saving_threads]
