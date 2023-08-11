import os
import pygame


def search_coordinates_on_board(coordinates, nested_list):
    x, y = coordinates
    for item in nested_list:
        if isinstance(item, list):
            result = search_coordinates_on_board(coordinates, item)
            if result is not None:
                return result
        elif isinstance(item, Square):
            if x in item.inside_pixels[0] and y in item.inside_pixels[1]:
                return item
    return None


class Board:
    on_fire_dict = {0: 'white', 1: 'black', 2: 'black and white', 3: None}

    def __init__(self, SQUARE_SIZE):
        self.board_square = []
        self.pieces = []
        self.turn = 1
        self.flag = 0
        self.square_size = SQUARE_SIZE
        self.who_move = None
        self.target = None

    def create(self):
        self.flag = 1

        def get_notation(row, col):
            return f"[{col}; {row}]"

        def get_square_color(row, col):
            return 'white' if (row + col) % 2 == 0 else 'black'

        for row in range(8):
            row_squares = []
            for col in range(8):
                notation = get_notation(row, col)
                color = get_square_color(row, col)
                end_line = row == 0 or row == 7
                coordinates = [col * self.square_size, row * self.square_size]
                square = Square(notation, color, end_line, coordinates)
                piece = None
                if row == 6 or row == 1:
                    if row == 6:
                        piece = Pawn('white', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    else:
                        piece = Pawn('black', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                elif row == 7:
                    if col == 4:
                        piece = King('white', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 0 or col == 7:
                        piece = Rook('white', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 2 or col == 5:
                        piece = Bishop('white', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 1 or col == 6:
                        piece = Knight('white', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 3:
                        piece = Q('white', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                elif row == 0:
                    if col == 1 or col == 6:
                        piece = Knight('black', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 3:
                        piece = Q('black', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 2 or col == 5:
                        piece = Bishop('black', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 0 or col == 7:
                        piece = Rook('black', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                    elif col == 4:
                        piece = King('black', self, square)
                        piece.set_img()
                        piece.img_rect.center = square.centre
                else:
                    piece = None
                square.set_piece(piece)
                # print(square.coordinates)
                row_squares.append(square)
            self.board_square.append(row_squares)

    def get_board_square(self):
        return self.board_square

    def update(self):
        pass

    def next_move(self):
        print(f'Текущий ход: {self.turn}')
        self.turn += 1
        pass

    def add_piece(self, piece):
        self.pieces.append(piece)

    def set_target(self, new_target):
        self.target = new_target

    def update_fire_status(self):
        data = self.board_square
        all_square = [element for sublist in data for element in sublist]
        # TODO Доделать

    def take_check(self):
        data = self.board_square
        all_square = [element for sublist in data for element in sublist]
        for i_square in all_square:
            if len(i_square.piece) > 1:
                i_square.piece.pop(0)


class Square:
    on_fire_dict = {0: 'white', 1: 'black', 2: 'black and white', 3: None}

    def __init__(self, notation, color, end_line, coordinates, piece=None, SQUARE_SIZE=100):
        self.notation = list(map(int, notation.replace('[', '').replace(']', '').replace(' ', '').split(';')))  # [0; 0]
        self.coordinates = coordinates  # [700; 800] левый верхний угол клетки
        self.size = SQUARE_SIZE
        self.centre = [x + y for x, y in zip(self.coordinates, [50, 50])]  # [750; 750]
        self.color = color
        self.end_line = end_line
        self.on_fire = self.on_fire_dict[3]
        self.piece = piece
        self.inside_pixels = [[x for x in range(self.coordinates[0], self.coordinates[0]+96)],
                              [y for y in range(self.coordinates[1], self.coordinates[1]+96)]]

    def get_notation(self):
        print(self.notation)
        return self.notation

    def set_piece(self, new_piece):
        self.piece = new_piece


class Piece:
    def __init__(self, color, current_board: Board, current_square: Square):
        self.piece_name = None
        self.current_board = current_board
        self.color = color
        self.current_square = current_square
        self.coordinates = self.current_square.coordinates
        self.position = self.current_square.notation
        self.img = None
        self.is_alive = True
        self.has_moved = False
        self.possible_moves = []
        self.value = 0
        self.current_board.add_piece(self)
        self.img_rect = None
        self.is_dragging = False
        self.def_status = False

    def move(self):
        pass

    def taken(self):
        pass

    def die(self):
        self.current_board.pieces.remove(self)
        self.img = None
        self.img_rect = None
        self.color = None
        self.is_alive = False
        self.current_board = None
        self.current_square = None
        self.coordinates = None
        self.position = None
        self.def_status = False

    def set_img(self):
        if self.color == "white":
            path_components = ['Piece_img', 'defolt', 'white', self.piece_name]
            test_image_path = os.path.abspath(os.path.join(*path_components))
            test_image = pygame.image.load(test_image_path)
            self.img = test_image
            self.img_rect = test_image.get_rect()
            image_x = self.current_square.centre[0]
            image_y = self.current_square.centre[1]
        else:
            path_components = ['Piece_img', 'defolt', 'black', self.piece_name]
            test_image_path = os.path.abspath(os.path.join(*path_components))
            test_image = pygame.image.load(test_image_path)
            self.img = test_image
            self.img_rect = test_image.get_rect()
            image_x = self.current_square.centre[0]
            image_y = self.current_square.centre[1]

    def handle_mouse_down(self, event):
        # Обработка события нажатия кнопки мыши
        # TODO Добавить проверку на то чей ход
        if event.button == 1 and self.img_rect.collidepoint(event.pos):
            self.is_dragging = True
            self.start_drag_x, self.start_drag_y = event.pos[0] - self.img_rect.x, event.pos[1] - self.img_rect.y
            self.current_board.set_target(self)

    def handle_mouse_up(self, event):
        # Обработка события отпускания кнопки мыши

        old_square = self.current_square
        self.is_dragging = False

        try:
            self.update_possible_moves()
            result = search_coordinates_on_board(coordinates=self.point_to_check,
                                            nested_list=self.current_board.board_square)

            if result and result in self.possible_moves and self.current_board.target == self:
                if result.piece != self and result.piece is not None:
                    result.piece.die()
                self.current_square.set_piece(None)
                self.current_square = result
                self.img_rect.center = self.current_square.centre
                self.has_moved = True
                self.position = self.current_square.notation
                result.set_piece(self)
                self.update_possible_moves()
                # TODO добавить переключение хода
            else:
                # self.possible_moves = []
                self.update_possible_moves()
                self.current_square = old_square
                old_square.set_piece(self)
                self.img_rect.center = old_square.centre
                self.position = old_square.notation
        except:
            pass

    def handle_mouse_drag(self, event):
        # Обработка события перетаскивания фигуры
        if self.is_dragging:
            self.img_rect.x = event.pos[0] - self.start_drag_x
            self.img_rect.y = event.pos[1] - self.start_drag_y
            self.point_to_check = [self.img_rect.x, self.img_rect.y]

    def update_possible_moves(self):
        data = self.current_board.board_square
        self.possible_moves = [element for sublist in data for element in sublist]


class Pawn(Piece):
    def __init__(self, color, current_board: Board, current_square: Square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'pawn.png'

    def update_possible_moves(self):
        # TODO Добавить превращение в ферзя
        # TODO Добавить взятие на проходе
        data = self.current_board.board_square
        all_square = [element for sublist in data for element in sublist]
        self.possible_moves = []

        x, y = self.position

        if self.color == "white":
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        # Добавляем ход вперёд-влево
        new_x, new_y = x - 1, y + direction
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            target_square = None
            for square in all_square:
                if square.notation == [new_x, new_y]:
                    if square.piece is not None:
                        if square.piece.color != self.color:
                            target_square = square
                            self.possible_moves.append(target_square)
                            break

            if target_square is not None and target_square.piece is None:
                self.possible_moves.append(target_square)

        # Добавляем ход вперёд-вправо
        new_x, new_y = x + 1, y + direction
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            target_square = None
            for square in all_square:
                if square.notation == [new_x, new_y]:
                    if square.piece is not None:
                        if square.piece.color != self.color:
                            target_square = square
                            self.possible_moves.append(target_square)
                            break

            if target_square is not None and target_square.piece is None:
                self.possible_moves.append(target_square)

        for move_distance in range(1, 3 if not self.has_moved else 2):
            new_x, new_y = x, y + direction * move_distance
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target_square = None
                for square in all_square:
                    if square.notation == [new_x, new_y]:
                        target_square = square
                        break

                path_clear = True
                for i in range(1, move_distance):
                    check_x, check_y = x, y + direction * i
                    for square in all_square:
                        if square.notation == [check_x, check_y] and square.piece is not None:
                            path_clear = False
                            break

                if target_square is not None and target_square.piece is None and path_clear:
                    self.possible_moves.append(target_square)


class King(Piece):
    castle_dict = {0: 'left', 1: "right"}

    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'king.png'
        self.castle_status = None

    def handle_mouse_up(self, event):
        # Обработка события отпускания кнопки мыши

        old_square = self.current_square
        self.is_dragging = False

        try:
            self.update_possible_moves()
            result = search_coordinates_on_board(coordinates=self.point_to_check,
                                            nested_list=self.current_board.board_square)

            if result and result in self.possible_moves and self.current_board.target == self:
                if result.piece != self and result.piece is not None:
                    result.piece.die()
                self.current_square.set_piece(None)
                if self.color == 'white':
                    if result == self.current_board.board_square[7][6] and self.has_moved is False:
                        rook = self.current_board.board_square[7][7].piece
                        rook.current_square = self.current_board.board_square[7][5]
                        rook.img_rect.center = rook.current_square.centre
                        rook.has_moved = True
                        rook.position = rook.current_square.notation
                        self.current_board.board_square[7][5].set_piece(rook)
                        self.current_board.board_square[7][7].set_piece(None)
                        rook.update_possible_moves()
                    if result == self.current_board.board_square[7][2] and self.has_moved is False:
                        rook = self.current_board.board_square[7][0].piece
                        rook.current_square = self.current_board.board_square[7][3]
                        rook.img_rect.center = rook.current_square.centre
                        rook.has_moved = True
                        rook.position = rook.current_square.notation
                        self.current_board.board_square[7][3].set_piece(rook)
                        self.current_board.board_square[7][0].set_piece(None)
                        rook.update_possible_moves()
                else:
                    if result == self.current_board.board_square[0][6] and self.has_moved is False:
                        rook = self.current_board.board_square[0][7].piece
                        rook.current_square = self.current_board.board_square[0][5]
                        rook.img_rect.center = rook.current_square.centre
                        rook.has_moved = True
                        rook.position = rook.current_square.notation
                        self.current_board.board_square[0][5].set_piece(rook)
                        self.current_board.board_square[0][7].set_piece(None)
                        rook.update_possible_moves()
                    if result == self.current_board.board_square[0][2] and self.has_moved is False:
                        rook = self.current_board.board_square[0][0].piece
                        rook.current_square = self.current_board.board_square[0][3]
                        rook.img_rect.center = rook.current_square.centre
                        rook.has_moved = True
                        rook.position = rook.current_square.notation
                        self.current_board.board_square[0][3].set_piece(rook)
                        self.current_board.board_square[0][0].set_piece(None)
                        rook.update_possible_moves()
                self.current_square = result
                self.img_rect.center = self.current_square.centre
                self.has_moved = True
                self.position = self.current_square.notation
                result.set_piece(self)
                self.update_possible_moves()
                # TODO добавить переключение хода
            else:
                # self.possible_moves = []
                self.update_possible_moves()
                self.current_square = old_square
                old_square.set_piece(self)
                self.img_rect.center = old_square.centre
                self.position = old_square.notation
        except:
            pass

    def update_possible_moves(self):
        data = self.current_board.board_square
        all_square = [element for sublist in data for element in sublist]
        self.possible_moves = []

        x, y = self.position

        possible_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        # TODO Добавить проверку на шах и на битое поле на пути рокировки
        try:
            if self.color == 'white':
                # print(self.current_board.board_square[7][0].piece)
                # print(self.current_board.board_square[7][7].piece)
                # Рокировка вправо
                if not self.has_moved and not self.current_board.board_square[7][7].piece.has_moved:
                    if all(self.current_board.board_square[7][i].piece is None for i in range(5, 7)):
                        self.possible_moves.append(self.current_board.board_square[7][6])
                # Рокировка влево
                if not self.has_moved and not self.current_board.board_square[7][0].piece.has_moved:
                    if all(self.current_board.board_square[7][i].piece is None for i in range(1, 4)):
                        self.possible_moves.append(self.current_board.board_square[7][2])

            else:
                if not self.has_moved and not self.current_board.board_square[0][7].piece.has_moved:
                    if all(self.current_board.board_square[0][i].piece is None for i in range(5, 7)):
                        self.possible_moves.append(self.current_board.board_square[0][6])
                if not self.has_moved and not self.current_board.board_square[0][0].piece.has_moved:
                    if all(self.current_board.board_square[0][i].piece is None for i in range(1, 4)):
                        self.possible_moves.append(self.current_board.board_square[0][2])
        except:
            pass
            # Рокировка невозможна
        # TODO Проверить чтобы король не мог наступить на клетку под боем
        for dx, dy in possible_offsets:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                for square in all_square:

                    if square.notation == [new_x, new_y] and square.piece is None:
                        self.possible_moves.append(square)
                        break
                    elif square.notation == [new_x, new_y] and square.piece is not None:
                        if square.piece.color != self.color and square.piece.def_status is False:
                            self.possible_moves.append(square)
                            break


class Rook(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'rook.png'

    def update_possible_moves(self):
        data = self.current_board.board_square
        all_square = [element for sublist in data for element in sublist]
        self.possible_moves = []

        x, y = self.position

        possible_offsets = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
        ]

        for dx, dy in possible_offsets:
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                target_square = None
                for square in all_square:
                    if square.notation == [new_x, new_y]:
                        target_square = square
                        break

                if target_square is not None:
                    if target_square.piece is None:
                        self.possible_moves.append(target_square)
                    else:
                        if target_square.piece.color != self.color:
                            self.possible_moves.append(target_square)
                        break

                    if target_square.piece is not None:
                        break

                new_x, new_y = new_x + dx, new_y + dy


class Bishop(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'bishop.png'

    def update_possible_moves(self):
        data = self.current_board.board_square
        all_square = [element for sublist in data for element in sublist]
        self.possible_moves = []

        x, y = self.position

        possible_offsets = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1),
        ]
        for dx, dy in possible_offsets:
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                target_square = None
                for square in all_square:
                    if square.notation == [new_x, new_y]:
                        target_square = square
                        break

                if target_square is not None:
                    if target_square.piece is None:
                        self.possible_moves.append(target_square)
                    else:
                        if target_square.piece.color != self.color:
                            self.possible_moves.append(target_square)
                        break

                new_x += dx
                new_y += dy


class Knight(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'knight.png'

    def update_possible_moves(self):
        data = self.current_board.board_square
        all_square = [element for sublist in data for element in sublist]
        self.possible_moves = []

        x, y = self.position

        possible_offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1),
        ]

        for dx, dy in possible_offsets:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                for square in all_square:
                    if square.notation == [new_x, new_y] and square.piece is None:
                        self.possible_moves.append(square)
                        break
                    elif square.notation == [new_x, new_y] and square.piece is not None:
                        if square.piece.color != self.color:
                            self.possible_moves.append(square)
                            break


class Q(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'q.png'

    def update_possible_moves(self):
        data = self.current_board.board_square
        all_square = [element for sublist in data for element in sublist]
        self.possible_moves = []

        x, y = self.position

        possible_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]

        for dx, dy in possible_offsets:
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                target_square = None
                for square in all_square:
                    if square.notation == [new_x, new_y]:
                        target_square = square
                        break

                if target_square is not None:
                    if target_square.piece is None:
                        self.possible_moves.append(target_square)
                    else:
                        if target_square.piece.color != self.color:
                            self.possible_moves.append(target_square)
                        break

                new_x += dx
                new_y += dy

