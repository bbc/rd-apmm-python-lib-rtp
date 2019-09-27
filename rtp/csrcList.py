from collections import UserList
from typing import Iterable
from .errors import LengthError


class CSRCList(UserList):
    '''
    A list of Contributing Source Identifiers (CSRCs). CSRCs are stored as
    integers. The list size and CSRC values are validated in accordance with
    RFC 3550. The list size is ``0-15``. CSRC values are ``0 <= x < 2**32``.
    '''

    def __init__(self, inList=[]):
        if len(inList) > 15:
            raise LengthError("CSRC list length too long. Max length is 15.")

        self.data = []

        for x in inList:
            self._csrcIsValid(x)
            self.data.append(x)

    def __add__(self, value: Iterable[int]) -> 'CSRCList':
        newList = CSRCList(self)
        newList += value
        return newList

    def __iadd__(self, value: Iterable[int]) -> 'CSRCList':
        self.extend(value)

        return self

    def extend(self, value: Iterable[int]) -> None:
        '''
        Extend the list by appending all the CSRCs from the iterable.
        '''

        if len(self.data) + len(list(value)) > 15:
            raise LengthError(
                "Extending would make CSRC list length too long. "
                "Max length is 15.")

        for x in value:
            self.append(x)

    def append(self, value: int) -> None:
        '''
        Add a CSRC to the end of the list.
        '''

        if len(self.data) == 15:
            raise LengthError(
                "Appending would make CSRC list length too long. "
                "Max length is 15.")

        self._csrcIsValid(value)

        self.data.append(value)

    def insert(self, i: int, x: int) -> None:
        '''
        Insert a CSRC at a given position. The first argument is the index of
        the element before which to insert, so ``a.insert(0, x)`` inserts at
        the front of the list, and ``a.insert(len(a), x)`` is equivalent to
        ``a.append(x)``.
        '''

        if (i < 0) or (i > len(self.data)) or (i >= 15):
            raise IndexError(
                "CSRC list index must be in range 0-15 and cannot leave gaps")
        self._csrcIsValid(x)

        self.data.insert(i, x)

    def _csrcIsValid(self, value: int) -> None:
        if type(value) != int:
            raise AttributeError(
                "CSRC values must be unsigned 32-bit integers")
        elif (value < 0) or (value >= 2**32):
            raise ValueError("CSRC values must be unsigned 32-bit integers")
