import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import matplotlib.ticker as mtick
import numpy as np

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


def plot_hospitalized_people(I_crit, hospital_beds):
    # %% Plotting
    fig, ax = plt.subplots(1, 1, figsize=(7,3))
    ax.plot(I_crit, c='lightskyblue', label=f'Hospitalized')
    ax.hlines(hospital_beds, *ax.get_xlim(), label=f'Respirators')
    ax.legend()
    ax.set_title('Number of hospitalized people')
    
    
def plot_fatalities(R_dead):
    fig, ax = plt.subplots(1, 1, figsize=(7,3))
    ax.plot(R_dead, c='lightskyblue', label=f'Deaths')
    ax.legend()
    ax.set_title('Total fatalities')


def plot_SIR(pandemic_info, as_percentage = True):
    fig, ax = plt.subplots(1, 1, figsize=(12,8))
    S = pandemic_info["S"]
    I = pandemic_info["I_inc"] + pandemic_info["I_symp"] + pandemic_info["I_no_symp"] + pandemic_info["I_crit"]
    R = pandemic_info["R_dead"] + pandemic_info["R_surv"]
    death = pandemic_info["R_dead"]
    surv = pandemic_info["R_surv"]
    
    if as_percentage:
        sum_SIR = (S+I+R)/100
        S, I, death, surv = S/sum_SIR, I/sum_SIR, death/sum_SIR, surv/sum_SIR
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    
    #ax.plot(S, c='lightskyblue', label=f'S')
    #ax.plot(I, c='darksalmon', label=f'I')
    #ax.plot(R, c='darkslategray', label=f'R')
    ax.stackplot(list(range(len(R))), I, S, death, surv, colors=["darksalmon", "darkslategray", "red", "lightskyblue"] ,labels=["I", "S", "Dead", "Surv"])
    ax.legend()


def plot_each_group(PI):
    fig, ax = plt.subplots(4, 2, figsize=(15,15))
    
    x = np.arange(len(PI["S"]))
    ax[0][0].plot(x, PI["S"],  color='lightskyblue', label=f'S')
    ax[0][1].bar(x, PI["I_inc"], color='darksalmon', label=f'I_inc')
    ax[1][0].bar(x, PI["I_symp"], color='darksalmon', label=f'I_symp')
    ax[1][1].bar(x, PI["I_no_symp"], color='darksalmon', label=f'I_no_symp')
    ax[2][0].bar(x, PI["I_crit"], color='darksalmon', label=f'I_crit')
    ax[2][1].plot(x, PI["R_surv"], color='darkslategray', label=f'R_surv')
    ax[3][0].plot(x, PI["R_dead"], color='darkslategray', label=f'R_dead')
    ax[3][1].remove()
    for i in range(len(ax)):
        for j in range(len(ax[i])):
            ax[i][j].legend()

def plot_intervals(y):
    x = range(y.shape[-1])

    plt.plot(x, np.median(y, axis=0))
    n_intervals = y.shape[0] // 2  # n_repeats // 2.
    norm = matplotlib.colors.Normalize(vmin=0, vmax=n_intervals)
    for i in reversed(range(n_intervals)):
        p = (i + 1) / n_intervals
        plt.fill_between(x, *np.quantile(y, q=[0.5 - p / 2, 0.5 + p / 2], axis=0), color=cm.jet(norm(i)))


