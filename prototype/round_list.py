class RoundList(object):
    """RoundList A list which only keeps the lasts elements inserted"""

    def __init__(self, size):
        """__init__
        Initialize the list
        :param size: The number of elements to remember
        """
        if type(size) == int:
            self.l_in = [None for _ in range(size)]
            self.idx = size - 1
            self.size = size
        elif type(size) == list:
            self.l_in = size[:]
            self.size = len(size)
            self.idx = self.size - 1

    def get(self):
        """get
        Get the list which represents this class
        :return: The list of the last elements inserted
        :rtype: list
        """
        return list(filter(lambda x: x is not None,
                           self.l_in[self.idx:] + self.l_in[:self.idx]))

    def push(self, v):
        """push
        Adds an element to the list
        :param v: The element to insert
        """
        self.l_in[self.idx] = v
        self.idx = (self.idx + 1) % self.size

    def __eq__(self, other):
        """__eq__
        Tests the egality between two rounded lists
        :param other: The list to which we should compare
        """
        if type(other) == list:
            return self.get() == other
        else:
            return self.get() == other.get()

    def __repr__(self):
        """__repr__
        Gets the representation of the RoundedList
        :return: A representation of a RoundedList
        :rtype: str
        """
        return str(self.get())

    def copy(self):
        """copy
        Copy the current class
        """
        temp = RoundList(self.size)
        temp.l_in = self.l_in[:]
        temp.idx = self.idx
        return temp
