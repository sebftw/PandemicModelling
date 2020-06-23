import os

import matplotlib.pyplot as plt
import numpy as np
from Country import Country
import Plotter
import time
from tqdm import tqdm
import matplotlib.ticker as mtick
import math
import scipy.stats as stats
from Plotter import collate, reduce
from multiprocessing import Pool
import copy

from Region import Region
from Sampler import Sampler
import pandas as pd

from simulation import simulate, repeat_simulate

n_repeats = 100

plot_path = 'plots'

def scenario1():
    np.random.seed(7)
    # Simple SIR model.
    sampler = Sampler(crit_prob=0.0, symp_prob=1.0,
                      fraction_symp_out=1.0, incubation=False)
    # We have S -> I_symp -> R
    # We get an R0 of 6.86*4.67416*0.04 = 1.28259
    # (Only true for memoryless? i.e. because we can just multiply by avg. sympt time.)

    population_size = 500_000
    I_initial = 5_000
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    country = Country([copenhagen])

    contageon_probs = [0.03, 0.04, 0.06, 0.10]
    fig, axs = plt.subplots(1, len(contageon_probs), squeeze=True, sharey='row', figsize=(12, 4.5))
    for ax, contageon_prob in zip(axs, contageon_probs):
        sampler.contagion_prob = contageon_prob
        result = simulate(country)
        Plotter.plot_SIR(result, ax=ax)
        ax.set_title(f'$p={contageon_prob:.2f}$')
        ax.set_xlabel('Days')
    ax.set_xlabel('')
    ax.legend(['I', 'S', 'R'], loc='upper center', bbox_to_anchor=(0.5, -0.17), fancybox=False, shadow=False, ncol=3)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # fig.legend(['S', 'I', 'R'], bbox_to_anchor=(2, 0), loc='lower right')
    # plt.subplots_adjust(left=0.07, right=0.93, wspace=0.25, hspace=0.35)
    plt.savefig(os.path.join(plot_path, '1_SIR.png'), dpi=300)
    plt.show()

