# noinspection PyPackageRequirements
import copy

import matplotlib.pyplot as plt
import numpy as np
import pygfunction as gt
import pytest

from GHEtool import GroundConstantTemperature, GroundFluxTemperature, FluidData, DoubleUTube, Borefield, CalculationSetup, FOLDER, MultipleUTube
from GHEtool.logger import ghe_logger
from GHEtool.Validation.cases import load_case
from GHEtool.VariableClasses.LoadData import MonthlyGeothermalLoadAbsolute, HourlyGeothermalLoad
from GHEtool.VariableClasses.BaseClass import UnsolvableDueToTemperatureGradient

data = GroundConstantTemperature(3, 10)
ground_data_constant = data
data_ground_flux = GroundFluxTemperature(3, 10)
fluidData = FluidData(0.2, 0.568, 998, 4180, 1e-3)
pipeData = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05)

borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 4, 0.075)

# Monthly loading values
peakCooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]              # Peak cooling in kW
peakHeating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]             # Peak heating in kW

# annual heating and cooling load
annualHeatingLoad = 300*10**3  # kWh
annualCoolingLoad = 160*10**3  # kWh

# percentage of annual load per month (15.5% for January ...)
monthlyLoadHeatingPercentage = [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144]
monthlyLoadCoolingPercentage = [0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025]

# resulting load per month
monthlyLoadHeating = list(map(lambda x: x * annualHeatingLoad, monthlyLoadHeatingPercentage))   # kWh
monthlyLoadCooling = list(map(lambda x: x * annualCoolingLoad, monthlyLoadCoolingPercentage))   # kWh


def borefields_equal(borefield_one, borefield_two) -> bool:
    for i in range(len(borefield_one)):
        if borefield_one[i].__dict__ != borefield_two[i].__dict__:
            return False   # pragma: no cover
    return True


def test_set_investment_cost():
    borefield = Borefield()
    borefield.set_investment_cost()
    assert borefield.cost_investment == Borefield.DEFAULT_INVESTMENT
    borefield.set_investment_cost([0, 39])
    assert borefield.cost_investment == [0, 39]


def test_logging():
    borefield = Borefield()
    assert ghe_logger.level == 20
    borefield.activate_logger()
    assert ghe_logger.level == 15
    borefield.deactivate_logger()
    assert ghe_logger.level == 20


def test_nb_of_boreholes():
    borefield = Borefield()
    assert borefield.number_of_boreholes == 0
    borefield = Borefield(borefield=copy.deepcopy(borefield_gt))
    borefield.set_ground_parameters(data_ground_flux)
    assert borefield.number_of_boreholes == 120
    borefield.set_borefield(gt.boreholes.rectangle_field(5, 5, 6, 6, 110, 0.1, 0.07))
    assert borefield.H == 110
    assert borefield.r_b == 0.07
    assert borefield.D == 0.1
    assert borefield.number_of_boreholes == 25
    borefield.gfunction(5000, 110)
    assert np.any(borefield.gfunction_calculation_object.depth_array)
    borefield.borefield = gt.boreholes.rectangle_field(6, 5, 6, 6, 100, 1, 0.075)
    assert not np.any(borefield.gfunction_calculation_object.depth_array)
    assert borefield.H == 100
    assert borefield.r_b == 0.075
    assert borefield.D == 1
    borefield.gfunction(5000, 110)
    assert np.any(borefield.gfunction_calculation_object.depth_array)
    assert borefield.number_of_boreholes == 30
    borefield.borefield = None
    assert not np.any(borefield.gfunction_calculation_object.depth_array)
    assert borefield.gfunction_calculation_object
    assert borefield.number_of_boreholes == 0
    borefield.borefield = gt.boreholes.rectangle_field(6, 5, 6, 6, 100, 1, 0.075)
    borefield.gfunction(5000, 110)
    assert np.any(borefield.gfunction_calculation_object.depth_array)
    borefield.set_borefield(None)
    assert not np.any(borefield.gfunction_calculation_object.depth_array)
    assert borefield.number_of_boreholes == 0


def test_create_rectangular_field():
    borefield = Borefield()
    borefield.create_rectangular_borefield(10, 10, 6, 6, 110, 4, 0.075)
    assert borefield.number_of_boreholes == 100
    borefields_equal(borefield.borefield, gt.boreholes.rectangle_field(10, 10, 6, 6, 110, 4, 0.075))


def test_create_circular_field():
    borefield = Borefield()
    borefield.create_circular_borefield(10, 10, 100, 1)
    assert borefield.number_of_boreholes == 10
    borefields_equal(borefield.borefield, gt.boreholes.circle_field(10, 10, 100, 1, 0.075))


def test_update_depth():
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    init_H = borefield.borefield[0].H

    borefield.H = init_H + 1
    borefield._update_borefield_depth()
    for bor in borefield.borefield:
        assert bor.H == init_H + 1

    borefield._update_borefield_depth(init_H + 2)
    for bor in borefield.borefield:
        assert bor.H == init_H + 2

    borefield._update_borefield_depth(init_H + 2)
    for bor in borefield.borefield:
        assert bor.H == init_H + 2


def test_create_custom_dataset():
    borefield_test = Borefield()
    try:
        borefield_test.create_custom_dataset([100, 1000], [50, 100])
        assert False  # pragma: no cover
    except ValueError:
        assert True
    borefield_test.create_rectangular_borefield(10, 10, 6, 6, 100, 1, 0.075)
    try:
        borefield_test.create_custom_dataset([100, 1000], [50, 100])
        assert False  # pragma: no cover
    except AssertionError:
        assert True


def test_load_custom_gfunction():
    borefield = Borefield()
    borefield.set_ground_parameters(ground_data_constant)
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.create_custom_dataset()
    borefield.custom_gfunction.dump_custom_dataset("./", "test")
    dataset = copy.copy(borefield.custom_gfunction)
    borefield.borefield = None
    assert borefield.custom_gfunction is None
    borefield.custom_gfunction = dataset
    borefield.set_borefield(None)
    assert borefield.custom_gfunction is None
    borefield.load_custom_gfunction("./test.gvalues")
    assert borefield.custom_gfunction == dataset


