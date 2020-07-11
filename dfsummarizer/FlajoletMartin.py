import math

def trailing_zeros(n):
    s = str(n)
    return len(s)-len(s.rstrip('0'))

def get_prefix(seed):
    return 'X' * seed

class FMEstimator():
    def __init__(self):
        self.sets = 10
        self.repeats = 10
        self.total = self.sets * self.repeats
        self.result = [ "" for i in range(self.total)]
        self.result_tail = [[] for i in range(self.total)]
    def update(self, val):
        for seed in range(self.total):
            self.result[seed] = format(abs(hash( get_prefix(seed) + str(val))), '128b')
            self.result_tail[seed].append(trailing_zeros(self.result[seed]))
    def update_all(self, vals):
        for val in vals:
            self.update(val)
    def estimate(self): 
        temp = 0
        result = [ 0 for i in range(self.sets)]
        for s in range(self.sets):
            for r in range(self.repeats):
                seed = r + (s * self.repeats)
                result[s] += (2**(max(self.result_tail[seed])))
            result[s] = result[s] / float(self.repeats)
        return (math.ceil(min(result)))


