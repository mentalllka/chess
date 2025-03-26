import string


class Piece:
    """Базовый класс для шахматных фигур (включая новые: Единорог, Дракон, Мудрец).

    Атрибуты:
        SYMBOLS (dict): Словарь Unicode-символов фигур (стандартные + новые).
        color (str): Цвет фигуры ('W' - белые, 'B' - чёрные).
        name (str): Название фигуры (ключ из SYMBOLS).
        symbol (str): Символ фигуры с учётом цвета.
    """
    SYMBOLS = {'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'U': '∆', 'D': '⊱', 'S': '⊞'}

    def __init__(self, color, name):
        """Инициализирует фигуру с цветом и типом.

        Args:
            color (str): 'W' (белые) или 'B' (чёрные).
            name (str): Тип фигуры (например, 'P' для пешки).
        """
        self.color = color
        self.name = name
        self.symbol = self.SYMBOLS[name] if color == 'W' else self.SYMBOLS[name].lower()

    def is_valid_move(self, start, end, board):
        """Проверяет допустимость хода (базовая реализация всегда False).

        Args:
            start (tuple): Начальная позиция (row, col).
            end (tuple): Конечная позиция (row, col).
            board (list): Текущее состояние доски.

        Returns:
            bool: False (переопределяется в дочерних классах).
        """
        return False

    def get_possible_moves(self, start, board):
        """Возвращает возможные ходы (пустой список по умолчанию).

        Args:
            start (tuple): Текущая позиция фигуры.
            Board (list): Доска.

        Returns:
            list: Пустой список (переопределяется в дочерних классах).
        """
        return []

    def get_possible_moves_unicorn(self, start, board):
        """Возможные ходы для Единорога (пустой список по умолчанию)."""
        return []

    def get_possible_moves_dragon(self, start, board):
        """Возможные ходы для Дракона (пустой список по умолчанию)."""
        return []

    def get_possible_moves_sage(self, start, board):
        """Возможные ходы для Мудреца (пустой список по умолчанию)."""
        return []


class Pawn(Piece):
    """Класс пешки. Наследует Piece."""

    def __init__(self, color):
        super().__init__(color, 'P')

    def is_valid_move(self, start, end, board):
        """Проверяет допустимость хода пешки.

        Пешка может:
        - Идти на 1 клетку вперёд.
        - Идти на 2 клетки с начальной позиции.
        - Бить по диагонали.

        Returns:
            bool: True, если ход допустим.
        """
        direction = -1 if self.color == 'W' else 1
        start_row, start_col = start
        end_row, end_col = end

        # Одно поле вперед
        if start_col == end_col and end_row == start_row + direction and board[end_row][end_col] is None:
            return True

        # Два поля вперед
        if start_col == end_col and start_row == (
        6 if self.color == 'W' else 1) and end_row == start_row + 2 * direction and \
                board[end_row][end_col] is None and board[start_row + direction][end_col] is None:
            return True

        # Ход по диагонали для взятия
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color

        return False

    def get_possible_moves(self, start, board):
        """Возвращает все возможные ходы пешки.

        Returns:
            list: Список кортежей (row, col) допустимых ходов.
        """
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
    """Класс ладьи. Наследует Piece."""

    def __init__(self, color):
        super().__init__(color, 'R')

    def is_valid_move(self, start, end, board):
        """Проверяет, есть ли end в возможных ходах ладьи."""
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        """Возвращает все возможные ходы ладьи (по горизонтали/вертикали)."""
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
    """Класс коня. Наследует Piece."""

    def __init__(self, color):
        super().__init__(color, 'N')

    def is_valid_move(self, start, end, board):
        """Проверяет ход коня (буквой 'Г')."""
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        """Возвращает все возможные ходы коня."""
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
    """Класс слона. Наследует Piece."""

    def __init__(self, color):
        super().__init__(color, 'B')

    def is_valid_move(self, start, end, board):
        """Проверяет диагональный ход слона."""
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        """Возвращает все возможные ходы слона."""
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
    """Класс ферзя. Наследует Piece."""

    def __init__(self, color):
        super().__init__(color, 'Q')

    def is_valid_move(self, start, end, board):
        """Проверяет ход ферзя (как ладья + слон)."""
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        """Возвращает все возможные ходы ферзя."""
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
    """Класс короля. Наследует Piece."""

    def __init__(self, color):
        super().__init__(color, 'K')

    def is_valid_move(self, start, end, board):
        """Проверяет ход короля (на 1 клетку в любом направлении)."""
        return end in self.get_possible_moves(start, board)

    def get_possible_moves(self, start, board):
        """Возвращает все возможные ходы короля."""
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
    """Класс Единорога. Наследует Piece. Ходит на 3 клетки по диагонали."""

    def __init__(self, color):
        super().__init__(color, 'U')

    def is_valid_move_sage(self, start, end, board):
        """Проверяет ход Единорога (строго на 3 клетки по диагонали)."""
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == abs(start_col - end_col) and abs(
            start_row - end_row) == 3

    def get_possible_moves_unicorn(self, start, board):
        """Возвращает возможные ходы Единорога."""
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
    """Класс Дракона. Наследует Piece. Ходит как ферзь, но максимум на 3 клетки."""

    def __init__(self, color):
        super().__init__(color, 'D')

    def is_valid_move_sage(self, start, end, board):
        """Проверяет ход Дракона (как ферзь, но до 3 клеток)."""
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == abs(
            start_col - end_col) or start_row == end_row or start_col == end_col

    def get_possible_moves_dragon(self, start, board):
        """Возвращает возможные ходы Дракона."""
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
    """Класс Мудреца. Наследует Piece. Ходит как король, но только по диагонали."""

    def __init__(self, color):
        super().__init__(color, 'S')

    def is_valid_move_sage(self, start, end, board):
        """Проверяет ход Мудреца (на 1 клетку по диагонали)."""
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1

    def get_possible_moves_sage(self, start, board):
        """Возвращает возможные ходы Мудреца."""
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
    """Класс шахматной доски (включая новые фигуры)."""

    def __init__(self):
        """Инициализирует доску и расставляет фигуры."""
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        """Расставляет фигуры в начальные позиции (стандартные + новые)."""
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
        """Отображает доску с подсветкой угроз и шаха.

        Args:
            move_count (int): Номер текущего хода.
            threats (set): Множество позиций под угрозой.
            check (bool): Флаг шаха.
        """
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
        """Отображает доску с подсказками (возможные ходы отмечены '*').

        Args:
            hints (list): Список возможных ходов.
        """
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
        """Перемещает фигуру, если ход допустим.

        Args:
            start (tuple): Начальная позиция.
            end (tuple): Конечная позиция.

        Returns:
            bool: Успешность перемещения.
        """
        piece = self.grid[start[0]][start[1]]
        if piece:
            possible_moves = []

            if isinstance(piece, Unicorn):
                possible_moves = piece.get_possible_moves_unicorn(start, self.grid)
            elif isinstance(piece, Dragon):
                possible_moves = piece.get_possible_moves_dragon(start, self.grid)
            elif isinstance(piece, Sage):
                possible_moves = piece.get_possible_moves_sage(start, self.grid)
            else:
                possible_moves = piece.get_possible_moves(start, self.grid)

            if end in possible_moves:
                self.grid[end[0]][end[1]] = piece
                self.grid[start[0]][start[1]] = None
                return True
        return False

    def get_threatened_pieces(self, color):
        """Возвращает позиции фигур под угрозой и флаг шаха.

        Args:
            color (str): Цвет анализируемых фигур.

        Returns:
            tuple: (threats, check), где:
                - threats: set позиций под угрозой,
                - check: bool (флаг шаха королю).
        """
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
    """Класс управления игровым процессом."""

    def __init__(self):
        """Инициализирует игру с доской и начальными настройками."""
        self.board = Board()
        self.current_turn = 'W'
        self.move_count = 0

    def parse_input(self, move):
        """Преобразует строку хода (например, 'e2e4') в координаты.

        Args:
            move (str): Строка хода.

        Returns:
            tuple: (start, end) или (None, None) при ошибке.
        """
        if len(move) != 4 or move[0] not in string.ascii_lowercase[:8] or move[2] not in string.ascii_lowercase[:8]:
            return None, None
        try:
            start = (8 - int(move[1]), string.ascii_lowercase.index(move[0])
                     end = (8 - int(move[3]), string.ascii_lowercase.index(move[2])
            return start, end
        except ValueError:
            return None, None

    def play(self):
        """Запускает игровой цикл с обработкой ходов и подсказок."""
        while True:
            threats, check = self.board.get_threatened_pieces(self.current_turn)
            self.board.display(self.move_count, threats, check)
            print("Введите 'hint <координата>' (например, 'hint e2'), чтобы получить подсказку по возможным ходам.")
            move = input(f"Ход {'белых' if self.current_turn == 'W' else 'чёрных'} (например, e2-e4): ")
            if move.startswith("hint "):
                pos = move.split()[1]
                if len(pos) == 2 and pos[0] in string.ascii_lowercase[:8]:
                    start = (8 - int(pos[1]), string.ascii_lowercase.index(pos[0])
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
