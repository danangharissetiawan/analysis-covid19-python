import pandas as pd
import matplotlib.pyplot as plt


confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('time_series_covid19_recovered_global.csv')

print(confirmed.head())

confirmed = confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)
deaths = deaths.drop(['Province/State', 'Lat', 'Long'], axis=1)
recovered = recovered.drop(['Province/State', 'Lat', 'Long'], axis=1)

confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')

confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T

new_cases = confirmed.copy()

for day in range(1, len(confirmed)):
    new_cases.iloc[day] = confirmed.iloc[day] - confirmed.iloc[day - 1]

growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    growth_rate.iloc[day] = (new_cases.iloc[day] / confirmed.iloc[day - 1])

active_cases = confirmed.copy()

for day in range(0, len(confirmed)):
    active_cases.iloc[day] = confirmed.iloc[day] - \
        deaths.iloc[day]-recovered.iloc[day]


overall_growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    overall_growth_rate.iloc[day] = (
        (active_cases.iloc[day] - active_cases.iloc[day-1]) / active_cases.iloc[day - 1]) * 100

death_rate = confirmed.copy()

for day in range(0, len(confirmed)):
    death_rate.iloc[day] = (deaths.iloc[day] / confirmed.iloc[day]) * 100


hospitalization_rate_estimate = 0.05

hospitalization_needed = confirmed.copy()

for day in range(0, len(confirmed)):
    hospitalization_needed.iloc[day] = active_cases.iloc[day] * \
        hospitalization_rate_estimate

estimated_death_rate = 0.03
#print(deaths['Italy'].tail()[4] / estimated_death_rate)


# Visualisasi data
# ax = plt.subplot()
# ax.set_facecolor('black')
# ax.figure.set_facecolor('#121212')
# ax.tick_params(axis='x', colors='white')
# ax.tick_params(axis='y', colors='white')
# ax.set_title('COVID 19 - Total Kasus Terkonfirmasi', color='white')
# ax.legend(loc='upper left')

# countries = ['Indonesia', 'Malaysia', 'China', 'Australia', 'Italy']

# # country = "Indonesia"
# for country in countries:
#     confirmed[country][0:].plot(label=country)

# plt.legend(loc='upper left')
# plt.show()

# countries = ['Indonesia', 'Malaysia', 'China', 'Australia', 'Italy']

# for country in countries:
#     ax = plt.subplot()
#     ax.set_facecolor('black')
#     ax.figure.set_facecolor('#121212')
#     ax.tick_params(axis='x', colors='white')
#     ax.tick_params(axis='y', colors='white')
#     ax.set_title(
#         f"COVID-19 - Tingkat Pertumbuhan Aktif Keseluruhan [{country}]", color='white')
#     overall_growth_rate[country][10:].plot.bar()
#     plt.show()

# ax = plt.subplot()
# ax.set_facecolor('black')
# ax.figure.set_facecolor('#121212')
# ax.tick_params(axis='x', colors='white')
# ax.tick_params(axis='y', colors='white')
# ax.set_title(
#     f"COVID-19 - Tingkat Pertumbuhan Aktif Keseluruhan [{'Indonesia'}]", color='white')
# overall_growth_rate['Indonesia'][10:].plot.bar()
# plt.show()


# Mensimulasikan
simulation_growth_rate = 0.1
dates = pd.date_range(start='08/28/2020', periods=40, freq='D')
dates = pd.Series(dates)
dates = dates.dt.strftime('%m/%d/%Y')

simulated = confirmed.copy()
simulated = simulated.append(pd.DataFrame(index=dates))

for day in range(len(confirmed), len(confirmed)+40):
    simulated.iloc[day] = simulated.iloc[day - 1] * \
        (simulation_growth_rate + 1)

ax = simulated['Indonesia'][10:].plot(label='Indonesia')
ax.set_axisbelow(True)
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('Simulasi COVID 19 Indonesia 40 Hari Kedepan', color='white')
ax.legend(loc='upper left')

plt.show()
