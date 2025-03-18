import string


class Piece:
    SYMBOLS = {'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'U': '∆', 'D': '⊱', 'S': '⊞'}

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.symbol = self.SYMBOLS[name] if color == 'W' else self.SYMBOLS[name].lower()

    def is_valid_move(self, start, end, board):
        return False

    def get_possible_moves(self, start, board):
        return []

    def get_possible_moves_unicorn(self, start, board):
        return []

    def get_possible_moves_dragon(self, start, board):
        return []

    def get_possible_moves_sage(self, start, board):
        return []


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')

    def is_valid_move(self, start, end, board):
        direction = -1 if self.color == 'W' else 1
        start_row, start_col = start
        end_row, end_col = end

        # Одно поле вперед
        if start_col == end_col and end_row == start_row + direction and board[end_row][end_col] is None:
            return True

        # Два поля вперед
        if start_col == end_col and start_row == (6 if self.color == 'W' else 1) and end_row == start_row + 2 * direction and \
                board[end_row][end_col] is None and board[start_row + direction][end_col] is None:
            return True

        # Ход по диагонали для взятия
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color

        return False

    def get_possible_moves(self, start, board):
        moves = []
        direction = -1 if self.color == 'W' else 1
        start_row, start_col = start

        # Одно поле вперед
        if 0 <= start_row + direction < 8 and board[start_row + direction][start_col] is None:
            moves.append((start_row + direction, start_col))

        # Два поля вперед (если на начальной позиции)
        if (self.color == 'W' and start_row == 6) or (self.color == 'B' and start_row == 1):
            if 0 <= start_row + 2 * direction < 8 and board[start_row + 2 * direction][start_col] is None:
                moves.append((start_row + 2 * direction, start_col))

        # Взятие по диагонали
        for col_offset in [-1, 1]:
            new_col = start_col + col_offset
            if 0 <= start_row + direction < 8 and 0 <= new_col < 8:
                if board[start_row + direction][new_col] and board[start_row + direction][new_col].color != self.color:
                    moves.append((start_row + direction, new_col))

        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R')

    def is_valid_move(self, start, end, board):
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # вертикально и горизонтально
        for direction in directions:
            row, col = start
            while True:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    if board[row][col] is None:
                        moves.append((row, col))
                    elif board[row][col].color != self.color:
                        moves.append((row, col))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N')

    def is_valid_move(self, start, end, board):
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        moves = []
        row, col = start
        directions = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B')

    def is_valid_move(self, start, end, board):
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # по диагоналям
        for direction in directions:
            row, col = start
            while True:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    if board[row][col] is None:
                        moves.append((row, col))
                    elif board[row][col].color != self.color:
                        moves.append((row, col))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q')

    def is_valid_move(self, start, end, board):
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # горизонтальные и вертикальные
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # диагонали
        ]
        for direction in directions:
            row, col = start
            while True:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    if board[row][col] is None:
                        moves.append((row, col))
                    elif board[row][col].color != self.color:
                        moves.append((row, col))
                        break
                    else:
                        break
                else:
                    break
        return moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')

    def is_valid_move(self, start, end, board):
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        moves = []
        row, col = start
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # горизонтальные и вертикальные
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # диагонали
        ]
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves


# Новые фигуры
class Unicorn(Piece):
    def __init__(self, color):
        super().__init__(color, 'U')

    def is_valid_move_sage(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == abs(start_col - end_col) and abs(
            start_row - end_row) == 3  # Двигается по диагонали на 3 клетки

    def get_possible_moves_unicorn(self, start, board):
        moves = []
        row, col = start
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # по диагоналям
        for direction in directions:
            new_row, new_col = row + 3 * direction[0], col + 3 * direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Dragon(Piece):
    def __init__(self, color):
        super().__init__(color, 'D')

    def is_valid_move_sage(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == abs(
            start_col - end_col) or start_row == end_row or start_col == end_col  # Двигается как ферзь, но только на 3 клетки максимум

    def get_possible_moves_dragon(self, start, board):
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # вертикально и горизонтально
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # по диагоналям
        ]
        for direction in directions:
            for distance in range(1, 4):  # ходим на максимум 3 клетки
                row, col = start
                row += direction[0] * distance
                col += direction[1] * distance
                if 0 <= row < 8 and 0 <= col < 8:
                    if board[row][col] is None:
                        moves.append((row, col))
                    elif board[row][col].color != self.color:
                        moves.append((row, col))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Sage(Piece):
    def __init__(self, color):
        super().__init__(color, 'S')

    def is_valid_move_sage(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == 1 and abs(
            start_col - end_col) == 1  # Двигается как король, но только по диагонали

    def get_possible_moves_sage(self, start, board):
        moves = []
        row, col = start
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # только по диагоналям
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        new_pieces = [Unicorn, Dragon, Sage]

        for i in range(8):
            self.grid[1][i] = Pawn('B')
            self.grid[6][i] = Pawn('W')

        for i, piece in enumerate(piece_order):
            self.grid[0][i] = piece('B')
            self.grid[7][i] = piece('W')

        # Добавляем новые фигуры в центр доски
        for i, piece in enumerate(new_pieces):
            self.grid[3][i + 2] = piece('B')
            self.grid[4][i + 2] = piece('W')

    def display(self, move_count, threats=None, check=False):
        print(f"Ход: {move_count}")
        if check:
            print("Шах королю!")
        print("   a b c d e f g h")
        print("  ----------------")
        for row in range(8):
            print(8 - row, end="| ")
            for col in range(8):
                if threats and (row, col) in threats:
                    print('!', end=' ')
                elif self.grid[row][col]:
                    print(self.grid[row][col].symbol, end=' ')
                else:
                    print('.', end=' ')
            print(f"| {8 - row}")
        print("  ----------------")
        print("   a b c d e f g h")

    def display_with_hints(self, hints):
        print("Подсказка: возможные ходы отмечены *")
        for row in range(8):
            for col in range(8):
                if (row, col) in hints:
                    print('*', end=' ')
                elif self.grid[row][col]:
                    print(self.grid[row][col].symbol, end=' ')
                else:
                    print('.', end=' ')
            print()

    def move_piece(self, start, end):
        piece = self.grid[start[0]][start[1]]
        if piece:
            # Получаем все возможные ходы для этой фигуры
            possible_moves = []

            # Проверяем, для какой фигуры нужно вызвать соответствующий метод
            if isinstance(piece, Unicorn):
                possible_moves = piece.get_possible_moves_unicorn(start, self.grid)
            elif isinstance(piece, Dragon):
                possible_moves = piece.get_possible_moves_dragon(start, self.grid)
            elif isinstance(piece, Sage):
                possible_moves = piece.get_possible_moves_sage(start, self.grid)
            else:
                possible_moves = piece.get_possible_moves(start, self.grid)

            # Проверяем, что конечная позиция допустима
            if end in possible_moves:
                self.grid[end[0]][end[1]] = piece
                self.grid[start[0]][start[1]] = None
                return True
        return False

    def get_threatened_pieces(self, color):
        threats = set()
        king_position = None

        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color and piece.name == 'K':
                    king_position = (row, col)
                if piece and piece.color != color:
                    for move in piece.get_possible_moves((row, col), self.grid):
                        if self.grid[move[0]][move[1]] and self.grid[move[0]][move[1]].color == color:
                            threats.add(move)

        check = king_position in threats if king_position else False
        return threats, check



class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'W'
        self.move_count = 0

    def parse_input(self, move):
        if len(move) != 4 or move[0] not in string.ascii_lowercase[:8] or move[2] not in string.ascii_lowercase[:8]:
            return None, None
        try:
            start = (8 - int(move[1]), string.ascii_lowercase.index(move[0]))
            end = (8 - int(move[3]), string.ascii_lowercase.index(move[2]))
            return start, end
        except ValueError:
            return None, None

    def play(self):
        while True:
            threats, check = self.board.get_threatened_pieces(self.current_turn)
            self.board.display(self.move_count, threats, check)
            print("Введите 'hint <координата>' (например, 'hint e2'), чтобы получить подсказку по возможным ходам.")
            move = input(f"Ход {'белых' if self.current_turn == 'W' else 'чёрных'} (например, e2-e4): ")
            print("Введите 'hint <координата>' (например, 'hint e2'), чтобы получить подсказку по возможным ходам.")
            if move.startswith("hint "):
                pos = move.split()[1]
                if len(pos) == 2 and pos[0] in string.ascii_lowercase[:8]:
                    start = (8 - int(pos[1]), string.ascii_lowercase.index(pos[0]))
                    piece = self.board.grid[start[0]][start[1]]
                    if piece and piece.color == self.current_turn:
                        self.board.display_with_hints(piece.get_possible_moves(start, self.board.grid))
                    else:
                        print("Выбранная фигура не принадлежит вам или отсутствует.")
                else:
                    print("Неверный формат запроса подсказки.")
                continue
            move = move.replace("-", "")
            start, end = self.parse_input(move)
            if start and end and self.board.move_piece(start, end):
                self.move_count += 1
                self.current_turn = 'B' if self.current_turn == 'W' else 'W'
            else:
                print("Неверный ход, попробуйте снова.")


if __name__ == "__main__":
    game = Game()
    game.play()