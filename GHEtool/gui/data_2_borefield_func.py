"""
Functions to create a borefield class from a datastorage
"""
from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING
import logging
import warnings

import numpy as np
from GHEtool import Borefield, FluidData, MultipleUTube, GroundConstantTemperature, GroundFluxTemperature, GroundTemperatureGradient, CoaxialPipe
from GHEtool.VariableClasses import GroundData, MonthlyGeothermalLoadAbsolute, HourlyGeothermalLoad, DATASET
from GHEtool.gui.gui_structure import load_data_GUI
import pygfunction as gt

if TYPE_CHECKING:  # pragma: no cover
    from numpy.typing import NDArray
    from ScenarioGUI.gui_classes.gui_data_storage import DataStorage


def data_2_borefield(ds: DataStorage) -> tuple[Borefield, partial[[], None]]:
    """
    This function converts the data from the GUI, stored in a data storage to a borefield object with a function
    that can be handled by the ScenarioGUI processing unit.

    Parameters
    ----------
    ds : DataStorage
        Data storage object that contains all the values inputted in a certain scenario within the GUI.

    Returns
    -------
    tuple
        Borefield object (filled with the data from the gui), partial function for a specific functionality of aim of the GUI.
    """
    # import bore field class from GHEtool and not in start up to save time
    from GHEtool import Borefield

    # create the bore field object
    borefield = Borefield(
        gui=True,
    )
    _set_boreholes(ds, borefield)
    # set temperature boundaries
    borefield.set_max_avg_fluid_temperature(ds.option_max_temp)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(ds.option_min_temp)  # minimum temperature

    # set ground data
    borefield.set_ground_parameters(_create_ground_data(ds))

    ### GENERAL SETUPS

    # check if Rb is a constant, otherwise set the fluid/pipe parameters
    if ds.option_method_rb_calc > 0:
    # Rb will be dynamically calculated
    # set fluid and pipe data
        borefield.set_fluid_parameters(_create_fluid_data(ds))
        borefield.set_pipe_parameters(_create_pipe_data(ds))
    else:
        borefield.Rb = ds.option_constant_rb  # equivalent borehole resistance (K/W)

    # set monthly loads
    peak_heating, peak_cooling, monthly_load_heating, monthly_load_cooling = _create_monthly_loads_peaks(ds)
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # set peak lengths
    load.peak_cooling_duration = ds.option_len_peak_cooling
    load.peak_heating_duration = ds.option_len_peak_heating
    borefield.load = load

    # set hourly loads if available
    if ds.option_temperature_profile_hourly == 1 or ds.aim_optimize:
        peak_heating, peak_cooling = load_data_GUI(
            filename=ds.option_filename,
            thermal_demand=ds.option_column,
            heating_load_column=ds.option_heating_column[1],
            cooling_load_column=ds.option_cooling_column[1],
            combined=ds.option_single_column[1],
            sep=";" if ds.option_seperator_csv == 0 else ",",
            dec="." if ds.option_decimal_csv == 0 else ",",
            fac=0.001 if ds.option_unit_data == 0 else 1 if ds.option_unit_data == 1 else 1000,
            hourly=True)

        # hourly data to be loaded
        hourly_data = HourlyGeothermalLoad()
        hourly_data.hourly_cooling_load = peak_cooling
        hourly_data.hourly_heating_load = peak_heating
        borefield.load = hourly_data

        # when this load is a building load, it needs to be converted to a geothermal load
        if ds.geo_load == 1 and not ds.aim_optimize:
            hourly_data = HourlyGeothermalLoad()
            hourly_data.hourly_cooling_load = peak_cooling * (1 + 1 / ds.SEER)
            hourly_data.hourly_heating_load = peak_heating * (1 - 1 / ds.SCOP)
            borefield.load = hourly_data
            borefield._secundary_borefield_load.hourly_heating_load = peak_heating
            borefield._secundary_borefield_load.hourly_cooling_load = peak_cooling

    # add dhw when needed
    if ds.option_include_dhw == 1 and not ds.aim_optimize:
        SCOP = ds.SCOP_DHW if ds.geo_load == 1 else 99999999999
        borefield.load.dhw = ds.DHW * (1 - 1 / SCOP)
        borefield._secundary_borefield_load.dhw = ds.DHW

    # set up the borefield sizing
    borefield.calculation_setup(use_constant_Rb=ds.option_method_rb_calc == 0,
                                L2_sizing=ds.option_method_size_depth == 0,
                                L3_sizing=ds.option_method_size_depth == 1,
                                L4_sizing=ds.option_method_size_depth == 2,
                                atol=ds.option_atol,
                                rtol=ds.option_rtol,
                                max_nb_of_iterations=ds.option_max_nb_of_iter)

    # set borefield simulation period
    borefield.simulation_period = ds.option_simu_period

    ### FUNCTIONALITIES (i.e. aims)

    # if load should be optimized do this
    if ds.aim_optimize:
        # optimize load profile without printing the results
        return borefield, partial(borefield.optimise_load_profile, borefield.load, borefield.H, ds.SCOP, ds.SEER)

            ### Size borefield
    if ds.aim_req_depth:
        return borefield, partial(borefield.size)


        ### Size borefield by length and width
        # if ds.aim_size_length:
        #     try:
        #         # To be implemented
        #         # option_method_size_length
        #         pass
        #     except RuntimeError or ValueError:
        #         # save bore field in Datastorage
        #         ds.borefield = None
        #         # return Datastorage as signal
        #         self.any_signal.emit((ds, self.idx))
        #         return

        ### Plot temperature profile
    if ds.aim_temp_profile:
        return borefield, partial(borefield.calculate_temperatures, borefield.H)


