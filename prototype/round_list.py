class RoundList(object):

    def __init__(self, size):
        if type(size) == int:
            self.l_in = [None for _ in range(size)]
            self.idx = size - 1
            self.size = size
        elif type(size) == list:
            self.l_in = size[:]
            self.size = len(size)
            self.idx = self.size - 1

    def get(self):
        return list(filter(lambda x: x is not None,
                           self.l_in[self.idx:] + self.l_in[:self.idx]))

    def push(self, v):
        self.l_in[self.idx] = v
        self.idx = (self.idx + 1) % self.size

    def __eq__(self, other):
        if type(other) == list:
            return self.get() == other
        else:
            return self.get() == other.get()

    def __repr__(self):
        return str(self.get())

    def copy(self):
        temp = RoundList(self.size)
        temp.l_in = self.l_in[:]
        temp.idx = self.idx
        return temp
