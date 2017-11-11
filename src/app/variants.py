# see more: https://en.wikipedia.org/wiki/List_of_chess_variants
import itertools
from copy import copy
from math import inf as infinity
from typing import Sequence, Type, TYPE_CHECKING, Tuple, Set

from app.board import StandardBoard
from app.move import StandardMove
from app.pieces import King, Pawn, Knight, Bishop, Rook, Queen
from app.position import StandardPosition
from app.sides import White, Black
from interface.variant import Variant

if TYPE_CHECKING:
    from interface.piece import Piece
    from interface.side import Side


class Normal(Variant):
    def __init__(self):
        self.__board = StandardBoard()
        self.init_board_state()

    @property
    def board(self) -> StandardBoard:
        return self.__board

    @property
    def sides(self) -> Sequence[Type['Side']]:
        return White, Black

    @property
    def pieces(self) -> Set[Type['Piece']]:
        return {King, Queen, Rook, Bishop, Knight, Pawn}

    def init_board_state(self):
        self.board.put_piece(piece=Rook(White), position=StandardPosition((0, 0)))
        self.board.put_piece(piece=Rook(White), position=StandardPosition((7, 0)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((1, 0)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((6, 0)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((2, 0)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((5, 0)))
        self.board.put_piece(piece=Queen(White), position=StandardPosition((3, 0)))
        self.board.put_piece(piece=King(White), position=StandardPosition((4, 0)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(White), position=StandardPosition((i, 1)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(Black), position=StandardPosition((i, 6)))

        self.board.put_piece(piece=Rook(Black), position=StandardPosition((0, 7)))
        self.board.put_piece(piece=Rook(Black), position=StandardPosition((7, 7)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((1, 7)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((6, 7)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((2, 7)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((5, 7)))
        self.board.put_piece(piece=Queen(Black), position=StandardPosition((3, 7)))
        self.board.put_piece(piece=King(Black), position=StandardPosition((4, 7)))

        return self.board.get_fen()

    def assert_move(self, move: 'StandardMove') -> bool:
        source, destination = move.source, move.destination
        piece = self.board.get_piece(source)
        if not piece:
            return False
        if destination not in self.standard_moves(source).union(self.attacked_fields(source)):
            return False
        test_board = copy(self.board)
        test_piece = test_board.remove_piece(source)
        test_board.put_piece(test_piece, destination)
        for pos, p in test_board.pieces.items():
            if p == King(piece.side) and pos in self.attacked_fields_by_sides(
                set(self.sides).difference({piece.side})
            ):
                return False

        return True

    def standard_moves(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        # TODO: REFACTOR
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise ValueError('Any piece on %s' % position)

        new_positions = set()
        for m_desc in piece.movement.move:
            for vector in self.__transform_vector(m_desc.vector, m_desc.any_direction, piece.side):
                if m_desc.distance is infinity:
                    loop = itertools.count(1)
                else:
                    loop = range(1, m_desc.distance + 1)

                for distance in loop:
                    new_position = StandardPosition(
                        (position[0] + int(vector[0] * distance),
                         position[1] + int(vector[1] * distance))
                    )
                    if not board.validate_position(new_position):
                        break

                    new_piece = board.get_piece(new_position)
                    if new_piece is not None:
                        break
                    new_positions.add(new_position)

        return new_positions

    def standard_captures(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise ValueError('Any piece on %s' % position)

        attacked_fields = self.attacked_fields(position, board)
        return {
            new_position for new_position, new_piece in board.pieces.items()
            if new_piece.side != piece.side and new_position in attacked_fields
        }

    def attacked_fields(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        # TODO: REFACTOR
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise ValueError('Any piece on %s' % position)

        new_positions = set()
        for c_desc in piece.movement.capture:
            for vector in self.__transform_vector(c_desc.vector, c_desc.any_direction, piece.side):
                if c_desc.distance is infinity:
                    loop = itertools.count(1)
                else:
                    loop = range(1, c_desc.distance + 1)

                for distance in loop:
                    new_position = StandardPosition(
                        (position[0] + int(vector[0] * distance),
                         position[1] + int(vector[1] * distance))
                    )
                    if not board.validate_position(new_position):
                        break

                    new_piece = board.get_piece(new_position)
                    if not new_piece:
                        new_positions.add(new_position)
                    elif new_piece and new_piece.side != piece.side:
                        new_positions.add(new_position)
                        break
                    elif new_piece and new_piece.side == piece.side:
                        break

        return new_positions

    def attacked_fields_by_sides(self, side: Set[Type['Side']], board: 'StandardBoard' = None) -> Set['StandardPosition']:
        if not board:
            board = self.board
        return {pos for position, piece in self.board.pieces.items()
                for pos in self.attacked_fields(position, board)
                if piece.side == side}

    @staticmethod
    def __transform_vector(vector: Tuple[int, int], all_directions: bool, side) -> Set[Tuple[int, int]]:
        # TODO: standard interface for resolving all vector combinations and for transforming not-all-directions vector
        # TODO: eg. a pawn, for Whites move forward means incrementing rank value, for Black - decrementing
        if all_directions:
            return {
                (vector[0], vector[1]),
                (vector[1], vector[0]),
                (vector[1], vector[0] * -1),
                (vector[0], vector[1] * -1),
                (vector[0] * -1, vector[1] * -1),
                (vector[1] * -1, vector[0] * -1),
                (vector[1] * -1, vector[0]),
                (vector[0] * -1, vector[1]),
            }

        if side == Black:
            return {(vector[0] * -1, vector[1] * -1)}
        else:
            return {vector}

# class Chess960(Variant):
#     pass
#
#
# class Crazyhouse(Variant):
#     pass
#
#
# class KingOfTheHill(Variant):
#     pass
#
#
# class ThreeCheck(Variant):
#     pass
#
#
# class Horde(Variant):
#     pass
#
#
# class PreChess(Variant):
#     """Could be interesting to implement"""
#     pass
#
#
# class UpsideDown(Variant):
#     pass
#
#
# class Double(Variant):
#     """Could be interesting to implement as well"""
#     pass
#
#
# class Antichess(Variant):
#     """Just because LiChess supports it"""
#     pass
#
#
# class RacingKings(Variant):
#     """Like above"""
#     pass