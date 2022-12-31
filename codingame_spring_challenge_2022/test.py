class DoubleTracker:
    def __init__(self, n):
        print('start init')
        self.n = n
        self.d = self.get_double()
        print('end init')

    def get_double(self):
        print('from get_double counting double')
        return 2*self.n

    def __str__(self):
        return f"n {self.n}"


dt = DoubleTracker(4)
dt1 = DoubleTracker(5)
dt2 = DoubleTracker(2)

print(dt.n, dt.d)
print(dt.get_double())

print("double trackers", [*map(lambda e: e.__str__(), [dt, dt1, dt2])])