def _set_boreholes(ds: DataStorage, borefield: Borefield) -> None:
    """
    This function creates the borefield based on the data in the DataStorage and sets attributes it to the borefield object.

    Parameters
    ----------
    ds : DataStorage
        Data storage object that contains all the values inputted in a certain scenario within the GUI.
    borefield : Borefield
        Borfield object to which a borefield should be set.

    Returns
    -------
    None
    """
    tilt = ds.option_tilted / 360 * 2 * np.pi
    if ds.aim_rect:
        boreholes = gt.boreholes.rectangle_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_length, ds.option_depth,
                                                  ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt)
        borefield.set_borefield(boreholes)
        return
    if ds.aim_Box_shaped:
        boreholes = gt.boreholes.box_shaped_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_length, ds.option_depth,
                                                  ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt)
        borefield.set_borefield(boreholes)
        return
    if ds.aim_L_shaped:
        boreholes = gt.boreholes.L_shaped_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_length, ds.option_depth,
                                                  ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt)
        borefield.set_borefield(boreholes)
        return
    if ds.aim_U_shaped:
        boreholes = gt.boreholes.U_shaped_field(ds.option_width, ds.option_length, ds.option_spacing_width, ds.option_spacing_length, ds.option_depth,
                                                  ds.option_pipe_depth, ds.option_pipe_borehole_radius, tilt)
        borefield.set_borefield(boreholes)
        return
    if ds.aim_circle:
        boreholes = gt.boreholes.circle_field(ds.option_number_circle_boreholes, ds.option_borefield_radius, ds.option_depth, ds.option_pipe_depth,
                                              ds.option_pipe_borehole_radius, tilt)
        borefield.set_borefield(boreholes)
        return
    borefield_gt = [gt.boreholes.Borehole(H, D, r_b, x=x, y=y) for x, y, H, D, r_b in ds.custom_borefield]
    borefield.set_borefield(borefield_gt)
    return


def _create_fluid_data(ds: DataStorage) -> FluidData:
    """
    This function creates a FluidData object based on the data entered in the GUI.

    Parameters
    ----------
    ds : DataStorage
        Data storage object that contains all the values inputted in a certain scenario within the GUI.

    Returns
    -------
    FluidData
    """
    fluid_data = FluidData(ds.option_fluid_mass_flow, ds.option_fluid_conductivity, ds.option_fluid_density, ds.option_fluid_capacity, ds.option_fluid_viscosity)
    if ds.option_fluid_selector == 1:

        # set warnings as error
        warnings.filterwarnings("error")

        # use pygfunction to get fluid properties
        if ds.option_glycol_selector == 0:
            fluid_data.import_fluid_from_pygfunction(gt.media.Fluid('MEG',
                                                                    ds.option_glycol_percentage, ds.option_fluid_ref_temp))
        else:
            fluid_data.import_fluid_from_pygfunction(gt.media.Fluid('MPG',
                                                                    ds.option_glycol_percentage, ds.option_fluid_ref_temp))
    warnings.resetwarnings()
    return fluid_data


