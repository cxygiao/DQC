from math import sqrt

class Result:
    def __init__(self, r1, r2, r3):
        self.result1 = r1
        self.result2 = r2
        self.result3 = r3

    def solve(self):
        delta = self.result2 ** 2 - 4 * self.result1 * self.result3
        if delta >= 0:
            x1 = (-self.result2 + sqrt(delta)) / (2 * self.result1)
            x2 = (-self.result2 - sqrt(delta)) / (2 * self.result1)
            return x1, x2
        else:
            return None, None

if __name__ == '__main__':
    a, b, c = 1, 2, 1
    ret = Result(a, b, c)
    print(ret.solve())
