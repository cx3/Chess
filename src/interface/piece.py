from abc import ABCMeta, abstractmethod
from typing import Type, TYPE_CHECKING, Tuple, TypeVar, Sequence

if TYPE_CHECKING:
    from interface.side import Side

Vector = TypeVar[Tuple[int, int]]  # Determine movement vector
AnyDirection = TypeVar[bool]  # Determine if movement Vector cover all combinations in any direction
Distance = TypeVar[int]  # Determine maximum move/capture distance (iterations of Vector)
SelfCapture = TypeVar[bool]  # Determine if self-capture is allowed (any variant even supports it?)
CaptureBreak = TypeVar[bool]  # Determine if a capture breaks availability to move behind enemy piece


class Movement(metaclass=ABCMeta):
    """
    This object explains for game engine basics of available piece movements, eg. where can go and where can capture.
    Explanation doesn't relate to GameMode specific movements which depends on game state, eg en passant (last pawn 
    move), or castling (King or Rook was ever moved, is field between King's source and destination attacked)
    Movement is separated to two section - capture and move. It may determine different Piece mechanics, eg. for 
    a pawn - can move forward but capture only diagonal in the front. This interface should be flexible to determine
    any type of movement, even as the stupidest as human being can imagine (as long as not depend on the game state).
    If not, Use this interface to implement your stupid movement ability.
    """

    @property
    @abstractmethod
    def capture(self) -> Sequence[Tuple[Vector, AnyDirection, Distance, SelfCapture]]:
        pass

    @property
    @abstractmethod
    def move(self) -> Sequence[Tuple[Vector, AnyDirection, Distance, CaptureBreak]]:
        pass


class Piece(metaclass=ABCMeta):
    def __init__(self, side: Type['Side']):
        self.__side = side

    @property
    @abstractmethod
    def name(self) -> str:
        """return piece name starts with uppercase, eg. Pawn"""
        pass

    @property
    @abstractmethod
    def char(self) -> str:
        """return one lowercase letter representation of piece, eg. p"""
        pass

    @property
    @abstractmethod
    def points(self) -> int:
        """return int piece value representation, eg. 1"""
        pass

    @abstractmethod
    def movement(self) -> Type['Movement']:
        """return something that describe piece movement and is easy to use by game engine, any ideas?"""
        pass

    @property
    def side(self) -> Type['Side']:
        return self.__side

    def __repr__(self):
        return '<%s %s>' % (self.side, self.name)

    def __str__(self):
        return self.char.upper() if self.side.capitalize else self.char.lower()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return isinstance(other, type(self)) and other.side == self.side

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return not (isinstance(other, type(self)) and other.side == self.side)
        return True
