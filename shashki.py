import string


class Piece:
    SYMBOLS = {'C': '⛀', 'D': '⛁'}  # C - обычная шашка, D - дамка

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.symbol = self.SYMBOLS[name] if color == 'W' else self.SYMBOLS[name].lower()

    def is_valid_move(self, start, end, board):
        return False

    def get_possible_moves(self, start, board):
        return []


class Checker(Piece):
    def __init__(self, color):
        super().__init__(color, 'C')

    def is_valid_move(self, start, end, board):
        direction = -1 if self.color == 'W' else 1
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_col - end_col) == 1 and end_row == start_row + direction and board[end_row][end_col] is None:
            return True

        if abs(start_col - end_col) == 2 and abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            if board[mid_row][mid_col] and board[mid_row][mid_col].color != self.color:
                return True

        return False

    def get_possible_moves(self, start, board):
        moves = []
        for drow, dcol in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            end = (start[0] + drow, start[1] + dcol)
            if 0 <= end[0] < 8 and 0 <= end[1] < 8 and self.is_valid_move(start, end, board):
                moves.append(end)
        return moves


class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Checker('B')

        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Checker('W')

    def display(self, move_count):
        print(f"Ход: {move_count}")
        print("  a b c d e f g h")
        print("  ----------------")
        for row in range(8):
            print(8 - row, end="| ")
            for col in range(8):
                if self.grid[row][col]:
                    print(self.grid[row][col].symbol, end=' ')
                else:
                    print('.', end=' ')
            print(f"| {8 - row}")
        print("  ----------------")
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        piece = self.grid[start[0]][start[1]]
        if piece and piece.is_valid_move(start, end, self.grid):
            mid_row = (start[0] + end[0]) // 2
            mid_col = (start[1] + end[1]) // 2
            if abs(start[0] - end[0]) == 2:
                self.grid[mid_row][mid_col] = None  # Убираем побитую шашку
            self.grid[end[0]][end[1]] = piece
            self.grid[start[0]][start[1]] = None
            if (piece.color == 'W' and end[0] == 0) or (piece.color == 'B' and end[0] == 7):
                self.grid[end[0]][end[1]] = Piece(piece.color, 'D')  # Превращение в дамку
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
            move = input(f"Ход {'белых' if self.current_turn == 'W' else 'чёрных'} (например, e3-d4): ")
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
            if piece and piece.is_valid_move(start, end, self.grid):
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