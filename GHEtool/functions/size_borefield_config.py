import logging
import math

import numpy as np

from GHEtool import Borefield


class NoBorefieldFoundError(Exception):
    def __init__(self):
        super().__init__("No Borefield configuration found")


def size_borefield(borefield: Borefield, *, check_configs: bool = False) -> list[tuple]:
    max_depth = borefield.borefield.depth_max
    best_config: tuple[list[tuple], int] = (borefield.create_start_config(), 1_000_000)
    borefield.calculate_temperatures(max_depth)
    h_cool = (np.max(borefield.results.peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    h_heat = (np.min(borefield.results.peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    if max(h_cool, h_heat) <= max_depth:
        return best_config[0]
    n = max(h_cool, h_heat) / max_depth
    n_ceil = math.ceil(n)
    config = borefield.update_config(n_ceil)
    borefield.calculate_temperatures(max_depth)
    h_cool = (np.max(borefield.results.peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    h_heat = (np.min(borefield.results.peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    if max(h_heat, h_cool) <= max_depth * borefield.number_of_boreholes:
        best_config = (config, borefield.number_of_boreholes)

    numbers = []

    while n_ceil not in numbers:
        n_old = n
        numbers.append(n_ceil)
        n = max(h_cool, h_heat) / max_depth * 0.73214 + n_old * (1 - 0.73214)
        logging.info((math.ceil(n), n_ceil, borefield.number_of_boreholes))
        if math.ceil(n) == n_ceil:
            continue
        n_ceil = math.ceil(n)
        config = borefield.update_config(n_ceil)
        diff = borefield.number_of_boreholes - n_ceil
        if diff > 0:
            del borefield.borefield.li_boreholes[-diff:]
            borefield.borefield = borefield.borefield
        logging.info((n, borefield.number_of_boreholes, n_old, config))
        borefield.calculate_temperatures(max_depth)
        h_cool = (np.max(borefield.results.peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
        h_heat = ((np.min(borefield.results.peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth *
                  borefield.number_of_boreholes)
        if max(h_heat, h_cool) <= max_depth * borefield.number_of_boreholes and borefield.number_of_boreholes < best_config[1]:
            best_config = (config, borefield.number_of_boreholes)
            continue
        if not check_configs or not (max_depth * 0.9 <= max(h_heat, h_cool) / borefield.number_of_boreholes <= max_depth * 1.1):
            continue
        other_configs = [conf for conf in config[1:] if borefield.check_config(conf)]
        if other_configs:
            borefield.borefield.reset_from_config(other_configs[0])
            if diff > 0:
                del borefield.borefield.li_boreholes[-diff:]
            borefield.borefield = borefield.borefield
            borefield.calculate_temperatures(max_depth)
            h_cool = (
                    (np.max(borefield.results.peak_cooling) - borefield._Tg()) / (
                    borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
            )
            h_heat = (
                    (np.min(borefield.results.peak_heating) - borefield._Tg()) / (
                    borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
            )
            best_config = (other_configs, borefield.number_of_boreholes)

    if best_config[0] == [] or best_config == (borefield.create_start_config(), 1_000_000):
        raise NoBorefieldFoundError
    borefield.borefield.reset_from_config(best_config[0][0])
    borefield.borefield = borefield.borefield
    return best_config[0]
