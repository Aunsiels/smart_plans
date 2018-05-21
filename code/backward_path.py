from function import Function

class BackwardPath(object):

    def __init__(self, backward_path, direction, ending=None, remaining=0):
        assert direction in ["f", "b"], "Wrong direction"
        if type(backward_path) == list:
            self.backward_path = " ".join(backward_path)
        elif isinstance(backward_path, Function):
            if direction == "b":
                self.backward_path = " ".join(backward_path.to_list()[::-1])
            else:
                self.backward_path = " ".join(backward_path.to_list())
        elif type(backward_path) == str:
            self.backward_path = backward_path
        self.direction = direction
        self.ending = ending
        self.remaining = remaining

    def is_end(self):
        return len(self.backward_path) == 0

    def length(self):
        base = 0
        if self.ending:
            base = self.ending.length() + self.remaining
        if self.is_end():
            return base
        else:
            return self.backward_path.count(" ") + base + 1

    def __eq__(self, other):
        return self.direction == other.direction and \
            self.backward_path == other.backward_path and \
            self.remaining == other.remaining and \
            self.ending == other.ending

    def __hash__(self):
        return hash(self.direction) + hash(self.backward_path) + \
            hash(self.ending) + hash(self.remaining)

    def remove_one_relation(self):
        first_space = self.backward_path.find(" ")
        if first_space == -1:
            return BackwardPath("", self.direction)
        return BackwardPath(self.backward_path[first_space + 1:],
                            self.direction)

    def get_constraint_path(self):
        if self.direction == "f":
            return self.backward_path
        else:
            return " ".join(map(get_inverse, self.backward_path.split(" ")))

    def __repr__(self):
        return self.backward_path + ', d:' + self.direction


def get_inverse(relation):
    if len(relation) == 0:
        return relation
    if relation[-1] == "-":
        return relation[:-1]
    else:
        return relation + "-"
