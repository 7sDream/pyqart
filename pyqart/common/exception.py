# Added at  : 2016.07.30
# Author    : 7sDream
# Usage     : Exceptions raised by common functions or classes,


class InvalidTypeException(Exception):
    def __init__(self, excepted, given, index, function):
        self._excepted = excepted
        self._given = given
        self._function = function
        self._index = index + 1

    def __str__(self):
        string = "Invalid type at No.{number} argument of {function}, " \
                 "except {excepted}, {given} given."
        return string.format(
            index=self._index,
            function=self._function,
            excepted=self._excepted,
            given=self._given,
        )

    __repr__ = __str__
