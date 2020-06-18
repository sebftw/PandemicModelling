

from Region import Region
from Sampler import Sampler


class Country:
    
    def __init__(self, regions, hospital_beds):
        
        self.hospital_beds = hospital_beds
        self.occupied_beds = 0

        self.regions = regions
        
        
    def simulate_day(self, t):
        
        I_critical = 0
        R_dead = 0
        
        for region in self.regions:
            region.simulate_day(t)
            I_critical += region.I_crit
            R_dead += region.R_dead
            
        return I_critical, R_dead