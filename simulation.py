import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import time

from Region import Region
from Sampler import Sampler

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

population_size = 5_000_000
I_initial = 50
hospital_beds = 750

sampler = Sampler(
    avg_people_met=5
    , contagion_prob=0.04
    , crit_prob=0.2
    , death_prob=0.22
    , symp_prob=1.0
    , fraction_symp_out=0.1

    , avg_time_inc=5
    , avg_time_symp=7.5
    , avg_time_no_symp=7.5
    , avg_time_crit=9
)

n_days = 1000
I_crits = np.zeros(n_days)
R_deads = np.zeros(n_days)

times = []

for _ in range(1):
    Copenhagen = Region('Copenhagen', population_size, sampler, I_initial)

    Denmark = Country([Copenhagen], hospital_beds)

    times.append(time.time())
    for t in range(0, n_days + 1):
        # if t % 10 == 0:
        #    print(f'Iteration {t}/{n_days}')
        I_critical, R_dead = Denmark.simulate_day(t)

        I_crits[t - 1] = I_critical
        R_deads[t - 1] = R_dead

        times.append(time.time())

print('Time taken', times[-1] - times[0])
if True:
    N = 10
    difftimes = np.diff(np.array(times))
    difftimes = np.convolve(difftimes, np.ones((N,)) / N, mode='valid')  # Smoothing
    plt.plot(difftimes)
    plt.title('Time per iteration.')
    plt.show()
    # %% Plotting

    fig, ax = plt.subplots(1, 1, figsize=(7, 3))
    ax.plot(I_crits, c='lightskyblue', label=f'Hospitalized')
    ax.hlines(hospital_beds, 0, n_days, label=f'Respirators')
    ax.legend()
    ax.set_title('Number of hospitalized people')
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(7, 3))
    ax.plot(R_deads, c='lightskyblue', label=f'Deaths')
    ax.legend()
    ax.set_title('Total fatalities')

    plt.show()
