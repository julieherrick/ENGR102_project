# action_functions.py
#
# functions that are called to run the simulation
#
# Julie Herrick (627001411), Rita Nedrow (526007286), Dominic Kinsey (427004840), Caitlin Garrigus (327001698)
# December 2018
# ENGR 102-213
# Final Project

import numpy as np


def create_class_list(pop):
    """
   This function creates list of individuals through the Student class
   pop: number of people in the simulation
   Return:
   --------
   population: list of students and their attributes
   """
    from individual import Student
    from scipy.stats import lognorm
    population = []
    resist_val = [1., 3.]
    recov_val = [1, 5]
    activ_val = [3, 7]
    transmis_val = [3., 8.]
    death_val = [.4, .3]
    for i in range(pop):
        resist = lognorm.rvs(sigma(resist_val), scale=np.exp(mu(resist_val)), size=1)
        recov = int(lognorm.rvs(sigma(recov_val), scale=np.exp(mu(recov_val)), size=1))
        activ = int(lognorm.rvs(sigma(activ_val), scale=np.exp(mu(activ_val)), size=1))
        transmis = lognorm.rvs(sigma(transmis_val), scale=np.exp(mu(transmis_val)), size=1)
        if resist < 6:
            death_chance = lognorm.rvs(sigma(death_val), scale=np.exp(mu(death_val)), size=1)
        else:
            death_chance = 0
        x = Student(resist, recov, activ, transmis, death_chance)
        population.append(x)

    return population


def sigma(val):
    """
    This function calculates the value of sigma to use in the lognorm equation
    val: sigma value, mu value
    Return:
    --------
    log(sigma value)
    """
    import numpy as np
    log_sigma = np.sqrt(np.log(1 + (val[0] / val[1]) ** 2))

    return log_sigma


def mu(val):
    """
    This function calculates the value of mu to use in the lognorm equation
    val:  sigma value, mu value
    Return:
    -------
    log(mu value)
    """
    import numpy as np
    log_mu = np.log(val[1] / (np.sqrt(1 + (val[0] / val[1]) ** 2)))

    return log_mu


def infected_stats(allStudents):
    """
   gets the number of infected people in the population
   allStudents: the list of students in the population
   Return:
   -------
   i: number of people infected
   """
    i = 0
    for x in range(len(allStudents)):
        test_student = allStudents[x]
        if test_student.sick:
            i += 1
    return i


def immune_stats(allStudents):
    """
   gets the number of immune people in the population
   allStudents: the list of students in the population
   Return:
   -------
   i: number of people immune
   """
    i = 0
    for x in range(len(allStudents)):
        if allStudents[x].immune:
            i += 1
    return i


def longest_recovery(allStudents):
    """
   This function finds the longest current recovery of students that are sick
   allStudents: the list of students in the population
   Return:
   -------
   longest: the longest recovery time of all infected students
   """
    longest = 0
    for student in allStudents:
        if student.sick == True:
            if student.time_until_healthy > longest:
                longest = student.time_until_healthy
    return longest


def status_at_end(allStudents, dur):
    """
    allStudents: the list of students in the population
    dur: the duration of the experiment
    Return:
    -------
    plot a bar graph showing if students are healthy, infected, immune, or dead
    """
    import matplotlib.pyplot as plt
    import numpy as np
    never_infected = 0
    infected = 0
    immune = 0
    death = 0
    for student in allStudents:
        if student.sick:
            infected += 1
        elif student.immune:
            immune += 1
        elif student.dead:
            death += 1
        elif not student.got_sick:
            never_infected += 1

    objects = ('Never Infected', 'Currently Infected', 'Immune', 'Dead')
    y_position = np.arange(len(objects))
    results = [never_infected, infected, immune, death]

    plt.bar(y_position, results, align='center', alpha=0.5)
    plt.xticks(y_position, objects)
    plt.ylabel('Number of People Infected')
    plt.title('Status of Population after ' + str(dur) + ' days')
    plt.show()


def test_input(text):
    """
    text: instructions for what to enter
    Return:
    -------
    tests if input is acceptable (positive and an integer)
    """
    try:
        # get input from user for coefficient of a
        a = int(input(text))
        try:
            list_test = np.zeros(a)
            try:
                y = 3/a
            except ZeroDivisionError:
                print('Zero is not a valid input!')
                a = test_input(text)
        except ValueError:
            print('You must enter a positive number!')
            a = test_input(text)

    except ValueError:
        print('You must enter an integer!')
        a = test_input(text)
    return a


def sick_plot(sick_list, dur):
    """
   sick_list: list of number of sick people per day
   dur: duration of simulation
   Return:
   -----
    plots the number sick people per day
   """
    import matplotlib.pyplot as plt
    plt.plot(sick_list)
    plt.xlabel('Day')
    plt.ylabel('Number Sick')
    plt.title('Number of People Sick over ' + str(dur) + ' days')
    plt.show()


def average_recovery(allStudents):
    """
  This function finds the average recovery time of everyone that got infected
  allStudents: list of all students in simulation
  Return:
  ------
  avg recovery time of students who got sick (float)
  """
    i = 0
    total = 0
    for student in allStudents:
        if student.got_sick:
            i += 1
            total += student.recovery
    avg = total / i
    return round(avg, 1)


def largest_sick_pop(sick_list):
    """
    sick_list: number of people sick each day
    Return:
    -------
    largest number of sick people on a given day and what day it was
    """
    import numpy as np
    largest_sick = np.max(sick_list)
    day = np.argmax(sick_list)

    return largest_sick, day


def death_stats(allStudents):
    """
   gets the number of dead people in the population
   allStudents: the list of students in the population
   Return:
   -------
   i: number of people that are dead
   """
    i = 0
    for student in allStudents:
        if student.dead:
            i += 1
    return i

def percent_sick(allStudents):
    """
    finds the percentage of the population that became infected
    allStudents: the list of students in the population
    Return:
   -------
    percent: the percentage of the population that got sick during the simulation
   """
    infected = 0
    for student in allStudents:
        if student.got_sick:
            infected += 1.

    percent = infected/(len(allStudents)) * 100

    return round(percent,1)
