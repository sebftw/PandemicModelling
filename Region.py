
from collections import defaultdict


class Region:
    
    def __init__(self, name, population_size, sampler, I_initial):
        
        self.name = name
        self.population_size = population_size
        self.sampler = sampler
        
        self.S = population_size - I_initial
        self.I_inc = I_initial
        self.I_no_symp = 0
        self.I_symp = 0
        self.I_crit = 0
        self.R_dead = 0
        self.R_surv = 0
        
        self.transition_inc = defaultdict(int)
        self.transition_symp = defaultdict(int)
        self.transition_no_symp = defaultdict(int)
        self.transition_crit = defaultdict(int)
        
        
        self.sampler.update_transition_inc(self.transition_inc, self.I_inc,0)

        
    def simulate_day(self, t):
        
        # S to I_inc
        new_infected = self.sampler.get_new_infected(
            self.I_inc + self.I_no_symp,
            self.S,
            self.I_symp,
            self.R_surv
        )
        
        self.S -= new_infected
        self.I_inc += new_infected
        
        self.sampler.update_transition_inc(self.transition_inc, new_infected, t)
        
        # I_inc to I_symp/I_no_symp
        n_transition_inc = self.transition_inc[t]
        n_symp, n_no_symp = self.sampler.cointoss_inc(n_transition_inc)
        
        self.I_inc -= (n_symp + n_no_symp)
        self.I_symp += n_symp
        self.I_no_symp += n_no_symp
        
        self.sampler.update_transition_symp(self.transition_symp, n_symp, t)
        self.sampler.update_transition_no_symp(self.transition_no_symp, n_no_symp, t)
        
        # I_symp to I_crit/R_surv
        n_transition_symp = self.transition_symp[t]
        n_crit, n_surv = self.sampler.cointoss_symp(n_transition_symp)
        
        self.I_symp -= (n_crit + n_surv)
        self.I_crit += n_crit
        self.R_surv += n_surv 
        
        self.sampler.update_transition_crit(self.transition_crit, n_crit, t)
        
        # I_no_symp to R_surv
        n_surv = self.transition_no_symp[t]
        
        self.I_no_symp -= n_surv
        self.R_surv += n_surv
        
        # I_crit to R_surv
        n_transition_crit = self.transition_crit[t]
        n_dead, n_surv = self.sampler.cointoss_crit(n_transition_crit)
        
        self.I_crit -= (n_dead + n_surv)
        self.R_dead += n_dead
        self.R_surv += n_surv
        
    



















        