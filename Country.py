

from Region import Region
from Sampler import Sampler


class Country:
    
    def __init__(self, n_regions, population_size, hospital_beds, I_initial,
                 contagion_prob, crit_prob, death_prob, symp_prob, 
                 fraction_symp_out, avg_time_inc, avg_time_symp,
                 avg_time_no_symp, avg_time_crit, avg_people_met):
        
        self.hospital_beds = hospital_beds
        self.occupied_beds = 0
        Sampler.contagion_prob = contagion_prob
        Sampler.crit_prob = crit_prob
        Sampler.death_prob = death_prob
        Sampler.symp_prob = symp_prob
        Sampler.fraction_symp_out = fraction_symp_out
        Sampler.avg_time_inc = avg_time_inc
        Sampler.avg_time_symp = avg_time_symp
        Sampler.avg_time_no_symp = avg_time_no_symp
        Sampler.avg_time_crit = avg_time_crit

        self.regions = [Region('Copenhagen', population_size, Sampler(avg_people_met), I_initial)]
        
        
    def simulate_day(self, t):
        
        I_critical = 0
        R_dead = 0
        
        for region in self.regions:
            region.simulate_day(t)
            I_critical += region.I_crit
            R_dead += region.R_dead
            
        return I_critical, R_dead