def test_set_length_peak():
    borefield = Borefield()
    borefield.set_length_peak_heating(8)
    borefield.set_length_peak_cooling(10)
    assert borefield.load.peak_cooling_duration == 10 * 3600
    assert borefield.load.peak_heating_duration == 8 * 3600
    borefield.set_length_peak(12)
    assert borefield.load.peak_cooling_duration == 12 * 3600
    assert borefield.load.peak_heating_duration == 12 * 3600
    borefield.set_length_peak_cooling()
    borefield.set_length_peak_heating()
    assert borefield.load.peak_heating_duration == 6 * 3600
    assert borefield.load.peak_cooling_duration == 6 * 3600
    borefield.set_length_peak_heating(8)
    borefield.set_length_peak_cooling(10)
    borefield.set_length_peak()
    assert borefield.load.peak_heating_duration == 6 * 3600
    assert borefield.load.peak_cooling_duration == 6 * 3600


def test_simulation_period():
    borefield = Borefield()
    assert borefield.simulation_period == 20
    assert len(borefield.load.time_L3) == 12 * 20
    borefield.simulation_period = 25
    assert borefield.simulation_period == 25
    assert len(borefield.load.time_L3) == 12 * 25
    borefield.set_simulation_period(40)
    assert borefield.simulation_period == 40
    assert len(borefield.load.time_L3) == 12 * 40


def test_set_Rb():
    borefield = Borefield()
    borefield.set_Rb(0.2)
    assert borefield.Rb == 0.2
    borefield.set_Rb(0.3)
    assert borefield.Rb == 0.3
    borefield.Rb = 0.4
    assert borefield.Rb == 0.4
    assert borefield.Rb == borefield.borehole._Rb


def test_ground_data_custom_gfunction():
    borefield = Borefield(borefield=copy.deepcopy(borefield_gt))
    assert borefield.ground_data == GroundConstantTemperature()
    borefield.ground_data = ground_data_constant
    assert borefield.custom_gfunction is None

    # create custom data set
    borefield.create_custom_dataset()
    borefield.gfunction([5000, 10000], 150)
    assert not borefield.custom_gfunction is None

    # test for property setter
    borefield.ground_data = ground_data_constant
    assert borefield.ground_data == ground_data_constant
    assert borefield._ground_data == ground_data_constant
    assert borefield.custom_gfunction is None

    # create custom data set
    borefield.create_custom_dataset()
    borefield.gfunction([5000, 10000], 150)
    assert not borefield.custom_gfunction is None

    # test for set function
    borefield.set_ground_parameters(data_ground_flux)
    assert borefield.ground_data == data_ground_flux
    assert borefield._ground_data == data_ground_flux
    assert borefield.custom_gfunction is None


def test_ground_data_jit_gfunction():
    borefield = Borefield(borefield=copy.deepcopy(borefield_gt))
    assert borefield.ground_data == GroundConstantTemperature()
    borefield.ground_data = ground_data_constant

    # calculate gfunction
    borefield.gfunction([5000, 10000], 150)
    assert np.any(borefield.gfunction_calculation_object.depth_array)

    # test for property setter
    borefield.ground_data = ground_data_constant
    assert borefield.ground_data == ground_data_constant
    assert borefield._ground_data == ground_data_constant
    assert not np.any(borefield.gfunction_calculation_object.depth_array)

    # calculate gfunction
    borefield.gfunction([5000, 10000], 150)
    assert np.any(borefield.gfunction_calculation_object.depth_array)

    # test for set function
    borefield.set_ground_parameters(data_ground_flux)
    assert borefield.ground_data == data_ground_flux
    assert borefield._ground_data == data_ground_flux
    assert not np.any(borefield.gfunction_calculation_object.depth_array)


def test_set_fluid_params():
    borefield = Borefield()
    assert borefield.borehole.fluid_data == FluidData()
    borefield.set_fluid_parameters(fluidData)
    assert borefield.borehole.fluid_data == fluidData


def test_set_pipe_params():
    borefield = Borefield()
    assert borefield.borehole.pipe_data == MultipleUTube()
    borefield.set_pipe_parameters(pipeData)
    assert borefield.borehole.pipe_data == pipeData


def test_set_max_temp():
    borefield = Borefield()
    borefield.set_max_avg_fluid_temperature(13)
    assert borefield.Tf_max == 13
    borefield.set_max_avg_fluid_temperature(14)
    assert borefield.Tf_max == 14
    try:
        borefield.set_max_avg_fluid_temperature(borefield.Tf_min - 1)
        assert False  # pragma: no cover
    except ValueError:
        assert True


def test_set_min_temp():
    borefield = Borefield()
    borefield.set_min_avg_fluid_temperature(3)
    assert borefield.Tf_min == 3
    borefield.set_min_avg_fluid_temperature(4)
    assert borefield.Tf_min == 4
    try:
        borefield.set_min_avg_fluid_temperature(borefield.Tf_max + 1)
        assert False  # pragma: no cover
    except ValueError:
        assert True


def test_Tg():
    borefield = Borefield()
    borefield.set_ground_parameters(ground_data_constant)
    assert borefield._Tg() == borefield.ground_data.calculate_Tg(borefield.H)
    assert borefield._Tg(20) == borefield.ground_data.calculate_Tg(20)
    borefield.set_ground_parameters(data_ground_flux)
    assert borefield._Tg() == borefield.ground_data.calculate_Tg(borefield.H)
    assert borefield._Tg(20) == borefield.ground_data.calculate_Tg(20)


@pytest.mark.parametrize("ground_data, constant_Rb, result",
                         zip([ground_data_constant, data_ground_flux, ground_data_constant, data_ground_flux],
                             [True, True, False, False],
                             [39.994203323480214, 38.70946566704161, 30.924434615896764, 30.245606119498383]))
