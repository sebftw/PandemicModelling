import numpy as np
from Region import Region
from Sampler import Sampler
from Plotter import collate


class Country:
    fields = ['I_crit', 'I_inc', 'R_dead', 'S', 'I_no_symp', 'I_symp', 'R_surv', 'new_infections']

    def __init__(self, regions, hospital_beds=0):
        self.hospital_beds = hospital_beds
        self.regions = regions

    def initialize(self, n_days):
        for region in self.regions:
            region.initialize(n_days)

    def simulate_day(self, t):
        pandemic_info = {name: np.zeros((1,), dtype=np.int) for name in self.fields + ['I', 'R']}

        control_variates = []
        for idx, region in enumerate(self.regions):
            control_variates.append(region.simulate_day(t))

            for key in self.fields:
                pandemic_info[key] += getattr(region, key)
            pandemic_info['R'] += pandemic_info['R_surv'] + pandemic_info['R_dead']
            pandemic_info['I'] += pandemic_info["I_inc"] + pandemic_info["I_symp"] +\
                                  pandemic_info["I_no_symp"] + pandemic_info["I_crit"]


        # Just collate all controls over regions.
        control_variates = collate(control_variates)
        return pandemic_info, control_variates