def _create_pipe_data(ds: DataStorage) -> MultipleUTube | CoaxialPipe:
    """
    This function creates a PipeData (either a MultipleUTube or a CoaxialPipe) object based on the data entered in the GUI.

    Parameters
    ----------
    ds : DataStorage
        Data storage object that contains all the values inputted in a certain scenario within the GUI.

    Returns
    -------
    MultipleUTube or CoaxialPipe
    """
    if ds.option_U_pipe_or_coaxial_pipe == 0:
        return MultipleUTube(ds.option_pipe_grout_conductivity, ds.option_pipe_inner_radius, ds.option_pipe_outer_radius, ds.option_pipe_conductivity,
                             ds.option_pipe_distance, ds.option_pipe_number, ds.option_pipe_roughness)
    return CoaxialPipe(ds.option_pipe_coaxial_inner_inner,
                       ds.option_pipe_coaxial_inner_outer,
                       ds.option_pipe_coaxial_outer_inner,
                       ds.option_pipe_coaxial_outer_outer,
                       ds.option_pipe_conductivity,
                       ds.option_pipe_grout_conductivity,
                       ds.option_pipe_roughness,
                       True)


def _create_ground_data(ds: DataStorage) -> GroundData:
    """
    This function creates a GroundData object based on the data entered in the GUI.

    Parameters
    ----------
    ds : DataStorage
        Data storage object that contains all the values inputted in a certain scenario within the GUI.

    Returns
    -------
    GroundData
    """
    if ds.option_source_ground_temperature == 0:
        return GroundConstantTemperature(ds.option_conductivity, ds.option_ground_temp, ds.option_heat_capacity * 1000)
    if ds.option_source_ground_temperature == 1:
        temperature, flux = DATASET[ds.option_ground_database[1]]
        return GroundFluxTemperature(ds.option_conductivity, temperature, ds.option_heat_capacity * 1000, flux)
    # custom
    ground_temp = ds.option_ground_temp_gradient
    if ds.option_flux_gradient == 0:
        return GroundFluxTemperature(ds.option_conductivity, ground_temp, ds.option_heat_capacity * 1000,
                              ds.option_ground_heat_flux)
    return GroundTemperatureGradient(ds.option_conductivity, ground_temp, ds.option_heat_capacity * 1000,
                                     ds.option_temp_gradient)


def _create_monthly_loads_peaks(ds: DataStorage) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """
    This function creates the monthly loads based on the data entered in the GUI.

    Parameters
    ----------
    ds : DataStorage
        Data storage object that contains all the values inputted in a certain scenario within the GUI.

    Returns
    -------
    peak heating [kW/month], peak cooling [kW/month], baseload heating [kWh/month], baseload cooling [kWh/month] : np.ndarray, np.ndarray, np.ndarray, np.ndarray
        Monthly peak heating/cooling loads as well as monthly baseloads for heating and cooling for 1 year
    """
    peak_heating: NDArray[np.float64] = np.array([ds.option_hp_jan, ds.option_hp_feb, ds.option_hp_mar, ds.option_hp_apr, ds.option_hp_may, ds.option_hp_jun,
                                                    ds.option_hp_jul, ds.option_hp_aug, ds.option_hp_sep, ds.option_hp_oct, ds.option_hp_nov, ds.option_hp_dec])
    peak_cooling: NDArray[np.float64] = np.array([ds.option_cp_jan, ds.option_cp_feb, ds.option_cp_mar, ds.option_cp_apr, ds.option_cp_may, ds.option_cp_jun,
                              ds.option_cp_jul, ds.option_cp_aug, ds.option_cp_sep, ds.option_cp_oct, ds.option_cp_nov, ds.option_cp_dec])
    monthly_load_heating: NDArray[np.float64] = np.array([ds.option_hl_jan, ds.option_hl_feb, ds.option_hl_mar, ds.option_hl_apr, ds.option_hl_may, ds.option_hl_jun,
                                     ds.option_hl_jul, ds.option_hl_aug, ds.option_hl_sep, ds.option_hl_oct, ds.option_hl_nov, ds.option_hl_dec])
    monthly_load_cooling: NDArray[np.float64] = np.array([ds.option_cl_jan, ds.option_cl_feb, ds.option_cl_mar, ds.option_cl_apr, ds.option_cl_may, ds.option_cl_jun,
                                     ds.option_cl_jul, ds.option_cl_aug, ds.option_cl_sep, ds.option_cl_oct, ds.option_cl_nov, ds.option_cl_dec])

    if hasattr(ds, 'geo_load') and ds.geo_load == 1:
        # building loads, which need to be converted to geothermal loads
        peak_heating = peak_heating * (1 - 1 / ds.SCOP)
        monthly_load_heating = monthly_load_heating * (1 - 1 / ds.SCOP)
        peak_cooling = peak_cooling * (1 + 1 / ds.SEER)
        monthly_load_cooling = monthly_load_cooling * (1 + 1 / ds.SEER)

    return peak_heating, peak_cooling, monthly_load_heating, monthly_load_cooling
