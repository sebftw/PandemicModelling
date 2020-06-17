from Country import Country

avg_people_met = 2
n_regions = 1
population_size = 10000
hospital_beds = 10
I_initial = 10

contagion_prob = 0.05
crit_prob = 0.2
death_prob = 0.22

avg_time_inc = 5
avg_time_symp = 7.5
avg_time_no_symp = 7.5
avg_time_crit = 9


Denmark = Country(n_regions, population_size, hospital_beds, I_initial,
                 contagion_prob, crit_prob, death_prob, avg_time_inc, 
                 avg_time_symp, avg_time_no_symp, avg_time_crit,avg_people_met)
for t in range(1,1000):
    I_critical, R_dead = Denmark.simulate_day(t)
    print(f"Crit: {I_critical}      dead: {R_dead}")
    
    