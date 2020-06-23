import os
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

# Matplotlib initialization
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

# Figures path
figpath = 'figures/'
if not os.path.exists(figpath):
    os.makedirs(figpath)

inc_pars = 0.65, 1.57
symp_pars = 0.79, 1.23
no_symp_pars = 0.79, 1.23
crit_pars = 12.5, 0.8

I_inc = stats.lognorm(s=inc_pars[0], scale=np.exp(inc_pars[1]))
I_symp = stats.lognorm(s=symp_pars[0], scale=np.exp(symp_pars[1]))
I_no_symp = stats.lognorm(s=no_symp_pars[0], scale=np.exp(no_symp_pars[1]))
I_crit = stats.gamma(*crit_pars)

distribs = [I_inc, I_symp, I_no_symp, I_crit]
names = [
    r'Incubation time$\sim Lognormal({0}, {1}^2)$'.format(*reversed(inc_pars)),
    r'(A)symptomatic time$\sim Lognormal({0}, {1}^2)$'.format(*reversed(symp_pars)),
    r'Asymptomatic time$\sim Lognormal({0}, {1}^2)$'.format(*reversed(no_symp_pars)),
    r'Critical time$\sim Gamma({0}, {1})$'.format(*crit_pars),
]
savenames = [
    'incubation.pdf',
    'symptomatic.pdf',
    'asymptomatic.pdf',
    'critical.pdf'
]

for i, dist in enumerate(distribs):
    
    if i == 3:
        max_x = 30
    else:
        max_x = 20

    X = np.arange(max_x+1)-0.5
    X1 = X[0:-1]
    X2 = X[1:]
    X_cdf = np.linspace(0, max_x, 10_000)
    X_rounded = np.round(X_cdf)

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    
    pdf = dist.cdf(X2) - dist.cdf(X1)
    cdf = dist.cdf(X_rounded)

    # Plot the pdf
    ax.bar(X1+0.5, pdf, color='darksalmon', label='pdf', width=0.8, align='center',
           edgecolor='black')
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, max_x+1, step=2))
    
    # Plot the cdf
    ax.plot(X_cdf+0.5, cdf, color='darkslategrey', label='cdf', linewidth=3)
    ax.grid()
    ax.legend()
    ax.set_title(names[i])
    
    plt.tight_layout()
    plt.savefig(os.path.normpath(figpath + savenames[i]), format='pdf')
    plt.show()

## Number of people met
fig, ax = plt.subplots(1, 1, figsize=(6, 4))

max_x = 20
X = np.arange(max_x+1)-0.5
X1 = X[0:-1]
X2 = X[1:]
X_cdf = np.linspace(0, max_x, 10_000)

pdf = stats.poisson(6.86).cdf(X2) - stats.poisson(6.86).cdf(X1)
cdf = stats.poisson(6.86).cdf(X_cdf)

# Plot the pdf
ax.bar(X1+0.5, pdf, color='darksalmon', label='pdf', width=0.8, align='center',
       edgecolor='black')
ax.set_xlim(0, max_x)
ax.set_ylim(0, 1)
ax.set_xticks(np.arange(0, max_x+1, step=4))

# Plot the cdf
ax.plot(X_cdf, cdf, color='darkslategrey', label='cdf', linewidth=3)
ax.grid()
ax.legend()
ax.set_title('People met per day$\sim Pois(6.86)$')

plt.tight_layout()
plt.savefig(figpath + 'people_met.pdf', format='pdf')
plt.show()









