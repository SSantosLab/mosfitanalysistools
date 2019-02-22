# MOSFiT Simulation Tools
# test_creation_mst.py
# January 2019
# Kamile Lukosiute Thesis Code
# python2

# MOSFiT  (https://github.com/SSantosLab/MOSFiT) REQUIRED
# Built to work with the kasen_model model in MOSFIT (found in the SSantosLab 
# github)

import sys
sys.path.append('../')

import mosfitsimulationtools as mst

## To test MOSFiT Analysis Tools, run this script, followed by 
## test_analysis_mst.py. 

# -----------------------------------------------------------------------------
simulation_data = mst.simulate.Set('test', model='kasen_model',
                  num_nights = 3,
                  night_length = 0.33, # fraction of day
                  N_obs = 4,
                  instrument = 'DECam',
                  telescope = 'CTIO',
                  bands = ['g',  'z'],
                  S = 100,
                  fixed_params = [('Msph1', 0.04), ('vk1', 0.1),('xlan1', 1e-2),
                                 ('phi', 0.7), ('Msph0', 0.025),
                                 ('vk0', 0.3), ('xlan0',1e-4), ('texplosion', 0.0)],
                  free_params = [('theta', [0, 1.57])],
                  mag_err = 0.002,
                  num_walkers = 10) # use default params
simulation_data.generate()
# -----------------------------------------------------------------------------

'''
    Now we go into the terminal and run the following:
        chmod +x simulation_script
        ./simulation_script
    
    This runs MOSFiT in determinative mode, and will produce the files needed 
    for analysis.
    
    After this step, open test_analysis_mst.py to see the results. 
'''