import numpy as np
from collections import Counter

class Sampler:
    
    contagion_prob = 0.05
    crit_prob = 0.2
    death_prob = 0.22
    symp_prob = 1
    fraction_symp_out = 0.5
    
    
    avg_time_inc = 5
    avg_time_symp = 7.5
    avg_time_no_symp = 7.5
    avg_time_crit = 9
    
    
    def __init__(self, avg_people_met):
        
        self.avg_people_met = avg_people_met
        
        ## TESTING
        self.time_spent_in = 0
    
    def get_new_infected(self, I_no_symp, S, I_symp, R_surv):

        I = I_no_symp + I_symp*Sampler.fraction_symp_out
        n_meetable = I + S + R_surv
        
        total_people_met = np.random.poisson(I*self.avg_people_met)
        people_met = np.random.randint(0, n_meetable, size=total_people_met)
        S_people_met = people_met[people_met<S]
        
        _, counts = np.unique(S_people_met, return_counts=True)
        infection_probs = (1 - np.power(1 - Sampler.contagion_prob, counts))
        coin_tosses = np.random.uniform(size=infection_probs.shape[0])
        n_infected = np.count_nonzero(coin_tosses < infection_probs)

        return n_infected
        
        
    def update_transition_inc(self, transition_inc, new_infected, t):
        inc_times = np.random.gamma(Sampler.avg_time_inc, 1, size=new_infected).astype(int)
        
        for inc_t in inc_times:
            transition_inc[t+inc_t] += 1
            
    def cointoss_inc(self, n_transition_inc):
        
        coin_tosses = np.random.uniform(size=n_transition_inc)
        
        n_symp = np.count_nonzero(coin_tosses<Sampler.symp_prob)
        n_no_symp = n_transition_inc - n_symp
        
        return n_symp, n_no_symp
    
    def update_transition_symp(self, transition_symp, n_symp, t):
        symp_times = np.random.gamma(Sampler.avg_time_symp/0.8, 0.8, size=n_symp).astype(int)
        
        for symp_t in symp_times:
            transition_symp[t+symp_t] += 1
        
    def update_transition_no_symp(self, transition_no_symp, n_no_symp, t):
        no_symp_times = np.random.gamma(Sampler.avg_time_no_symp/0.8, 0.8, size=n_no_symp).astype(int)
        
        for no_symp_t in no_symp_times:
            transition_no_symp[t+no_symp_t] += 1
    
    def cointoss_symp(self, n_transition_symp):
        coin_tosses = np.random.uniform(size=n_transition_symp)
        
        n_crit = np.count_nonzero(coin_tosses<Sampler.crit_prob)
        n_surv = n_transition_symp - n_crit
        
        return n_crit, n_surv
    
    def update_transition_crit(self, transition_crit, n_crit, t):
        crit_times = np.random.gamma(Sampler.avg_time_crit/0.5, 0.5, size=n_crit).astype(int)
        
        for crit_t in crit_times:
            transition_crit[t+crit_t] += 1
            
    def cointoss_crit(self,n_transition_crit):
        coin_tosses = np.random.uniform(size=n_transition_crit)
        
        n_dead = np.count_nonzero(coin_tosses<Sampler.death_prob)
        n_surv = n_transition_crit - n_dead
        
        return n_dead, n_surv