def test_Ahmadfard(ground_data, constant_Rb, result):
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    load = MonthlyGeothermalLoadAbsolute(*load_case(3))
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluidData)
    borefield.set_pipe_parameters(pipeData)
    borefield.calculation_setup(use_constant_Rb=constant_Rb)
    th, qh, qm, qa = load._calculate_last_year_params(True)
    assert np.isclose(result, borefield._Ahmadfard(th, qh, qm, qa))
    assert np.isclose(result, borefield.H)

@pytest.mark.parametrize("ground_data, constant_Rb, result",
                         zip([ground_data_constant, data_ground_flux, ground_data_constant, data_ground_flux],
                             [True, True, False, False],
                             [48.76844845370183, 46.593433439950985, 38.53491016745154, 37.100782551185]))
def test_Carcel(ground_data, constant_Rb, result):
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    load = MonthlyGeothermalLoadAbsolute(*load_case(3))

    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluidData)
    borefield.set_pipe_parameters(pipeData)
    borefield.calculation_setup(use_constant_Rb=constant_Rb)
    th, _, tcm, qh, qpm, qm = load._calculate_first_year_params(True)
    assert np.isclose(result, borefield._Carcel(th, tcm, qh, qpm, qm))
    assert np.isclose(result, borefield.H)


def test_set_sizing_setup():
    borefield = Borefield()
    sizing_setup_backup = copy.deepcopy(borefield._calculation_setup)
    borefield.calculation_setup()
    assert borefield._calculation_setup == sizing_setup_backup
    # set calculation_setup
    test = CalculationSetup(4, False, True, False)
    test2 = CalculationSetup(3, False, False, True)
    borefield.calculation_setup(use_constant_Rb=True, quadrant_sizing=4, L2_sizing=False, L3_sizing=True, L4_sizing=False)
    assert borefield._calculation_setup == test
    borefield.calculation_setup(calculation_setup=test2)
    assert borefield._calculation_setup == test2

    borefield.calculation_setup(rtol=10)
    assert borefield._calculation_setup.rtol == 10
    borefield.calculation_setup(atol=10)
    assert borefield._calculation_setup.atol == 10
    assert borefield._calculation_setup.rtol == 10


def test_size():
    borefield = Borefield()
    try:
        borefield.size()
        assert False  # pragma: no cover
    except ValueError:
        assert True
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(3))

    borefield.set_ground_parameters(ground_data_constant)
    sizing_setup_backup = copy.deepcopy(borefield._calculation_setup)
    borefield.size(L3_sizing=True)
    assert borefield._calculation_setup == sizing_setup_backup


def test_select_size():
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(3))

    # with constant Tg
    borefield.set_ground_parameters(ground_data_constant)
    assert borefield._select_size(100, 20) == 100
    assert borefield._select_size(10, 20) == 20

    # with variable Tg
    borefield.set_ground_parameters(data_ground_flux)
    assert borefield._select_size(100, 20) == 100
    assert borefield._select_size(10, 80) == 80
    borefield.set_max_avg_fluid_temperature(14)
    try:
        borefield._select_size(10, 80)
        assert False  # pragma: no cover
    except UnsolvableDueToTemperatureGradient:
        assert True


def test_size_L2_value_errors():
    borefield = Borefield()
    try:
        borefield.size_L2(100)
        assert False  # pragma: no cover
    except ValueError:
        assert True
    monthly_load_cooling, monthly_load_heating, peak_cooling, peak_heating = load_case(2)
    borefield.set_peak_heating(peak_heating)
    borefield.set_peak_cooling(peak_cooling)
    borefield.set_baseload_cooling(monthly_load_cooling)
    borefield.set_baseload_heating(monthly_load_heating)
    borefield.set_ground_parameters(ground_data_constant)
    try:
        borefield.size_L2(100, 5)
        assert False  # pragma: no cover
    except ValueError:
        assert True


@pytest.mark.parametrize("quadrant, result",
                         zip([1, 2, 3, 4], [74.55862437702756, 96.85342542746277, 27.2041541800546, 21.903857780936665]))
def test_size_L2(quadrant, result):
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    borefield.set_ground_parameters(ground_data_constant)
    borefield.size_L2(100, quadrant_sizing=quadrant)

    assert np.isclose(result, borefield.size_L2(100, quadrant_sizing=quadrant))
    assert borefield.limiting_quadrant == quadrant
    assert np.isclose(result, borefield.H)


def test_size_L3_value_errors():
    borefield = Borefield()
    try:
        borefield.size_L3(100)
        assert False  # pragma: no cover
    except ValueError:
        assert True
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    borefield.set_ground_parameters(ground_data_constant)
    try:
        borefield.size_L3(100, 5)
        assert False  # pragma: no cover
    except ValueError:
        assert True

@pytest.mark.parametrize("quadrant, result",
                         zip([1, 2, 3, 4], [56.37136629360852, 71.42698877336204, 26.722846792067735, 21.333161686968708]))
def test_size_L3(quadrant, result):
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.set_max_avg_fluid_temperature(18)
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    borefield.set_ground_parameters(ground_data_constant)

    assert np.isclose(result, borefield.size_L3(100, quadrant_sizing=quadrant))
    assert np.isclose(result, borefield.H)


def test_size_L4_value_errors():
    borefield = Borefield()
    try:
        borefield.size_L4(100)
        assert False  # pragma: no cover
    except ValueError:
        assert True
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    borefield.set_ground_parameters(ground_data_constant)
    try:
        borefield.size_L4(100, 5)
        assert False  # pragma: no cover
    except ValueError:
        assert True
    try:
        borefield.size_L4(100)
        assert False  # pragma: no cover
    except ValueError:
        assert True


