# simulation.py
#
# calls individual.py and action functions.py to run the simulation
#
# Julie Herrick (627001411), Rita Nedrow (526007286), Dominic Kinsey (427004840), Caitlin Garrigus (327001698)
# December 2018
# ENGR 102-213
# Final Project

from individual import Student
from action_functions import *
import numpy as np


population = test_input('Enter the number of people in the sample population: ')
duration = test_input('Enter the desired duration (in days) of the simulation: ')
sample_students = create_class_list(population)
sample_students[0].sick = True
sample_students[0].time_until_healthy = sample_students[0].recovery
sample_students[0].transmission_rate = 100
sample_students[0].activity = 30
sick_list = np.zeros(duration)
for d in range(duration):
    if infected_stats(sample_students) >= 0:
        print('\nDay', d)
        print('Number of individuals infected: ', infected_stats(sample_students))
        print('Number of immune individuals: ', immune_stats(sample_students))
        print('Time for the person with the longest recovery time to recover: ', longest_recovery(sample_students))
        print('Number of individuals that have been killed by the infection: ', death_stats(sample_students))
        sick_list[d] = infected_stats(sample_students)
        if infected_stats(sample_students) == 0 and longest_recovery(sample_students) == 0:
            print('Population is all healthy after ' + str(d) + ' days')
            break
        for i in range(len(sample_students)):
            studentX = sample_students[i]
            interactions = studentX.interact(sample_students)
            studentX.get_sick(interactions, sample_students)
            studentX.update(sample_students)
            studentX.death()

print('\nEnd of Simulation Statistics')
print('-----------------------------------')
print('The average recovery time throughout the simulation was ', average_recovery(sample_students), 'days')
print('The most people sick at a given time was on day', largest_sick_pop(sick_list)[1], 'when', int(largest_sick_pop(sick_list)[0]), 'students were sick')
print(str(percent_sick(sample_students)) + '% of the population became infected')
sick_plot(sick_list, duration)
status_at_end(sample_students, duration)
