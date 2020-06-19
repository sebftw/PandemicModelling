import numpy as np
from Region import Region
from Sampler import Sampler


class Country:
    def __init__(self, regions, hospital_beds, n_days):
        self.hospital_beds = hospital_beds
        # self.occupied_beds = 0
        self.regions = regions

    def initialize(self, n_days):
        for region in self.regions:
            region.initialize(n_days)

    def simulate_day(self, t):

        pandemic_info = dict(I_crit=0, I_inc=0, R_dead=0, S=0, I_no_symp=0, I_symp=0, R_surv=0)

        for idx, region in enumerate(self.regions):
            region.simulate_day(t)

            pandemic_info['I_crit'] += region.I_crit
            pandemic_info['R_dead'] += region.R_dead
            pandemic_info['S'] += region.S
            pandemic_info['I_inc'] += region.I_inc
            pandemic_info['I_no_symp'] += region.I_no_symp
            pandemic_info['I_symp'] += region.I_symp
            pandemic_info['R_surv'] += region.R_surv
            
        return pandemic_info