import os
import pygame


class Board:
    def __init__(self, SQUARE_SIZE):
        self.board_square = []
        self.pieces = []
        self.turn = 1
        self.flag = 0
        self.square_size = SQUARE_SIZE
        self.who_move = None

    def create(self):
        self.flag = 1

        def get_notation(row, col):
            return f"[{col}; {row}]"

        def get_square_color(row, col):
            return 'white' if (row + col) % 2 == 0 else 'black'

        # Create the board squares and pieces (assuming you have a Piece class)
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
                row_squares.append(square)
            self.board_square.append(row_squares)

    def get_board_square(self):
        # print(self.board_square)
        return self.board_square

    def update(self):
        pass

    def next_move(self):
        print(f'Текущий ход: {self.turn}')
        self.turn += 1
        pass

    def add_piece(self, piece):
        self.pieces.append(piece)


class Square:
    on_fire_dict = {0: 'white', 1: 'black', 2: 'black and white', 3: None}

    def __init__(self, notation, color, end_line, coordinates, piece=None, SQUARE_SIZE=100):
        self.notation = notation  # [0; 0]
        self.coordinates = coordinates  # [700; 800] левый верхний угол клетки
        self.size = SQUARE_SIZE
        self.centre = [x + y for x, y in zip(self.coordinates, [50, 50])]  # [750; 750]
        self.color = color
        self.end_line = end_line
        self.on_fire = self.on_fire_dict[3]
        self.piece = piece

    def get_notation(self):
        print(self.notation)

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

    def move(self):
        pass

    def taken(self):
        pass

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
        if event.button == 1 and self.img_rect.collidepoint(event.pos):
            self.is_dragging = True
            self.start_drag_x, self.start_drag_y = event.pos[0] - self.img_rect.x, event.pos[1] - self.img_rect.y

    def handle_mouse_up(self, event):
        # Обработка события отпускания кнопки мыши
        self.is_dragging = False
        # if self.current_square:
        #     self.img_rect.center = self.current_square.centre

    def handle_mouse_drag(self, event):
        # Обработка события перетаскивания фигуры
        if self.is_dragging:
            self.img_rect.x = event.pos[0] - self.start_drag_x
            self.img_rect.y = event.pos[1] - self.start_drag_y


class Pawn(Piece):
    def __init__(self, color, current_board: Board, current_square: Square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'pawn.png'
        self.img_rect = None
        self.is_dragging = False


class King(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'king.png'
        self.img_rect = None
        self.is_dragging = False


class Rook(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'rook.png'
        self.img_rect = None
        self.is_dragging = False


class Bishop(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'bishop.png'
        self.img_rect = None
        self.is_dragging = False


class Knight(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'knight.png'
        self.img_rect = None
        self.is_dragging = False


class Q(Piece):
    def __init__(self, color, current_board, current_square):
        super().__init__(color, current_board, current_square)
        self.piece_name = 'q.png'
        self.img_rect = None
        self.is_dragging = False
