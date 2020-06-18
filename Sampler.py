import numpy as np
from collections import Counter

class Sampler:

    def __init__(self, avg_people_met,
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
        
        total_people_met = np.random.poisson(I*self.avg_people_met)
        people_met = np.random.randint(0, n_meetable, size=total_people_met)  #-1
        S_people_met = people_met[people_met < S]

        coin_tosses = np.random.uniform(size=S_people_met.shape[0])
        S_new_infected = S_people_met[coin_tosses < self.contagion_prob]
        n_infected = len(np.unique(S_new_infected))

        return n_infected

    def sample_incubation_times(self, new_infected):
        inc_times = np.random.gamma(self.avg_time_inc, 1, size=new_infected).astype(int)
        return inc_times
            
    def cointoss_inc(self, n_transition_inc):
        coin_tosses = np.random.uniform(size=n_transition_inc)
        
        n_symp = np.count_nonzero(coin_tosses < self.symp_prob)
        n_no_symp = n_transition_inc - n_symp
        
        return n_symp, n_no_symp
    
    def update_transition_symp(self, transition_symp, n_symp, t):
        symp_times = np.random.gamma(self.avg_time_symp/0.8, 0.8, size=n_symp).astype(int)
        
        for symp_t in symp_times:
            transition_symp[t+symp_t] += 1
        
    def update_transition_no_symp(self, transition_no_symp, n_no_symp, t):
        no_symp_times = np.random.gamma(self.avg_time_no_symp/0.8, 0.8, size=n_no_symp).astype(int)
        
        for no_symp_t in no_symp_times:
            transition_no_symp[t+no_symp_t] += 1
    
    def cointoss_symp(self, n_transition_symp):
        coin_tosses = np.random.uniform(size=n_transition_symp)
        
        n_crit = np.count_nonzero(coin_tosses < self.crit_prob)
        n_surv = n_transition_symp - n_crit
        
        return n_crit, n_surv
    
    def update_transition_crit(self, transition_crit, n_crit, t):
        crit_times = np.random.gamma(self.avg_time_crit/0.5, 0.5, size=n_crit).astype(int)
        
        for crit_t in crit_times:
            transition_crit[t+crit_t] += 1
            
    def cointoss_crit(self,n_transition_crit):
        coin_tosses = np.random.uniform(size=n_transition_crit)
        
        n_dead = np.count_nonzero(coin_tosses < self.death_prob)
        n_surv = n_transition_crit - n_dead
        
        return n_dead, n_surv