def scenario2():
    # SEIR model.
    sampler = Sampler()  # crit_prob=0.0, symp_prob=1.0, fraction_symp_out=1.0
    # We have S -> E (latent/incubation period) -> I_symp -> R

    population_size = 500_000
    I_initial = 500
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    country = Country([copenhagen])

    contageon_probs = [0.02, 0.025, 0.04, 0.05]
    average_people_mets = [4, 5, 6.86, 10]
    symp_people_out = [0.0, 0.1, 0.5, 1]


    fig, axs = plt.subplots(1, len(contageon_probs), squeeze=True, sharey='row', figsize=(12, 4))
    for i, (ax, contageon_prob) in enumerate(zip(axs, contageon_probs)):
        sampler.contagion_prob = contageon_prob
        np.random.seed(7)
        result = simulate(country)
        Plotter.plot_SIR(result, ax=ax)
        ax.set_title(f'$p={contageon_prob:.3f}$')
        ax.set_xlabel('Days')
        if i == len(contageon_probs)-1:
            ax.legend(['I', 'S', 'Recovered', 'Dead'], loc='upper center',
                      bbox_to_anchor=(1.5, 1), fancybox=False, shadow=False, ncol=1)
        if i == 2:
            ax.set_title(f'$\\bf p={contageon_prob:.3f}$')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '2_SEIR_hygene.png'), dpi=300)
    plt.show()

    fig, axs = plt.subplots(1, len(contageon_probs), squeeze=True, sharey='row', figsize=(12, 4))
    for i, (ax, contageon_prob) in enumerate(zip(axs, contageon_probs)):
        sampler.contagion_prob = contageon_prob
        np.random.seed(7)
        result = repeat_simulate(country, n_repeats=n_repeats)
        Plotter.plot_intervals(result['I_crit'], ax=ax, colorbar=i==len(contageon_probs)-1)
        ax.set_title(f'$p={contageon_prob:.3f}$')
        ax.set_xlabel('Days')
        if i == 0:
            ax.set_ylabel('# Hospitalized ($I_{crit}$)')
        if i == 2:
            ax.set_title(f'$\\bf p={contageon_prob:.3f}$')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '2_SEIR_hygene_hospitalized.png'), dpi=300)
    plt.show()

    sampler.contagion_prob = 0.04  # Set back to default
    fig, axs = plt.subplots(1, len(average_people_mets), squeeze=True, sharey='row', figsize=(12, 4))
    for i, (ax, avg_people_met_pr_day) in enumerate(zip(axs, average_people_mets)):
        sampler.avg_people_met_pr_day = avg_people_met_pr_day
        np.random.seed(7)
        result = simulate(country)
        Plotter.plot_SIR(result, ax=ax)
        ax.set_title(f'$Avg. met ={avg_people_met_pr_day:.2f}$')
        if i == 2:
            ax.set_title(f'$\\bf Avg. met ={avg_people_met_pr_day:.2f}$')
        ax.set_xlabel('Days')
        if i == len(average_people_mets)-1:
            ax.legend(['I', 'S', 'Recovered', 'Dead'], loc='upper center',
                      bbox_to_anchor=(1.5, 1), fancybox=False, shadow=False, ncol=1)
    plt.tight_layout()  # rect=[0, 0.03, 1, 0.95]
    plt.savefig(os.path.join(plot_path, '2_SEIR_distancing.png'), dpi=300)
    plt.show()

    fig, axs = plt.subplots(1, len(contageon_probs), squeeze=True, sharey='row', figsize=(12, 4))
    for i, (ax, avg_people_met_pr_day) in enumerate(zip(axs, average_people_mets)):
        sampler.avg_people_met_pr_day = avg_people_met_pr_day
        np.random.seed(7)
        result = repeat_simulate(country, n_repeats=n_repeats)
        Plotter.plot_intervals(result['I_crit'], ax=ax, colorbar=i==len(contageon_probs)-1)
        ax.set_title(f'$Avg. met ={avg_people_met_pr_day:.2f}$')
        ax.set_xlabel('Days')
        if i == 0:
            ax.set_ylabel('# Hospitalized')
        if i == 2:
            ax.set_title(f'$\\bf Avg. met ={avg_people_met_pr_day:.2f}$')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '2_SEIR_distancing_hospitalized.png'), dpi=300)
    plt.show()

    sampler.avg_people_met_pr_day = 6.86  # Set back to default
    fig, axs = plt.subplots(1, len(symp_people_out), squeeze=True, sharey='row', figsize=(12, 4))
    for i, (ax, fraction_symp_out) in enumerate(zip(axs, symp_people_out)):
        sampler.fraction_symp_out = fraction_symp_out
        np.random.seed(7)
        result = simulate(country)
        Plotter.plot_SIR(result, ax=ax)
        ax.set_title(f'$p_o ={fraction_symp_out * 100:.1f}$%')
        if i == 1:
            ax.set_title(f'$\\bf p_o ={fraction_symp_out * 100:.1f}\%$')
        ax.set_xlabel('Days')
        if i == len(symp_people_out)-1:
            ax.legend(['I', 'S', 'Recovered', 'Dead'], loc='upper center',
                      bbox_to_anchor=(1.5, 1), fancybox=False, shadow=False, ncol=1)
    plt.tight_layout()  # rect=[0, 0.03, 1, 0.95]
    plt.savefig(os.path.join(plot_path, '2_SEIR_symp_out.png'), dpi=300)
    plt.show()

    fig, axs = plt.subplots(1, len(symp_people_out), squeeze=True, sharey='row', figsize=(12, 4))
    for i, (ax, fraction_symp_out) in enumerate(zip(axs, symp_people_out)):
        sampler.fraction_symp_out = fraction_symp_out
        np.random.seed(7)
        result = repeat_simulate(country, n_repeats=n_repeats)
        Plotter.plot_intervals(result['I_crit'], ax=ax, colorbar=i==len(contageon_probs)-1)
        ax.set_title(f'$p_o ={fraction_symp_out * 100:.1f}$%')
        ax.set_xlabel('Days')
        if i == 0:
            ax.set_ylabel('# Hospitalized')
        if i == 1:
            ax.set_title(f'$\\bf p_o ={fraction_symp_out * 100:.1f}\%$')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '2_SEIR_symp_out_hospitalized.png'), dpi=300)
    plt.show()

    if False:  # 2D grid plots
        fig, axs = plt.subplots(len(average_people_mets), len(contageon_probs), squeeze=False,
                                sharey='row', sharex='col', figsize=(12, 12))
        for j, axs2 in enumerate(axs):
            for i, ax in enumerate(axs2):
                contageon_prob = contageon_probs[i]
                average_people_met = average_people_mets[j]
                sampler.contagion_prob = contageon_prob
                sampler.avg_people_met_pr_day = average_people_met
                result = simulate(country)
                Plotter.plot_SIR(result, ax=ax)
                if j == 0:
                    ax.set_title(f'$p={contageon_prob:.2f}$')
                if j == len(average_people_mets)-1:
                    ax.set_xlabel('Days')
                    if i == 1:
                        ax.legend(['I', 'S', 'Recovered', 'Dead'], loc='lower left',
                                  bbox_to_anchor=(0.5, -0.54, 2, .102), fancybox=False, shadow=False, ncol=4)
                if i == 0:
                    ax.set_ylabel(f'$Avg. met. ={average_people_met:.2f}$')

        plt.savefig(os.path.join(plot_path, '2_SEIR.png'), dpi=300)
        plt.show()


