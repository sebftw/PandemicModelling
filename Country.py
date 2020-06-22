import numpy as np
from Region import Region
from Sampler import Sampler
from Plotter import collate


class Country:
    def __init__(self, regions, hospital_beds):
        self.hospital_beds = hospital_beds
        self.regions = regions

    def initialize(self, n_days):
        for region in self.regions:
            region.initialize(n_days)

    def simulate_day(self, t):
        pandemic_info = {name: np.zeros((1,), dtype=np.int) for name in
                         ['I_crit', 'I_inc', 'R_dead', 'S', 'I_no_symp', 'I_symp', 'R_surv',
                          'I', 'R']}

        control_variates = []
        for idx, region in enumerate(self.regions):
            control_variates.append(region.simulate_day(t))

            pandemic_info['I_crit'] += region.I_crit
            pandemic_info['R_dead'] += region.R_dead
            pandemic_info['S'] += region.S
            pandemic_info['I_inc'] += region.I_inc
            pandemic_info['I_no_symp'] += region.I_no_symp
            pandemic_info['I_symp'] += region.I_symp
            pandemic_info['R_surv'] += region.R_surv
            pandemic_info['R'] += pandemic_info['R_surv'] + pandemic_info['R_dead']
            pandemic_info['I'] += pandemic_info["I_inc"] + pandemic_info["I_symp"] +\
                                  pandemic_info["I_no_symp"] + pandemic_info["I_crit"]


        # Just collate all controls over regions.
        control_variates = collate(control_variates)
        return pandemic_info, control_variates