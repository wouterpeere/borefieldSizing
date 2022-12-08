import pytest
import numpy as np

from GHEtool.VariableClasses import CustomGFunction, load_custom_gfunction
import pygfunction as gt


def test_initiate_custom_gfunction():
    custom_gfunction = CustomGFunction()


def test_initiate_with_random_values():
    custom_gfunction = CustomGFunction(np.array([1, 5, 6]), np.array([2, 5, 7]))
    assert custom_gfunction.max_t == 6
    assert custom_gfunction.min_t == 1
    assert custom_gfunction.max_H == 7
    assert custom_gfunction.min_H == 2


def test_update_min_max_H():
    custom_gfunction = CustomGFunction()
    assert custom_gfunction.max_H == CustomGFunction.DEFAULT_DEPTH_ARRAY[-1]
    assert custom_gfunction.min_H == CustomGFunction.DEFAULT_DEPTH_ARRAY[0]
    assert np.array_equal(custom_gfunction.depth_array, CustomGFunction.DEFAULT_DEPTH_ARRAY)

    custom_gfunction.depth_array = np.array([1, 5, 10])
    assert np.array_equal(custom_gfunction.depth_array, np.array([1, 5, 10]))
    assert custom_gfunction.max_H == 10
    assert custom_gfunction.min_H == 1


def test_update_min_max_t():
    custom_gfunction = CustomGFunction()
    assert custom_gfunction.max_t == CustomGFunction.DEFAULT_TIME_ARRAY[-1]
    assert custom_gfunction.min_t == CustomGFunction.DEFAULT_TIME_ARRAY[0]
    assert np.array_equal(custom_gfunction.time_array, CustomGFunction.DEFAULT_TIME_ARRAY)

    custom_gfunction.time_array = np.array([2, 5, 11])
    assert np.array_equal(custom_gfunction.time_array, np.array([2, 5, 11]))
    assert custom_gfunction.max_t == 11
    assert custom_gfunction.min_t == 2


def test_create_dataset():
    custom_gfunction = CustomGFunction()
    custom_gfunction.create_custom_dataset(gt.boreholes.rectangle_field(10, 10, 6, 6, 100, 4, 0.075), 2.*10**-6)
    assert np.any(custom_gfunction._gvalues_array)
    custom_gfunction.delete_custom_gfunction()
    assert not np.any(custom_gfunction._gvalues_array)


def test_dump_dataset():
    custom_gfunction = CustomGFunction()
    custom_gfunction.dump_custom_dataset("./", "test")


def test_set_options():
    custom_gfunction = CustomGFunction()
    custom_gfunction.set_options_gfunction_calculation({"method": "equivalentt"})
    assert custom_gfunction.options["method"] == "equivalentt"


def test_load_custom_gfunction():
    custom_gfunction = load_custom_gfunction("./test.gvalues")
