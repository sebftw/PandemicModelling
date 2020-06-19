import numpy as np
from Region import Region
from Sampler import Sampler


class Country:
    def __init__(self, regions, hospital_beds, n_days):
        self.hospital_beds = hospital_beds
        self.occupied_beds = 0
        self.regions = regions

        states = ['S', 'I_inc', 'I_no_symp', 'I_symp', 'I_crit', 'R_surv', 'R_dead']
        self.pandemic_info = {name: np.zeros((len(regions), n_days), dtype=np.int) for name in states}

        for region in self.regions:
            region.initialize(n_days)
        
        
    def simulate_day(self, t):
        S = 0
        I_inc = 0
        I_no_symp = 0
        I_symp = 0
        I_crit = 0
        R_dead = 0
        R_surv = 0
        
        
        for idx, region in enumerate(self.regions):
            region.simulate_day(t)
            
            I_crit += region.I_crit
            R_dead += region.R_dead
            S += region.S
            I_inc += region.I_inc
            I_no_symp += region.I_no_symp
            I_symp += region.I_symp
            R_surv += region.R_surv
            
        return I_crit, R_dead, S, I_inc, I_no_symp, I_symp, R_surv