import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import Plotter
import time
from tqdm import tqdm

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

population_size = 1_000_000  # 5_000_000
I_initial = 500
hospital_beds = 750

sampler = Sampler(
    avg_people_met=4,
    contagion_prob=0.032,
    crit_prob=0.2,
    death_prob=0.22,
    symp_prob=0.5,
    fraction_symp_out=0.2,
    avg_time_inc=5,
    avg_time_symp=7.5,
    avg_time_no_symp=7.5,
    avg_time_crit=9
)

n_days = 365

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

    pandemic_info = dict({"I_crit": I_crit,
                          "I_inc": I_inc,
                          "R_dead": R_dead,
                          "S": S,
                          "I_no_symp": I_no_symp,
                          "I_symp": I_symp,
                          "R_surv": R_surv})

print('Time taken', times[-1] - times[0])

Plotter.plot_hospitalized_people(I_crit, hospital_beds, n_days)
plt.show()

if False:
    # %% Plotting
    Plotter.plot_fatalities(R_dead)
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

    # dette er en ændring
