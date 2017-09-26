from reduced_rule import ReducedRule


class ConsommationRule(ReducedRule):
    """ConsommationRule
        Contains a representation of a consumption rule, i.e. a rule of the
        form:
            C[ r sigma] -> B[sigma]
    """

    def isConsommation(self):
        """isConsommation Indicates we have a consumption function"""
        return True

    def getF(self):
        """getF Gets the symbole which is consumed"""
        return self.f

    def getRight(self):
        """getRight Gets the symbole on the right of the rule"""
        return self.right

    def getLeft(self):
        """getLeft Gets the symbole on the left of the rule"""
        return self.left

    def __init__(self, f, left, right):
        """__init_ Initialises a rule of the form:
            C[ f sigma] -> B[sigma]
        :param f: The consummed symbole
        :param left: The non terminal on the left (here C)
        :param right: The non terminal on the right (here B)
        """
        self.f = f
        self.right = right
        self.left = left

    def getTerminals(self):
        """getTerminals Gets the terminals used in the rule"""
        return {self.left, self.right}

    def __repr__(self):
        """__repr__ Gives the string representation of the rule, ignoring the
        sigmas"""
        return self.left + " [ " + self.f + " ] -> " + self.right
