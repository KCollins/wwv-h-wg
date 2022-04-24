# wwv-h-wg
Analysis of WWV/H scientific modulation signal. 

Click here to launch Binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KCollins/wwv-h-wg/main)

If you are running outside Binder, make sure the Python packages listed in `requirements.txt` are installed.

## Automation

You can run this notebook from the command line while setting various parameters with (https://papermill.readthedocs.io/en/latest/index.html)[papermill].

Run with the parameters as set in the notebook:
`papermill sunrisefest.ipynb OUTPUT_PATH`

Run against a different station's recording:
`papermill sunrisefest.ipynb OUTPUT_PATH -p input_filename 'w2naf.com_2021-11-15T19_07_36Z_10000.00_iq.wav' -p input_requires_modulation True -p lat 12.34 -p lon -12.34 -p radio 'KX3' -p antenna 'tower-mounted beam'`

or provide a YAML string:
```
papermill sunrisefest.ipynb OUTPUT_PATH -y "
input_filename: w2naf.com_2021-11-15T19_07_36Z_10000.00_iq.wav
input_requires_modulation: True
lat: 12.34
lon: -12.34
radio: KX3
antenna: tower-mounted beam"
```

which may be easier to type.


See parameters of the notebook:
`papermill --help-notebook sunrisefest.ipynb`
