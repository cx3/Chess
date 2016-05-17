# -*- coding: utf-8 -*-
from string import ascii_letters, digits, ascii_lowercase
from copy import deepcopy as copy


class chess:
    def __init__(self):
        self.history = {}
        self.history_seq = 0
        self.board = [[None for x in range(8)] for i in range(8)]
        self.on_move = 'w'
        self.castle = 'KQkq'
        self.en_passant = None
        self.half_moves = 0
        self.moves = 1

    def _exec_move(self, pos_a, pos_b, promotion='q', debug=False, display=True):
        x1, y1 = self.coordinates_to_matrix(pos_a)
        x2, y2 = self.coordinates_to_matrix(pos_b)
        piece = self.board[y1][x1]

        valid_moves = []
        if debug is False:
            self._save_history(self.history_seq)

            valid_moves = self.legal_moves(pos_a)

        if valid_moves is None and debug is False:
            print('%s: Any piece here you stipid whore, fuck you!' % pos_a)
        elif piece.isupper() and self.on_move != 'w' and debug is False:
            print('Black on move you retarted motherfucker!, not white!')
        elif piece.islower() and self.on_move != 'b' and debug is False:
            print('White on move you retarted idiot!, not black!')
        elif pos_b not in valid_moves and debug is False:
            print('It is not a valid move!\n')
        else:
            self.board[y1][x1] = None
            self.board[y2][x2] = piece

            if debug is False:
                if piece == 'P' and y2 == 7:
                    self.board[y2][x2] = promotion.capitalize()

                if piece == 'p' and y2 == 0:
                    self.board[y2][x2] = promotion.casefold()

                if piece in 'pP' and pos_b == self.en_passant:
                    self.board[y1][x2] = None

                if piece in 'pP' and abs(y1 - y2) == 2:
                    self.en_passant = self.coordinates_to_human(x1, int((y1 + y2) / 2))
                else:
                    self.en_passant = None

                if piece in 'kK':
                    if self.castle is not None:
                        if piece.isupper():
                            self.castle = self.castle.replace('K', '')
                            self.castle = self.castle.replace('Q', '')
                        elif piece.islower():
                            self.castle = self.castle.replace('k', '')
                            self.castle = self.castle.replace('q', '')
                        if not self.castle:
                            self.castle = None

                    if piece == 'K':
                        if pos_a == 'e1' and pos_b == 'g1':
                            self.board[0][7] = None
                            self.board[0][5] = 'R'
                        elif pos_a == 'e1' and pos_b == 'c1':
                            self.board[0][0] = None
                            self.board[0][2] = 'R'
                    elif piece == 'k':
                        if pos_a == 'e8' and pos_b == 'g8':
                            self.board[7][7] = None
                            self.board[7][5] = 'r'
                        elif pos_a == 'e8' and pos_b == 'c8':
                            self.board[7][0] = None
                            self.board[7][2] = 'r'
                if piece in 'rR':
                    if self.castle is not None:
                        if piece.isupper():
                            if x1 == 7:
                                self.castle = self.castle.replace('K', '')
                            elif x1 == 0:
                                self.castle = self.castle.replace('Q', '')
                        elif piece.islower():
                            if x1 == 7:
                                self.castle = self.castle.replace('k', '')
                            elif x1 == 0:
                                self.castle = self.castle.replace('q', '')
                        if not self.castle:
                            self.castle = None

                #postmove operations
                if self.on_move == 'w':
                    self.on_move = 'b'
                else:
                    self.on_move = 'w'
                    self.moves += 1

                self.history_seq += 1
                self._save_history(self.history_seq)

                if display:
                    self.show_board()

                if self.am_i_mated():
                    print('checkmate!')
                elif self.am_i_stalemated():
                    print('stealmate!')
                elif self.am_i_checked():
                    print('check!')

    def _save_history(self, key):
        self.history[key] = (copy(self.board),
                             copy(self.on_move),
                             copy(self.castle),
                             copy(self.en_passant),
                             copy(self.half_moves),
                             copy(self.moves))

    def _clear_board(self):
        self.board = [[None for x in range(8)] for i in range(8)]

    def _avabile_moves(self, pos):
        a1, a2 = self.coordinates_to_matrix(pos)

        piece = self.board[a2][a1]
        if piece is None:
            raise IOError('No piece at %s' % pos)
        color = self.read_color(piece)

        moves = []

        # Pawns ###
        if piece.casefold() == 'p' and color == 'w':
            tmp1, tmp2 = a1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1, a2 + 2
            if tmp1 in range(8) and tmp2 in range(8):
                if a2 == 1 and self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            if self.en_passant and a2 == 4:
                tmp1, tmp2 = self.coordinates_to_matrix(self.en_passant)
                if (a1 + 1 == tmp1 or a1 - 1 == tmp1) and a2 + 1 == tmp2:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))

        elif piece.casefold() == 'p' and color == 'b':
            tmp1, tmp2 = a1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1, a2 - 2
            if tmp1 in range(8) and tmp2 in range(8):
                if a2 == 6 and self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            if self.en_passant and a2 == 3:
                tmp1, tmp2 = self.coordinates_to_matrix(self.en_passant)
                if (a1 + 1 == tmp1 or a1 - 1 == tmp1) and a2 - 1 == tmp2:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))

        # Rook ###
        elif piece.casefold() == 'r':
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

        # Knight ###
        elif piece.casefold() == 'n':
            tmp1, tmp2 = a1 + 2, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 + 2, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 + 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 + 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 - 2, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 - 2, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 - 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 - 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.coordinates_to_human(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.coordinates_to_human(tmp1, tmp2))

        # Bishop ###
        elif piece.casefold() == 'b':
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

        # Queen ###
        elif piece.casefold() == 'q':
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

        # King ###
        elif piece.casefold() == 'k':
            for i in range(1, 2):
                tmp1, tmp2 = a1 + i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 2):
                tmp1, tmp2 = a1 + i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 2):
                tmp1, tmp2 = a1 - i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 2):
                tmp1, tmp2 = a1 - i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

            for i in range(1, 2):
                tmp1, tmp2 = a1 + i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 2):
                tmp1, tmp2 = a1 - i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 2):
                tmp1, tmp2 = a1, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 2):
                tmp1, tmp2 = a1, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.coordinates_to_human(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

            if self.castle is not None and color == 'w':
                if 'K' in self.castle:
                    if self.board[0][5] is None and self.board[0][6] is None and self.board[0][7] == 'R':
                        moves.append('g1')
                if 'Q' in self.castle:
                    if self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None and self.board[0][0] == 'R':
                        moves.append('c1')
            elif self.castle is not None and color == 'b':
                if 'k' in self.castle:
                    if self.board[7][5] is None and self.board[7][6] is None and self.board[7][7] == 'r':
                        moves.append('g8')
                if 'q' in self.castle:
                    if self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None and self.board[7][0] == 'r':
                        moves.append('c8')

        return moves

    def _attacked_fields(self):
        """lista pól atakowanych przez przeciwnika, metoda do wadilacji posunięć"""

        validation = []
        if self.on_move == 'w':
            y = 0
            for row in self.board:
                x = 0
                for piece in row:
                    if piece is not None and piece in 'rnbqkp':
                        validation.extend(self._avabile_moves(self.coordinates_to_human(x, y)))
                    x += 1
                y += 1

        elif self.on_move == 'b':
            y = 0
            for row in self.board:
                x = 0
                for piece in row:
                    if piece is not None and piece in 'RNBQKP':
                        validation.extend(self._avabile_moves(self.coordinates_to_human(x, y)))
                    x += 1
                y += 1

        validation = list(set(validation))
        return validation

    def legal_moves(self, pos):
        moves = self._avabile_moves(pos)
        real_moves = []

        backup = copy(self.board)
        for move in moves:
            self._exec_move(pos, move, debug=True)
            if not self.am_i_checked():
                real_moves.append(move)
            self.board = copy(backup)

        x, y = self.coordinates_to_matrix(pos)
        if self.board[y][x] == 'K' and self.castle is not None and x == 4 and y == 0:
            if 'f1' not in real_moves and 'K' in self.castle:
                if 'g1' in real_moves:
                    real_moves.remove('g1')
            if 'd1' not in real_moves and 'Q' in self.castle:
                if 'c1' in real_moves:
                    real_moves.remove('c1')
        elif self.board[y][x] == 'k' and self.castle is not None and x == 4 and y == 7:
            if 'f8' not in real_moves and 'k' in self.castle:
                if 'g8' in real_moves:
                    real_moves.remove('g8')
            if 'd8' not in real_moves and 'q' in self.castle:
                if 'c8' in real_moves:
                    real_moves.remove('c8')

        return real_moves

    def new_game(self, type='standard'):
        if type == 'standard':
            self._clear_board()

            self.board[0][0], self.board[0][7] = 'R', 'R'
            self.board[0][1], self.board[0][6] = 'N', 'N'
            self.board[0][2], self.board[0][5] = 'B', 'B'
            self.board[0][3], self.board[0][4] = 'Q', 'K'

            for i in range(8):
                self.board[1][i] = 'P'

            for i in range(8):
                self.board[6][i] = 'p'

            self.board[7][0], self.board[7][7] = 'r', 'r'
            self.board[7][1], self.board[7][6] = 'n', 'n'
            self.board[7][2], self.board[7][5] = 'b', 'b'
            self.board[7][3], self.board[7][4] = 'q', 'k'

            self.on_move = 'w'
            self.castle = 'KQkq'
            self.en_passant = None
            self.half_moves = 0
            self.moves = 1

            self.history = {}
            self.history_seq = 0

        print('New Game!\n')

    def move(self, move, promotion='q', debug=False, display=True):
        if isinstance(move, str) and len(move) == 4:
            self._exec_move(move[:2], move[2:], promotion=promotion, debug=debug, display=display)

    def undo(self, moves=1):
        self.board = copy(self.history[self.history_seq - moves][0])
        self.on_move = copy(self.history[self.history_seq - moves][1])
        self.castle = copy(self.history[self.history_seq - moves][2])
        self.en_passant = copy(self.history[self.history_seq - moves][3])
        self.half_moves = copy(self.history[self.history_seq - moves][4])
        self.moves = copy(self.history[self.history_seq - moves][5])

        print('undo %s moves!' % moves)
        self.show_board()
        self.history_seq -= moves

    def redo(self, moves=1):
        self.board = copy(self.history[self.history_seq + moves][0])
        self.on_move = copy(self.history[self.history_seq + moves][1])
        self.castle = copy(self.history[self.history_seq + moves][2])
        self.en_passant = copy(self.history[self.history_seq + moves][3])
        self.half_moves = copy(self.history[self.history_seq + moves][4])
        self.moves = copy(self.history[self.history_seq + moves][5])

        print('redo %s moves!' % moves)
        self.show_board()
        self.history_seq += moves

    def show_board(self, compact=False, flipped=False):
        if not compact:
            if not flipped:
                for row in reversed(self.board):
                    print('+---+---+---+---+---+---+---+---+ ')
                    string = '| '
                    for piece in row:
                        if piece is not None:
                            string += piece
                        else:
                            string += ' '
                        string += ' | '
                    print(string)
                print('+---+---+---+---+---+---+---+---+ ')
                print()
            else:
                for row in self.board:
                    print('+---+---+---+---+---+---+---+---+ ')
                    string = '| '
                    for piece in reversed(row):
                        if piece is not None:
                            string += piece
                        else:
                            string += ' '
                        string += ' | '
                    print(string)
                print('+---+---+---+---+---+---+---+---+ ')
                print()
        else:
            if not flipped:
                for row in reversed(self.board):
                    string = ''
                    for piece in row:
                        if piece is not None:
                            string += piece
                        else:
                            string += '.'
                        string += ' '
                    print(string)
                print()
            else:
                for row in self.board:
                    string = ''
                    for piece in reversed(row):
                        if piece is not None:
                            string += piece
                        else:
                            string += '.'
                        string += ' '
                    print(string)
                print()

    def show_legal_moves(self, pos, compact=False):
        v1, v2 = self.coordinates_to_matrix(pos)
        if self.read_color(self.board[v2][v1]) != self.on_move:
            if self.on_move == 'w':
                print('Whine on move! You can verify only white pieces now.')
            elif self.on_move == 'b':
                print('Black on move! You can verify only black pieces now.')
        else:
            moves = self.legal_moves(pos)

            if moves is None:
                print('Any piece on %s field!' % pos)
            else:
                backup = copy(self.board)
                for move in moves:
                    x, y = self.coordinates_to_matrix(move)
                    self.board[y][x] = '+'

                if not compact:
                    self.show_board()
                else:
                    self.show_board(compact=True)
                self.board = backup

    def get_position(self):
        fenstring = ''
        empty_field = 0
        row_count = 0
        for row in reversed(self.board):
            for piece in row:
                if piece is not None:
                    if empty_field > 0:
                        fenstring += str(empty_field)
                        empty_field = 0
                    fenstring += piece
                else:
                    empty_field += 1
            if empty_field > 0:
                fenstring += str(empty_field)
                empty_field = 0
            if row_count < 7:
                fenstring += '/'
            row_count += 1

        fenstring += ' %s' % self.on_move

        if self.castle is not None:
            fenstring += ' %s' % self.castle
        else:
            fenstring += ' -'

        if self.en_passant is not None:
            fenstring += ' %s' % self.en_passant
        else:
            fenstring += ' -'

        fenstring += ' %s' % str(self.moves)
        fenstring += ' %s' % str(self.half_moves)

        return fenstring

    def set_position(self, fenstring, display=True):
        # Fen documentation http://www.thechessdrum.net/PGN_Reference.txt
        # @TODO validate: http://chess.stackexchange.com/questions/1482/how-to-know-when-a-fen-position-is-legal
        if not isinstance(fenstring, str):
            raise TypeError('fenstring must be a string!')

        fenstring = fenstring.replace(u'\u200b', '')
        fendata = fenstring.split(' ')
        fenboard = fendata[0].split('/')
        if len(fenboard) != 8:
            raise ValueError('Missing/too_much rows of pieces in fenstring!')

        dumped = [[None for x in range(8)] for i in range(8)]
        x, y = 0, 0
        for row in reversed(fenboard):
            if len(row) > 8:
                raise ValueError('too_much pieces in one row of fenstring!')
            for piece in row:
                if piece not in digits:
                    dumped[x][y] = piece
                else:
                    for i in range(int(piece) - 1):
                        dumped[x][y] = None
                        y += 1
                y += 1
            y = 0
            x += 1

        self.board = dumped
        if len(fendata) == 6:
            self.on_move = fendata[1]
            if fendata[2] != '-':
                self.castle = fendata[2]
            else:
                self.castle = None
            if fendata[3] != '-':
                self.en_passant = fendata[3]
            else:
                self.castle = None
            self.half_moves = int(fendata[5])
            self.moves = int(fendata[4])

        if display:
            self.show_board()

    def am_i_checked(self):

        king_pos = None
        if self.on_move == 'w':
            y = 0
            for row in self.board:
                x = 0
                for piece in row:
                    if piece == 'K':
                        king_pos = self.coordinates_to_human(x, y)
                    x += 1
                y += 1

        elif self.on_move == 'b':
            y = 0
            for row in self.board:
                x = 0
                for piece in row:
                    if piece == 'k':
                        king_pos = self.coordinates_to_human(x, y)
                    x += 1
                y += 1

        if king_pos is None:
            raise IOError('What the fuck, where is my king?!?!')
        if king_pos in self._attacked_fields():
            return True
        else:
            return False

    def am_i_stalemated(self):
        all_avabile_moves = []
        board = copy(self.board)

        if self.on_move == 'w':
            y = 0
            for row in board:
                x = 0
                for piece in row:
                    if piece is not None and piece.isupper():
                        all_avabile_moves.extend(self.legal_moves(self.coordinates_to_human(x, y)))
                    x += 1
                y += 1

        elif self.on_move == 'b':
            y = 0
            for row in board:
                x = 0
                for piece in row:
                    if piece is not None and piece.islower():
                        all_avabile_moves.extend(self.legal_moves(self.coordinates_to_human(x, y)))
                    x += 1
                y += 1

        all_avabile_moves = list(set(all_avabile_moves))

        if not all_avabile_moves and not self.am_i_checked():
            return True
        else:
            return False

    def am_i_mated(self):
        all_avabile_moves = []
        board = copy(self.board)

        if self.on_move == 'w':
            y = 0
            for row in board:
                x = 0
                for piece in row:
                    if piece is not None and piece.isupper():
                        all_avabile_moves.extend(self.legal_moves(self.coordinates_to_human(x, y)))
                    x += 1
                y += 1

        elif self.on_move == 'b':
            y = 0
            for row in board:
                x = 0
                for piece in row:
                    if piece is not None and piece.islower():
                        all_avabile_moves.extend(self.legal_moves(self.coordinates_to_human(x, y)))
                    x += 1
                y += 1

        all_avabile_moves = list(set(all_avabile_moves))

        if not all_avabile_moves and self.am_i_checked():
            return True
        else:
            return False

    @staticmethod
    def read_piece(piece_code):
        if piece_code in 'pP':
            return 'pawn'
        elif piece_code in 'rR':
            return 'rook'
        elif piece_code in 'nN':
            return 'knight'
        elif piece_code in 'bB':
            return 'bishop'
        elif piece_code in 'qQ':
            return 'queen'
        elif piece_code in 'kK':
            return 'king'

    @staticmethod
    def read_color(piece_code):
        if piece_code.isupper():
            return 'w'
        else:
            return 'b'

    @staticmethod
    def coordinates_to_matrix(string):
        if not isinstance(string, str):
            raise TypeError('you need to select position as text only!')
        if len(string) != 2:
            raise ValueError('wrong value! insert two chars for describe position on board. (eg. "a2")')
        if string[0] not in ascii_letters:
            raise ValueError('first letter need to be a char!')
        if string[1] not in digits:
            raise ValueError('second letter need to be a digit')

        a_in, b_in = string[0], string[1]

        a_out = ascii_lowercase.index(a_in.casefold())
        if not 0 <= a_out <= 7:
            raise ValueError('rank out of range!')

        b_out = int(b_in) - 1
        if not 0 <= b_out <= 7:
            raise ValueError('file out of range!')

        return a_out, b_out

    @staticmethod
    def coordinates_to_human(v1, v2):
        if not isinstance(v1, int) or not isinstance(v2, int):
            raise TypeError('values need to be an int!')
        if not 0 <= v1 <= 7:
            raise ValueError('file out of range!')
        if not 0 <= v2 <= 7:
            raise ValueError('rank out of range!')

        return ascii_lowercase[v1] + str(v2 + 1)


if __name__ == '__main__':
    game = chess()
    game.set_position('k7/2P/2K/8/8/8/8/8 w - - 0 1')
    game.move('c7c8')
    game.show_board()
    game.show_legal_moves('c8')
    game.show_legal_moves('a8', compact=True)
    game.show_board(compact=True, flipped=True)