def test_size_L4():
    borefield = Borefield()
    borefield.set_ground_parameters(ground_data_constant)
    load = HourlyGeothermalLoad()
    # quadrant 1
    borefield.borefield = copy.deepcopy(borefield_gt)
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    borefield.load = load
    assert np.isclose(182.17317343989652, borefield.size_L4(100, quadrant_sizing=1))
    assert np.isclose(182.17317343989652, borefield.H)
    assert borefield.calculate_quadrant() == 1
    # quadrant 2
    borefield.borefield = copy.deepcopy(borefield_gt)
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"), col_cooling=0, col_heating=1)
    borefield.load = load

    assert np.isclose(305.2876065045127, borefield.size_L4(100, quadrant_sizing=2))
    assert np.isclose(305.2876065045127, borefield.H)
    assert borefield.calculate_quadrant() == 2
    # quadrant 3
    borefield.borefield = copy.deepcopy(borefield_gt)
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"), col_cooling=0, col_heating=1)
    borefield.load = load

    borefield.set_max_avg_fluid_temperature(25)
    assert np.isclose(109.4742962707615, borefield.size_L4(100, quadrant_sizing=3))
    assert np.isclose(109.4742962707615, borefield.H)
    assert borefield.calculate_quadrant() == 3
    # quadrant 4
    borefield.borefield = copy.deepcopy(borefield_gt)
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    borefield.load = load

    # to increase coverage
    borefield.calculation_setup(L4_sizing=True)
    assert np.isclose(174.23648328808213, borefield.size(100, quadrant_sizing=4))
    assert np.isclose(174.23648328808213, borefield.H)
    assert borefield.calculate_quadrant() == 4


def test_investment_cost():
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.H = 100
    cost = 10 * 12 * 100
    assert borefield.investment_cost == cost * borefield.cost_investment[0]
    borefield.set_investment_cost([38, 0])
    assert borefield.investment_cost == cost * 38


def test_reynolds_number():
    borefield = Borefield()
    borefield.set_pipe_parameters(pipeData)
    borefield.set_fluid_parameters(fluidData)
    assert np.isclose(4244.131815783876, borefield.Re)


def test_last_year_params():
    load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    th, qh, qm, qa = load._calculate_last_year_params(False)
    assert np.isclose(9132.420091324202, qa)
    assert np.isclose(65753.42465753425, qm)
    assert np.isclose(240000.0, qh)
    assert np.isclose(21600.0, th)
    th, qh, qm, qa = load._calculate_last_year_params(True)
    assert np.isclose(-9132.420091324202, qa)
    assert np.isclose(25753.424657534248, qm)
    assert np.isclose(160000.0, qh)
    assert np.isclose(21600.0, th)


def test_first_year_params():
    load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    th, tpm, tcm, qh, qpm, qcm = load._calculate_first_year_params(False)
    assert np.isclose(65753.42465753425, qcm)
    assert np.isclose(6410.95890410959, qpm)
    assert np.isclose(21024000.0, tcm)
    assert np.isclose(18396000.0, tpm)
    assert np.isclose(240000.0, qh)
    assert np.isclose(21600.0, th)
    th, tpm, tcm, qh, qpm, qcm = load._calculate_first_year_params(True)
    assert np.isclose(25753.424657534248, qcm)
    assert np.isclose(0, qpm)
    assert np.isclose(2628000.0, tcm)
    assert np.isclose(0, tpm)
    assert np.isclose(160000.0, qh)
    assert np.isclose(21600.0, th)


