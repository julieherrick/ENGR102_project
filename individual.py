# individual.py
#
# creates Student class and it's attributes and methods
#
# Julie Herrick (627001411), Rita Nedrow (526007286), Dominic Kinsey (427004840), Caitlin Garrigus (327001698)
# December 2018
# ENGR 102-213
# Final Project


class Student(object):
    """"""
    def __init__(self, resistance, recovery, activity, transmission_rate, chance_of_death):
        super(Student, self).__init__()
        self.resistance = resistance
        self.recovery = recovery
        self.activity = activity  #change with update
        self.transmission_rate = transmission_rate
        self.chance_of_death = chance_of_death
        # initialize other object attributes
        self.immune = False
        self.sick = False
        self.time_until_healthy = 0
        self.got_sick = False
        self.dead = False

    def get_sick(self, interacted, all_students):
        """
        interacted: list of index numbers of the students the current test student is interacting with
        all_students: the list of all students
        Action:
        --------
        uses poisson distribution to determine if individual that is interacted with gets sick
        """
        from scipy.stats import poisson
        for y in interacted:
            subject = all_students[y]
            if not self.dead:
                if not subject.dead:
                    if (self.sick != subject.sick) and not (self.immune or subject.immune):
                        if poisson.rvs(self.transmission_rate, size=1):
                            if poisson.rvs(subject.resistance, size=1):
                                subject.sick = True
                                subject.time_until_healthy = subject.recovery
                                subject.activity = (subject.activity // 2)

    def interact(self, all_students):
        """
        all_students: list of all students in the population
        Action:
        --------
        randomly generates a list of students the test student interacts with, returns that list
        """
        from numpy.random import uniform
        interacted = []
        for i in range(int(self.activity)):
            interacted.append(int(uniform(0, len(all_students))))
        Student.get_sick(self, interacted, all_students)
        return interacted

    def update(self, allStudents):
        """
        allStudents: list of all students in the population
        self: the test student
        Action:
        --------
        reduces time_until_healthy by 1 day, updates interactions
        """

        if self.sick:
            self.got_sick = True
            if self.time_until_healthy > 0:
                self.interact(allStudents)
                self.time_until_healthy -= 1
            if self.time_until_healthy == 0:
                self.immune = True
                self.activity = self.activity * 2
                self.sick = False

    def death(self):
        """
        allStudents: list of all students in the population
        Action:
        --------
        based on the subjects chance of death the simulation will kill individuals after a day of being sick
        """
        from scipy.stats import poisson
        if self.sick:
            if self.chance_of_death > .7:
                if poisson.rvs(10, size=1):
                    self.sick = False
                    self.dead = True
                    self.immune = False
                    self.got_sick = True
                    self.time_until_healthy = 0


if __name__ == '__main__':
    student0 = Student(9, 12, 5, 17, .4)
    student1 = Student(2, 8, 4, 27, .45)
    student2 = Student(14, 13, 3, 92, .65)
    student3 = Student(6, 7, 2, 38, .8)
    student4 = Student(1, 9, 1, 54, .9)
    student5 = Student(5, 10, 1, 88, .53)
    student6 = Student(12, 4, 2, 73, .74)
    student7 = Student(10, 15, 3, 41, .59)
    student8 = Student(13, 5, 4, 8, .71)
    student9 = Student(5, 2, 5, 62, .49)

    students = [student0, student1, student2, student3, student4, student5, student6, student7, student8, student9]

    student0_interactions = student0.interact(students)
    print(student0_interactions)
    student6_interactions = student6.interact(students)
    print(student6_interactions)

    student0.sick = True
    student0.get_sick(student0_interactions, students)
    duration = 6
    for d in range(duration):
        print('\nday', d)
        i = 0
        for student in students:
            print('Student' + str(i) + ' sick: ', student.sick, '\trecovery remaining: ', student.time_until_healthy, '   \tdead: ', student.dead)
            i += 1
            student.update(students)
            student.death()


