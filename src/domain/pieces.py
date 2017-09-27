from string import ascii_lowercase
from typing import Union, Tuple, List, Optional, Iterator


class Side:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def __str__(self):
        return self.__name


White = Side("White")
Black = Side("Black")


class Piece:
    """
    I don't know how to force overwrite these parameters when this class is used as Base instance.
    """
    name = 'Piece'
    char = 'p'
    points = 1

    def __init__(self, side: Side):
        self.__side = side

    @property
    def side(self) -> Side:
        return self.__side

    def __repr__(self):
        return '%s %s' % (self.__side, self.name)

    def __str__(self):
        return self.char.upper() if self.__side == White else self.char.lower()


class Position:
    """
    tuple with two board coordinates is too simple of course
    """

    def __init__(self, pos: Union[str, Tuple[int], List[int]]):
        if isinstance(pos, tuple) or isinstance(pos, list):
            if len(pos) != 2:
                raise ValueError('Position should be given as tuple/list with only two ints')
            self.__pos = (pos[0], pos[1])
        elif isinstance(pos, str):
            if len(pos) != 2:
                raise ValueError('Position should be given as two letter coordinates (file, rank)')
            self.__pos = (ascii_lowercase.index(pos[0]), int(pos[1]) - 1)

    @property
    def pos(self) -> Tuple[int, int]:
        return self.__pos

    def __pos_to_str(self) -> str:
        # y = str(self.__pos[1] + 1)

        # output_chars = 1
        # while (len(a)) ** output_chars <= x:
        #     output_chars += 1
        # print('chars:', output_chars)
        # lel = []
        # for i in range(output_chars):
        #     val = (x // len(a) ** i) % (len(a))
        #     if i == output_chars:
        #         val -= 1
        #     lel.append('%2d' % val)
        #
        # print('out:', ':'.join(lel))

        return NotImplemented

    def __repr__(self):
        return 'Position: %s' % self

    def __str__(self):
        return '%s' % self.__pos_to_str()

    def __iter__(self) -> Iterator[int]:
        for coordinate in self.__pos:
            yield coordinate


class Move:
    """
    Two Position aggregator with optional pawn promotion information
    """

    def __init__(self, a: Position, b: Position, promotion: Optional[Piece]):
        self.__a = a
        self.__b = b
        self.__promotion = promotion

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def promotion(self):
        return self.__promotion

    def __repr__(self):
        if self.__promotion:
            return 'Move: %s to %s with promotion to %s' % (self.__a, self.__b, self.__promotion.name)
        else:
            return 'Move: %s to %s' % (self.__a, self.__b)

    def __str__(self):
        if self.__promotion:
            return '%s%s%s' % (self.__a, self.__b, self.__promotion.char)
        else:
            return '%s%s' % (self.__a, self.__b)
