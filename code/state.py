from forward_state import ForwardState
from backward_state import BackwardState
from backward_path import BackwardPath
from utils import starts_with, inverse, inverse_path

class State(object):

    def __init__(self, forward_state, backward_state):
        self.forward_state = forward_state
        self.backward_state = backward_state

    def __eq__(self, other):
        return self.forward_state == other.forward_state and \
            self.backward_state == other.backward_state

    def __hash__(self):
        return hash(self.forward_state) + hash(self.backward_state)

    def is_end(self):
        if not self.is_valid():
            return False
        ends_f, ends_b = self.backward_state.number_ends()
        counter_f, counter_b = self.backward_state.length()
        return self.forward_state.is_end() and ends_b == 1 and counter_b == 1\
            and counter_f == 0

    def is_valid(self):
        if not self.backward_state.is_valid():
            return False
        ends_f, ends_b = self.backward_state.number_ends()
        counter_f, counter_b = self.backward_state.length()
        if self.forward_state.is_end() and ends_b >= 1 and (counter_f > 0 or\
                                                            counter_b > 1):
            return False
        if self.forward_state.is_end() and ends_f > 0:
            return False
        return True

    def get_next_states(self, functions, max_size):
        if not self.is_valid():
            return []
        if not self.forward_state.is_end() and \
                self.backward_state.total_length() >= max_size:
            return [self.remove_one_relation()]
        function_list = []
        cp = self.get_constraint_path()
        for f in functions:
            f_str = " ".join(f.to_list())
            f_str_inv = " ".join(f.get_inverse_function())
            if starts_with(f_str, cp) or \
                    starts_with(f_str_inv, cp):
                function_list.append(f)
        res = []
        ends_f, ends_b = self.backward_state.number_ends()
        if self.forward_state.is_end():
            for f in functions:
                f_str = " ".join(f.to_list())
                if starts_with(f_str, cp):
                    next_state = State(ForwardState(f), self.backward_state)
                    cp_n = next_state.get_constraint_path()
                    res.append(next_state)
            res += self.add_kink_fb(functions, cp)
        elif ends_f > 0 or ends_b > 0:
            res_temp = self.backward_state.add_one(function_list, cp)
            for bs in res_temp:
                res.append(State(self.forward_state, bs))
            res += self.add_kink_fb(functions, cp)
        else:
            if self.backward_state.total_length() == 0:
                res += self.add_kink_fb(functions, cp)
            res.append(self)
        complete_res = []
        for state in res:
            complete_res += generate_all_states(state,
                                                functions,
                                                max_size)
        complete_res = filter(lambda x: x.backward_state.total_length() != 0,
                             complete_res)
        complete_res = map(lambda x: x.remove_one_relation(), complete_res)
        return list(set(complete_res))

    def add_kink_fb(self, functions, cp):
        res = []
        for f in functions:
            f_l = f.to_list()
            for i in range(1, len(f_l)):
                f_left = f_l[:i]
                f_right = f_l[i:]
                if self.forward_state.is_end():
                    corrects = []
                    for bp in self.backward_state.backward_paths:
                        if len(f_left) == len(f_right) + bp.length() and \
                                bp.direction == "b":
                            corrects.append(bp)
                    if len(corrects) != 1:
                        continue
                    forward_path = " ".join(f_left)
                    backward_path = corrects[0].backward_path + " " + \
                        " ".join(f_right[::-1])
                else:
                    # find ending backward
                    found = []
                    # One path at least needs to start
                    if len(self.backward_state.backward_paths) != 0:
                        for bp in self.backward_state.backward_paths:
                            if bp.is_end() and bp.direction == "b":
                                found.append(bp)
                        if len(found) != 1 or (len(f_right) != len(f_left) +\
                                               self.forward_state.length()):
                            continue
                    elif (len(f_right) != len(f_left) +\
                                               self.forward_state.length()):
                        continue

                    forward_path = self.forward_state.forward_path + " " +\
                        " ".join(f_left)
                    backward_path = " ".join(f_right[::-1])
                backward_inv = inverse_path(backward_path)
                if starts_with(forward_path, cp) and\
                        starts_with(backward_inv, cp) and \
                        starts_with(forward_path, backward_inv):
                    clean_bp = []
                    for bp in self.backward_state.backward_paths:
                        if not bp.is_end():
                            if corrects and bp != corrects[0]:
                                clean_bp.append(bp)
                    res.append(State(ForwardState(forward_path),
                                     BackwardState(clean_bp +
                                                   [BackwardPath(backward_path,
                                                                "b")])))
        return res

    def get_constraint_path(self):
        cp_f = self.forward_state.get_constraint_path()
        cp_b = self.backward_state.get_constraint_path()
        if cp_f.count(" ") > cp_b.count(" "):
            return cp_f
        elif cp_f.count(" ") < cp_b.count(" "):
            return cp_b
        elif len(cp_f) >= len(cp_b):
            return cp_f
        else:
            return cp_b

    def remove_one_relation(self):
        return State(self.forward_state.remove_one_relation(),
                     self.backward_state.remove_one_relation())

    def __repr__(self):
        return "State(" + str(self.forward_state) + ", " + \
            str(self.backward_state) + ")"


def generate_all_states(state, functions, max_size):
    res = []
    cp = state.get_constraint_path()
    bs = state.backward_state

    def generate_all_states_rec(bs, functions):
        if bs.total_length() >= max_size or len(functions) == 0:
            res.append(bs)
            return
        cp_temp = bs.get_constraint_path()
        function = functions[0]
        f_l = function.to_list()
        f_str = " ".join(f_l)
        if starts_with(f_str, cp) and\
                starts_with(f_str, cp_temp):
            generate_all_states_rec(BackwardState(
                    bs.backward_paths[:] + [BackwardPath(f_str, "f")]),
                functions[1:])
        f_str = " ".join(function.get_inverse_function())
        if starts_with(f_str, cp) and \
                starts_with(f_str, cp_temp):
            generate_all_states_rec(BackwardState(
                    bs.backward_paths[:] + [BackwardPath(function, "b")]),
                functions[1:])
        # kinks
        for i in range(1, len(f_l)):
            f_left = f_l[:i]
            f_right = f_l[i:]
            f_str_right = " ".join(f_right)
            f_left_inv = " ".join(map(lambda x: inverse(x, "-"),
                                       f_left[::-1]))
            if starts_with(f_str_right, cp) and \
                    starts_with(f_str_right, cp_temp) and \
                    starts_with(f_left_inv, cp) and \
                    starts_with(f_left_inv, cp_temp) and \
                    starts_with(f_str_right, f_left_inv):
                generate_all_states_rec(BackwardState(
                        bs.backward_paths[:] +
                    [BackwardPath(f_left[::-1], "b"),
                     BackwardPath(f_right, "f")]),
                    functions)

        generate_all_states_rec(bs, functions[1:])

    generate_all_states_rec(bs, functions)
    final_res = []
    for bs in res:
        final_res.append(State(state.forward_state, bs))
    return final_res