def test_calculate_temperatures():
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.set_ground_parameters(ground_data_constant)
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(2))

    borefield.calculate_temperatures(120)
    np.testing.assert_array_almost_equal(borefield.results.peak_heating,
                                         np.array([ 7.76418446,  8.06457527,  8.59144992,  9.22406634,  9.9176661 ,
       10.35493277, 10.85933332, 10.99023511, 10.04321457,  9.33984947,
        8.73958309,  8.33426967,  7.95321315,  8.25111367,  8.77481226,
        9.40383895, 10.09353655, 10.5277391 , 11.0286007 , 11.15588842,
       10.20550443,  9.49891063,  8.89711368,  8.48897111,  8.10475521,
        8.40152873,  8.92186612,  9.54812266, 10.23750597, 10.66895627,
       11.16793946, 11.29298095, 10.33877877,  9.63005137,  9.02564022,
        8.61429916,  8.23026722,  8.52687095,  9.04635676,  9.67200231,
       10.35752987, 10.78586212, 11.28414338, 11.40870247, 10.4539418 ,
        9.74400479,  9.13598366,  8.72305746,  8.33858471,  8.634735  ,
        9.15403364,  9.77722199, 10.45979104, 10.88747028, 11.38536271,
       11.50938828, 10.55490203,  9.84263615,  9.23315991,  8.8199902 ,
        8.43494984,  8.72970861,  9.24496831,  9.86323625, 10.54399003,
       10.97114404, 11.46961158, 11.59667566, 10.64391217,  9.93266049,
        9.32375678,  8.91014653,  8.52304048,  8.81336419,  9.32332937,
        9.93881764, 10.61875755, 11.04626604, 11.54703051, 11.67614232,
       10.72430305, 10.01361578,  9.404581  ,  8.98957459,  8.59924833,
        8.88514083,  9.39208797, 10.00668693, 10.68670226, 11.11560581,
       11.61858065, 11.74854509, 10.79725993, 10.08666356,  9.4767217 ,
        9.05938796,  8.66528206,  8.94801036,  9.45402141, 10.06849598,
       10.74924083, 11.1804467 , 11.68421179, 11.81471642, 10.8636843 ,
       10.15255075,  9.54096457,  9.12037341,  8.72303207,  9.00480061,
        9.51054181, 10.12547914, 10.80869029, 11.24107298, 11.74562143,
       11.87654742, 10.92504277, 10.21207583,  9.59666225,  9.17178911,
        8.77253798,  9.0537501 ,  9.55988622, 10.17614817, 10.85968208,
       11.29206477, 11.79661323, 11.92753922, 10.97603456, 10.26306763,
        9.64765405,  9.2227809 ,  8.82352977,  9.1047419 ,  9.61146373,
       10.22920734, 10.91368494, 11.34666291, 11.85119791, 11.9809148 ,
       11.02648776, 10.30917151,  9.69046041,  9.2646135 ,  8.86532916,
        9.14747171,  9.65520666, 10.27295028, 10.95742787, 11.39040584,
       11.89494084, 12.02465773, 11.07023069, 10.35291444,  9.73420334,
        9.30835643,  8.90907209,  9.19243444,  9.70106276, 10.31940964,
       11.00419406, 11.43669622, 11.93961809, 12.06604757, 11.10816011,
       10.38957388,  9.7704954 ,  9.3450551 ,  8.9469248 ,  9.23041   ,
        9.73903832, 10.3573852 , 11.04216962, 11.47467178, 11.97759365,
       12.10402313, 11.14613567, 10.42754944,  9.80847096,  9.38353452,
        8.98631798,  9.27039079,  9.77937765, 10.39763925, 11.08153248,
       11.51198131, 12.01208298, 12.13659709, 11.17814528, 10.45960879,
        9.84120172,  9.41680976,  9.01959321,  9.30366603,  9.81265289,
       10.43091449, 11.11480772, 11.54525655, 12.04535822, 12.16987233,
       11.21142051, 10.49289526,  9.87539571,  9.451568  ,  9.05473695,
        9.33898907,  9.84758987, 10.46467316, 11.14623848, 11.57437959,
       12.07379672, 12.19811941, 11.23999967, 10.52229065,  9.90479109,
        9.48096338,  9.08413234,  9.36838445,  9.87698525, 10.49406855,
       11.17563386, 11.60377497, 12.1031921 , 12.2275148 , 11.27004561,
       10.55323455,  9.93631861,  9.51283391,  9.1158352 ,  9.39905299,
        9.90536243, 10.51952398, 11.19933578, 11.62696168, 12.12650419,
       12.25159304, 11.29457142, 10.57776036,  9.96084442,  9.53735972]))
    np.testing.assert_array_almost_equal(borefield.results.peak_cooling,
                                         np.array([ 9.7265228 ,  9.87217467, 10.134688  , 10.63927884, 11.62475183,
       12.59873554, 13.28921831, 13.76520367, 12.39881805, 10.70464274,
       10.2834413 , 10.00058989,  9.91555149, 10.05871306, 10.31805035,
       10.81905145, 11.80062228, 12.77154188, 13.45848569, 13.93085698,
       12.56110791, 10.8637039 , 10.44097189, 10.15529133, 10.06709355,
       10.20912812, 10.46510421, 10.96333516, 11.94459169, 12.91275905,
       13.59782445, 14.06794951, 12.69438225, 10.99484464, 10.56949843,
       10.28061938, 10.19260556, 10.33447035, 10.58959485, 11.0872148 ,
       12.0646156 , 13.02966489, 13.71402837, 14.18367104, 12.80954528,
       11.10879806, 10.67984187, 10.38937768, 10.30092305, 10.44233439,
       10.69727173, 11.19243448, 12.16687676, 13.13127305, 13.8152477 ,
       14.28435684, 12.91050551, 11.20742942, 10.77701813, 10.48631042,
       10.39728818, 10.53730801, 10.7882064 , 11.27844875, 12.25107576,
       13.21494681, 13.89949657, 14.37164422, 12.99951565, 11.29745376,
       10.867615  , 10.57646675, 10.48537882, 10.62096358, 10.86656746,
       11.35403014, 12.32584328, 13.29006881, 13.9769155 , 14.45111088,
       13.07990653, 11.37840904, 10.94843922, 10.65589481, 10.56158666,
       10.69274023, 10.93532606, 11.42189943, 12.39378799, 13.35940858,
       14.04846564, 14.52351365, 13.1528634 , 11.45145683, 11.02057992,
       10.72570818, 10.6276204 , 10.75560975, 10.9972595 , 11.48370848,
       12.45632655, 13.42424948, 14.11409678, 14.58968498, 13.21928778,
       11.51734402, 11.08482278, 10.78669363, 10.68537041, 10.81240001,
       11.0537799 , 11.54069163, 12.51577601, 13.48487575, 14.17550642,
       14.65151598, 13.28064624, 11.5768691 , 11.14052047, 10.83810933,
       10.73487631, 10.8613495 , 11.1031243 , 11.59136067, 12.56676781,
       13.53586755, 14.22649822, 14.70250778, 13.33163804, 11.6278609 ,
       11.19151226, 10.88910112, 10.78586811, 10.91234129, 11.15470182,
       11.64441984, 12.62077067, 13.59046568, 14.2810829 , 14.75588336,
       13.38209124, 11.67396477, 11.23431862, 10.93093372, 10.82766749,
       10.9550711 , 11.19844475, 11.68816277, 12.6645136 , 13.63420862,
       14.32482583, 14.79962629, 13.42583417, 11.71770771, 11.27806156,
       10.97467665, 10.87141043, 11.00003384, 11.24430085, 11.73462214,
       12.71127979, 13.680499  , 14.36950308, 14.84101614, 13.46376359,
       11.75436715, 11.31435362, 11.01137532, 10.90926314, 11.03800939,
       11.28227641, 11.7725977 , 12.74925535, 13.71847456, 14.40747864,
       14.87899169, 13.50173915, 11.79234271, 11.35232918, 11.04985474,
       10.94865631, 11.07799019, 11.32261574, 11.81285175, 12.78861821,
       13.75578409, 14.44196797, 14.91156566, 13.53374875, 11.82440205,
       11.38505994, 11.08312998, 10.98193155, 11.11126542, 11.35589097,
       11.84612698, 12.82189345, 13.78905932, 14.47524321, 14.94484089,
       13.56702399, 11.85768853, 11.41925392, 11.11788822, 11.01707529,
       11.14658846, 11.39082796, 11.87988566, 12.85332421, 13.81818236,
       14.50368171, 14.97308798, 13.59560315, 11.88708391, 11.44864931,
       11.1472836 , 11.04647067, 11.17598384, 11.42022334, 11.90928104,
       12.88271959, 13.84757774, 14.53307709, 15.00248336, 13.62564909,
       11.91802782, 11.48017683, 11.17915413, 11.07817353, 11.20665239,
       11.44860052, 11.93473647, 12.90642151, 13.87076446, 14.55638918,
       15.0265616 , 13.6501749 , 11.94255363, 11.50470264, 11.20367994]))
    np.testing.assert_array_almost_equal(borefield.results.monthly_cooling,
                                         np.array([ 9.7265228 ,  9.87217467,  9.91023486,  9.96749514, 10.24004053,
       10.62890537, 11.40727853, 11.53818031, 10.77407145, 10.54689525,
       10.2834413 , 10.00058989,  9.91555149, 10.05871306, 10.09359721,
       10.14726775, 10.41591098, 10.8017117 , 11.5765459 , 11.70383362,
       10.93636131, 10.70595641, 10.44097189, 10.15529133, 10.06709355,
       10.20912812, 10.24065107, 10.29155146, 10.55988039, 10.94292887,
       11.71588467, 11.84092616, 11.06963565, 10.83709715, 10.56949843,
       10.28061938, 10.19260556, 10.33447035, 10.36514171, 10.41543111,
       10.6799043 , 11.05983472, 11.83208858, 11.95664768, 11.18479868,
       10.95105057, 10.67984187, 10.38937768, 10.30092305, 10.44233439,
       10.47281859, 10.52065079, 10.78216546, 11.16144288, 11.93330791,
       12.05733349, 11.28575891, 11.04968193, 10.77701813, 10.48631042,
       10.39728818, 10.53730801, 10.56375326, 10.60666505, 10.86636446,
       11.24511664, 12.01755679, 12.14462086, 11.37476905, 11.13970627,
       10.867615  , 10.57646675, 10.48537882, 10.62096358, 10.64211432,
       10.68224644, 10.94113198, 11.32023864, 12.09497572, 12.22408753,
       11.45515993, 11.22066156, 10.94843922, 10.65589481, 10.56158666,
       10.69274023, 10.71087292, 10.75011573, 11.00907669, 11.38957841,
       12.16652586, 12.2964903 , 11.5281168 , 11.29370934, 11.02057992,
       10.72570818, 10.6276204 , 10.75560975, 10.77280636, 10.81192478,
       11.07161525, 11.4544193 , 12.23215699, 12.36266163, 11.59454118,
       11.35959653, 11.08482278, 10.78669363, 10.68537041, 10.81240001,
       10.82932676, 10.86890794, 11.13106472, 11.51504558, 12.29356664,
       12.42449263, 11.65589964, 11.41912161, 11.14052047, 10.83810933,
       10.73487631, 10.8613495 , 10.87867116, 10.91957697, 11.18205651,
       11.56603738, 12.34455843, 12.47548442, 11.70689144, 11.47011341,
       11.19151226, 10.88910112, 10.78586811, 10.91234129, 10.93024868,
       10.97263614, 11.23605937, 11.62063551, 12.39914311, 12.52886   ,
       11.75734464, 11.51621729, 11.23431862, 10.93093372, 10.82766749,
       10.9550711 , 10.97399161, 11.01637908, 11.2798023 , 11.66437844,
       12.44288605, 12.57260294, 11.80108757, 11.55996022, 11.27806156,
       10.97467665, 10.87141043, 11.00003384, 11.01984771, 11.06283844,
       11.32656849, 11.71066883, 12.4875633 , 12.61399278, 11.83901699,
       11.59661966, 11.31435362, 11.01137532, 10.90926314, 11.03800939,
       11.05782327, 11.100814  , 11.36454405, 11.74864438, 12.52553885,
       12.65196834, 11.87699255, 11.63459522, 11.35232918, 11.04985474,
       10.94865631, 11.07799019, 11.0981626 , 11.14106805, 11.40390691,
       11.78595391, 12.56002819, 12.6845423 , 11.90900215, 11.66665457,
       11.38505994, 11.08312998, 10.98193155, 11.11126542, 11.13143783,
       11.17434329, 11.43718215, 11.81922915, 12.59330342, 12.71781753,
       11.94227739, 11.69994104, 11.41925392, 11.11788822, 11.01707529,
       11.14658846, 11.16637482, 11.20810196, 11.46861291, 11.84835219,
       12.62174192, 12.74606462, 11.97085655, 11.72933643, 11.44864931,
       11.1472836 , 11.04647067, 11.17598384, 11.1957702 , 11.23749734,
       11.49800829, 11.87774757, 12.65113731, 12.77546   , 12.00090249,
       11.76028033, 11.48017683, 11.17915413, 11.07817353, 11.20665239,
       11.22414738, 11.26295278, 11.52171021, 11.90093428, 12.67444939,
       12.79953825, 12.0254283 , 11.78480614, 11.50470264, 11.20367994]))
    np.testing.assert_array_almost_equal(borefield.results.monthly_heating,
                                         np.array([ 9.37492462,  9.46486873,  9.54493806,  9.64968692,  9.9176661 ,
       10.35493277, 10.85933332, 10.99023511, 10.38868332, 10.18251169,
        9.93275637,  9.66908304,  9.56395331,  9.65140713,  9.72830041,
        9.82945953, 10.09353655, 10.5277391 , 11.0286007 , 11.15588842,
       10.55097318, 10.34157285, 10.09028696,  9.82378448,  9.71549538,
        9.80182219,  9.87535427,  9.97374324, 10.23750597, 10.66895627,
       11.16793946, 11.29298095, 10.68424752, 10.47271359, 10.2188135 ,
        9.94911253,  9.84100739,  9.92716441,  9.99984491, 10.09762289,
       10.35752987, 10.78586212, 11.28414338, 11.40870247, 10.79941055,
       10.58666701, 10.32915694, 10.05787083,  9.94932487, 10.03502846,
       10.10752179, 10.20284257, 10.45979104, 10.88747028, 11.38536271,
       11.50938828, 10.90037078, 10.68529837, 10.4263332 , 10.15480357,
       10.04569001, 10.13000207, 10.19845646, 10.28885683, 10.54399003,
       10.97114404, 11.46961158, 11.59667566, 10.98938092, 10.77532271,
       10.51693007, 10.2449599 , 10.13378064, 10.21365764, 10.27681752,
       10.36443822, 10.61875755, 11.04626604, 11.54703051, 11.67614232,
       11.0697718 , 10.856278  , 10.59775429, 10.32438796, 10.20998849,
       10.28543429, 10.34557611, 10.43230751, 10.68670226, 11.11560581,
       11.61858065, 11.74854509, 11.14272868, 10.92932578, 10.66989498,
       10.39420133, 10.27602223, 10.34830382, 10.40750956, 10.49411656,
       10.74924083, 11.1804467 , 11.68421179, 11.81471642, 11.20915305,
       10.99521297, 10.73413785, 10.45518678, 10.33377223, 10.40509407,
       10.46402996, 10.55109972, 10.80869029, 11.24107298, 11.74562143,
       11.87654742, 11.27051152, 11.05473805, 10.78983554, 10.50660248,
       10.38327814, 10.45404356, 10.51337436, 10.60176875, 10.85968208,
       11.29206477, 11.79661323, 11.92753922, 11.32150331, 11.10572985,
       10.84082733, 10.55759427, 10.43426994, 10.50503536, 10.56495187,
       10.65482792, 10.91368494, 11.34666291, 11.85119791, 11.9809148 ,
       11.37195651, 11.15183373, 10.88363369, 10.59942687, 10.47606932,
       10.54776517, 10.60869481, 10.69857086, 10.95742787, 11.39040584,
       11.89494084, 12.02465773, 11.41569944, 11.19557666, 10.92737662,
       10.6431698 , 10.51981225, 10.5927279 , 10.65455091, 10.74503022,
       11.00419406, 11.43669622, 11.93961809, 12.06604757, 11.45362886,
       11.2322361 , 10.96366869, 10.67986847, 10.55766497, 10.63070346,
       10.69252646, 10.78300578, 11.04216962, 11.47467178, 11.97759365,
       12.10402313, 11.49160442, 11.27021166, 11.00164424, 10.71834789,
       10.59705814, 10.67068425, 10.7328658 , 10.82325983, 11.08153248,
       11.51198131, 12.01208298, 12.13659709, 11.52361402, 11.30227101,
       11.03437501, 10.75162313, 10.63033338, 10.70395949, 10.76614103,
       10.85653507, 11.11480772, 11.54525655, 12.04535822, 12.16987233,
       11.55688926, 11.33555748, 11.06856899, 10.78638137, 10.66547712,
       10.73928253, 10.80107801, 10.89029374, 11.14623848, 11.57437959,
       12.07379672, 12.19811941, 11.58546842, 11.36495287, 11.09796438,
       10.81577675, 10.6948725 , 10.76867791, 10.8304734 , 10.91968913,
       11.17563386, 11.60377497, 12.1031921 , 12.2275148 , 11.61551436,
       11.39589677, 11.1294919 , 10.84764728, 10.72657536, 10.79934645,
       10.85885057, 10.94514456, 11.19933578, 11.62696168, 12.12650419,
       12.25159304, 11.64004017, 11.42042258, 11.15401771, 10.87217309]))


