import numpy as np

class Region:
    control_variates = ['incubation_times', 'symptom_times', 'no_symptom_times']
    def __init__(self, name, population_size, sampler, I_initial, cyclical=False):
        self.name = name
        self.population_size = population_size
        self.sampler = sampler
        self.I_initial = I_initial
        self.cyclical = cyclical

    def initialize(self, n_days):
        self.transition_inc = np.zeros(n_days, dtype=np.int)
        self.transition_symp = np.zeros(n_days, dtype=np.int)
        self.transition_no_symp = np.zeros(n_days, dtype=np.int)
        self.transition_crit = np.zeros(n_days, dtype=np.int)

        self.S = self.population_size
        self.I_inc = 0
        self.I_no_symp = 0
        self.I_symp = 0
        self.I_crit = 0
        self.R_dead = 0
        self.R_surv = 0

        self.new_infections = 0
        # At day 0, we initialize. I.e. we set the incubation times for the initial infected.
        # inc_times = self.sampler.sample_incubation_times(self.I_inc)
        # self.increment_array(self.transition_inc, inc_times)
        # control_variates['incubation_times'] = inc_times
        self.ready = True

    def increment_array(self, array, increments):
        increments = np.around(increments).astype(int)
        increments = increments[increments < array.shape[0]]  # Prevent out of bounds at sim. end.
        indices, counts = np.unique(increments, return_counts=True)
        array[indices] += counts

    def simulate_day(self, _):
        control_variates = {}

        # S to I_inc
        new_infected = self.sampler.get_new_infected(
            self.I_inc + self.I_no_symp,
            self.S,
            self.I_symp,
            self.R_surv
        )

        self.new_infections = new_infected

        if self.ready:
            new_infected += self.I_initial
            self.ready = False

        self.S -= new_infected
        self.I_inc += new_infected

        # Cyclical/periodic pattern of infection.
        if self.cyclical:
            if self.I_crit > self.population_size * 0.0005:
                self.sampler.avg_people_met_pr_day = self.cyclical
                self.sampler.contagion_prob = 0.02
            else:
                self.sampler.avg_people_met_pr_day = 6.86

            #if self.I_crit > self.population_size*0.0005 and self.sampler.avg_people_met_pr_day == 6.86:
            #    self.sampler.avg_people_met_pr_day = self.cyclical
            #if self.I_crit <= self.population_size*0.00035 and self.sampler.avg_people_met_pr_day == self.cyclical:
            #    self.sampler.avg_people_met_pr_day = 6.86

        control_variates['incubation_times'] = self.sampler.sample_incubation_times(new_infected)
        self.increment_array(self.transition_inc, control_variates['incubation_times'])

        # I_inc to I_symp/I_no_symp
        n_transition_inc = self.transition_inc[0]
        n_symp, n_no_symp = self.sampler.cointoss_inc(n_transition_inc)
        
        self.I_inc -= (n_symp + n_no_symp)
        self.I_symp += n_symp
        self.I_no_symp += n_no_symp

        control_variates['symptom_times'] = self.sampler.sample_symptom_times(n_symp)
        control_variates['no_symptom_times'] = self.sampler.sample_symptom_times(n_no_symp)

        self.increment_array(self.transition_symp, control_variates['symptom_times'])
        self.increment_array(self.transition_no_symp, control_variates['no_symptom_times'])

        
        # I_symp to I_crit/R_surv
        n_transition_symp = self.transition_symp[0]
        n_crit, n_surv = self.sampler.cointoss_symp(n_transition_symp)

        self.I_symp -= (n_crit + n_surv)
        self.I_crit += n_crit
        self.R_surv += n_surv

        self.increment_array(self.transition_crit,
                             self.sampler.sample_critical_times(n_crit))

        # I_no_symp to R_surv
        n_surv = self.transition_no_symp[0]
        
        self.I_no_symp -= n_surv
        self.R_surv += n_surv
        
        # I_crit to R_surv
        n_transition_crit = self.transition_crit[0]
        n_dead, n_surv = self.sampler.cointoss_crit(n_transition_crit)
        
        self.I_crit -= (n_dead + n_surv)  # = n_transition_crit
        self.R_dead += n_dead
        self.R_surv += n_surv

        # Increment transition arrays
        self.transition_inc = self.transition_inc[1:]
        self.transition_symp = self.transition_symp[1:]
        self.transition_no_symp = self.transition_no_symp[1:]
        self.transition_crit = self.transition_crit[1:]

        return control_variates
