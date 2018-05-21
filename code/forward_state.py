from function import Function

class ForwardState(object):

    def __init__(self, forward_path):
        if type(forward_path) == list:
            self.forward_path = " ".join(forward_path)
        elif isinstance(forward_path, Function):
            self.forward_path = " ".join(forward_path.to_list())
        elif type(forward_path) == str:
            self.forward_path = forward_path
        else:
            raise ValueError("Wrong type " + str(forward_path))

    def is_end(self):
        return len(self.forward_path) == 0

    def __eq__(self, other):
        return self.forward_path == other.forward_path

    def __hash__(self):
        return hash(self.forward_path)

    def remove_one_relation(self):
        first_space = self.forward_path.find(" ")
        if first_space == -1:
            return ForwardState("")
        return ForwardState(self.forward_path[first_space + 1:])

    def get_constraint_path(self):
        return self.forward_path

    def __repr__(self):
        return self.forward_path

    def length(self):
        if self.is_end():
            return 0
        else:
            return self.forward_path.count(" ") + 1