def test_set_options_gfunction_calculation():
    borefield = Borefield()
    borefield.set_options_gfunction_calculation({"method": "equivalentt"})
    assert borefield.gfunction_calculation_object.options["method"] == "equivalentt"
    borefield.set_options_gfunction_calculation({"method": "equivalent"})


def test_gfunction():
    borefield = Borefield()
    borefield.set_ground_parameters(data_ground_flux)
    borefield.create_rectangular_borefield(10, 10, 6, 6, 100, 1, 0.075)
    borefield.H = 100_000
    try:
        borefield.gfunction(56491)
        assert False  # pragma: no cover
    except UnsolvableDueToTemperatureGradient:
        assert True
    borefield.H = 102.3

    np.testing.assert_array_almost_equal(borefield.gfunction([6000, 60000, 600000]), np.array([0.63751082, 1.70657847, 2.84227252]))
    borefield.create_custom_dataset()
    np.testing.assert_array_almost_equal(borefield.gfunction([6000, 60000, 600000]), np.array([0.622017, 1.703272, 2.840246]))
    borefield.calculation_setup(use_precalculated_dataset=False)
    np.testing.assert_array_almost_equal(borefield.gfunction([6000, 60000, 600000]), np.array([0.63751082, 1.70657847, 2.84227252]))


