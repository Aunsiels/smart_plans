from function import Function
from typing import Union


class Node(object):

    def __init__(self, value: Union[Function, str]) -> None:
        """__init__
        Initialize a node
        :param value: The value of the node
        :type value: Function or str
        :return: Nothing
        :rtype: None
        """
        self.value = value

    def is_str(self) -> bool:
        """is_str
        Is the node a string ?
        :return: Whether the node is a string
        :rtype: bool
        """
        return type(self.value) == str

    def is_function(self) -> bool:
        """is_function
        Is the node a function ?
        :return: Whether the node is a function
        :rtype: bool
        """
        return type(self.value) == Function

    def get_str(self) -> str:
        """get_str
        Gets the string representation of the node
        :return: The string representation of the node
        :rtype: str
        """
        return str(self.value)

    def get_function(self) -> Function:
        """get_function
        Gets the function representation of the node
        :return: The function representation of the node
        :rtype: Function
        """
        return Function(self.value)

    def __repr__(self) -> str:
        """__repr__
        Gets the string representation
        :return: The string representation
        :rtype: str
        """
        return self.get_str()
