class CFGRule(object):

    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        res = str(self.head) + " -> "
        res += ", ".join(map(str, self.body))
        return res

    def __eq__(self, other):
        return isinstance(other, CFGRule) and\
            self.head == other.head and\
            self.body == other.body

    def __hash__(self):
        return hash(self.head) + hash(tuple(self.body))

    def init_generating(self):
        self.remaining = len(self.body)

    def remove_one_remaining(self):
        self.remaining -= 1

    def is_generating(self):
        return self.remaining == 0
