from typing import List


class Translations:  # pragma: no cover
    __slots__ = (
        "icon",
        "short_cut",
        "scenarioString",
        "label_Language",
        "category_language",
        "option_language",
        "push_button_save_scenario",
        "push_button_add_scenario",
        "push_button_delete_scenario",
        "push_button_start_multiple",
        "push_button_cancel",
        "page_aim",
        "page_borefield",
        "page_earth",
        "page_borehole_resistance",
        "page_thermal",
        "page_result",
        "page_options",
        "page_settings",
        "label_Status",
        "label_File",
        "label_Calculation",
        "category_borehole",
        "option_depth",
        "option_spacing_width",
        "option_spacing_length",
        "option_conductivity",
        "option_ground_temp",
        "option_max_depth",
        "option_min_spacing",
        "option_max_spacing",
        "option_max_width",
        "option_max_length",
        "option_heat_capacity",
        "option_width",
        "option_length",
        "category_temperatures",
        "option_min_temp",
        "option_max_temp",
        "option_temp_gradient",
        "option_simu_period",
        "option_constant_rb",
        "label_next",
        "label_previous",
        "hint_depth",
        "function_save_results",
        "function_save_figure",
        "X_Axis",
        "Y_Axis",
        "BaseCooling",
        "BaseHeating",
        "PeakCooling",
        "PeakHeating",
        "label_Import",
        "checkBox_Import",
        "hint_peak_heating",
        "hint_peak_cooling",
        "hint_load_heating",
        "hint_load_cooling",
        "label_UnitPeak",
        "label_UnitLoad",
        "hint_jan",
        "hint_feb",
        "hint_mar",
        "hint_apr",
        "hint_may",
        "hint_jun",
        "hint_jul",
        "hint_aug",
        "hint_sep",
        "hint_oct",
        "hint_nov",
        "hint_dec",
        "label_DataType",
        "option_seperator_csv",
        "option_filename",
        "button_load_csv",
        "option_decimal_csv",
        "label_dataColumn",
        "label_DataUnit",
        "label_HeatingLoadLine",
        "label_CoolingLoadLine",
        "label_combined",
        "label_TimeStep",
        "label_DateLine",
        "option_column",
        "pushButton_calculate",
        "ErrorMassage",
        "UnableDataFormat",
        "ChooseCSV",
        "ChooseXLS",
        "ChooseXLSX",
        "no_file_selected",
        "ValueError",
        "ColumnError",
        "choose_load",
        "SaveFigure",
        "SaveData",
        "Save",
        "label_WarningCustomBorefield",
        "label_WarningDepth",
        "checkBox_SizeBorefield",
        "label_Size_B",
        "label_Size_L",
        "label_Size_W",
        "label_New",
        "label_Save",
        "label_Open",
        "label_Save_As",
        "Calculation_Finished",
        "tool_imported",
        "tool_imported_start",
        "label_new_scenario",
        "new_name",
        "label_okay",
        "label_abort",
        "no_backup_file",
        "label_close",
        "label_cancel",
        "label_CancelTitle",
        "label_LeaveScenarioText",
        "label_LeaveScenario",
        "label_StayScenario",
        "X_Axis_Load",
        "Y_Axis_Load_P",
        "Y_Axis_Load_Q",
        "menu_language",
        "menu_settings",
        "menu_calculation",
        "menu_file",
        "menu_scenario",
        "action_start_multiple",
        "action_new",
        "action_save",
        "action_open",
        "action_update_scenario",
        "action_add_scenario",
        "action_delete_scenario",
        "action_save_as",
        "button_rename_scenario",
        "button_rename_scenario",
        "label_Language_Head",
        "label_aim_question",
        "category_select_file",
        "label_Filename_2",
        "category_th_demand",
        "option_heating_column",
        "option_cooling_column",
        "option_single_column",
        "option_unit_data",
        "category_save_scenario",
        "option_toggle_buttons",
        "option_auto_saving",
        "hint_saving",
        "category_constant_rb",
        "category_fluid_data",
        "option_fluid_conductivity",
        "option_fluid_mass_flow",
        "option_fluid_density",
        "option_fluid_capacity",
        "option_fluid_viscosity",
        "category_pipe_data",
        "option_pipe_number",
        "option_pipe_grout_conductivity",
        "option_pipe_conductivity",
        "option_pipe_outer_radius",
        "option_pipe_inner_radius",
        "option_pipe_borehole_radius",
        "option_pipe_borehole_radius_2",
        "option_pipe_distance",
        "option_pipe_roughness",
        "option_pipe_depth",
        "label_ResOptimizeLoad1",
        "label_ResOptimizeLoad2",
        "label_ResOptimizeLoad3",
        "label_ResOptimizeLoad4",
        "label_CancelText",
        "label_ResOptimizeLoad5",
        "label_ResOptimizeLoad6",
        "push_button_start_single",
        "not_calculated",
        "NoSolution",
        "aim_temp_profile",
        "aim_req_depth",
        "aim_size_length",
        "aim_optimize",
        "category_calculation",
        "option_method_size_depth",
        "option_method_size_length",
        "option_method_rb_calc",
        "category_earth",
        "cat_no_results",
        "text_no_result",
        "numerical_results",
        "result_text_depth",
        "result_Rb_calculated",
        "result_Reynolds",
        "results_ground_temperature",
        "results_heating_load",
        "results_heating_load_percentage",
        "results_heating_ext",
        "results_heating_peak",
        "results_cooling_load",
        "results_cooling_load_percentage",
        "results_cooling_ext",
        "results_cooling_peak",
        "max_temp",
        "min_temp",
        "figure_temperature_profile",
        "legend_figure_temperature_profile",
        "hourly_figure_temperature_profile",
        "figure_load_duration",
        "legend_figure_load_duration",
        "option_len_peak_heating",
        "option_len_peak_cooling",
        "option_temperature_profile_hourly",
        "option_ground_temp_gradient",
        "option_ground_heat_flux",
        "option_n_threads",
        "option_number_circle_boreholes",
        "option_borefield_radius",
        "custom_borefield",
        "option_seperator_borefield",
        "borefield_file",
        "import_borefield",
        "option_decimal_borefield",
        "category_demand_building_or_geo",
        "geo_load",
        "SCOP",
        "SEER",
        "results_heating_peak_geo",
        "results_cooling_peak_geo",
        "option_ground_temp_gradient",
        "hint_press_load",
        "cannot_load_new_version",
        "pipe_thermal_resistance",
        "option_U_pipe_or_coaxial_pipe",
        "option_pipe_coaxial_inner_inner",
        "option_pipe_coaxial_outer_inner",
        "option_pipe_coaxial_inner_outer",
        "option_pipe_coaxial_outer_outer",
        "option_advanced_options",
        "category_advanced_options",
        "option_atol",
        "option_rtol",
        "option_max_nb_of_iter",
        "SCOP_DHW",
        "option_include_dhw",
        "DHW",
        "option_fluid_selector",
        "option_glycol_selector",
        "option_glycol_percentage",
        "option_fluid_ref_temp",
        "option_ground_database",
        "hint_ground_database",
        "hint_borehole_depth",
        "hint_ground_flux_database",
        "option_source_ground_temperature",
        "option_flux_gradient",
        "label_Continue",
        "label_ContinueText",
        "label_ContinueTitle",
        "languages",
    )

    def __init__(self):
        self.languages: List[str] = ["English", "German", "Dutch", "Italian", "French", "Spanish", "Galician"]
        self.icon: List[str] = [
            "Flag_English.svg",
            "Flag_German.svg",
            "Flag_Dutch.svg",
            "Flag_Italian.svg",
            "Flag_French.svg",
            "Flag_Spain.svg",
            "Flag_Galicia.svg",
        ]
        self.short_cut: List[str] = ["Ctrl+Alt+E", "Ctrl+Alt+G", "Ctrl+Alt+D", "Ctrl+Alt+I", "Ctrl+Alt+F", "Ctrl+Alt+S", "Ctrl+Alt+A"]
        self.scenarioString: List[str] = ["Scenario", "Szenario", "Scenario", "Scenario", "Scénario", "Escenario", "Escenario"]
        self.label_Language: List[str] = ["Language: ", "Sprache: ", "Taal: ", "Languange: ", "Languange: ", "Idioma:", "Lingua: "]
        self.category_language: List[str] = ["Language: ", "Sprache: ", "Taal: ", "Languange: ", "Languange: ", "Idioma:", "Lingua: "]
        self.option_language: List[str] = [
            "Language:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Sprache:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Taal:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Languange:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Languange:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Idioma:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Lingua:,English,German,Dutch,Italian,French,Spanish,Galician",
        ]
        self.push_button_save_scenario: List[str] = [
            "Update scenario",
            "Szenario aktualisieren",
            "Update scenario",
            "Aggiorna scenario",
            "Mettre à jour le scénario",
            "Actualizar escenario",
            "Actualizar escenario",
        ]
        self.push_button_add_scenario: List[str] = [
            "Add scenario",
            "Szenario hinzufügen",
            "Nieuw scenario",
            "Aggiungi scenario",
            "Ajouter un scénario",
            "Añadir escenario",
            "Engadir escenario",
        ]
        self.push_button_delete_scenario: List[str] = [
            "Delete scenario",
            "Szenario löschen",
            "Verwijder scenario",
            "Cancella scenario",
            "Supprimer un scénario",
            "Borrar escenario",
            "Eliminar escenario",
        ]
        self.push_button_start_multiple: List[str] = [
            "Calculate all scenarios",
            "Berechne alle Szenarios",
            "Bereken alle scenarios",
            "Calculate all scenarios",
            "Calculate all scenarios",
            "Calculate all scenarios",
            "Calculate all scenarios",
        ]
        self.push_button_cancel: List[str] = ["Exit", "Verlassen", "Sluit", "Esci", "Sortie", "Salir", "Saír"]
        self.page_aim: List[str] = [
            "Aim,Aim of simulation",
            "Ziel,Ziel der Simulation",
            "Doel,Doel van de simulatie",
            "Aim,Aim of simulation",
            "Aim,Aim of simulation",
            "Aim,Aim of simulation",
            "Aim,Aim of simulation",
        ]
        self.page_borefield: List[str] = [
            "Borefield,Borefield",
            "Bohrlochfeld,Bohrlochfeld",
            "Boorveld,Boorveld",
            "Foro,Foro",
            "Forage,Forage",
            "Pozo,Pozo",
            "Pozo,Pozo",
        ]
        self.page_earth: List[str] = ["Earth,Earth", "Erdreich,Erdreich", "Grond,Grond", "Terra,Terra", "Terre,Terre", "Terreno,Terreno", "Chan,Chan"]
        self.page_borehole_resistance: List[str] = [
            "Borehole @resistance,Equivalent borehole resistance",
            "Bohrloch-@widerstand,Equivalänter Bohrlochwiderstand",
            "Boorgat-@weerstand,Equivalente boorgatweerstand",
            "Borehole@resistance,Equivalent borehole resistance",
            "Borehole@resistance,Equivalent borehole resistance",
            "Borehole@resistance,Equivalent borehole resistance",
            "Borehole@resistance,Equivalent borehole resistance",
        ]
        self.page_thermal: List[str] = [
            "Thermal @demand,Thermal demands",
            "Thermischer @Bedarf,Thermische Last",
            "Thermische @vraag,Thermische vraag",
            "Richieste @termiche,Richieste termiche",
            "Demande @thermique,Demande thermique",
            "Cargas @térmicas,Cargas térmicas",
            "Cargas @térmicas,Cargas térmicas",
        ]
        self.page_result: List[str] = [
            "Results,Results",
            "Ergebnisse,Ergebnisse",
            "Resultaten,Resultaten",
            "Risultati,Risultati",
            "Résultats,Résultats",
            "Resultados,Resultados",
            "Resultados,Resultados",
        ]
        self.page_options: List[str] = [
            "Options,Options",
            "Optionen,Optionen",
            "Opties,Opties",
            "Options,Options",
            "Options,Options",
            "Options,Options",
            "Options,Options",
        ]
        self.page_settings: List[str] = [
            "Settings,Settings",
            "Einstellungen,Einstellungen",
            "Instellingen,Instellingen",
            "Settings,Settings",
            "Settings,Settings",
            "Settings,Settings",
            "Settings,Settings",
        ]
        self.label_Status: List[str] = ["Progress: ", "Fortschritt: ", "Vooruitgang: ", "Progressi: ", "Progrès: ", "Progreso: ", "Progreso: "]
        self.label_File: List[str] = ["File", "Datei", "Bestand", "File", "File", "File", "File"]
        self.label_Calculation: List[str] = ["Calculation", "Berechnung", "Berekening", "Calculation", "Calculation", "Calculation", "Calculation"]
        self.category_borehole: List[str] = [
            "Borefield properties",
            "Bohrlochfeldeigenschaften",
            "Eigenschappen van boorveld",
            "Proprietà del foro e della terra",
            "Propriétés du trou de sonde et de la terre",
            "Propiedades del pozo y terreno",
            "Propiedades do pozo e do chan",
        ]
        self.option_depth: List[str] = [
            "Borehole depth [m]: ",
            "Bohrlochtiefe [m]: ",
            "Boorgatdiepte [m]: ",
            "Profondità foro [m]: ",
            "Profondeur du forage [m]: ",
            "Profundidad del pozo [m]: ",
            "Profundidade do pozo [m]: ",
        ]
        self.option_spacing_width: List[str] = [
            "Borehole spacing width [m]: ",
            "Bohrlochabstand Breitenrichtung [m]: ",
            "Boorgatspatiëring breedte [m]: ",
            "Spaziatura del foro [m]: ",
            "Espacement des trous de forage [m]: ",
            "Espaciado entre pozos [m]: ",
            "Espazamento entre pozos [m]:",
        ]
        self.option_spacing_length: List[str] = [
            "Borehole spacing length [m]: ",
            "Bohrlochabstand Längenrichtung [m]: ",
            "Boorgatspatiëring lengte [m]: ",
            "Spaziatura del foro [m]: ",
            "Espacement des trous de forage [m]: ",
            "Espaciado entre pozos [m]: ",
            "Espazamento entre pozos [m]:",
        ]
        self.option_conductivity: List[str] = [
            "Conductivity of the soil [W/mK]: ",
            "Wärmeleitfähigkeit des Erdreiches [W/mK]: ",
            "Conductiviteit van de bodem [W/mK]: ",
            "Conducibilità del terreno [W/mK]: ",
            "Conductivité du sol [W/mK]: ",
            "Conductividad del suelo [W/mK]: ",
            "Conductividade do chan [W/mK]: ",
        ]
        self.option_ground_temp: List[str] = [
            "Ground temperature at infinity [°C]: ",
            "Erdreichtemperatur in der Unendlichkeit [°C]: ",
            "Grondtemperatuur op oneindig [°C]: ",
            "Temperatura del terreno all'infinito [°C]: ",
            "Température du sol à l'infini [°C]: ",
            "Temperatura del suelo en el infinito [°C]: ",
            "Temperatura do chan no infinito [°C]: ",
        ]
        self.option_max_depth: List[str] = [
            "Maximal borehole depth [m]: ",
            "Maximale Bohrlochtiefe [m]: ",
            "Maximale boorvelddiepte[m]: ",
            "Maximal borehole depth [m]: ",
            "Maximal borehole depth [m]: ",
            "Maximal borehole depth [m]: ",
            "Maximal borehole depth [m]: ",
        ]
        self.option_min_spacing: List[str] = [
            "Minimal borehole spacing [m]: ",
            "Minimaler Bohrlochabstand [m]: ",
            "Minimale boorgatspatiëring [m]: ",
            "Minimal borehole spacing [m]: ",
            "Minimal borehole spacing [m]: ",
            "Minimal borehole spacing [m]: ",
            "Minimal borehole spacing [m]: ",
        ]
        self.option_max_spacing: List[str] = [
            "Maximal borehole spacing [m]: ",
            "Maximaler Bohrlochabstand [m]: ",
            "Maximale boorgatspatiëring [m]: ",
            "Maximal borehole spacing [m]: ",
            "Maximal borehole spacing [m]: ",
            "Maximal borehole spacing [m]: ",
            "Maximal borehole spacing [m]: ",
        ]
        self.option_max_width: List[str] = [
            "Maximal width of rectangular field [m]: ",
            "Maximale Breite des rechteckigen Feldes [m]: ",
            "Maximale breedte van het rechthoekig boorveld [m]: ",
            "Maximal width of rectangular field [m]: ",
            "Maximal width of rectangular field [m]: ",
            "Maximal width of rectangular field [m]: ",
            "Maximal width of rectangular field [m]: ",
        ]
        self.option_max_length: List[str] = [
            "Maximal length of rectangular field [m]: ",
            "Maximale Länge des rechteckigen Feldes [m]: ",
            "Maximale lengte van het rechthoekig boorveld [m]: ",
            "Maximal length of rectangular field [m]: ",
            "Maximal length of rectangular field [m]: ",
            "Maximal length of rectangular field [m]: ",
            "Maximal length of rectangular field [m]: ",
        ]
        self.option_heat_capacity: List[str] = [
            "Ground volumetric heat capacity [kJ / m³ K]:",
            "Spezifische Wärmekapazität des Erdreiches [kJ / m³ K]:",
            "Volumetrische warmtecapaciteit van de grond [kJ / m³ K]:",
            "Ground volumetric heat capacity [kJ / m³ K]:",
            "Ground volumetric heat capacity [kJ / m³ K]:",
            "Ground volumetric heat capacity [kJ / m³ K]:",
            "Ground volumetric heat capacity [kJ / m³ K]:",
        ]
        self.option_width: List[str] = [
            "Number of boreholes in the width direction [-]:",
            "Anzahl der Bohrungen in der Breite [-]:",
            "Aantal boringen in de breedte [#]:",
            "Number of boreholes in the width direction [-]:",
            "Number of boreholes in the width direction [-]:",
            "Number of boreholes in the width direction [-]:",
            "Number of boreholes in the width direction [-]:",
        ]
        self.option_length: List[str] = [
            "Number of boreholes in the length direction [-]:",
            "Anzahl der Bohrungen in der Länge [-]:",
            "Aantal boringen in de lengte [#]:",
            "Number of boreholes in the length direction [-]:",
            "Number of boreholes in the length direction [-]:",
            "Number of boreholes in the length direction [-]:",
            "Number of boreholes in the length direction [-]:",
        ]
        self.category_temperatures: List[str] = [
            "Temperature constraints and simulation period",
            "Temperaturgrenzwerte und Simulationszeit",
            "Temperatuursgrenzen en simulatieperiode",
            "Vincoli di temperatura e periodo di simulazione",
            "Contraintes de température et période de simulation",
            "Restricciones de temperatura y período de simulación",
            "Restriccións de temperatura e período de simulación",
        ]
        self.option_min_temp: List[str] = [
            "Minimum average fluid temperature [°C]: ",
            "Minimale durchschnittliche Fluidtemperatur [°C]:",
            "Minimale gemiddelde fluïdumtemperatuur [°C]: ",
            "Minimum average fluid temperature [°C]: ",
            "Minimum average fluid temperature [°C]: ",
            "Minimum average fluid temperature [°C]: ",
            "Minimum average fluid temperature [°C]: ",
        ]
        self.option_max_temp: List[str] = [
            "Maximum average fluid temperature [°C]: ",
            "Maximale durchschnittliche Fluidtemperatur [°C]:",
            "Maximale gemiddelde fluïdumtemperatuur [°C]: ",
            "Maximum average fluid temperature [°C]: ",
            "Maximum average fluid temperature [°C]: ",
            "Maximum average fluid temperature [°C]: ",
            "Maximum average fluid temperature [°C]: ",
        ]
        self.option_temp_gradient: List[str] = [
            "Temperature gradient [K/100m]: ",
            "Temperaturgradient [K/100m]: ",
            "Temperatuursgradiënt [K/100m]: ",
            "Temperature gradient [K/100m]: ",
            "Temperature gradient [K/100m]: ",
            "Temperature gradient [K/100m]: ",
            "Temperature gradient [K/100m]: ",
        ]
        self.option_simu_period: List[str] = [
            "Simulation period [years]: ",
            "Simulationszeit [Jahre]: ",
            "Simulatieperiode [jaar]: ",
            "Periodo di simulazione [anni]: ",
            "Période de simulation [années]: ",
            "Período de simulación [años]: ",
            "Período de simulación [anos]: ",
        ]
        self.option_constant_rb: List[str] = [
            "Equivalent borehole resistance (e.g. from TRT) [mK/W]: ",
            "Äquivalenter Bohrlochwiderstand [mK/W]: ",
            "Equivalente boorgatweerstand [mK/W]: ",
            "Resistenza equivalente del foro [mK/W]: ",
            "Résistance équivalente du trou de forage [mK/W]: ",
            "Resistencia del pozo equivalente [mK/W]: ",
            "Resistencia do pozo equivalente [mK/W]:",
        ]
        self.label_next: List[str] = ["next", "nächstes", "volgende", "successivo", "suivant", "siguiente", "seguinte"]
        self.label_previous: List[str] = ["previous", "vorheriges", "vorige", "precedente", "précédente", "anterior", "anterior"]
        self.hint_depth: List[str] = [
            "Borehole depth: ",
            "Bohrlochtiefe: ",
            "Boorgatdiepte: ",
            "Profondità del foro:  ",
            "Profondeur du trou de sonde: ",
            "Profundidad del pozo: ",
            "Profundidade do pozo: ",
        ]
        self.function_save_results: List[str] = [
            "Save results",
            "Ergebnisse speichern",
            "Bewaar resultaten",
            "Salva i risultati",
            "Enregistrer les résultats",
            "Guardar resultados",
            "Gardar resultados",
        ]
        self.function_save_figure: List[str] = [
            "Save figure",
            "Abbildung speichern",
            "Bewaar figuren",
            "Salva figura",
            "Sauvegarder la figure",
            "Guardar figura",
            "Gardar figura",
        ]
        self.X_Axis: List[str] = ["Time [year]", "Zeit [Jahr]", "Tijd [jaar]", "Tempo [anno]", "Heure [année]", "Tiempo [año]", "Tempo [ano]"]
        self.Y_Axis: List[str] = [
            "Temperature [°C]",
            "Temperatur [°C]",
            "Temperatuur [°C]",
            "Temperatura [°C]",
            "Température [°C]",
            "Temperatura [°C]",
            "Temperatura [°C]",
        ]
        self.BaseCooling: List[str] = [
            "base cooling",
            "Grundkühlung",
            "Basisbelasting koeling",
            "Base raffreddamento",
            "Base de refroidissement",
            "Base de refrigeración",
            "Base de refrixeración",
        ]
        self.BaseHeating: List[str] = [
            "base heating",
            "Grundheizung",
            "Basisbelasting verwarming",
            "Base riscaldamento",
            "Chauffage de base",
            "Base de calefacción",
            "Base de calefacción",
        ]
        self.PeakCooling: List[str] = [
            "peak cooling",
            "Kühlspitzen",
            "Piekkoeling",
            "Picco raffreddamento",
            "Refroidissement maximal",
            "Pico de refrigeración",
            "Pico de refrixeración",
        ]
        self.PeakHeating: List[str] = [
            "peak heating",
            "Heizspitzen",
            "Piekverwarming",
            "Picco di riscaldamento",
            "Pic de chauffage",
            "Pico de calefacción",
            "Pico de calefacción",
        ]
        self.label_Import: List[str] = ["Import", "Importieren", "Importeer", "Importazione", "Importation", "Importar", "Importar"]
        self.checkBox_Import: List[str] = [
            "Import Demands?",
            "Lasten importieren?",
            "Importeer vraag?",
            "Richieste di @importazione?",
            "Demande d'importation?",
            "Importar cargas?",
            "Importar cargas?",
        ]
        self.hint_peak_heating: List[str] = [
            "Heating peak",
            "Heizspitzen",
            "Verwarmingspiek",
            "Picco di riscaldamento",
            "Pic de chauffage",
            "Pico de calefacción",
            "Pico de calefacción",
        ]
        self.hint_peak_cooling: List[str] = [
            "Cooling peak",
            "Kühlspitzen",
            "Koelpiek",
            "Picco di raffreddamento",
            "Pic de refroidissement",
            "Pico de refrigeración",
            "Pico de refrixeración",
        ]
        self.hint_load_heating: List[str] = [
            "Heating load",
            "Heizlast",
            "Verwarmingslast",
            "Carico di riscaldamento",
            "Charge de chauffage",
            "Carga de calefacción",
            "Carga de calefacción",
        ]
        self.hint_load_cooling: List[str] = [
            "Cooling load",
            "Kühllast",
            "Koellast",
            "Carico di raffreddamento",
            "Charge de refroidissement",
            "Carga de refrigeración",
            "Carga de refrixeración",
        ]
        self.label_UnitPeak: List[str] = [
            "Peak unit: ",
            "Einheit Spitze: ",
            "Eenheid piek: ",
            "Unità di picco: ",
            "Unité de pointe: ",
            "Unidad de pico: ",
            "Unidade de pico: ",
        ]
        self.label_UnitLoad: List[str] = [
            "Load unit: ",
            "Einheit Last: ",
            "Eenheid belasting: ",
            "Unità di carico: ",
            "Unité de charge: ",
            "Unidad de carga: ",
            "Unidade de carga: ",
        ]
        self.hint_jan: List[str] = ["January", "Januar", "Januari", "Gennaio", "Janvier", "Enero", "Xaneiro"]
        self.hint_feb: List[str] = ["February", "Februar", "Februari", "Febbraio", "Février", "Febrero", "Febreiro"]
        self.hint_mar: List[str] = ["March", "März", "Maart", "Marzo", "Mars", "Marzo", "Marzo"]
        self.hint_apr: List[str] = ["April", "April", "April", "Aprile", "Avril", "Abril", "Abril"]
        self.hint_may: List[str] = ["May", "Mai", "Mei", "Maggio", "Mai", "Mayo", "Maio"]
        self.hint_jun: List[str] = ["June", "Juni", "Juni", "Giugno", "Juin", "Junio", "Xuño"]
        self.hint_jul: List[str] = ["July", "Juli", "Juli", "Luglio", "Juillet", "Julio", "Xullo"]
        self.hint_aug: List[str] = ["August", "August", "Augustus", "Agosto", "Août", "Agosto", "Agosto"]
        self.hint_sep: List[str] = ["September", "September", "September", "Settembre", "Septembre", "Septiembre", "Setembro"]
        self.hint_oct: List[str] = ["October", "Oktober", "Oktober", "Ottobre", "Octobre", "Octubre", "Outubro"]
        self.hint_nov: List[str] = ["November", "November", "November", "Novembre", "Novembre", "Noviembre", "Novembro"]
        self.hint_dec: List[str] = ["December", "Dezember", "December", "Dicembre", "Décembre", "Diciembre", "Decembro"]
        self.label_DataType: List[str] = [
            "File type: ",
            "Dateityp: ",
            "Bestandstype: ",
            "Tipo di fileImport: ",
            "Type de fichier: ",
            "Tipo de archivo: ",
            "Tipo de ficheiro: ",
        ]
        self.option_seperator_csv: List[str] = [
            "Separator in CSV-file:,Semicolon ';',Comma '++'",
            "Trenner in der CSV-Datei:,Semikolon ';',Komma '++'",
            "Scheidingsteken in CSV-file:,Puntkomma ';',Komma '++'",
            "Separator in CSV-file:,Semicolon ';',Comma '++'",
            "Separator in CSV-file:,Semicolon ';',Comma '++'",
            "Separator in CSV-file:,Semicolon ';',Comma '++'",
            "Separator in CSV-file:,Semicolon ';',Comma '++'",
        ]
        self.option_filename: List[str] = [
            "Filename: ",
            "Dateiname: ",
            "Bestandsnaam: ",
            "Nome fileImport: ",
            "Nom de fichier: ",
            "Nombre de archivo: ",
            "Nome de ficheiro: ",
        ]
        self.button_load_csv: List[str] = ["Load", "Laden", "Laad", "Caricare", "Chargement", "Cargar", "Cargar"]
        self.option_decimal_csv: List[str] = [
            "Decimal sign in CSV-file:,Point '.',Comma '++'",
            "Dezimalzeichen in CSV-Datei:,Punkt '.',Komma '++'",
            "Decimaalteken in de CSV-file:,Punt '.',Komma '++'",
            "Decimal sign in CSV-file:,Point '.',Comma '++'",
            "Decimal sign in CSV-file:,Point '.',Comma '++'",
            "Decimal sign in CSV-file:,Point '.',Comma '++'",
            "Decimal sign in CSV-file:,Point '.',Comma '++'",
        ]
        self.label_dataColumn: List[str] = [
            "Thermal demands: ",
            "Thermische Lasten: ",
            "Thermische vraag: ",
            "Richieste termiche: ",
            "Demande thermique: ",
            "Cargas térmicas: ",
            "Cargas térmicas: ",
        ]
        self.label_DataUnit: List[str] = [
            "Unit data: ",
            "Dateneinheit: ",
            "Eenheid data: ",
            "Dati @dell'unità:  ",
            "Données de l'unité: ",
            "Datos de unidad: ",
            "Datos de unidade: ",
        ]
        self.label_HeatingLoadLine: List[str] = [
            "Heating load line: ",
            "Heizlastspalte: ",
            "Belastingslijn verwarming: ",
            "Linea di carico di riscaldamento: ",
            "Ligne de charge de chauffage: ",
            "Línea de carga de calefacción: ",
            "Liña de carga de calefacción: ",
        ]
        self.label_CoolingLoadLine: List[str] = [
            "Cooling load line: ",
            "Kühllastspalte: ",
            "Belastingslijn koeling: ",
            "Linea del carico di raffreddamento: ",
            "Ligne de charge de refroidissement: ",
            "Línea de carga de refrigeración: ",
            "Liña de carga de refrixeración: ",
        ]
        self.label_combined: List[str] = [
            "Load line: ",
            "Load line: ",
            "Belastingslijn: ",
            "Linea di carico: ",
            "Ligne de charge: ",
            "Línea de carga: ",
            "Liña de carga: ",
        ]
        self.label_TimeStep: List[str] = [
            "Time step: ",
            "Zeitschritt: ",
            "Tijdsstap: ",
            "Passo temporale: ",
            "Pas de temps: ",
            "Paso temporal: ",
            "Paso temporal: ",
        ]
        self.label_DateLine: List[str] = [
            "Date line: ",
            "Datumsspalte: ",
            "Datumlijn: ",
            "Linea della data: ",
            "Ligne de date: ",
            "Línea de fecha: ",
            "Liña de data: ",
        ]
        self.option_column: List[str] = [
            "Thermal demand in one or two columns?,1 column,2 columns",
            "Thermischer Bedarf einer oder zwei Spalten?,1 Spalte,2 Spalten",
            "Thermische vraag in één of twee kolommen?,1 kolom,2 kolommen",
            "Thermal demand in one or two columns?,1 colonna,2 colonne",
            "Thermal demand in one or two columns?;,1 colonne,2 colonnes",
            "Thermal demand in one or two columns?,1 columna,2 columnas",
            "Thermal demand in one or two columns?,1 columna,2 columnas",
        ]
        self.pushButton_calculate: List[str] = ["Calculate", "Berechne", "Bereken", "Calcola", "Calculer", "Calcular", "Calcular"]
        self.ErrorMassage: List[str] = ["Error!", "Fehler!", "Error!", "Errore!", "Erreur!", "Error!", "Erro!"]
        self.UnableDataFormat: List[str] = [
            "Unable to open selected data format!",
            "Das ausgewählte Datenformat kann nicht geöffnet werden!",
            "Het is niet mogelijk het geselecteerde dataformaat te openen!",
            "Impossibile aprire il formato dati selezionato!",
            "Impossible d'ouvrir le format de données sélectionné!",
            "No se puede abrir el formato de datos seleccionado!",
            "Non se pode abrir o formato de datos escollido!",
        ]
        self.ChooseCSV: List[str] = [
            "Choose csv to load data fileImport",
            "Wählen Sie csv zum Laden einer Datendatei",
            "Selecteer csv",
            "Scegli csv per caricare il fileImport dei dati",
            "Choisissez csv pour charger le fichier de données.",
            "Elija csv para cargar el archivo de datos",
            "Escolla csv para cargar o ficheiro de datos",
        ]
        self.ChooseXLS: List[str] = [
            "Choose xlsx to load data fileImport",
            "Wählen Sie xlsx zum Laden einer Datendatei",
            "Selecteer xlsx",
            "Scegli xlsx per caricare il fileImport di dati",
            "Choisissez xlsx pour charger le fichier de données",
            "Elija xlsx para cargar el archivo de datos",
            "Escolla xlsx para cargar o ficheiro de datos",
        ]
        self.ChooseXLSX: List[str] = [
            "Choose xls to load data fileImport",
            "Wählen Sie xls zum Laden einer Datendatei",
            "Selecteer xls",
            "Scegli xls per caricare il fileImport di dati",
            "Choisissez xls pour charger le fichier de données",
            "Elija xls para cargar el archivo de datos",
            "Escolla xls para cargar o ficheiro de datos",
        ]
        self.no_file_selected: List[str] = [
            "No file selected.",
            "Keine Datei ausgewählt.",
            "Geen bestand geselecteerd.",
            "Nessun il file selezionato.",
            "Aucun fichier sélectionné.",
            "No se ha seleccionado ningún archivo.",
            "Non se escolleu ningún ficheiro.",
        ]
        self.ValueError: List[str] = [
            "Value error: check selected columns",
            "Wertefehler: ausgewählte Spalten prüfen",
            "Waarde-error: controleer geselecteerde kolommen",
            "Errore di valore: controlla le colonne selezionate",
            "Erreur de valeur : vérifiez les colonnes sélectionnées",
            "Error de valor: compruebe las columnas seleccionadas",
            "Erro de valor: comprobe as columnas escollidas",
        ]
        self.ColumnError: List[str] = [
            "Wrong column: check selected columns",
            "Falsche Spalte: ausgewählte Spalten prüfen",
            "Foute kolom: controleer geselecteerde kolommen",
            "Colonna errata: controlla le colonne selezionate",
            "Colonne incorrecte : vérifiez les colonnes sélectionnées",
            "Columna incorrecta: compruebe las columnas seleccionadas",
            "Columna incorrecta: comprobe as columnas escollidas",
        ]
        self.choose_load: List[str] = [
            "Choose *.GHEtool to load scenarios",
            "Wählen Sie *.GHEtool zum Laden von Szenarien",
            "Kies *.GHEtool bestand",
            "Scegliere *.GHEtool per caricare gli scenari",
            "Choisir *.GHEtool pour charger les scénarios",
            "Elija *.GHEtool para cargar escenarios",
            "Escolla *.GHEtool para cargar escenarios",
        ]
        self.SaveFigure: List[str] = [
            "Choose png location to save figure",
            "Wählen Sie einen png-Speicherort für die Abbildung",
            "Kies gewenste png locatie",
            "Scegli il percorso png per salvare la figura",
            "Choisissez l'emplacement png pour enregistrer la figure",
            "Elija la localización del png para guardar figura",
            "Escolla a localización do png para gardar figura",
        ]
        self.SaveData: List[str] = [
            "Choose csv location to save results",
            "Wählen Sie einen csv-Speicherort zum Speichern der Ergebnisse",
            "Kies gewenste csv locatie",
            "Scegli il percorso csv per salvare i risultati",
            "Choisissez l'emplacement csv pour enregistrer les résultats",
            "Elija la localización del csv para guardar resultados",
            "Escolla a localización do csv para gardar resultados",
        ]
        self.Save: List[str] = [
            "Choose *.GHEtool location to save scenarios",
            "Wählen Sie den *.GHEtool-Speicherort zum Speichern von Szenarien",
            "Kies gewenste *.GHEtool locatie",
            "Scegli il percorso *.GHEtool per salvare gli scenari",
            "Choisissez un emplacement *.GHEtool pour enregistrer les scénarios",
            "Elija la localización del *.GHEtool para guardar escenarios",
            "Escolla a localización do *.GHEtool para gardar escenarios",
        ]
        self.label_WarningCustomBorefield: List[str] = [
            "With the selected values a customized bore field will be calculated. This will dramatically increase the calculation time.",
            "Mit den gewählten Werten wird ein individuelles Borefeld berechnet. Dadurch wird die Berechnungszeit drastisch erhöht.",
            "Met de geselecteerde waarden moet een aangepast boorveld worden berekend.Dit zal de berekentijd drastisch doen toenemen.",
            "With the selected values a customized bore field will be calculated. This will dramatically increase the calculation time.",
            "With the selected values a customized bore field will be calculated. This will dramatically increase the calculation time.",
            "Un campo de captación será calculado con los valores seleccionados. El tiempo de computación aumentará drásticamente.",
            "Calcularase un campo de captación cos valores escollidos. O tempo de cálculo aumentará drásticamente.",
        ]
        self.label_WarningDepth: List[str] = [
            "The calculated size is below the suggested minimum of 50 m. The calculation may be incorrect.",
            "Die berechnete Größe liegt unter dem empfohlenen Minimum von 50 m. Die Berechnung ist möglicherweise fehlerhaft.",
            "De berekende diepte is lager dan het voorgestelde minimum van 50m.De berekening kan inaccuraat zijn.",
            "The calculated size is below the suggested minimum of 50 m. The calculation may be incorrect.",
            "The calculated size is below the suggested minimum of 50 m. The calculation may be incorrect.",
            "El tamaño calculado se encuentra por debajo del mínimo sugerido de 15 m. El dimensionado puede no ser correcto.",
            "O tamaño calculado está por debaixo do mínimo suxerido de 15 m. O dimensionado pode non ser o correcto.",
        ]
        self.checkBox_SizeBorefield: List[str] = [
            "Size borefield by length and width",
            "Dimensionierung des Bohrlochfeldes nach Länge und Breite",
            "Dimensioneer boorveld met breedte en lengte",
            "Size borefield by length and width",
            "Size borefield by length and width",
            "Size borefield by length and width",
            "Size borefield by length and width",
        ]
        self.label_Size_B: List[str] = [
            "Borehole spacing: ",
            "Bohrlochabstand: ",
            "Boorgatspatiëring: ",
            "Borehole spacing: ",
            "Borehole spacing: ",
            "Borehole spacing: ",
            "Borehole spacing: ",
        ]
        self.label_Size_L: List[str] = [
            "Length of rectangular field: ",
            "Länge des rechteckigen Feldes: ",
            "Lengte van het rechthoekig veld: ",
            "Length of rectangular field: ",
            "Length of rectangular field: ",
            "Length of rectangular field: ",
            "Length of rectangular field: ",
        ]
        self.label_Size_W: List[str] = [
            "Width of rectangular field: ",
            "Breite des rechteckigen Feldes: ",
            "Breedte van het rechthoekig veld: ",
            "Width of rectangular field: ",
            "Width of rectangular field: ",
            "Width of rectangular field: ",
            "Width of rectangular field: ",
        ]
        self.label_New: List[str] = ["New Project", "Neues Projekt", "Nieuw project", "New Project", "New Project", "New Project", "New Project"]
        self.label_Save: List[str] = ["Save Project", "Speichere Projekt", "Bewaar project", "Save Project", "Save Project", "Save Project", "Save Project"]
        self.label_Open: List[str] = ["Open Project", "Öffne Projekt", "Open project", "Open Project", "Open Project", "Open Project", "Open Project"]
        self.label_Save_As: List[str] = ["Save as", "Speichere Projekt unter ...", "Sla op als", "Save as", "Save as", "Save as", "Save as"]
        self.Calculation_Finished: List[str] = [
            "Calculation finished",
            "Berechnung fertiggestellt",
            "Berekening beëindigd",
            "Calculation finished",
            "Calculation finished",
            "Calculation finished",
            "Calculation finished",
        ]
        self.tool_imported: List[str] = [
            "GHEtool imported",
            "GHEtool importiert",
            "GHEtool geïmporteerd",
            "GHEtool imported",
            "GHEtool imported",
            "GHEtool imported",
            "GHEtool imported",
        ]
        self.tool_imported_start: List[str] = [
            "Start importing GHEtool",
            "Starte GHEtool zu importieren",
            "Start importering GHEtool",
            "Start importing GHEtool",
            "Start importing GHEtool",
            "Start importing GHEtool",
            "Start importing GHEtool",
        ]
        self.label_new_scenario: List[str] = [
            "Enter new scenario name",
            "Neuer Name für das Szenario",
            "Nieuwe naam scenario",
            "Enter new scenario name",
            "Enter new scenario name",
            "Enter new scenario name",
            "Enter new scenario name",
        ]
        self.new_name: List[str] = ["New name for ", "Neuer Name für ", "Nieuwe naam voor ", "New name for ", "New name for ", "New name for ", "New name for "]
        self.label_okay: List[str] = ["Okay ", "Okay ", "Oke ", "Okay ", "Okay ", "Okay ", "Okay "]
        self.label_abort: List[str] = ["Abort ", "Abbruch ", "Geannuleerd ", "Abort ", "Abort ", "Abort ", "Abort "]
        self.no_backup_file: List[str] = [
            "no backup fileImport",
            "Keine Sicherungsdatei gefunden",
            "geen backup fileImport",
            "no backup fileImport",
            "no backup fileImport",
            "no backup fileImport",
            "no backup fileImport",
        ]
        self.label_close: List[str] = ["Close", "Schließen", "Sluit", "Close", "Close", "Close", "Close"]
        self.label_cancel: List[str] = ["Cancel", "Abbrechen", "Annuleer", "Cancel", "Cancel", "Cancel", "Cancel"]
        self.label_CancelTitle: List[str] = ["Warning", "Warnung", "Waarschuwing", "Warning", "Warning", "Warning", "Warning"]
        self.label_LeaveScenarioText: List[str] = [
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Bist du sicher das Szenario zu verlasen? Alle ungesicherten Änderungen gehen sonst verloren.",
            "Bent u zeker dat u het scenario wilt verlaten?Onopgeslagen werk kan verloren gaan.",
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
        ]
        self.label_LeaveScenario: List[str] = [
            "Leave scenario",
            "Szenario verlassen",
            "Verlaat scenario",
            "Leave scenario",
            "Leave scenario",
            "Leave scenario",
            "Leave scenario",
        ]
        self.label_StayScenario: List[str] = [
            "Stay by scenario",
            "Beim Szenario bleiben",
            "Blijf bij scenario",
            "Stay by scenario",
            "Stay by scenario",
            "Stay by scenario",
            "Stay by scenario",
        ]
        self.X_Axis_Load: List[str] = [
            "Month of year",
            "Monat des Jahres",
            "Maand van het jaar",
            "Month of year",
            "Month of year",
            "Month of year",
            "Month of year",
        ]
        self.Y_Axis_Load_P: List[str] = [
            "Remaining peak thermal power [kW]",
            "Übriggebliebene Spitzenleistung [kW]",
            "Overblijvende piek [kW]",
            "Remaining peak thermal power [kW]",
            "Remaining peak thermal power [kW]",
            "Remaining peak thermal power [kW]",
            "Remaining peak thermal power [kW]",
        ]
        self.Y_Axis_Load_Q: List[str] = [
            "Remaining thermal energy [kWh]",
            "Übriggebliebene thermische Last [kWh]",
            "Overblijvende thermische energie [kWh]",
            "Remaining thermal energy [kWh]",
            "Remaining thermal energy [kWh]",
            "Remaining thermal energy [kWh]",
            "Remaining thermal energy [kWh]",
        ]
        self.menu_language: List[str] = ["Language", "Sprache", "Taal", "Languange", "Languange", "Idiom", "Lingua"]
        self.menu_settings: List[str] = ["Settings", "Einstellungen", "Instellingen", "Settings", "Settings", "Settings", "Settings"]
        self.menu_calculation: List[str] = ["Calculation", "Berechnung", "Berekening", "Calculation", "Calculation", "Calculation", "Calculation"]
        self.menu_file: List[str] = ["File", "Datei", "Bestand", "File", "File", "File", "File"]
        self.menu_scenario: List[str] = ["Scenario", "Szenario", "Scenario", "Scenario", "Scénario", "Escenario", "Escenario"]
        self.action_start_multiple: List[str] = [
            "Calculate all scenarios",
            "Berechne alle Szenarios",
            "Bereken alle scenarios",
            "Calculate all scenarios",
            "Calculate all scenarios",
            "Calculate all scenarios",
            "Calculate all scenarios",
        ]
        self.action_new: List[str] = ["New Project", "Neues Projekt", "Nieuw project", "New Project", "New Project", "New Project", "New Project"]
        self.action_save: List[str] = ["Save Project", "Speichere Projekt", "Bewaar project", "Save Project", "Save Project", "Save Project", "Save Project"]
        self.action_open: List[str] = ["Open Project", "Öffne Projekt", "Open project", "Open Project", "Open Project", "Open Project", "Open Project"]
        self.action_update_scenario: List[str] = [
            "Update scenario",
            "Szenario aktualisieren",
            "Update scenario",
            "Aggiorna scenario",
            "Mettre à jour le scénario",
            "Actualizar escenario",
            "Actualizar escenario",
        ]
        self.action_add_scenario: List[str] = [
            "Add scenario",
            "Szenario hinzufügen",
            "Nieuw scenario",
            "Aggiungi scenario",
            "Ajouter un scénario",
            "Añadir escenario",
            "Engadir escenario",
        ]
        self.action_delete_scenario: List[str] = [
            "Delete scenario",
            "Szenario löschen",
            "Verwijder scenario",
            "Cancella scenario",
            "Supprimer un scénario",
            "Borrar escenario",
            "Eliminar escenario",
        ]
        self.action_save_as: List[str] = ["Save as", "Speichere Projekt unter ...", "Sla op als", "Save as", "Save as", "Save as", "Save as"]
        self.button_rename_scenario: List[str] = [
            "Rename scenario",
            "Szenario umbenennen",
            "Hernoem scenario",
            "Rename scenario",
            "Rename scenario",
            "Rename scenario",
            "Rename scenario",
        ]
        self.button_rename_scenario: List[str] = [
            "Rename scenario",
            "Szenario umbenennen",
            "Hernoem scenario",
            "Rename scenario",
            "Rename scenario",
            "Rename scenario",
            "Rename scenario",
        ]
        self.label_Language_Head: List[str] = ["Language", "Sprache", "Taal", "Languange", "Languange", "Idiom", "Lingua"]
        self.label_aim_question: List[str] = [
            "What is the purpose of the simulation?",
            "Was ist das Ziel der Simulation?",
            "Wat is het doel van de berekening?",
            "What is the purpose of the simulation?",
            "What is the purpose of the simulation?",
            "What is the purpose of the simulation?",
            "What is the purpose of the simulation?",
        ]
        self.category_select_file: List[str] = [
            "Select data file",
            "Wähle Datendatei",
            "Selecteer data fileImport",
            "Select data file",
            "Select data file",
            "Select data file",
            "Select data file",
        ]
        self.label_Filename_2: List[str] = [
            "Filename: ",
            "Dateiname: ",
            "Bestandsnaam: ",
            "Nome fileImport: ",
            "Nom de fichier: ",
            "Nombre de archivo: ",
            "Nome de ficheiro: ",
        ]
        self.category_th_demand: List[str] = [
            "Thermal demands",
            "Thermische Lasten",
            "Thermische vraag",
            "Richieste termiche",
            "Demande thermique",
            "Cargas térmicas",
            "Cargas térmicas",
        ]
        self.option_heating_column: List[str] = [
            "Heating load line: ",
            "Heizlastspalte: ",
            "Belastingslijn verwarming: ",
            "Linea di carico di riscaldamento: ",
            "Ligne de charge de chauffage: ",
            "Línea de carga de calefacción: ",
            "Liña de carga de calefacción: ",
        ]
        self.option_cooling_column: List[str] = [
            "Cooling load line: ",
            "Kühllastspalte: ",
            "Belastingslijn koeling: ",
            "Linea del carico di raffreddamento: ",
            "Ligne de charge de refroidissement: ",
            "Línea de carga de refrigeración: ",
            "Liña de carga de refrixeración: ",
        ]
        self.option_single_column: List[str] = [
            "Load line: ",
            "Lastspalte: ",
            "Belastingslijn: ",
            "Linea di carico: ",
            "Ligne de charge: ",
            "Línea de carga: ",
            "Liña de carga: ",
        ]
        self.option_unit_data: List[str] = [
            "Unit data: ",
            "Dateneinheit: ",
            "Eenheid data: ",
            "Dati @dell'unità:  ",
            "Données de l'unité: ",
            "Datos de unidad: ",
            "Datos de unidade: ",
        ]
        self.category_save_scenario: List[str] = [
            "Scenario settings",
            "Szenarioeinstellungen",
            "Instellingen opslaan scenario",
            "Scenario saving settings",
            "Scenario saving settings",
            "Scenario saving settings",
            "Scenario saving settings",
        ]
        self.option_toggle_buttons: List[str] = [
            "Use toggle buttons?, No , Yes ",
            "Umschalterbutton?, Nein , Ja ",
            "Toggle-gedrag?, Nee , Ja",
            "Toggle buttons?, No , Yes ",
            "Toggle buttons?, No , Yes ",
            "Toggle buttons?, No , Yes ",
            "Toggle buttons?, No , Yes",
        ]
        self.option_auto_saving: List[str] = [
            "Use automatic saving?, No , Yes ",
            "Automatisches speichern nutzen?, Nein, Ja ",
            "Automatisch opslaan, Nee , Ja ",
            "Automatic saving, No , Yes ",
            "Automatic saving, No , Yes ",
            "Automatic saving, No , Yes ",
            "Automatic saving, No , Yes",
        ]
        self.hint_saving: List[str] = [
            "If Auto saving is selected the scenario will automatically saved if a scenario is changed. Otherwise the scenario has to be saved with the Update scenario button in the upper left corner if the changes should not be lost.",
            "Wenn Automatisch speichern ausgewählt ist, wird das Szenario automatisch gespeichert, wenn ein Szenario geändert wird. Andernfalls muss das Szenario mit der Schaltfläche Szenario aktualisieren in der oberen linken Ecke gespeichert werden, wenn die Änderungen nicht verloren gehen sollen.",
            'Als auto-opslaan is geselecteerd, zal het scenario automatisch worden opgeslagen als het wordt gewijzigd. Anders kan het scenario opgeslagen worden als op de "update scenario"-kopwordt gedrukt als deze niet verloren mogen gaan.',
            "If Auto saving is selected the scenario will automatically saved if a scenario is changed. Otherwise the scenario has to be saved with the Update scenario button in the upper left corner if the changes should not be lost.",
            "If Auto saving is selected the scenario will automatically saved if a scenario is changed. Otherwise the scenario has to be saved with the Update scenario button in the upper left corner if the changes should not be lost.",
            "If Auto saving is selected the scenario will automatically saved if a scenario is changed. Otherwise the scenario has to be saved with the Update scenario button in the upper left corner if the changes should not be lost.",
            "If Auto saving is selected the scenario will automatically saved if a scenario is changed. Otherwise the scenario has to be saved with the Update scenario button in the upper left corner if the changes should not be lost.",
        ]
        self.category_constant_rb: List[str] = [
            "Constant equivalent borehole resistance",
            "Konstanter equivalänter Bohrlochwiderstand",
            "Equivalente boorgatweerstand",
            "Equivalent borehole resistance",
            "Equivalent borehole resistance",
            "Equivalent borehole resistance",
            "Equivalent borehole resistance",
        ]
        self.category_fluid_data: List[str] = ["Fluid data", "Fluiddaten", "Fluidumdata", "Fluid data", "Fluid data", "Fluid data", "Fluid data"]
        self.option_fluid_conductivity: List[str] = [
            "Thermal conductivity [W/mK]: ",
            "Wärmeleitfähigkeit [W/mK]: ",
            "Thermische conductiviteit [W/mK]: ",
            "Thermal conductivity [W/mK]: ",
            "Thermal conductivity [W/mK]: ",
            "Thermal conductivity [W/mK]: ",
            "Thermal conductivity [W/mK]: ",
        ]
        self.option_fluid_mass_flow: List[str] = [
            "Mass flow rate [kg/s]: ",
            "Massenstrom [kg/s]: ",
            "Massadebiet [kg/s]: ",
            "Mass flow rate [kg/s]: ",
            "Mass flow rate [kg/s]: ",
            "Mass flow rate [kg/s]: ",
            "Mass flow rate [kg/s]: ",
        ]
        self.option_fluid_density: List[str] = [
            "Density [kg/m³]:",
            "Dichte [kg/m³]:",
            "Dichtheid [kg/m³]:",
            "Density [kg/m³]:",
            "Density [kg/m³]:",
            "Density [kg/m³]:",
            "Density [kg/m³]:",
        ]
        self.option_fluid_capacity: List[str] = [
            "Thermal capacity [J/kg K]:",
            "Wärmekapazität [J/kg K]:",
            "Thermisch warmtecapaciteit [J/kg K]:",
            "Thermal capacity [J/kg K]:",
            "Thermal capacity [J/kg K]:",
            "Thermal capacity [J/kg K]:",
            "Thermal capacity [J/kg K]:",
        ]
        self.option_fluid_viscosity: List[str] = [
            "Dynamic viscosity [Pa s]:",
            "Dynamische Viskosität [Pa s]:",
            "Dynamische viscositeit [Pa s]:",
            "Dynamic viscosity [Pa s]:",
            "Dynamic viscosity [Pa s]:",
            "Dynamic viscosity [Pa s]:",
            "Dynamic viscosity [Pa s]:",
        ]
        self.category_pipe_data: List[str] = ["Pipe data", "Rohrdaten", "Boorgatdata", "Pipe data", "Pipe data", "Pipe data", "Pipe data"]
        self.option_pipe_number: List[str] = [
            "Number of pipes [-]:",
            "Anzahl an Rohren [-]:",
            "Aantal U-buizen [-]:",
            "Number of pipes [-]:",
            "Number of pipes [-]:",
            "Number of pipes [-]:",
            "Number of pipes [-]:",
        ]
        self.option_pipe_grout_conductivity: List[str] = [
            "Grout thermal conductivity [W/mK]: ",
            "Wärmeleitfähigkeit der Füllung [W/mK]: ",
            "Thermische conductiviteit van de vulling [W/mK]: ",
            "Grout thermal conductivity [W/mK]: ",
            "Grout thermal conductivity [W/mK]: ",
            "Grout thermal conductivity [W/mK]: ",
            "Grout thermal conductivity [W/mK]: ",
        ]
        self.option_pipe_conductivity: List[str] = [
            "Pipe thermal conductivity [W/mK]: ",
            "Wärmeleitfähigkeit der Rohre [W/mK]: ",
            "Thermische conductiviteit van de leiding [W/mK]: ",
            "Pipe thermal conductivity [W/mK]: ",
            "Pipe thermal conductivity [W/mK]: ",
            "Pipe thermal conductivity [W/mK]: ",
            "Pipe thermal conductivity [W/mK]: ",
        ]
        self.option_pipe_outer_radius: List[str] = [
            "Outer pipe radius [m]: ",
            "Äußerer Rohrradius [m]: ",
            "Straal buitenkant leiding [m]: ",
            "Outer pipe radius [m]: ",
            "Outer pipe radius [m]: ",
            "Outer pipe radius [m]: ",
            "Outer pipe radius [m]: ",
        ]
        self.option_pipe_inner_radius: List[str] = [
            "Inner pipe radius [m]: ",
            "Innerer Rohrradius [m]: ",
            "Straal binnenkant leiding [m]: ",
            "Inner pipe radius [m]: ",
            "Inner pipe radius [m]: ",
            "Inner pipe radius [m]: ",
            "Inner pipe radius [m]: ",
        ]
        self.option_pipe_borehole_radius: List[str] = [
            "Borehole radius [m]:",
            "Bohrlochradius [m]:",
            "Boorgatstraal [m]:",
            "Borehole radius [m]:",
            "Borehole radius [m]:",
            "Borehole radius [m]:",
            "Borehole radius [m]:",
        ]
        self.option_pipe_borehole_radius_2: List[str] = [
            "Borehole radius [m]:",
            "Bohrlochradius [m]:",
            "Boorgatstraal [m]:",
            "Borehole radius [m]:",
            "Borehole radius [m]:",
            "Borehole radius [m]:",
            "Borehole radius [m]:",
        ]
        self.option_pipe_distance: List[str] = [
            "Distance of pipe until center [m]:",
            "Distanz zwischen Rohr und Mittelpunkt [m]:",
            "Afstand van de leiding tot het centrum van het boorgat [m]:",
            "Distance of pipe until center [m]:",
            "Distance of pipe until center [m]:",
            "Distance of pipe until center [m]:",
            "Distance of pipe until center [m]:",
        ]
        self.option_pipe_roughness: List[str] = [
            "Pipe roughness [m]:",
            "Rohrrauhigkeit [m]:",
            "Ruwheid leiding [m]:",
            "Pipe roughness [m]:",
            "Pipe roughness [m]:",
            "Pipe roughness [m]:",
            "Pipe roughness [m]:",
        ]
        self.option_pipe_depth: List[str] = [
            "Buried depth [m]:",
            "Vergrabungstiefe [m]:",
            "Deklaag [m]:",
            "Buried depth [m]:",
            "Buried depth [m]:",
            "Buried depth [m]:",
            "Buried depth [m]:",
        ]
        self.label_ResOptimizeLoad1: List[str] = [
            "The peak heating / cooling load is: ",
            "Die Spitzenheiz-/kühllast ist: ",
            "De piek verwarming / koeling is: ",
            "The peak heating / cooling load is: ",
            "The peak heating / cooling load is: ",
            "The peak heating / cooling load is: ",
            "The peak heating / cooling load is: ",
        ]
        self.label_ResOptimizeLoad2: List[str] = [
            "The heating / cooling load is: ",
            "Die Heiz-/Kühllast: ",
            "De belasting in verwarming / koeling is: ",
            "The heating / cooling load is:  ",
            "The heating / cooling load is: ",
            "The heating / cooling load is: ",
            "The heating / cooling load is: ",
        ]
        self.label_ResOptimizeLoad3: List[str] = ["This is ", "Dies ist ", "Dit is ", "This is ", "This is ", "This is ", "This is "]
        self.label_ResOptimizeLoad4: List[str] = [
            "% of the total load. ",
            "% der kompletten Last. ",
            "% van de totale belasting. ",
            "% of the total load. ",
            "% of the total load. ",
            "% of the total load. ",
            "% of the total load. ",
        ]
        self.label_CancelText: List[str] = [
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Bist du sicher das Programm zu schließen? Alle ungesicherten Änderungen gehen sonst verloren.",
            "Bent u zeker dat u wilt afsluiten? Niet opgeslagen wijzigingen zullen verloren gaan.",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Are you sure you want to quit? Any unsaved work will be lost.",
        ]
        self.label_ResOptimizeLoad5: List[str] = [
            "The remaining peak heating / cooling load is: ",
            "Die übrigbleibende Spitzenheiz-/kühllast ist: ",
            "De resulterende piek in verwarming / koeling is: ",
            "The remaining peak heating / cooling load is: ",
            "The remaining peak heating / cooling load is: ",
            "The remaining peak heating / cooling load is: ",
            "The remaining peak heating / cooling load is: ",
        ]
        self.label_ResOptimizeLoad6: List[str] = [
            "The remaining heating / cooling load is: ",
            "Die übrigbleibende Heiz-/Kühllast:  ",
            "De resulterende belasting in verwarming / koeling is: ",
            "The remaining heating / cooling load is: ",
            "The remaining heating / cooling load is: ",
            "The remaining heating / cooling load is: ",
            "The remaining heating / cooling load is: ",
        ]
        self.push_button_start_single: List[str] = [
            "Calculate current scenario",
            "Berechne ausgewähltes Szenario",
            "Bereken huidig scenario",
            "Calculate current scenario",
            "Calculate current scenario",
            "Calculate current scenario",
            "Calculate current scenario",
        ]
        self.not_calculated: List[str] = [
            "Not calculated",
            "Noch nicht berechnet",
            "Niet berekend",
            "Not calculated",
            "Not calculated",
            "Not calculated",
            "Not calculated",
        ]
        self.NoSolution: List[str] = [
            "No Solution found",
            "Keine Lösung gefunden",
            "Geen oplossing gevonden",
            "No Solution found",
            "No Solution found",
            "No Solution found",
            "No Solution found",
        ]
        self.aim_temp_profile: List[str] = [
            "Determine temperature profile",
            "Temperaturprofil berechnen",
            "Bepaal temperatuursprofiel",
            "Determine temperature profile",
            "Determine temperature profile",
            "Determine temperature profile",
            "Determine temperature profile",
        ]
        self.aim_req_depth: List[str] = [
            "Determine required depth",
            "Notwendige Tiefe berechnen",
            "Bereken benodigde diepte",
            "Determine required depth",
            "Determine required depth",
            "Determine required depth",
            "Determine required depth",
        ]
        self.aim_size_length: List[str] = [
            "Size by length and width",
            "Bestimme Länge und Breite des Bohrfeldes",
            "Dimensioneer bij breedte en lengte",
            "Size by length and width",
            "Size by length and width",
            "Size by length and width",
            "Size by length and width",
        ]
        self.aim_optimize: List[str] = [
            "Optimize load profile",
            "Optimiere Lastprofil",
            "Optimaliseer belastingsprofiel",
            "Optimize load profile",
            "Optimize load profile",
            "Optimize load profile",
            "Optimize load profile",
        ]
        self.category_calculation: List[str] = [
            "Calculation options",
            "Berechnungsoptionen",
            "Berekeningsopties",
            "Calculation options",
            "Calculation options",
            "Calculation options",
            "Calculation options",
        ]
        self.option_method_size_depth: List[str] = [
            "Method for size borehole depth:,  Simplified  ,  Monthly  ,  Hourly  ",
            "Methode zur Bohrlochtiefendimensionierung:,  Vereinfacht  ,  Monatlich  ,  Stündlich  ",
            "Methode voor boorvelddimensionering:,  Vereenvoudigd  ,  Maandelijks  ,  Uurlijks  ",
            "Method for size borehole depth:,  Simplified  ,  Monthly  ,  Hourly  ",
            "Method for size borehole depth:,  Simplified  ,  Monthly  ,  Hourly  ",
            "Method for size borehole depth:,  Simplified  ,  Monthly  ,  Hourly  ",
            "Method for size borehole depth:,  Simplified  ,  Monthly  ,  Hourly",
        ]
        self.option_method_size_length: List[str] = [
            "Method for size width and length:,  Simplified  ,  Monthly  ",
            "Methode für Längen- und Breitendimensionierung:,  Vereinfacht  ,  Monatlich  ",
            "Methode voor boorvelddimensionering:,  Vereenvoudigd  ,  Maandelijks  ",
            "Method for size width and length:,  Simplified  ,  Monthly  ",
            "Method for size width and length:,  Simplified  ,  Monthly  ",
            "Method for size width and length:,  Simplified  ,  Monthly  ",
            "Method for size width and length:,  Simplified  ,  Monthly",
        ]
        self.option_method_rb_calc: List[str] = [
            "Borehole resistance calculation method:, Constant , Dynamic ",
            "Methode zur Bohrlochwiderstangsberechnung:, Konstant , Dynamisch ",
            "Berekeningsmethode boorgatweerstand:, Constant , Dynamisch ",
            "Borehole resistance calculation method:, Constant , Dynamic ",
            "Borehole resistance calculation method:, Constant , Dynamic ",
            "Borehole resistance calculation method:, Constant , Dynamic ",
            "Borehole resistance calculation method:, Constant , Dynamic",
        ]
        self.category_earth: List[str] = [
            "Earth properties",
            "Erdeigenschaften",
            "Grondeigenschappen",
            "Earth properties",
            "Earth properties",
            "Earth properties",
            "Earth properties",
        ]
        self.cat_no_results: List[str] = ["No results", "Keine Ergebnisse", "Geen resultaten", "No results", "No results", "No results", "No results"]
        self.text_no_result: List[str] = [
            "No results are yet calculated",
            "Es wurden noch keine Ergebnisse berechnet",
            "Er zijn nog geen resultaten berekend",
            "No results are yet calculated",
            "No results are yet calculated",
            "No results are yet calculated",
            "No results are yet calculated",
        ]
        self.numerical_results: List[str] = [
            "Numerical results",
            "Numerische Ergebnisse",
            "Numerische resultaten",
            "Numerical results",
            "Numerical results",
            "Numerical results",
            "Numerical results",
        ]
        self.result_text_depth: List[str] = ["Depth: , m", "Tiefe: , m", "Diepte: , m", "Depth: , m", "Depth: , m", "Depth: , m", "Depth: , m"]
        self.result_Rb_calculated: List[str] = [
            "Equivalent borehole thermal resistance: , mK/W",
            "Äquivalenter thermischer Bohrlochwiderstand: , mK/W",
            "Equivalente boorgatweerstand: , mK/W",
            "Equivalent borehole thermal resistance: , mK/W",
            "Equivalent borehole thermal resistance: , mK/W",
            "Equivalent borehole thermal resistance: , mK/W",
            "Equivalent borehole thermal resistance: , mK/W",
        ]
        self.result_Reynolds: List[str] = [
            "Reynolds number: , ",
            "Reynoldszahl  : , ",
            "Reynoldsgetal: , ",
            "Reynolds number: , ",
            "Reynolds number: , ",
            "Reynolds number: , ",
            "Reynoldsnumber: ,",
        ]
        self.results_ground_temperature: List[str] = [
            "Average ground temperature: , °C",
            "Durchschnittliche Erdreichtemperatur , °C",
            "Gemiddelde grondtemperatuur: , °C",
            "Average ground temperature: , °C",
            "Average ground temperature: , °C",
            "Average ground temperature: , °C",
            "Average ground temperature: , °C",
        ]
        self.results_heating_load: List[str] = [
            "Heating load on the borefield: , kWh",
            "Die Heizlast für das Bohrfeld beträgt: , kWh",
            "Verwarmingsvraag op het boorveld: , kWh",
            "Heating load on the borefield: , kWh",
            "Heating load on the borefield: , kWh",
            "Heating load on the borefield: , kWh",
            "Heating load on the borefield: , kWh",
        ]
        self.results_heating_load_percentage: List[str] = [
            "This is , % of the heating load",
            "Das sind , % der Heizlast",
            "Dit is , % van de verwarmingsvraag",
            "This is , % of the heating load",
            "This is , % of the heating load",
            "This is , % of the heating load",
            "This is , % of the heating load",
        ]
        self.results_heating_ext: List[str] = [
            "Heating load external: , kWh",
            "Die externe Heizlast beträgt: , kWh",
            "Verwarmingsvraag extern: , kWh",
            "Heating load external: , kWh",
            "Heating load external: , kWh",
            "Heating load external: , kWh",
            "Heating load external: , kWh",
        ]
        self.results_heating_peak: List[str] = [
            "with a peak of: , kW",
            "mit einer Spitzenlast von , kW",
            "met een piek van: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
        ]
        self.results_cooling_load: List[str] = [
            "Cooling load on the borefield: , kWh",
            "Die Kühllast für das Bohrfeld beträgt: , kWh",
            "Koelvraag op het boorveld: , kWh",
            "Cooling load on the borefield: , kWh",
            "Cooling load on the borefield: , kWh",
            "Cooling load on the borefield: , kWh",
            "Cooling load on the borefield: , kWh",
        ]
        self.results_cooling_load_percentage: List[str] = [
            "This is , % of the cooling load",
            "Das sind , % der Kühllast",
            "Dit is , % van de koelvraag",
            "This is , % of the cooling load",
            "This is , % of the cooling load",
            "This is , % of the cooling load",
            "This is , % of the cooling load",
        ]
        self.results_cooling_ext: List[str] = [
            "Cooling load external: , kWh",
            "Die externe Kühllast beträgt: , kWh",
            "Koelvraag extern: , kWh",
            "Cooling load external: , kWh",
            "Cooling load external: , kWh",
            "Cooling load external: , kWh",
            "Cooling load external: , kWh",
        ]
        self.results_cooling_peak: List[str] = [
            "with a peak of: , kW",
            "mit einer Spitzenlast von , kW",
            "met een piek van: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
        ]
        self.max_temp: List[str] = [
            "The maximum average fluid temperature is , °C",
            "Die maximale Fluidtemperatur ist , °C",
            "De maximum gemiddelde fluïdumtemperatuur is , °C",
            "The maximum average fluid temperature is , °C",
            "The maximum average fluid temperature is , °C",
            "The maximum average fluid temperature is , °C",
            "The maximum average fluid temperature is , °C",
        ]
        self.min_temp: List[str] = [
            "The minimum average fluid temperature is , °C",
            "Die minimale Fluidtemperatur ist , °C",
            "De minimum gemiddelde fluïdumtemperatuur is , °C",
            "The minimum average fluid temperature is , °C",
            "The minimum average fluid temperature is , °C",
            "The minimum average fluid temperature is , °C",
            "The minimum average fluid temperature is , °C",
        ]
        self.figure_temperature_profile: List[str] = [
            "Temperature evolution, Temperature [°C], Time [years]",
            "Temperaturverlauf, Temperatur [°C], Zeit [Jahren]",
            "Temperatuurevolutie, Temperatuur [°C], Tijd [jaar]",
            "Temperature evolution, Temperature [°C], Time [years]",
            "Temperature evolution, Temperature [°C], Time [years]",
            "Temperature evolution, Temperature [°C], Time [years]",
            "Temperature evolution, Temperature [°C], Time [years]",
        ]
        self.legend_figure_temperature_profile: List[str] = [
            "Show legend?, No , Yes ",
            "Legende zeigen?, Nein , Ja ",
            "Toon legende?, Nee , Ja ",
            "Mostra la legenda?, No , Yes ",
            "Afficher la légende?, No , Yes ",
            "Mostrar leyenda?, No , Yes ",
            "Mostrar lenda?, No , Yes",
        ]
        self.hourly_figure_temperature_profile: List[str] = [
            "Hourly profile, No , Yes ",
            "Stündliches Profil, Nein , Ja ",
            "Uurlijks profiel, Nee , Ja ",
            "Hourly profile, No , Yes ",
            "Hourly profile, No , Yes ",
            "Hourly profile, No , Yes ",
            "Hourly profile, No , Yes",
        ]
        self.figure_load_duration: List[str] = [
            "Load-duration curve, Power [kW], Time [hours]",
            "Jahresdauerlinie, Leistung [kW], Zeit [Stunden]",
            "Belastings-duurcurve (geothermisch), Vermogen [kW], Tijd [jaar]",
            "Load-duration curve, Power [kW], Time [hours]",
            "Load-duration curve, Power [kW], Time [hours]",
            "Load-duration curve, Power [kW], Time [hours]",
            "Load-duration curve, Power [kW], Time [hours]",
        ]
        self.legend_figure_load_duration: List[str] = [
            "Show legend?, No , Yes ",
            "Legende zeigen?, Nein , Ja ",
            "Toon legende?, Nee , Ja ",
            "Mostra la legenda?, No , Yes ",
            "Afficher la légende?, No , Yes ",
            "Mostrar leyenda?, No , Yes ",
            "Mostrar lenda?, No , Yes",
        ]
        self.option_len_peak_heating: List[str] = [
            "Peak duration heating [hours]: ",
            "Spitzenlastlänge Heizen [Stunden]: ",
            "Piekduur verwarming [uren]: ",
            "Peak duration heating [hours]: ",
            "Peak duration heating [hours]: ",
            "Peak duration heating [hours]: ",
            "Peak duration heating [hours]:",
        ]
        self.option_len_peak_cooling: List[str] = [
            "Peak duration cooling [hours]: ",
            "Spitzenlastlänge Kühlen [Stunden]: ",
            "Piekduur koeling [uren]: ",
            "Peak duration cooling [hours]: ",
            "Peak duration cooling [hours]: ",
            "Peak duration cooling [hours]: ",
            "Peak duration cooling [hours]:",
        ]
        self.option_temperature_profile_hourly: List[str] = [
            "Should hourly data be used for the temperature profile?, No , Yes ",
            "Should hourly data be used for the temperature profile?, No , Yes ",
            "Moet uurlijkse data gebruikt worden voor het temperatuursprofiel?, Nee , Ja ",
            "Should hourly data be used for the temperature profile?, No , Yes ",
            "Should hourly data be used for the temperature profile?, No , Yes ",
            "Should hourly data be used for the temperature profile?, No , Yes ",
            "Should hourly data be used for the temperature profile?, No , Yes",
        ]
        self.option_ground_temp_gradient: List[str] = [
            "Ground temperature at infinity [°C]: ",
            "Erdreichtemperatur in der Unendlichkeit [°C]: ",
            "Grondtemperatuur op oneindig [°C]: ",
            "Temperatura del terreno all'infinito [°C]: ",
            "Température du sol à l'infini [°C]: ",
            "Temperatura del suelo en el infinito [°C]: ",
            "Temperatura do chan no infinito [°C]:",
        ]
        self.option_ground_heat_flux: List[str] = [
            "Geothermal heat flux [W/m2]:",
            "Geothermischer Wärmestrom [W/m²]:",
            "Geothermische warmteflux [W/m2]:",
            "Geothermal heat flux [W/m2]:",
            "Geothermal heat flux [W/m2]:",
            "Geothermal heat flux [W/m2]:",
            "Geothermal heat flux [W/m2]:",
        ]
        self.option_n_threads: List[str] = [
            "Number of parallel threads [-]: ",
            "Anzahl an parallelen Prozessen [-]:",
            "Aantal parallelle threads [-]:",
            "Number of parallel threads [-]: ",
            "Number of parallel threads [-]: ",
            "Number of parallel threads [-]: ",
            "Number of parallel threads [-]: ",
        ]
        self.option_number_circle_boreholes: List[str] = [
            "Number of boreholes [-]:",
            "Anzahl der Bohrlöcher [-]:",
            "Aantal boringen [-]:",
            "Number of boreholes [-]:",
            "Number of boreholes [-]:",
            "Number of boreholes [-]:",
            "Number of boreholes [-]:",
        ]
        self.option_borefield_radius: List[str] = [
            "Distance of the boreholes from the center of the field [m]:",
            "Abstand der Bohrlöcher vom Zentrum der Feldes [m]:",
            "Afstand van de boringen tot het centrum van de cirkel [m]:",
            "Distance of the boreholes from the center of the field [m]:",
            "Distance of the boreholes from the center of the field [m]:",
            "Distance of the boreholes from the center of the field [m]:",
            "Distance of the boreholes from the center of the field [m]:",
        ]
        self.custom_borefield: List[str] = [
            "Custom borefield,Borehole,x [m]:,y [m]:,Depth [m]:,Buried depth [m]:,Borehole radius [m]",
            "Benutzerdefiniertes Bohrelochfeld,Bohrloch,x [m]:,y [m]:,Tiefe [m]:,Vergrabungstiefe [m]:,Bohrlochradius [m]",
            "Manueel boorveld,Boorgat,x [m]:,y [m]:,Diepte [m]:,Deklaag [m]:,Boorgatstraal [m]",
            "Custom borefield,Borehole,x [m]:,y [m]:,Depth [m]:,Buried depth [m]:,Borehole radius [m]",
            "Custom borefield,Borehole,x [m]:,y [m]:,Depth [m]:,Buried depth [m]:,Borehole radius [m]",
            "Custom borefield,Borehole,x [m]:,y [m]:,Depth [m]:,Buried depth [m]:,Borehole radius [m]",
            "Custom borefield,Borehole,x [m]:,y [m]:,Depth [m]:,Buried depth [m]:,Borehole radius [m]",
        ]
        self.option_seperator_borefield: List[str] = [
            "Separator in file:,Semicolon ';',Comma '++',Tab '   '",
            "Trenner in der Datei:,Semikolon ';',Komma '++',Tab '   '",
            "Scheidingsteken in file:,Puntkomma ';',Komma '++',Tab '   '",
            "Separator in file:,Semicolon ';',Comma '++',Tab '   '",
            "Separator in file:,Semicolon ';',Comma '++',Tab '   '",
            "Separator in file:,Semicolon ';',Comma '++',Tab '   '",
            "Separator in file:,Semicolon ';',Comma '++',Tab '   '",
        ]
        self.borefield_file: List[str] = [
            "Filename: ",
            "Dateiname: ",
            "Bestandsnaam: ",
            "Nome fileImport: ",
            "Nom de fichier: ",
            "Nombre de archivo: ",
            "Nome de ficheiro: ",
        ]
        self.import_borefield: List[str] = ["Load", "Laden", "Laad", "Caricare", "Chargement", "Cargar", "Cargar"]
        self.option_decimal_borefield: List[str] = [
            "Decimal sign in file:,Point '.',Comma '++'",
            "Dezimalzeichen in der Datei:,Punkt '.',Komma '++'",
            "Decimaalteken in de file:,Punt '.',Komma '++'",
            "Decimal sign in file:,Point '.',Comma '++'",
            "Decimal sign in file:,Point '.',Comma '++'",
            "Decimal sign in file:,Point '.',Comma '++'",
            "Decimal sign in file:,Point '.',Comma '++'",
        ]
        self.category_demand_building_or_geo: List[str] = [
            "Load type ",
            "Art der Belastung ",
            "Type belasting ",
            "Load type ",
            "Load type ",
            "Load type",
            "Load type",
        ]
        self.geo_load: List[str] = [
            "Load type, Geothermal , Building ",
            "Art der Belastung, Geothermieseite , Gebäudeseite ",
            "Type belasting, grondzijdig , gebouwzijdig ",
            "Load type, Geothermal , Building ",
            "Load type, Geothermal , Building ",
            "Load type, Geothermal , Building ",
            "Load type, Geothermal , Building ",
        ]
        self.SCOP: List[str] = ["SCOP [-]: ", "SCOP [-]: ", "SCOP [-]: ", "SCOP [-]: ", "SCOP [-]: ", "SCOP [-]: ", "SCOP [-]:"]
        self.SEER: List[str] = ["SEER [-]: ", "SEER [-]: ", "SEER [-]: ", "SEER [-]: ", "SEER [-]: ", "SEER [-]: ", "SEER [-]:"]
        self.results_heating_peak_geo: List[str] = [
            "with a peak of: , kW",
            "mit einer Spitzenlast von , kW",
            "met een piek van: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
        ]
        self.results_cooling_peak_geo: List[str] = [
            "with a peak of: , kW",
            "mit einer Spitzenlast von , kW",
            "met een piek van: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
            "with a peak of: , kW",
        ]
        self.option_ground_temp_gradient: List[str] = [
            "Surface temperature [°C]: ",
            "Umgebungstemperatur[°C]: ",
            "Omgevingstemperatuur [°C]: ",
            "Surface temperature [°C]: ",
            "Surface temperature [°C]: ",
            "Surface temperature [°C]: ",
            "Surface temperature [°C]:",
        ]
        self.hint_press_load: List[str] = [
            "Press 'load' to load the hourly data.",
            "Drücken Sie 'Laden', um die stündlichen Daten zu laden.",
            "Druk op 'laden' om de data in te lezen.",
            "Press 'load' to load the hourly data.",
            "Press 'load' to load the hourly data.",
            "Press 'load' to load the hourly data.",
            "Press 'load' to load the hourly data.",
        ]
        self.cannot_load_new_version: List[str] = [
            " You cannot load a file that is from a newer GHEtool version.",
            "Sie können keine Datei laden, die von einer neueren GHEtool-Version stammt.",
            "Je kunt geen bestand laden dat van een nieuwere GHEtool-versie is.",
            "You cannot load a file that is from a newer GHEtool version.",
            "You cannot load a file that is from a newer GHEtool version.",
            "You cannot load a file that is from a newer GHEtool version.",
            "You cannot load a file that is from a newer GHEtool version.",
        ]
        self.pipe_thermal_resistance: List[str] = [
            "The equivalent borehole thermal resistance (at , mK/W",
            "Äquivalenter thermischer Bohrlochwiderstand (auf , mK/W",
            "De equivalente boorgatweerstand (op , mK/W",
            "The equivalent borehole thermal resistance (at , mK/W",
            "The equivalent borehole thermal resistance (at , mK/W",
            "The equivalent borehole thermal resistance (at , mK/W",
            "The equivalent borehole thermal resistance (at , mK/W",
        ]
        self.option_U_pipe_or_coaxial_pipe: List[str] = [
            "Borehole interals:, U-tube , Coaxial pipe ",
            "Sondentyp:, U-Sonde , Koaxialsonde ",
            "Type leiding:, U-buis , Coaxiaal",
            "Borehole interal:, U-tube , Coaxial pipe ",
            "Borehole interal:, U-tube , Coaxial pipe ",
            "Borehole interal:, U-tube , Coaxial pipe ",
            "Borehole interal:, U-tube , Coaxial pipe",
        ]
        self.option_pipe_coaxial_inner_inner: List[str] = [
            "Inner pipe inner radius [m]: ",
            "Innerer Radius des inneren Rohres [m]:",
            "Binnenste leiding binnenstraal [m]:",
            "Inner pipe inner radius [m]: ",
            "Inner pipe inner radius [m]: ",
            "Inner pipe inner radius [m]: ",
            "Inner pipe inner radius [m]:",
        ]
        self.option_pipe_coaxial_outer_inner: List[str] = [
            "Outer pipe inner radius [m]:",
            "Äußerer Radius des inneren Rohres [m]:",
            "Buitenste leiding binnenstraal [m]:",
            "Outer pipe inner radius [m]:",
            "Outer pipe inner radius [m]:",
            "Outer pipe inner radius [m]:",
            "Outer pipe inner radius [m]:",
        ]
        self.option_pipe_coaxial_inner_outer: List[str] = [
            "Inner pipe outer radius [m]:",
            "Innerer Radius des äußeren Rohres [m]:",
            "Binnenste leiding buitenstraal [m]:",
            "Inner pipe outer radius [m]:",
            "Inner pipe outer radius [m]:",
            "Inner pipe outer radius [m]:",
            "Inner pipe outer radius [m]:",
        ]
        self.option_pipe_coaxial_outer_outer: List[str] = [
            "Outer pipe outer radius [m]:",
            "Äußerer Radius des äußeren Rohres [m]:",
            "Buitenste leiding buitenstraal [m]:",
            "Outer pipe outer radius [m]:",
            "Outer pipe outer radius [m]:",
            "Outer pipe outer radius [m]:",
            "Outer pipe outer radius [m]:",
        ]
        self.option_advanced_options: List[str] = [
            "Enable advanced options?, No , Yes ",
            "Aktiviere erweiterte Optionen?, Nein , Ja ",
            "Activeer geavanceerde opties?, Nee, Ja ",
            "Enable advanced options?, No , Yes ",
            "Enable advanced options?, No , Yes ",
            "Enable advanced options?, No , Yes ",
            "Enable advanced options?, No , Yes ",
        ]
        self.category_advanced_options: List[str] = [
            "Advanced options",
            "Erweiterte Optionen",
            "Geavanceerde opties",
            "Advanced options",
            "Advanced options",
            "Advanced options",
            "Advanced options",
        ]
        self.option_atol: List[str] = [
            "Absolute tolerance for iteration convergence [m]:",
            "Absolute Toleranz für Iterationskonvergenz [m]:",
            "Absolute tolerantie voor convergentie van de iteratie [m]:",
            "Absolute tolerance for iteration convergence [m]:",
            "Absolute tolerance for iteration convergence [m]:",
            "Absolute tolerance for iteration convergence [m]:",
            "Absolute tolerance for iteration convergence [m]:",
        ]
        self.option_rtol: List[str] = [
            "Relative tolerance for iteration convergence [%]:",
            "Relative Toleranz für Iterationskonvergenz [%]:",
            "Relative tolerantie voor de convergentie van de iteratie [%]:",
            "Relative tolerance for iteration convergence [%]:",
            "Relative tolerance for iteration convergence [%]:",
            "Relative tolerance for iteration convergence [%]:",
            "Relative tolerance for iteration convergence [%]:",
        ]
        self.option_max_nb_of_iter: List[str] = [
            "Maximum number of iterations to check for convergence [-]:",
            "Maximale Anzahl der Iterationen, um auf Konvergenz zu prüfen [-]:",
            "Maximum aantal iteraties [-]:",
            "Maximum number of iterations to check for convergence [-]:",
            "Maximum number of iterations to check for convergence [-]:",
            "Maximum number of iterations to check for convergence [-]:",
            "Maximum number of iterations to check for convergence [-]:",
        ]
        self.SCOP_DHW: List[str] = ["SCOP DHW [-]:", "SCOP Warmwasser [-]", "SCOP SWW [-]", "SCOP DHW [-]", "SCOP DHW [-]", "SCOP DHW [-]", "SCOP DHW [-]"]
        self.option_include_dhw: List[str] = [
            "Include Domestic Hot Water?, No , Yes ",
            "Warmwasser hinzufügen?, Nein , Ja ",
            "Sanitair warm water toevoegen?, Nee , Ja ",
            "Include Domestic Hot Water?, No , Yes ",
            "Include Domestic Hot Water?, No , Yes ",
            "Include Domestic Hot Water?, No , Yes ",
            "Include Domestic Hot Water?, No , Yes ",
        ]
        self.DHW: List[str] = [
            "Yearly DHW consumption [kWh/year]:",
            "Jährlicher Verbrauch von Warmwasser [kWh/Jahr]:",
            "Jaarlijkse SWW vraag [kWh/jaar]",
            "Yearly DHW consumption [kWh/year]:",
            "Yearly DHW consumption [kWh/year]:",
            "Yearly DHW consumption [kWh/year]:",
            "Yearly DHW consumption [kWh/year]:",
        ]
        self.option_fluid_selector: List[str] = [
            "Fluid properties:, Custom , Water-glycol  ",
            "Fluid-Eigenschaften: Benutzerdefiniert, Wasser-Glykol",
            "Vloeistofeigenschappen:, Manueel , Water-glycol  ",
            "Fluid properties:, Custom , Water-glycol  ",
            "Fluid properties:, Custom , Water-glycol  ",
            "Fluid properties:, Custom , Water-glycol  ",
            "Fluid properties:, Custom , Water-glycol  ",
        ]
        self.option_glycol_selector: List[str] = [
            "Type of glycol:, Ethylene glycol , Propylene glycol ",
            "Glykoltyp: Ethylenglykol, Propylenglykol",
            "Type glycol:, Ethyleenglycol , Propyleenglycol",
            "Type of glycol:, Ethylene glycol , Propylene glycol ",
            "Type of glycol:, Ethylene glycol , Propylene glycol ",
            "Type of glycol:, Ethylene glycol , Propylene glycol ",
            "Type of glycol:, Ethylene glycol , Propylene glycol ",
        ]
        self.option_glycol_percentage: List[str] = [
            "Percentage of glycol [%]:",
            "Glykolanteil [%]:",
            "Percentage glycol [%]:",
            "Percentage of glycol [%]:",
            "Percentage of glycol [%]:",
            "Percentage of glycol [%]:",
            "Percentage of glycol [%]:",
        ]
        self.option_fluid_ref_temp: List[str] = [
            "Reference fluid temperature [°C]:",
            "Referenz-Fluidtemperatur [°C]:",
            "Referentietemperatuur fluidum [°C]:",
            "Reference fluid temperature [°C]:",
            "Reference fluid temperature [°C]:",
            "Reference fluid temperature [°C]:",
            "Reference fluid temperature [°C]:",
        ]
        self.option_ground_database: List[str] = [
            "Select from the database: ",
            "Aus der Datenbank auswählen:",
            "Selecteer van de databank:",
            "Select from the database: ",
            "Select from the database: ",
            "Select from the database: ",
            "Select from the database: ",
        ]
        self.hint_ground_database: List[str] = [
            "The ground temperature at the selected location is: , °C",
            "Die Bodentemperatur an der ausgewählten Stelle beträgt: , °C",
            "De grondtemperatuur op de geselecteerde locatie is: , °C",
            "The ground temperature at the selected location is: , °C",
            "The ground temperature at the selected location is: , °C",
            "The ground temperature at the selected location is: , °C",
            "The ground temperature at the selected location is: , °C",
        ]
        self.hint_borehole_depth: List[str] = [
            "The borehole depth is relative w.r.t. the buried depth, not the surface level.",
            "Die Bohrlochtiefe ist relativ zur eingegrabenen Tiefe, nicht zur Geländeoberfläche.",
            "De boorgatdiepte is relatief ten opzichte van de deklaag, niet het maaiveld.",
            "The borehole depth is relative w.r.t. the buried depth, not the surface level.",
            "The borehole depth is relative w.r.t. the buried depth, not the surface level.",
            "The borehole depth is relative w.r.t. the buried depth, not the surface level.",
            "The borehole depth is relative w.r.t. the buried depth, not the surface level.",
        ]
        self.hint_ground_flux_database: List[str] = [
            "The geothermal heat flux at the selected location is: , W/m²",
            "Die geothermische Wärmeflussdichte an der ausgewählten Stelle beträgt: , W/m²",
            "De geothermische warmteflux op de gekozen locatie is: , W/m²",
            "The geothermal heat flux at the selected location is: , W/m²",
            "The geothermal heat flux at the selected location is: , W/m²",
            "The geothermal heat flux at the selected location is: , W/m²",
            "The geothermal heat flux at the selected location is: , W/m²",
        ]
        self.option_source_ground_temperature: List[str] = [
            "Source of the ground temperature data:, Measured , Database , Custom",
            "Quelle der Bodentemperaturdaten:, Gemessen , Datenbank , Benutzerdefiniert",
            "Bron voor de grondtemperatuur:, Gemeten , Databank , Manueel",
            "Source of the ground temperature data:, Measured , Database , Custom",
            "Source of the ground temperature data:, Measured , Database , Custom",
            "Source of the ground temperature data:, Measured , Database , Custom",
            "Source of the ground temperature data:, Measured , Database , Custom",
        ]
        self.option_flux_gradient: List[str] = [
            "How to take into account temperature variation?, Flux , Gradient",
            "Wie berücksichtigt man Temperaturschwankungen?, Fluss , Gradient ",
            "Hoe temperatuurvariatie meenemen?, Flux , Gradiënt ",
            "How to take into account temperature variation?, Flux , Gradient",
            "How to take into account temperature variation?, Flux , Gradient",
            "How to take into account temperature variation?, Flux , Gradient",
            "How to take into account temperature variation?, Flux , Gradient",
        ]
        self.label_Continue: List[str] = ["Continue", "Fortsetzen", "Ga verder", "Continue", "Continue", "Continue", "Continue"]
        self.label_ContinueText: List[str] = [
            "Would you like to save the project before you continue?",
            "Möchten Sie das Projekt speichern bevor sie fortfahren?",
            "Wilt u het project opslaan voor u verdergaat?",
            "Would you like to save the project before you continue?",
            "Would you like to save the project before you continue?",
            "Would you like to save the project before you continue?",
            "Would you like to save the project before you continue?",
        ]
        self.label_ContinueTitle: List[str] = ["Warning", "Warnung", "Waarschuwing", "Warning", "Warning", "Warning", "Warning"]