def test_load_duration(monkeypatch):
    borefield = Borefield()
    monkeypatch.setattr(plt, 'show', lambda: None)
    borefield.set_ground_parameters(ground_data_constant)
    borefield.borefield = copy.deepcopy(borefield_gt)
    load = HourlyGeothermalLoad()
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    borefield.load = load
    borefield.plot_load_duration(legend=True)
    borefield.optimise_load_profile(load, 150)


def test_optimise_load_profile(monkeypatch):
    borefield = Borefield()
    monkeypatch.setattr(plt, 'show', lambda: None)
    borefield.set_ground_parameters(ground_data_constant)
    borefield.borefield = copy.deepcopy(borefield_gt)
    load = HourlyGeothermalLoad()
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    load.simulation_period = 40
    borefield.optimise_load_profile(load, 150)
    assert borefield.load.simulation_period == 40
    assert borefield._building_load.simulation_period == 40
    assert borefield._secundary_borefield_load.simulation_period == 40
    assert borefield._external_load.simulation_period == 40


def test_optimise_borefield_small(monkeypatch):
    borefield = Borefield()
    monkeypatch.setattr(plt, 'show', lambda: None)
    borefield.set_ground_parameters(ground_data_constant)
    borefield.create_rectangular_borefield(5, 1, 6, 6, 100)
    load = HourlyGeothermalLoad()
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    load.simulation_period = 40
    borefield.optimise_load_profile(load, 150, print_results=True)
    assert borefield.load.simulation_period == 40
    assert borefield._building_load.simulation_period == 40
    assert borefield._secundary_borefield_load.simulation_period == 40
    assert borefield._external_load.simulation_period == 40


