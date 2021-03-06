 # MOSFiT Simulation Tools
# analyze.py
# January 2019
# Kamile Lukosiute Thesis Code
# python2

# MOSFiT  (https://github.com/SSantosLab/MOSFiT) REQUIRED
# Built to work with the kasen_model model in MOSFIT (found in the SSantosLab 
# github)

# After running the script outputted by simulate.py ('simulation_script'),
# we need a way to analyze all that output. This is the script that creates
# the data structures you'll need to make your pretty plots and do all
# sorts of analysis


import json
import numpy as np

class Single(object):
    '''
    Represents the data output by MOSFiT after parameter determination
    '''
    def __init__(self, freeparamname=" ", trueval=0, datapath=" "):
        self.free_param = freeparamname
        self.true_val = trueval
        self.data_path = datapath
        
    
        
        with open(self.data_path, 'r') as f:
            data = json.loads(f.read())
            if 'name' not in data:
                data = data[list(data.keys())[0]]
    
        
        model = data['models'][0]       
        realizations = model[u'realizations']
        param_values = []
        for i in realizations:
            val = i[u'parameters'][self.free_param][u'value']
            param_values.append(val)
            
        self.param_vals = param_values
        
        photometry = data['photometry']
        self.data_set = [x for x in photometry if 'band' in x and 'magnitude' in x and (
            'realization' not in x or 'simulated' in x)]
        self.models = [x for x in photometry if x not in self.data_set]

        
    def get_param_vals(self):
        return self.param_vals
    
    def get_true_val(self):
        return self.true_val
    
    def get_num_realizations(self):
        return len(self.param_vals)
    
    
    def get_data(self):
        '''
        The data used for the run
        '''
        return self.data_set
        
    def get_determined_data(self):
        '''
        Determined data
        '''
        return self.models
    
    def get_plotting_vals(self):
        '''
        Gets the four values needed for plotting:
            - true value
            - q50
            - q_m = q_50-q_16 (minus)
            - q_p = q_84-q_50 (plus)
            
        '''
        true_val = self.true_val
        
        q16 = np.quantile(self.param_vals, 0.16)
        q50 = np.quantile(self.param_vals, 0.50)
        q84 = np.quantile(self.param_vals, 0.84)
        
        q_m, q_p = q50-q16, q84-q50
        
        return np.array([true_val, q50, q_m, q_p])
    
    
class Set(object):
    '''
    Represents a set of single simulations output by MOSFiT after parameter
    determination
    '''
    def __init__(self, freeparamname, data_path_file):
        # the data path file contains a pairing of true_val : run location
        # can be gotten from simulate.Set.get_run_paths()
        self.free_param = freeparamname
        self.datapaths = {}        
        f = open(data_path_file, 'r')
        for line in f:
            val, path = line.split(' ')
            self.datapaths[float(val)] = path
        f.close()
    
        self.simulations = []
        for val in self.datapaths:
            walkers = self.datapaths[val].strip() + "/products/walkers.json" 
            simulation = Single(freeparamname = self.free_param, trueval = val,
                                datapath = walkers)
            
            self.simulations.append(simulation)
            
    def get_plotting_vals(self):
        true = []
        q50s = []
        qms = []
        qps = []
        for i in self.simulations:
            true_val, q50, q_m, q_p = i.get_plotting_vals()
            true.append(true_val)
            q50s.append(q50)
            qms.append(q_m)
            qps.append(q_p)

        return np.array([true, q50s, qms, qps])

    def get_simulations(self):
        return self.simulations
