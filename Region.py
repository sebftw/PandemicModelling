from collections import defaultdict
import numpy as np

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

    def initialize(self, n_days):
        # self.data = data[1, 0]
        self.transition_inc = np.zeros(n_days, dtype=np.int)
        self.transition_symp = np.zeros(n_days, dtype=np.int)
        self.transition_no_symp = np.zeros(n_days, dtype=np.int)
        self.transition_crit = np.zeros(n_days, dtype=np.int)

    def increment_array(self, array, increments):
        increments = increments[increments < array.shape[0]]  # Prevent out of bounds at sim. end.
        indices, counts = np.unique(increments, return_counts=True)
        array[indices] += counts

        #for inc_t in :
        #    if inc_t + t < self.transition_inc.shape[0]:
        #        self.transition_inc[t + inc_t] += 1


    def simulate_day(self, t):
        if t == 0:
            # At day 0, we initialize. I.e. we set the incubation times for the initial infected.
            inc_times = self.sampler.sample_incubation_times(self.I_inc)
            self.increment_array(self.transition_inc[t:], inc_times)
            return None

        # S to I_inc
        new_infected = self.sampler.get_new_infected(
            self.I_inc + self.I_no_symp,
            self.S,
            self.I_symp,
            self.R_surv
        )

        self.S -= new_infected
        self.I_inc += new_infected

        self.increment_array(self.transition_inc[t:],
                             self.sampler.sample_incubation_times(new_infected))


        # I_inc to I_symp/I_no_symp
        n_transition_inc = self.transition_inc[t]
        n_symp, n_no_symp = self.sampler.cointoss_inc(n_transition_inc)
        
        self.I_inc -= (n_symp + n_no_symp)
        self.I_symp += n_symp
        self.I_no_symp += n_no_symp

        self.increment_array(self.transition_symp[t:],
                             self.sampler.sample_symptom_times(n_symp))
        self.increment_array(self.transition_no_symp[t:],
                             self.sampler.sample_no_symptom_times(n_no_symp))


        
        # I_symp to I_crit/R_surv
        n_transition_symp = self.transition_symp[t]
        n_crit, n_surv = self.sampler.cointoss_symp(n_transition_symp)
        
        self.I_symp -= (n_crit + n_surv)
        self.I_crit += n_crit
        self.R_surv += n_surv

        self.increment_array(self.transition_crit[t:],
                             self.sampler.sample_critical_times(n_crit))

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
    




















        