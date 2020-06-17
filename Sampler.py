

class Sampler:
    
    contagion_prob = 0.05
    crit_prob = 0.05
    death_prob = 0.05
    avg_time_inc = 10
    avg_time_symp = 23
    avg_time_no_symp = 23
    avg_time_crit = 30
    
    def __init__(self, avg_people_met):
        
        self.avg_people_met = avg_people_met
    
    