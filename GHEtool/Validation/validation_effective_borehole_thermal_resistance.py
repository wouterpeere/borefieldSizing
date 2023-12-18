"""
This document contains the code to compare the equivalent borehole thermal resistance calculated with GHEtool
(based on pygfunction) with the results from Earth Energy Designer. The differences can be explained by using other
correlations and another assumption for the Nusselt number in the laminar regime.
"""

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygfunction as gt

from GHEtool import Borefield, FOLDER
from GHEtool.VariableClasses import FluidData, GroundConstantTemperature, DoubleUTube


def validate():
    # initiate parameters
    ground_data = GroundConstantTemperature(3, 10)  # ground data with an inaccurate guess of 100m for the depth of the borefield
    borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 100, 1, 0.075)
    pipe_data = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05, epsilon=1e-6)

    # initiate borefield model
    borefield = Borefield()
    borefield.set_ground_parameters(ground_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.set_borefield(borefield_gt)
    borefield.Rb = 0.12

    # initialise variables
    R_fp = []
    R_p = []
    Rb = []

    # load data EED
    data_EED = pd.read_csv(FOLDER.joinpath("Validation/resistances_EED.csv"), sep=";")

    mfr_range = np.arange(0.05, 0.55, 0.05)

    # calculate effective borehole thermal resistance (Rb*)
    for mfr in mfr_range:
        fluid_data = FluidData(mfr, 0.568, 998, 4180, 1e-3)
        borefield.set_fluid_parameters(fluid_data)
        Rb.append(borefield.Rb)
        R_p.append(borefield.borehole.pipe_data.R_p)
        R_fp.append(borefield.borehole.pipe_data.R_f)


    # make figure
    plt.figure()
    plt.plot(R_fp, 'r+', label="GHEtool")
    plt.plot(data_EED["R_fp"], 'bo', label="EED")
    plt.xlabel("Mass flow rate per borehole l/s")
    plt.ylabel("Fluid-pipe resistance resistance mK/W")
    plt.title("Comparison R_fp from GHEtool with EED")
    plt.legend()

    plt.figure()
    plt.plot(mfr_range, (R_fp - data_EED["R_fp"])/data_EED["R_fp"]*100, 'bo')
    plt.xlabel("Mass flow rate per borehole l/s")
    plt.ylabel("Difference in fluid-pipe resistance %")
    plt.title("Comparison R_fp from GHEtool with EED (relative)")

    plt.figure()
    plt.plot(Rb, 'r+', label="GHEtool")
    plt.plot(data_EED["Rb*"], 'bo', label="EED")
    plt.xlabel("Mass flow rate per borehole l/s")
    plt.ylabel("Effective borehole thermal resistance mK/W")
    plt.title("Comparison Rb* from GHEtool with EED")
    plt.legend()

    plt.figure()
    plt.plot(mfr_range, (Rb - data_EED["Rb*"])/data_EED["Rb*"]*100, 'bo')
    plt.xlabel("Mass flow rate per borehole l/s")
    plt.ylabel("Difference in effective borehole thermal resistance %")
    plt.title("Comparison Rb* from GHEtool with EED (relative)")

    plt.show()


if __name__ == '__main__':   # pragma: no cover
    validate()
