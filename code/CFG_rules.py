class CFGRules(object):

    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        res = head + " -> "
        res += ", ".join(map(str, self.body))
