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

def collate(lst, axis=0, func=np.concatenate):
    # A simple collate function:
    return {key:func([sub[key] for sub in lst], axis=axis) for key in lst[-1].keys()}

def reduce(dictonary, func=np.mean):
    return {key:func(value) for key, value in dictonary.items()}


def plot_hospitalized_people(I_crit, hospital_beds):
    # %% Plotting
    fig, ax = plt.subplots(1, 1, figsize=(7, 3))
    ax.plot(I_crit, c='lightskyblue', label=f'Hospitalized')
    ax.hlines(hospital_beds, *ax.get_xlim(), label=f'Respirators')
    ax.legend()
    ax.set_title('Number of hospitalized people')


def plot_fatalities(R_dead):
    fig, ax = plt.subplots(1, 1, figsize=(7, 3))
    ax.plot(R_dead, c='lightskyblue', label=f'Deaths')
    ax.legend()
    ax.set_title('Total fatalities')


def plot_SIR(pandemic_info, as_percentage=True, stack=True, ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    S = pandemic_info["S"]
    I = pandemic_info["I"]
    R = pandemic_info["R"]
    death = pandemic_info["R_dead"]
    surv = pandemic_info["R_surv"]

    if as_percentage:
        sum_SIR = (S+I+R)/100
        S, I, death, surv = S/sum_SIR, I/sum_SIR, death/sum_SIR, surv/sum_SIR
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    labels = ["I", "S", "Surv", "Dead"]
    colors = ["darksalmon", "darkslategray", "lightskyblue", "red"]
    if stack:
        ax.stackplot(list(range(len(S))), I, S, surv, death, colors=colors, labels=labels)
    else:
        for S, label, color in zip([I, S, surv, death], labels, colors):
            ax.plot(S, c=color, label=label)


def plot_each_group(PI):
    fig, ax = plt.subplots(4, 2, figsize=(15, 15))

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

    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('custom',
                                                               [(0, 'lime'), (0.5, '#EFFD6F'), (1, 'tomato')])  # cm.jet

    plt.plot(x, np.median(y, axis=0), color='k', lw=0.5)
    norm = matplotlib.colors.Normalize(vmin=0, vmax=100)
    y.sort(0)
    for i in reversed(range(len(y))):
        p = i / (len(y) - 1) * 100
        plt.fill_between(x, *y[[0, i], :], color=cmap(norm(p)))
    cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap.reversed() ))
    plt.legend(['median'], loc='best')
    plt.xlabel('Day')

    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('Risk', rotation=270)
    cbar.ax.get_yaxis().set_major_formatter(mtick.PercentFormatter())
    cbar.ax.plot([0, 100], [50] * 2, 'k-', lw=0.5)
