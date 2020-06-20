import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import Plotter
import time
from tqdm import tqdm

from Region import Region
from Sampler import Sampler

population_size = 5_000_000  # 5_000_000
I_initial = 1
hospital_beds = 750
SIR = False
plot_data = True

if SIR:
    sampler = Sampler( ####### SIR ###########
        avg_people_met=5
        , contagion_prob=0.04
        , crit_prob=0.0 # DONT CHANGE (0)
        , death_prob=1.0 # UNUSED
        , symp_prob=1.0 # DONT CHANGE (1)
        , fraction_symp_out = 0.5 
    
        #, avg_time_inc=0.0 # DONT CHANGE (0)
        #, avg_time_symp=7.5 # UNUSED
        #, avg_time_no_symp=7.5 
        , avg_time_crit=10 #UNUSED
    )
else:
    sampler = Sampler( ###### EXTENDED SIR ##########
        avg_people_met=20
        , contagion_prob=0.04
        , crit_prob=0.03
        , death_prob=0.22
        , symp_prob=0.9
        , fraction_symp_out=0.3
    
        #, avg_time_inc=5
        #, avg_time_symp=7.5
        #, avg_time_no_symp=7.5
        , avg_time_crit=10
    )



n_days = 100 # Indæmningsfasen

I_inc = np.zeros(n_days)
I_crit = np.zeros(n_days)
R_dead = np.zeros(n_days)
S = np.zeros(n_days)
I_no_symp = np.zeros(n_days)
I_symp = np.zeros(n_days)
R_surv = np.zeros(n_days)

times = []

for _ in range(1):
    Copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    Denmark = Country([Copenhagen], hospital_beds, n_days)
    times.append(time.time())
    for t in tqdm(range(n_days)):
        I_crit[t], R_dead[t], S[t], I_inc[t], I_no_symp[t], I_symp[t], R_surv[t] = Denmark.simulate_day(t)
        times.append(time.time())

    pandemic_info = dict({"I_crit" : I_crit,
                          "I_inc" : I_inc,
                          "R_dead" : R_dead,
                          "S" : S,
                          "I_no_symp": I_no_symp,
                          "I_symp": I_symp,
                          "R_surv": R_surv})

print('Time taken', times[-1] - times[0])

if plot_data:
    # %% Plotting
    Plotter.plot_fatalities(R_dead)
    plt.show()

    if SIR:
        sick_people_on_hospital_fraction = 0.1
        Plotter.plot_hospitalized_people(I_symp*sick_people_on_hospital_fraction, hospital_beds, n_days)
    else:
        Plotter.plot_hospitalized_people(I_crit, hospital_beds, n_days)
    plt.show()

    N = 10
    difftimes = np.diff(np.array(times))
    difftimes = np.convolve(difftimes, np.ones((N,)) / N, mode='valid')  # Smoothing
    plt.plot(difftimes)
    plt.title('Time per iteration.')
    plt.show()
    # %% Plotting

    Plotter.plot_SIR(pandemic_info)

    Plotter.plot_each_group(pandemic_info)



















