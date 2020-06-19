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

SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 18

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

population_size = 50_000  # 5_000_000
I_initial = 50
hospital_beds = 750

sampler = Sampler(
    avg_people_met=5
    , contagion_prob=0.03
    , crit_prob=0.2
    , death_prob=0.22
    , symp_prob=0.2
    , fraction_symp_out=0.1

    , avg_time_inc=5
    , avg_time_symp=7.5
    , avg_time_no_symp=7.5
    , avg_time_crit=9
)

n_days = 365


def collate(results, axis=0):
    d = {}
    for k in results[0].keys():
        d[k] = np.stack(list(d[k] for d in results), axis=axis)
    return d

def simulate(country, n_days=365, progress_bar=True):
    country.initialize(n_days)  # Alternatively: copy.deepcopy(country)

    results = []
    for t in tqdm(range(n_days), desc='Simulating pandemic', unit='day', disable=not progress_bar):
        pandemic_info = country.simulate_day(t)
        pandemic_info['iter_time'] = time.time()
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

















