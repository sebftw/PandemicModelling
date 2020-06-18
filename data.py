import pandas as pd
import matplotlib.pyplot as plt
import os

# DTU model is used to simulate and predict:
# https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus

# We are mostly interested in the number of admitted, as this is a more reliable number.
# https://www.ssi.dk/sygdomme-beredskab-og-forskning/sygdomsovervaagning/c/covid19-overvaagning

# Some explanations of the definitions are given (in Danish) at:
# https://politi.dk/coronavirus-i-danmark/foelg-smittespredningen-globalt-regionalt-og-lokalt

date_parser = lambda col: pd.to_datetime(col, format='%Y-%m-%d')

def add_vlines(ax):
    vlineargs = dict(linestyles='dashed', lw=1, alpha=0.8)
    # First tested positive was at 2020-02-26 (results 2020-02-27?)
    # src: https://www.ssi.dk/aktuelt/nyheder/2020/02_27_foerste-tilfaelde-af-ny-coronavirus-i-dk
    limits = ax.get_ybound()
    v1 = ax.vlines(date_parser('2020-02-26'), *limits, label='First positive case DK.', **vlineargs)
    v2 = ax.vlines(date_parser('2020-03-06'), *limits, label='Press meeting: Limit of 1000 people.', color='r', **vlineargs)
    v3 = ax.vlines(date_parser('2020-03-11'), *limits, label='Press meeting: Schools close.', **vlineargs)
    # Start of "afbødningsfase" (Fig. 1.1.)
    v4 = ax.vlines(date_parser('2020-03-13'), *limits, label='Press meeting: Borders close.', **vlineargs)
    v5 = ax.vlines(date_parser('2020-03-29'), *limits, label='Change in test criteria to match ECDC.', color='b', **vlineargs)

    # Lifting of restrictions
    # https://politi.dk/coronavirus-i-danmark/kontrolleret-genaabning-af-danmark
    v6 = ax.vlines(date_parser('2020-04-20'), *limits, label='Opening of e.g. barbers.', color='g', **vlineargs)
    # In between at 11. May, the clothing stores were opened.
    v7 = ax.vlines(date_parser('2020-05-18'), *limits, label='Opening of shops, schools, churches etc.', **vlineargs)
    v8 = ax.vlines(date_parser('2020-06-15'), *limits, label='Borders open to some countries.', **vlineargs)
    return [v1, v2, v3, v4, v5, v6, v7, v8]

def get_data(datadir = 'data', plot=False):
    sharedargs = dict(sep=';', decimal=',', thousands='.', encoding='utf-8',
                      date_parser=date_parser,
                      parse_dates=True, index_col=0)

    pos_tests = os.path.join(datadir, 'Test_pos_over_time.csv')
    admitted = os.path.join(datadir, 'Newly_admitted_over_time.csv')
    deaths = os.path.join(datadir, 'Deaths_over_time.csv')

    pos_tests = pd.read_csv(pos_tests, skipfooter=2, engine='python', **sharedargs)
    admitted = pd.read_csv(admitted, **sharedargs)
    admitted.columns = ['Admitted_' + name for name in admitted.columns]

    deaths = pd.read_csv(deaths, skipfooter=1, engine='python', **sharedargs)
    deaths.columns = ['Deaths']  # Warning: There was some issues due to 'Ø' in the second column.

    alldata = admitted.join(deaths, how='outer').join(pos_tests, how='outer')

    # We see that this column is redundant.
    # print((data['Tested_kumulativ'] - data['Tested'].cumsum()).max())
    # We don't care too much if people are tested twice etc.
    alldata = alldata.drop(columns=['Tested_kumulativ', 'NotPrevPos', 'PrevPos'])

    if plot:
        axes = alldata.plot(subplots=True, figsize=(8, 20))
        for ax in axes:
            vlines = add_vlines(ax)
        # plt.subplots_adjust(bottom=0.3, wspace=0.33)
        plt.legend(handles=vlines, bbox_to_anchor=(0.5, -0.3), loc='upper center', ncol=2)
        plt.tight_layout()
        # plt.savefig(os.path.join(datadir, 'info', 'plot.pdf'))
        plt.show()

    return alldata

def get_contact_data(file=os.path.join('data', 'BBC_matrices_reciprocal_filled_modified.xlsx')):
    contact_data = pd.read_excel(file, index_col=0, sheet_name=None)

    # https://cran.r-project.org/web/packages/socialmixr/vignettes/introduction.html
    #
    contact_data['all_physical']

    pass



if __name__ == "__main__":
    get_contact_data()

    #data = get_data(plot=True)
    #print(data.describe())
    # Most interesting is probably the Positive, NumDeaths, and Admissions.

