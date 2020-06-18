import matplotlib.pyplot as plt

def plot_hospitalized_people(I_crit, hospital_beds, n_days):
    # %% Plotting

    fig, ax = plt.subplots(1, 1, figsize=(7,3))
    ax.plot(I_crit, c='lightskyblue', label=f'Hospitalized')
    ax.hlines(hospital_beds, 0, n_days, label=f'Respirators')
    ax.legend()
    ax.set_title('Number of hospitalized people')
    
    
def plot_fatalities(R_dead):
    fig, ax = plt.subplots(1, 1, figsize=(7,3))
    ax.plot(R_dead, c='lightskyblue', label=f'Deaths')
    ax.legend()
    ax.set_title('Total fatalities')


def plot_SIR(pandemic_info):
    fig, ax = plt.subplots(1, 1, figsize=(7,3))
    S = pandemic_info["S"]
    I = pandemic_info["I_inc"] + pandemic_info["I_symp"] + pandemic_info["I_no_symp"] + pandemic_info["I_crit"]
    R = pandemic_info["R_dead"] + pandemic_info["R_surv"]
    
    ax.plot(S, c='lightskyblue', label=f'S')
    ax.plot(I, c='darksalmon', label=f'I')
    ax.plot(R, c='darkslategray', label=f'R')
    ax.legend()


def plot_each_group(PI):
    fig, ax = plt.subplots(4, 2, figsize=(15,15))
    
    ax[0][0].plot(PI["S"],  c='lightskyblue', label=f'S',)
    ax[0][1].plot(PI["I_inc"], c='darksalmon', label=f'I_inc')
    ax[1][0].plot(PI["I_symp"], c='darksalmon', label=f'I_symp')
    ax[1][1].plot(PI["I_no_symp"], c='darksalmon', label=f'I_no_symp')
    ax[2][0].plot(PI["I_crit"], c='darksalmon', label=f'I_crit')
    ax[2][1].plot(PI["R_surv"], c='darkslategray', label=f'R_surv')
    ax[3][0].plot(PI["R_dead"], c='darkslategray', label=f'R_dead')
    ax[3][1].remove()
    for i in range(len(ax)):
        for j in range(len(ax[i])):
            ax[i][j].legend()
    plt.show()

   