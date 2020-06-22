import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import Plotter
import time
from tqdm import tqdm
import copy

from Region import Region
from Sampler import Sampler
import pandas as pd

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


def collate(results, axis=0):
    d = {}
    for k in results[0].keys():
        d[k] = np.stack(list(d[k] for d in results), axis=axis)
    return d

def simulate(country, n_days=365, progress_bar=True):
    country.initialize(n_days)  # Alternatively: copy.deepcopy(country)

    results = []
    start = time.time()
    for t in tqdm(range(n_days), desc='Simulating pandemic', unit='day', disable=not progress_bar):
        pandemic_info = country.simulate_day(t)
        pandemic_info['iter_time'] = time.time()-start  # Add the current time.
        results.append(pandemic_info)

    return collate(results)

def repeat_simulate(country, n_repeats=50, n_days=365):
    results = []
    for _ in tqdm(range(n_repeats), desc='Repeating simulations', unit='simulations'):
        results.append(simulate(country, n_days, False))
    return collate(results)

### SINGLE SIMULATION
copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
country = Country([copenhagen], hospital_beds, n_days)
result = simulate(country)

if plot_data:
    # %% Plotting
    Plotter.plot_fatalities(result['R_dead'])
    plt.show()

    if SIR:
        sick_people_on_hospital_fraction = 0.1
        Plotter.plot_hospitalized_people(result['I_symp']*sick_people_on_hospital_fraction, hospital_beds)
    else:
        Plotter.plot_hospitalized_people(result['I_crit'], hospital_beds)
    plt.show()

# Plotting
Plotter.plot_fatalities(result['R_dead'])
plt.show()

Plotter.plot_hospitalized_people(result['I_crit'], country.hospital_beds)
plt.show()

Plotter.plot_SIR(result)
plt.show()

Plotter.plot_each_group(result)
plt.show()


### MULTIPLE SIMULATION
result = repeat_simulate(country)
Plotter.plot_intervals(result['R_dead'])
plt.show()

















