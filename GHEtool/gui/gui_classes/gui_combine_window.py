from __future__ import annotations

import logging
from json import JSONDecodeError, load, dump
from os.path import dirname, realpath, splitext
from pathlib import Path, PurePath
from sys import path

from ScenarioGUI import MainWindow
from ScenarioGUI.gui_classes.gui_combine_window import JsonDict
from ScenarioGUI.gui_classes.gui_data_storage import DataStorage
import ScenarioGUI.global_settings as globs
import PySide6.QtWidgets as QtW


currentdir = dirname(realpath(__file__))
parentdir = dirname(currentdir)
path.append(parentdir)

BACKUP_FILENAME: str = 'backup.GHEtoolBackUp'


# main GUI class
class MainWindow(MainWindow):
    """
    This class contains the general functionalities of the GUI (e.g. the handling of creating new scenarios,
    saving documents etc.)
    """

    def _load_from_data(self, location: str | Path, append: bool = False) -> bool:
        """
        This function loads the data from a JSON formatted file.

        Parameters
        ----------
        location : str| Path
            Location of the data file

        Returns
        -------
        True if it is loaded, False otherwise
        """

        def convert_v21x_to_v220(val: dict) -> None:
            """
            This function converts the data from a stored datafile from a version v2.1.x to v2.2.0.

            Parameters
            ----------
            val : dict
                Loaded values

            Returns
            -------
            None
            """
            logging.info("Convert data to v.2.2.0 format.")
            data = val.pop("option_spacing")
            val["option_spacing_width"] = data
            val["option_spacing_length"] = data
            val["option_heating_column"] = (val["option_heating_column"], "")
            val["option_single_column"] = (val["option_single_column"], "")
            val["option_cooling_column"] = (val["option_cooling_column"], "")
            val["option_language"] = (val["option_language"], "")
            val["aim_rect"] = True
            val["aim_Box_shaped"] = False
            val["aim_L_shaped"] = False
            val["aim_U_shaped"] = False
            val["aim_circle"] = False
            val["aim_custom"] = False
            val["option_pipe_borehole_radius_2"] = val["option_pipe_borehole_radius"]
            if val["option_method_temp_gradient"] == 0:
                val["option_source_ground_temperature"] = 0
            if val["option_method_temp_gradient"] == 1:
                val["option_source_ground_temperature"] = 2
                val["option_flux_gradient"] = 1

        def general_changes() -> None:
            # change window title to new loaded filename
            self.change_window_title()
            self.list_widget_scenario.setCurrentRow(0)
            self.list_widget_scenario.item(0).data(MainWindow.role).set_values(self.gui_structure)
            self.check_results()

        try:
            # open file and get data
            with open(location) as file:
                saving = load(file)

            version = saving['version']
        except FileNotFoundError:
            logging.info(self.translations.no_file_selected[self.gui_structure.option_language.get_value()[0]])
            return False
            # raise ImportError("The datafile cannot be loaded!")
        except (JSONDecodeError, UnicodeDecodeError) as e:
            if 'Expecting' in str(e):  # pragma: no cover
                globs.LOGGER.warning('The back-up file has been corrupted! And will hence be overwritten.')
                # change language to english
                self.change_language()
                # add a first scenario
                self.add_scenario()
                return False
            # try to open as pickle
            globs.LOGGER.warning('One cannot open a GHEtool v2.1.0 file!')
            return False

        if not append:
            self.list_widget_scenario.clear()

        if version in ["2.2.0", "2.2.0.1"]:
            # write data to variables
            for val, name in zip(saving['values'], saving['names']):
                ds = DataStorage(self.gui_structure)
                ds.from_dict(val)
                ds.results = None
                item = QtW.QListWidgetItem(name)
                item.setData(MainWindow.role, ds)
                self.list_widget_scenario.addItem(item)
            # set and change the window title
            self.filename = tuple(saving['filename']) if 'GHEtoolBackUp' in str(location) else (str(location), 'GHEtool (*.GHEtool)')
            general_changes() if not append else None
            return True

        if version in ["2.1.1", "2.1.2"]:
            # write data to variables
            for val, borefield, name in zip(saving['values'], saving['borefields'], saving['names']):
                ds = DataStorage(self.gui_structure)
                convert_v21x_to_v220(val)
                ds.from_dict(val)
                ds.results = None
                item = QtW.QListWidgetItem(name)
                item.setData(MainWindow.role, ds)
                self.list_widget_scenario.addItem(item)

            # set and change the window title
            self.filename = tuple(saving['filename']) if 'GHEtoolBackUp' in str(location) else (str(location), 'GHEtool (*.GHEtool)')
            general_changes() if not append else None
            return True

        # print warning if the version is not a previous one
        logging.error(self.translations.cannot_load_new_version[self.gui_structure.option_language.get_value()[0]])

    def _save_to_data(self, location: str | Path) -> None:
        """
        This function saves the gui data to a json formatted file.

        Parameters
        ----------
        location : str | Path
            Location of the data file.

        Returns
        -------
        None
        """
        # create list of all scenario names
        scenario_names = [self.list_widget_scenario.item(idx).text() for idx in range(self.list_widget_scenario.count())]
        # create saving dict
        list_ds = [self.list_widget_scenario.item(idx).data(MainWindow.role) for idx in range(self.list_widget_scenario.count())]
        saving: JsonDict = {
            "filename": self.filename,
            "names": scenario_names,
            "version": globs.VERSION,
            "values": [d_s.to_dict() for d_s in list_ds],
            "results": [None] * len(list_ds),
            "default_path": f"{self.default_path}",
        }
        file_extension = splitext(location)[1].replace(".", "")
        try:
            self.export_functions[file_extension](Path(location), saving)
        except FileNotFoundError:
            globs.LOGGER.error(self.translations.no_file_selected[self.gui_structure.option_language.get_value()[0]])
        except PermissionError:  # pragma: no cover
            globs.LOGGER.error("PermissionError")