def scenario3():
    np.random.seed(7)
    # Simple SIR model.
    sampler = Sampler()
    n_days = 365*1
    population_size = 500_000
    I_initial = 500
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial, cyclical=2.5)
    country = Country([copenhagen])

    np.random.seed(7)
    result = simulate(country, n_days=n_days)
    Plotter.plot_SIR(result)
    plt.legend()
    plt.xlabel('Days')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '3_SEIR_periodic.png'), dpi=300)
    plt.show()

    np.random.seed(7)
    result = repeat_simulate(country, n_repeats=n_repeats, n_days=n_days)
    Plotter.plot_intervals(result['I_crit'].copy(), plot_median=False)
    plt.plot(result['I_crit'][0], '--k', label='Example path', lw=0.5)
    plt.xlabel('Days')
    plt.ylabel('# Hospitalized')
    plt.hlines(copenhagen.population_size * 0.0005, *plt.xlim())
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '3_SEIR_periodic_hospitalized.png'), dpi=300)
    plt.show()


    sampler = Sampler()
    n_days = 365*4
    population_size = 500_000
    I_initial = 500
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial, cyclical=2.5)
    country = Country([copenhagen])

    np.random.seed(7)
    result = repeat_simulate(country, n_repeats=n_repeats, n_days=n_days)
    Plotter.plot_intervals(result['I_crit'].copy(), plot_median=False)
    plt.plot(result['I_crit'][0], '--k', label='Example path', lw=0.5)
    plt.xlabel('Days')
    plt.ylabel('# Hospitalized')
    plt.hlines(copenhagen.population_size * 0.0005, *plt.xlim())
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '3_SEIR_periodic_hospitalized_long.png'), dpi=300)
    plt.show()

def scenario4():
    # High death rate
    sampler = Sampler(death_prob=1.0, crit_prob=1.0, symp_prob=1.0, contagion_prob=0.0228)
    #  6.86*4.67416*0.04 = 1.28259
    n_days = 5000
    population_size = 500_000
    I_initial = 5_000
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    country = Country([copenhagen])

    np.random.seed(7)
    result = simulate(country, n_days=n_days)
    Plotter.plot_SIR(result)
    plt.legend()
    plt.xlabel('Days')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '4_DEATH.png'), dpi=300)
    plt.show()

    np.random.seed(7)
    result = repeat_simulate(country, n_repeats=n_repeats, n_days=n_days)
    Plotter.plot_intervals((result['R_dead'] / copenhagen.population_size).copy() * 100, plot_median=False)
    plt.plot((result['R_dead'] / copenhagen.population_size)[0] * 100, '--k', label='Example path', lw=0.5)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.xlabel('Days')
    plt.ylabel('% Dead')
    plt.hlines(100, *plt.xlim())
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '4_DEATH_deaths.png'), dpi=300)
    plt.show()


def scenario5():
    # Control variables
    np.random.seed(7)
    sampler = Sampler()  # (symp_prob=0.98, crit_prob=0.98, death_prob=0.1)
    n_days = 50
    population_size = 5_000
    I_initial = 100
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    country = Country([copenhagen])

    np.random.seed(7)
    result = simulate(country, n_days=n_days)
    Plotter.plot_SIR(result)
    plt.legend()
    plt.xlabel('Days')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '5_CONTROL.png'), dpi=300)
    plt.show()

    np.random.seed(7)
    result = repeat_simulate(country, n_repeats=n_repeats, n_days=n_days)
    Plotter.plot_intervals(result['R_dead'].copy(), plot_median=False)
    plt.plot(result['R_dead'][0], '--k', label='Example path', lw=0.5)
    plt.xlabel('Days')
    plt.ylabel('# Dead')
    # plt.hlines(copenhagen.population_size * 0.0005, *plt.xlim())
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, '5_CONTROL_DEATH.png'), dpi=300)
    plt.show()

    def control(x, control_variable, mu_control=None):
        # mu_control = np.mean(control_variable)
        # fx = f(x)
        variances = np.cov(x, control_variable)

        # print('Control correlation:', np.corrcoef(x, control_variable)[1, 0])
        c = -variances[0, 1] / variances[1, 1]
        return x + c * (control_variable - mu_control)

    def confidence_interval(sample):
        mean, var, _ = stats.bayes_mvs(sample)
        return dict(x=mean.statistic, xerr=mean.minmax[1] - mean.statistic)

    x = 'max_R_dead'
    plt.errorbar(y=-1, **confidence_interval(result[x]), lw=1, fmt='o', capsize=10)

    for i, (control_var, mu) in enumerate(
            zip(Region.control_variates, [sampler.avg_time_inc, sampler.avg_time_symp, sampler.avg_time_symp,
                                          sampler.avg_time_crit, sampler.symp_prob, sampler.crit_prob,
                                          sampler.death_prob])):
        control_result = control(result[x], result[control_var], mu)
        plt.errorbar(y=i, **confidence_interval(control_result), lw=1, fmt='o', capsize=10, label=control_var)
    plt.yticks(range(-1, len(Region.control_variates)), labels=['Without control'] + Region.control_variates)

    plt.savefig(os.path.join(plot_path, '5_CONTROL_DEATH_control.png'), dpi=300)
    plt.show()

    pass



if __name__ == "__main__":
    scenario5()
