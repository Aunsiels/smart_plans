from backward_path import BackwardPath
from utils import starts_with, inverse_path

class BackwardState(object):

    def __init__(self, backward_paths):
        self.backward_paths = backward_paths
        ends_f, ends_b = self.number_ends()
        # remove the common ending forward and backward. Exploration of it
        # would result into a loop
        if ends_f == 1 and ends_b == 1:
            clean_backward_paths = []
            for bp in self.backward_paths:
                if not bp.is_end():
                    clean_backward_paths.append(bp)
            self.backward_paths = clean_backward_paths
        self.backward_paths_set = frozenset(backward_paths)

    def number_ends(self):
        counter_f = 0
        counter_b = 0
        for bp in self.backward_paths:
            if bp.is_end():
                if bp.direction == "f":
                    counter_f += 1
                else:
                    counter_b += 1
        return (counter_f, counter_b)


    def total_length(self):
        return len(self.backward_paths)

    def length(self):
        counter_f = 0
        counter_b = 0
        for bp in self.backward_paths:
            if bp.direction == "f":
                counter_f += 1
            else:
                counter_b += 1
        return (counter_f, counter_b)

    def have_different_length(self):
        forwards = []
        backwards = []
        for bp in self.backward_paths:
            if bp.direction == "f":
                forwards.append(bp.length())
            else:
                backwards.append(bp.length())
        return len(set(forwards)) == len(forwards) and \
            len(set(backwards)) == len(backwards)

    def is_valid(self):
        if len(self.backward_paths) == 0:
            return True
        counter_f, counter_b = self.length()
        if not counter_f == counter_b - 1:
            return False
        ends_f, ends_b = self.number_ends()
        if ends_b > 1:
            return False
        if ends_b == 1 and len(self.backward_paths) > 1 and ends_f != 1:
            return False
        if not self.have_different_length():
            return False
        return True

    def __eq__(self, other):
        return self.backward_paths_set == other.backward_paths_set and\
            len(self.backward_paths) == len(other.backward_paths)

    def __hash__(self):
        return hash(self.backward_paths_set)

    def remove_one_relation(self):
        new_bps = []
        for bp in self.backward_paths:
            if not bp.is_end():
                new_bps.append(bp.remove_one_relation())
        return BackwardState(new_bps)

    def get_constraint_path(self):
        max_length = -1
        best_path = ""
        for bp in self.backward_paths:
            cp = bp.get_constraint_path()
            n_spaces = cp.count(" ")
            if n_spaces > max_length:
                max_length = n_spaces
                best_path = cp
        return best_path

    def add_one(self, functions, cp):
        forward = True
        bp_ending = []
        # Add forward or backward ?
        for bp in self.backward_paths:
            if bp.is_end():
                bp_ending.append(bp)
            if bp.is_end() and bp.direction == "b":
                forward = False
        if len(bp_ending) != 1:
            return []
        res_f = []
        for f in functions:
            if forward:
                f_str = " ".join(f.to_list())
            else:
                f_str = " ".join(f.get_inverse_function())
            if starts_with(f_str, cp):
                res_f.append(f)
        clean_bp = []
        for bp in self.backward_paths:
            if not bp.is_end():
                clean_bp.append(bp)
        res = []
        if forward:
            direction = "f"
        else:
            direction = "b"
        for f in res_f:
            res.append(BackwardState(clean_bp[:] +
                                     [BackwardPath(f, direction)]))
        # Deal with kinks
        # For now, we do a simplify version, which is INCOMPLETE
        for f in functions:
            f_l = f.to_list()
            for i in range(1, len(f_l)):
                f_left = f_l[:i]
                f_right = f_l[i:]
                if forward:
                    # We need to find a backward path which has the correct
                    # length
                    corrects = []
                    for bp in clean_bp:
                        if len(f_left) == len(f_right) + bp.length() and\
                                bp.direction == "b":
                            corrects.append(bp)
                    if len(corrects) != 1:
                        continue
                    forward_p = " ".join(f_left)
                    backward_p = corrects[0].backward_path + " " + \
                        " ".join(f_right[::-1])
                else:
                    corrects = []
                    for bp in clean_bp:
                        if len(f_right) == len(f_left) + bp.length() and \
                                bp.direction == "f":
                            corrects.append(bp)
                    if len(corrects) != 1:
                        continue
                    forward_p = corrects[0].backward_path + " " + \
                        " ".join(f_left)
                    backward_p = f_right[::-1]
                backward_inv = inverse_path(backward_p)
                if starts_with(forward_p, cp) and\
                        starts_with(backward_inv, cp) and\
                        stars_with(forward_p, backward_inv):
                    res.append(BackwardState(clean_bp[:] +
                                             [BackwardPath(forward_p, "f"),
                                              BackwardPath(backward_p,
                                                           "b")]))
        return res

    def __repr__(self):
        return "(" + ", ".join(map(str, self.backward_paths)) + ")"
