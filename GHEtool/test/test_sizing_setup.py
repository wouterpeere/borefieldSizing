import pytest
from GHEtool import *


def test_initialising_setups():
    test = SizingSetup()
    test.L2_sizing = True
    test.L3_sizing = True
    test.L4_sizing = True


def test_no_backup():
    test = SizingSetup()
    try:
        test.restore_backup()
    except ValueError:
        assert True


def test_backup_functionality():
    test = SizingSetup()
    test.make_backup()
    test.L3_sizing = True
    assert test.L2_sizing == False
    assert test._backup.L2_sizing == True
    test.restore_backup()
    assert test.L2_sizing == True
    assert test.L3_sizing == False


def test_gfunction_calc_needed():
    test = SizingSetup(relative_borefield_threshold=0.05)
    assert not test.gfunction_calculation_needed(100, 98)
    assert test.gfunction_calculation_needed(100, 94)
