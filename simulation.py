import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import Plotter
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
    Denmark = Country([Copenhagen], hospital_beds)
    for t in range(1, n_days+1):
        if t % 10 == 0:
            print(f'Iteration {t}/{n_days}')
        I_crit[t-1], R_dead[t-1], S[t-1], I_inc[t-1], I_no_symp[t-1], I_symp[t-1], R_surv[t-1] = Denmark.simulate_day(t)

    pandemic_info = dict({"I_crit" : I_crit,
                          "I_inc" : I_inc,
                          "R_dead" : R_dead,
                          "S" : S,
                          "I_no_symp": I_no_symp,
                          "I_symp": I_symp,
                          "R_surv": R_surv})
    times.append(time.time())




# %% Plotting
Plotter.plot_fatalities(R_dead)

Plotter.plot_hospitalized_people(I_crit, hospital_beds, n_days)
        times.append(time.time())

print('Time taken', times[-1] - times[0])
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


















