import string


class Piece:
    SYMBOLS = {'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔'}

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.symbol = self.SYMBOLS[name] if color == 'W' else self.SYMBOLS[name].lower()

    def is_valid_move(self, start, end, board):
        return False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')

    def is_valid_move(self, start, end, board):
        direction = -1 if self.color == 'W' else 1
        start_row, start_col = start
        end_row, end_col = end

        # Пешка может двигаться вперёд на одну клетку, если там пусто
        if start_col == end_col and end_row == start_row + direction and board[end_row][end_col] is None:
            return True

        # Пешка может двигаться на две клетки вперёд, если стоит на начальной позиции
        if start_col == end_col and start_row == (
        6 if self.color == 'W' else 1) and end_row == start_row + 2 * direction and board[end_row][end_col] is None and \
                board[start_row + direction][end_col] is None:
            return True

        # Пешка может бить по диагонали
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color

        return False


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R')

    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        if start_row != end_row and start_col != end_col:
            return False

        # Проверка на блокировку фигурами
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False
        elif start_col == end_col:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False

        return True


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N')

    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1 or \
            abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B')

    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        # Проверка на блокировку
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step

        while row != end_row and col != end_col:
            if board[row][col] is not None:
                return False
            row += row_step
            col += col_step

        return True


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q')

    def is_valid_move(self, start, end, board):
        # Ферзь может двигаться как ладья и как слон
        return Rook(self.color).is_valid_move(start, end, board) or \
            Bishop(self.color).is_valid_move(start, end, board)


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')

    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        # Король может двигаться на одну клетку в любом направлении
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1


class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(8):
            self.grid[1][i] = Pawn('B')
            self.grid[6][i] = Pawn('W')

        for i, piece in enumerate(piece_order):
            self.grid[0][i] = piece('B')
            self.grid[7][i] = piece('W')

    def display(self, move_count):
        print(f"Ход: {move_count}")
        print("   " + " ".join(string.ascii_lowercase[:8]))
        print("  +-----------------+")
        for i in range(8):
            row_display = f"{8 - i} | "
            for j in range(8):
                piece = self.grid[i][j]
                row_display += (piece.symbol if piece else '.') + ' '
            print(row_display + f"| {8 - i}")
        print("  +-----------------+")
        print("   " + " ".join(string.ascii_lowercase[:8]))

    def move_piece(self, start, end):
        piece = self.grid[start[0]][start[1]]
        if piece and piece.is_valid_move(start, end, self.grid):
            self.grid[end[0]][end[1]] = piece
            self.grid[start[0]][start[1]] = None
            return True
        return False


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
            self.board.display(self.move_count)
            move = input(f"Ход {'белых' if self.current_turn == 'W' else 'чёрных'} (например, e2-e4): ")
            move = move.replace("-", "")  # Поддержка формата e2-e4
            start, end = self.parse_input(move)
            if start and end and self.board.move_piece(start, end):
                self.move_count += 1
                self.current_turn = 'B' if self.current_turn == 'W' else 'W'
            else:
                print("Неверный ход, попробуйте снова.")


if __name__ == "__main__":
    game = Game()
    game.play()


