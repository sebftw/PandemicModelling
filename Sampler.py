import numpy as np
from collections import Counter

class Sampler:

    def __init__(self, avg_people_met=4,
                 contagion_prob=0.05, crit_prob=0.2,
                 death_prob=0.22, symp_prob=1, fraction_symp_out=0.5,
                 avg_time_inc=5, avg_time_symp=7.5, avg_time_no_symp=7.5,
                 avg_time_crit=9):
        self.avg_people_met = avg_people_met
        self.contagion_prob = contagion_prob
        self.crit_prob = crit_prob
        self.death_prob = death_prob
        self.symp_prob = symp_prob
        self.fraction_symp_out = fraction_symp_out
        self.avg_time_inc = avg_time_inc
        self.avg_time_symp = avg_time_symp
        self.avg_time_no_symp = avg_time_no_symp
        self.avg_time_crit = avg_time_crit

        ## TESTING
        self.time_spent_in = 0
    
    def get_new_infected(self, I_no_symp, S, I_symp, R_surv):
        I = I_no_symp + I_symp*self.fraction_symp_out
        n_meetable = I + S + R_surv

        total_S_people_met = np.random.poisson(I*self.avg_people_met * (S / n_meetable))

        # S_people_met = np.random.randint(0, S, size=total_S_people_met)  # -1
        S_people_met = np.floor(np.random.uniform(size=total_S_people_met) * S)

        # Sample for each S-person a binomial of how many infected people they meet.
        coin_tosses = np.random.uniform(size=total_S_people_met)
        S_new_infected = S_people_met[coin_tosses < self.contagion_prob]
        n_infected = len(np.unique(S_new_infected))
        # print(np.random.binomial(S, p=1-(1-self.contagion_prob) ** (total_S_people_met/S)), n_infected)
        # n_infected = np.random.binomial(S, p=1 - (1 - self.contagion_prob) ** (total_S_people_met / S))
        return n_infected

    def sample_incubation_times(self, new_infected):
        if self.avg_time_inc == 0:
            inc_times = np.zeros(new_infected).astype(int)
        else:
            #inc_times = np.random.gamma(self.avg_time_inc, 1, size=new_infected).astype(int)
            inc_times = np.random.lognormal(1.57, 0.65, size=new_infected).astype(int)

        return inc_times
            
    def cointoss_inc(self, n_transition_inc):
        n_symp = np.random.binomial(n_transition_inc, self.symp_prob)
        n_no_symp = n_transition_inc - n_symp
        return n_symp, n_no_symp
    
    def sample_symptom_times(self, n_symp):
        #symp_times = np.random.gamma(self.avg_time_symp/0.8, 0.8, size=n_symp).astype(int)
        symp_times = np.random.lognormal(1.23, 0.79, size=n_symp).astype(int)
        return symp_times
        
    def sample_no_symptom_times(self, n_no_symp):
        #no_symp_times = np.random.gamma(self.avg_time_no_symp/0.8, 0.8, size=n_no_symp).astype(int)
        no_symp_times = np.random.lognormal(1.23, 0.79, size=n_no_symp).astype(int)
        return no_symp_times
    
    def cointoss_symp(self, n_transition_symp):
        n_crit = np.random.binomial(n_transition_symp, self.crit_prob)
        n_surv = n_transition_symp - n_crit
        return n_crit, n_surv
    
    def sample_critical_times(self, n_crit):
        crit_times = np.random.gamma(self.avg_time_crit/0.8, 0.8, size=n_crit).astype(int)
        return crit_times
            
    def cointoss_crit(self, n_transition_crit):
        n_dead = np.random.binomial(n_transition_crit, self.death_prob)
        n_surv = n_transition_crit - n_dead
        return n_dead, n_surv