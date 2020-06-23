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

from simulation import simulate, repeat_simulate

n_repeats = 5

plot_path = 'plots'

def scenario1():
    np.random.seed(7)
    # Simple SIR model.
    sampler = Sampler(crit_prob=0.0, symp_prob=1.0,
                      fraction_symp_out=1.0, incubation=False)
    # We have S -> I_symp -> R
    # We get an R0 of 6.86*4.67416*0.04 = 1.28259

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

    return None
    fig, axs = plt.subplots(len(average_people_mets), len(contageon_probs), squeeze=False,
                            sharey='row', sharex='col', figsize=(12, 12))
    for j, axs2 in enumerate(axs):
        for i, ax in enumerate(axs2):
            contageon_prob = contageon_probs[i]
            average_people_met = average_people_mets[j]
            sampler.contagion_prob = contageon_prob
            sampler.avg_people_met_pr_day = average_people_met
            result = repeat_simulate(country)
            Plotter.plot_intervals(result['I'], ax=ax)
            if j == 0:
                ax.set_title(f'$p={contageon_prob:.2f}$')
            if j == len(average_people_mets) - 1:
                ax.set_xlabel('Days')
                # if i == 1:
                #    ax.legend(['I', 'S', 'Recovered', 'Dead'], loc='lower left',
                #              bbox_to_anchor=(0.5, -0.54, 2, .102), fancybox=False, shadow=False, ncol=4)
            if i == 0:
                ax.set_ylabel(f'$Avg. met. ={average_people_met:.2f}$')

    plt.savefig(os.path.join(plot_path, '2_SEIR_infections.png'), dpi=300)
    plt.show()

def scenario3():
    np.random.seed(7)
    # Simple SIR model.
    sampler = Sampler()

    population_size = 500_000
    I_initial = 5_000
    copenhagen = Region('Copenhagen', population_size, sampler, I_initial)
    country = Country([copenhagen])

    symp_people_out = [0.0, 0.05, 0.1, 0.2, 0.5]
    fig, axs = plt.subplots(1, len(symp_people_out), squeeze=True, sharey='row', figsize=(12, 4.5))
    for ax, fraction_symp_out in zip(axs, symp_people_out):
        sampler.fraction_symp_out = fraction_symp_out
        result = simulate(country)
        Plotter.plot_SIR(result, ax=ax)
        ax.set_title(f'$Symp. out ={fraction_symp_out:.2f}$')
        ax.set_xlabel('Days')
    ax.set_xlabel('')
    ax.legend(['I', 'S', 'R'], loc='upper center', bbox_to_anchor=(0.5, -0.17), fancybox=False, shadow=False, ncol=3)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # fig.legend(['S', 'I', 'R'], bbox_to_anchor=(2, 0), loc='lower right')
    # plt.subplots_adjust(left=0.07, right=0.93, wspace=0.25, hspace=0.35)
    plt.savefig(os.path.join(plot_path, '3_SEIR.png'), dpi=300)
    plt.show()

if __name__ == "__main__":
    scenario2()