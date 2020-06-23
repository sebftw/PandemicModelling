import os

import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import Plotter
import time
from tqdm import tqdm
from Plotter import collate, reduce
from multiprocessing import Pool
import copy

from Region import Region
from Sampler import Sampler
import pandas as pd

np.random.seed(7)
population_size = 50_000  # 5_000_000
I_initial = 50
hospital_beds = population_size * 0.0078
SIR = False
plot_data = True

if SIR:
    sampler = Sampler( ####### SIR ###########
        avg_people_met_pr_day=6.86
        , contagion_prob=0.04
        , crit_prob=0.0 # DONT CHANGE (0)
        , symp_prob=1.0  # DONT CHANGE (1)
        , fraction_symp_out = 1.0
        , incubation=False
        # We get an R0 of 6.86*4.67416*0.04 = 1.28259
    )
else:
    sampler = Sampler( ###### EXTENDED SIR ##########
        avg_people_met_pr_day=6.86
        , contagion_prob=0.04
        , crit_prob=0.03
        , death_prob=1-0.78
        , symp_prob=0.9
        , fraction_symp_out=0.3
    )

n_days = 100  # Indæmningsfasen

def simulate(country, n_days=365, progress_bar=True):
    country.initialize(n_days)  # Alternatively: copy.deepcopy(country)

    results = []
    control_variates = []
    start = time.time()
    for t in tqdm(range(n_days), desc='Simulating pandemic', unit='day', disable=not progress_bar):
        pandemic_info, control_variate = country.simulate_day(t)
        pandemic_info['iter_time'] = np.array([time.time()-start])  # Add the current time.

        results.append(pandemic_info)
        control_variates.append(control_variate)
    # Concatenate daily results into arrays.
    results = collate(results)

    # We want this indicator to be 1 if there is ever overcapacity.
    results['overcapacity'] = np.any(results['I_crit'] > country.hospital_beds)

    # Add control variates.
    control_variates = reduce(collate(control_variates))
    results.update(control_variates)

    return results


def repeat_simulate(country, n_repeats=30, n_days=365, multiprocessing=False):
    if multiprocessing:
        print('Using multiprocessing with', os.cpu_count(), 'workers.')
        pool = Pool(os.cpu_count())
        return collate(pool.starmap(simulate, [(country, n_days, False)] * n_repeats), func=np.stack)

    results = []
    for _ in tqdm(range(n_repeats), desc='Repeating simulations', unit='simulations'):
        results.append(simulate(country, n_days, False))
    results = collate(results, func=np.stack)

    return results


if __name__ == "__main__":
    ### SINGLE SIMULATION
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    country = Country([copenhagen], hospital_beds)
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
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)  # cyclical=3
    country = Country([copenhagen], hospital_beds)
    result = repeat_simulate(country)
    Plotter.plot_intervals(result['I'])
    plt.title('# of infected (I)')
    plt.show()

    # Plotter.plot_intervals(result['R_dead'])
    # plt.title('# of dead')
    # plt.show()

    Plotter.plot_intervals(result['R'] / copenhagen.population_size)
    plt.ylim([0, 1])
    plt.title('R / population size')
    plt.show()

    Plotter.plot_intervals(result['I_crit'])
    plt.title('# Hospitalized (I_crit)')
    plt.hlines(country.hospital_beds, *plt.xlim(), linestyles='dashed', label=f'Respirators')
    plt.show()

    def control(x, control_variable, mu_control=None):
        # mu_control = np.mean(control_variable)
        # fx = f(x)
        variances = np.cov(x, control_variable)

        # print('Control correlation:', np.corrcoef(x, control_variable)[1, 0])
        c = -variances[0, 1] / variances[1, 1]
        return x + c * (control_variable - mu_control)


    # TODO: Try other controls such as time of sickness
    print(result['overcapacity'].mean(), result['overcapacity'].var())
    control_overcapacity = control(result['overcapacity'], result['incubation_times'], sampler.avg_time_inc)  # 5.937273374
    print('incubation times control:', control_overcapacity.mean(), control_overcapacity.var())

    control_overcapacity = control(result['overcapacity'], result['symptom_times'], sampler.avg_time_symp) # 4.674162489
    print('symptom times control:', control_overcapacity.mean(), control_overcapacity.var())

    # Estimate, how this overcapacity changes as a function of parameters.
    # E.g. use subplots with different parameter settings, and then show all the development quantiles.
