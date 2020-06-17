import pandas as pd
import matplotlib.pyplot as plt
import os

datadir = 'data'

pos_tests = os.path.join(datadir, 'Test_pos_over_time.csv')
deaths = os.path.join(datadir, 'Deaths_over_time.csv')
admitted = os.path.join(datadir, 'Newly_admitted_over_time.csv')

sharedargs = dict(sep=';', decimal=',', thousands='.',  encoding='utf-8',
                  date_parser=lambda col: pd.to_datetime(col, format='%Y-%m-%d'),
                  parse_dates=True, index_col=0)

pos_tests = pd.read_csv(pos_tests, skipfooter=2, engine='python', **sharedargs)
pos_tests.plot(subplots=True)
plt.show()

deaths = pd.read_csv(deaths, skipfooter=1, engine='python', **sharedargs)
deaths.columns = ['NumDeaths']  # Warning: There was some issues due to 'Ø' in the second column.
deaths.plot(subplots=True)
plt.show()

admitted = pd.read_csv(admitted, **sharedargs)
admitted.plot(subplots=True)
plt.show()

# We are mostly interested in the number of admitted, as this is a more reliable number.
# https://www.ssi.dk/sygdomme-beredskab-og-forskning/sygdomsovervaagning/c/covid19-overvaagning
print(pos_tests)
print(deaths)
print(admitted)
