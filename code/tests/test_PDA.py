import unittest
from PDA import PDA
from CFG import CFG
from regex_tree import RegexTree
from node import Node
from pda_state import PDAState
from pda_transition_function import PDATransitionFunction

class TestPDA(unittest.TestCase):

    def test_creation(self):
        states = []
        input_symbols = []
        stack_alphabet = []
        transition_function = []
        start_state = []
        start_symbol = None
        final_states = []
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        self.assertIsInstance(pda, PDA)

    def test_accepts_final(self):
        states = [PDAState("q0"), PDAState("q1"), PDAState("q2")]
        input_symbols = [0, 1]
        stack_alphabet = [0, 1, "end"]
        transition_function = []
        transition_function.append(
            PDATransitionFunction(states[0], 0, "end",
                                  states[0], [0, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, "end",
                                  states[0], [1, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 0,
                                  states[0], [0, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 1,
                                  states[0], [0, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 1,
                                  states[0], [1, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 0,
                                  states[0], [1, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "end",
                                  states[1], ["end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 0,
                                  states[1], [0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 1,
                                  states[1], [1]))
        transition_function.append(
            PDATransitionFunction(states[1], 0, 0,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], 1, 1,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "epsilon", "end",
                                  states[2], ["end"]))
        start_state = states[0]
        start_symbol = "end"
        final_states = [states[2]]
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        self.assertTrue(pda.accepts_by_final_state([0, 0, 1, 1, 0, 0]))
        self.assertTrue(pda.accepts_by_final_state([0, 1, 1, 0]))
        self.assertTrue(pda.accepts_by_final_state([1, 1]))
        self.assertTrue(pda.accepts_by_final_state([]))
        self.assertFalse(pda.accepts_by_final_state([0, 1, 0, 0]))
        self.assertFalse(pda.accepts_by_final_state([0, 0, 1, 0]))

    def test_accepts_empty_stack(self):
        states = [PDAState("q0"), PDAState("q1"), PDAState("q2")]
        input_symbols = [0, 1]
        stack_alphabet = [0, 1, "end"]
        transition_function = []
        transition_function.append(
            PDATransitionFunction(states[0], 0, "end",
                                  states[0], [0, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, "end",
                                  states[0], [1, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 0,
                                  states[0], [0, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 1,
                                  states[0], [0, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 1,
                                  states[0], [1, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 0,
                                  states[0], [1, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "end",
                                  states[1], ["end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 0,
                                  states[1], [0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 1,
                                  states[1], [1]))
        transition_function.append(
            PDATransitionFunction(states[1], 0, 0,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], 1, 1,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "epsilon", "end",
                                  states[2], []))
        start_state = states[0]
        start_symbol = "end"
        final_states = [states[2]]
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        self.assertTrue(pda.accepts_by_empty_stack([0, 0, 1, 1, 0, 0], 100))
        self.assertTrue(pda.accepts_by_empty_stack([0, 1, 1, 0], 100))
        self.assertTrue(pda.accepts_by_empty_stack([1, 1], 100))
        self.assertTrue(pda.accepts_by_empty_stack([], 100))
        self.assertFalse(pda.accepts_by_empty_stack([0, 1, 0, 0], 1000))
        self.assertFalse(pda.accepts_by_empty_stack([0, 0, 1, 0], 1000))

    def test_to_CFG(self):
        states = [PDAState("q0"), PDAState("q1"), PDAState("q2")]
        input_symbols = [0, 1]
        stack_alphabet = [0, 1, "end"]
        transition_function = []
        transition_function.append(
            PDATransitionFunction(states[0], 0, "end",
                                  states[0], [0, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, "end",
                                  states[0], [1, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 0,
                                  states[0], [0, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 1,
                                  states[0], [0, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 1,
                                  states[0], [1, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 0,
                                  states[0], [1, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "end",
                                  states[1], ["end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 0,
                                  states[1], [0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 1,
                                  states[1], [1]))
        transition_function.append(
            PDATransitionFunction(states[1], 0, 0,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], 1, 1,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "epsilon", "end",
                                  states[2], []))
        start_state = states[0]
        start_symbol = "end"
        final_states = [states[2]]
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        cfg = pda.to_CFG()
        self.assertIsInstance(cfg, CFG)
        self.assertFalse(cfg.is_empty())
        it = iter(cfg)
        for _ in range(50):
            temp = next(it)
            self.assertGreaterEqual(len(temp), 0)
            self.assertEqual(temp, temp[::-1])

    def test_end_to_stack(self):
        states = [PDAState("q0"), PDAState("q1"), PDAState("q2")]
        input_symbols = [0, 1]
        stack_alphabet = [0, 1, "end"]
        transition_function = []
        transition_function.append(
            PDATransitionFunction(states[0], 0, "end",
                                  states[0], [0, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, "end",
                                  states[0], [1, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 0,
                                  states[0], [0, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 1,
                                  states[0], [0, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 1,
                                  states[0], [1, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 0,
                                  states[0], [1, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "end",
                                  states[1], ["end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 0,
                                  states[1], [0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 1,
                                  states[1], [1]))
        transition_function.append(
            PDATransitionFunction(states[1], 0, 0,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], 1, 1,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "epsilon", "end",
                                  states[2], ["end"]))
        start_state = states[0]
        start_symbol = "end"
        final_states = [states[2]]
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        pda = pda.from_final_state_to_empty_stack()
        self.assertTrue(pda.accepts_by_empty_stack([0, 0, 1, 1, 0, 0]))
        self.assertTrue(pda.accepts_by_empty_stack([0, 1, 1, 0]))
        self.assertTrue(pda.accepts_by_empty_stack([1, 1]))
        self.assertTrue(pda.accepts_by_empty_stack([]))
        self.assertFalse(pda.accepts_by_empty_stack([0, 1, 0, 0]))
        self.assertFalse(pda.accepts_by_empty_stack([0, 0, 1, 0]))

    def test_stack_to_end(self):
        states = [PDAState("q0"), PDAState("q1"), PDAState("q2")]
        input_symbols = [0, 1]
        stack_alphabet = [0, 1, "end"]
        transition_function = []
        transition_function.append(
            PDATransitionFunction(states[0], 0, "end",
                                  states[0], [0, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, "end",
                                  states[0], [1, "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 0,
                                  states[0], [0, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], 0, 1,
                                  states[0], [0, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 1,
                                  states[0], [1, 1]))
        transition_function.append(
            PDATransitionFunction(states[0], 1, 0,
                                  states[0], [1, 0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "end",
                                  states[1], ["end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 0,
                                  states[1], [0]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", 1,
                                  states[1], [1]))
        transition_function.append(
            PDATransitionFunction(states[1], 0, 0,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], 1, 1,
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "epsilon", "end",
                                  states[2], []))
        start_state = states[0]
        start_symbol = "end"
        final_states = [states[2]]
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        pda = pda.from_empty_stack_to_final_state()
        self.assertIsInstance(pda, PDA)
        self.assertTrue(pda.accepts_by_final_state([0, 0, 1, 1, 0, 0], 100))
        self.assertTrue(pda.accepts_by_final_state([0, 1, 1, 0], 100))
        self.assertTrue(pda.accepts_by_final_state([1, 1], 100))
        self.assertTrue(pda.accepts_by_final_state([], 100))
        self.assertFalse(pda.accepts_by_final_state([0, 1, 0, 0], 1000))
        self.assertFalse(pda.accepts_by_final_state([0, 0, 1, 0], 1000))

    def test_intersect(self):
        regex = RegexTree(Node("1"))
        fsm = regex.to_fsm()
        fsm.close()
        states = [PDAState("q0"), PDAState("q1"), PDAState("q2")]
        input_symbols = ["0", "1"]
        stack_alphabet = ["0", "1", "end"]
        transition_function = []
        transition_function.append(
            PDATransitionFunction(states[0], "0", "end",
                                  states[0], ["0", "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "1", "end",
                                  states[0], ["1", "end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "0", "0",
                                  states[0], ["0", "0"]))
        transition_function.append(
            PDATransitionFunction(states[0], "0", "1",
                                  states[0], ["0", "1"]))
        transition_function.append(
            PDATransitionFunction(states[0], "1", "1",
                                  states[0], ["1", "1"]))
        transition_function.append(
            PDATransitionFunction(states[0], "1", "0",
                                  states[0], ["1", "0"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "end",
                                  states[1], ["end"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "0",
                                  states[1], ["0"]))
        transition_function.append(
            PDATransitionFunction(states[0], "epsilon", "1",
                                  states[1], ["1"]))
        transition_function.append(
            PDATransitionFunction(states[1], "0", "0",
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "1", "1",
                                  states[1], []))
        transition_function.append(
            PDATransitionFunction(states[1], "epsilon", "end",
                                  states[2], []))
        start_state = states[0]
        start_symbol = "end"
        final_states = [states[2]]
        pda = PDA(states, input_symbols, stack_alphabet, transition_function,
                  start_state, start_symbol, final_states)
        pda = pda.from_empty_stack_to_final_state()
        pda = pda.intersect(fsm)
        self.assertIsInstance(pda, PDA)
        self.assertFalse(pda.accepts_by_final_state(["0", "0", "1",
                                                     "1", "0", "0"], 1000))
        self.assertFalse(pda.accepts_by_final_state(["0", "1", "1", "0"], 1000))
        self.assertTrue(pda.accepts_by_final_state(["1", "1"], 10000))
        self.assertFalse(pda.accepts_by_final_state([], 1000))
        self.assertFalse(pda.accepts_by_final_state(["0", "1", "0", "0"], 1000))
        self.assertFalse(pda.accepts_by_final_state(["0", "0", "1", "0"], 1000))
