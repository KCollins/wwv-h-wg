# Run the notebook multiple times against recordings from different stations.


import re
import papermill as pm
import yaml


input_notebook = 'sunrisefest.ipynb'
output_prefix = input_notebook.removesuffix('.ipynb')


# Separate each target with triple dots (...)
targets = """
# bogus data
input_filename: w2naf.com_2021-11-15T19_07_36Z_10000.00_iq.wav
input_requires_demodulation: True
lat: 12.34
lon: -12.34
radio: KX3
antenna: tower-mounted beam

...

# bogus data
input_filename: N6GN_20211115T190749_iq_15.wav
input_requires_demodulation: True
lat: 41.50
lon: -81.61
radio: ICOM 7600
antenna: half-wave dipole
"""


for t in yaml.load_all(targets, yaml.Loader):
    input_filename = t['input_filename']
    output_notebook = f"{output_prefix}-{input_filename}.ipynb"
    
    pm.execute_notebook(
        input_notebook,
        output_notebook,
        parameters=t)
