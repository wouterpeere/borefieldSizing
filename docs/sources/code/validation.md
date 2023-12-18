# Validation

GHEtool is validated in a couple of ways. The goal is to increase the number of validation documents in the future.

First of all, it is internally checked for coherence, meaning that different methodology give (more or less) the same result.
Examples of this can be found in the validation files below.

```{toctree}
:maxdepth: 1

Validation/sizing_method_comparison.rst
Validation/sizing_method_comparison_L2_L3_L4.rst
Validation/speed_comparison.rst
```

Peere et al. (2021) validates the hybrid sizing method of GHEtool. The validation code can be found below.
```{toctree}
:maxdepth: 1

Validation/cases.rst
```

The equivalent borehole thermal resistance is validated with the commercial software of Earth Energy Designer (EED) and can be found here.

```{toctree}
:maxdepth: 1

Validation/validation_effective_borehole_thermal_resistance.rst
```

The deep sizing methodology, using a 1/depth assumption for the convergence of the borefield sizing when there is a temperature gradient can be found here.
```{toctree}
:maxdepth: 1

Validation/deep_sizing.rst
```