def test_optimise_borefield_wrong_threshold(monkeypatch):
    borefield = Borefield()
    monkeypatch.setattr(plt, 'show', lambda: None)
    borefield.set_ground_parameters(ground_data_constant)
    borefield.create_rectangular_borefield(5, 1, 6, 6, 100)
    load = HourlyGeothermalLoad()
    load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    load.simulation_period = 40
    try:
        borefield.optimise_load_profile(load, 150, print_results=True, temperature_threshold=-0.5)
        assert False  # pragma: no cover
    except ValueError:
        assert True

def test_calculate_quadrants_without_data():
    borefield = Borefield()
    borefield.borefield = copy.deepcopy(borefield_gt)
    borefield.set_max_avg_fluid_temperature(18)
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    borefield.set_ground_parameters(ground_data_constant)
    borefield.calculate_quadrant()


def test_optimise_load_profile_without_data():
    borefield = Borefield()
    try:
        borefield.optimise_load_profile(MonthlyGeothermalLoadAbsolute())
        assert False  # pragma: no cover
    except ValueError:
        assert True


def test_load_load():
    borefield1 = Borefield()
    borefield2 = Borefield()

    load = MonthlyGeothermalLoadAbsolute(*load_case(1))
    borefield2.load = load
    borefield1.set_load(load)
    assert borefield1.load is borefield2.load


def test_calculate_temperature_profile():
    borefield = Borefield()
    load = MonthlyGeothermalLoadAbsolute(*load_case(1))
    borefield.load = load

    try:
        borefield.calculate_temperatures(hourly=True)
        assert False   # pragma: no cover
    except ValueError:
        assert True


def test_optimise_load_profile_without_hourly_data():
    borefield = Borefield()
    borefield.load = MonthlyGeothermalLoadAbsolute(*load_case(1))
    try:
        borefield.optimise_load_profile(borefield.load)
        assert False   # pragma: no cover
    except ValueError:
        assert True
    borefield.load = HourlyGeothermalLoad()
    borefield.set_ground_parameters(ground_data_constant)
    borefield.load.load_hourly_profile(FOLDER.joinpath("Examples/hourly_profile.csv"))
    borefield.create_rectangular_borefield(10, 10, 6, 6, 150)
    borefield.optimise_load_profile(borefield.load)


@pytest.mark.parametrize("H, result",
                         zip(range(110, 130, 1), [122.99210426454648, 122.99135446500962, 122.99135409065917,
                                                  122.99135403971272, 122.99135403719148, 122.9913540367823,
                                                  122.99135403674013, 122.99135403673134, 122.99221686744185,
                                                  122.99217229220649, 122.99135553171544, 122.99220727438545,
                                                  122.99477143007601, 122.9921794642058, 122.99220615327106,
                                                  122.99221262582992, 122.99221900364599, 122.9922252887964,
                                                  122.99223148329897, 122.99223758911434]))
def test_effect_H_init(H, result):
    borefield = Borefield()
    borefield.ground_data = GroundConstantTemperature(3, 11)
    borefield.create_rectangular_borefield(10, 5, 7, 7, 100, 0.75)
    load = MonthlyGeothermalLoadAbsolute(*load_case(1))
    borefield.load = load
    borefield.calculation_setup(H_init=H)
    assert np.isclose(borefield.size(), result)
    borefield = Borefield()
    borefield.ground_data = GroundConstantTemperature(3, 11)
    borefield.create_rectangular_borefield(10, 5, 7, 7, 100, 0.75)
    load = MonthlyGeothermalLoadAbsolute(*load_case(1))
    borefield.load = load
    assert np.isclose(borefield.size(H_init=H), result)


def test_depth_convergence():
    borefield = Borefield()
    borefield.calculation_setup(atol=1, rtol=0.01, max_nb_of_iterations=10)
    try:
        borefield._check_convergence(10, 12, 10)
        assert False  # pragma: no cover
    except RuntimeError:
        assert True

    assert borefield._check_convergence(10, 10, 1)
    assert not borefield._check_convergence(10, 10.5, 1)
    assert borefield._check_convergence(10, 10.001, 1)
    assert not borefield._check_convergence(10000, 10002, 1)


def test_calculate_next_depth_deep_sizing():
    borefield = Borefield()
    borefield.ground_data = GroundFluxTemperature(3, 10)
    borefield.create_rectangular_borefield(10, 5, 7, 7, 100, 0.75)
    load = MonthlyGeothermalLoadAbsolute(*load_case(1))
    borefield.load = load

    borefield.calculate_temperatures(75)
    assert np.isclose(borefield.calculate_next_depth_deep_sizing(75), 117.98660599828808)
    borefield.calculate_temperatures(117.98660599828808)
    assert np.isclose(borefield.calculate_next_depth_deep_sizing(117.98660599828808), 128.16618036528823)
    borefield.calculate_temperatures(128.16618036528823)
    assert np.isclose(borefield.calculate_next_depth_deep_sizing(128.16618036528823), 130.8812255630479)


@pytest.mark.parametrize("case, result",
                         zip((1, 2, 3, 4),
                             [131.90418292004594, 0, 139.46239300837794, 131.90418292004594]))
def test_deep_sizing(case, result):
    borefield = Borefield()
    borefield.ground_data = GroundFluxTemperature(3, 10)
    borefield.create_rectangular_borefield(10, 5, 7, 7, 100, 0.75)
    load = MonthlyGeothermalLoadAbsolute(*load_case(case))
    borefield.load = load

    assert np.allclose(result, borefield._size_based_on_temperature_profile(10, deep_sizing=True)[0])

    borefield = Borefield()
    borefield.ground_data = GroundFluxTemperature(3, 10)
    borefield.create_rectangular_borefield(10, 5, 7, 7, 100, 0.75)
    load = MonthlyGeothermalLoadAbsolute(*load_case(case))
    borefield.load = load

    # methods should more or less lead to the same results, 1% diff taken as a reference
    assert np.allclose(result, borefield._size_based_on_temperature_profile(10, deep_sizing=False)[0], rtol=0.01)
