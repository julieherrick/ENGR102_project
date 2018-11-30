

class Student(object):
    """"""
    def __init__(self, resistance, recovery, activity, transmission_rate):
        super(Student, self).__init__()
        self.resistance = resistance
        self.recovery = recovery
        self.activity = activity
        self.transmission_rate = transmission_rate


#if __name__ == '__main__':