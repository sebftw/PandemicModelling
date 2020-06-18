import matplotlib.pyplot as plt
import numpy as np
from Country import Country

SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 18

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

avg_people_met = 5
n_regions = 1
population_size = 5_000_000
hospital_beds = 750
I_initial = 50

contagion_prob = 0.04
crit_prob = 0.2
death_prob = 0.22
symp_prob = 1.0
fraction_symp_out = 0.1

avg_time_inc = 5
avg_time_symp = 7.5
avg_time_no_symp = 7.5
avg_time_crit = 9

n_days = 1000

I_inc = np.zeros(n_days)
I_crit = np.zeros(n_days)
R_dead = np.zeros(n_days)
S = np.zeros(n_days)
I_no_symp = np.zeros(n_days)
I_symp = np.zeros(n_days)
R_surv = np.zeros(n_days)


Denmark = Country(n_regions, population_size, hospital_beds, I_initial,
                 contagion_prob, crit_prob, death_prob, symp_prob, 
                 fraction_symp_out, avg_time_inc, avg_time_symp, 
                 avg_time_no_symp, avg_time_crit, avg_people_met)

for t in range(1, n_days+1):
    if t % 10 == 0:
        print(f'Iteration {t}/{n_days}')
    I_crit[t-1], R_dead[t-1], S[t-1], I_inc[t-1], I_no_symp[t-1], I_symp[t-1], R_surv[t-1] = Denmark.simulate_day(t)
            
    

# %% Plotting

fig, ax = plt.subplots(1, 1, figsize=(7,3))
ax.plot(I_crit, c='lightskyblue', label=f'Hospitalized')
ax.hlines(hospital_beds, 0, n_days, label=f'Respirators')
ax.legend()
ax.set_title('Number of hospitalized people')

fig, ax = plt.subplots(1, 1, figsize=(7,3))
ax.plot(R_dead, c='lightskyblue', label=f'Deaths')
ax.legend()
ax.set_title('Total fatalities')



















