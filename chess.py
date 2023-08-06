from classes import *


BOARD_SIZE = 8
SQUARE_SIZE = 100


WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
TEXT_COLOR = (0, 0, 0)

letter_dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

pygame.init()


screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))  # +200 в y для места под
# настройки
pygame.display.set_caption("Chess board")


def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_chessboard():
    global letter_dict
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, WHITE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                if row % 7 == 0:
                    draw_text(screen, letter_dict[col], 25, x + 5, 780, BLACK)
                if col % 7 == 0:
                    draw_text(screen, str(col-row+1), 25, 700 + 85, y+5, BLACK)

            else:
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                if row % 7 == 0:
                    draw_text(screen, letter_dict[col], 25, x + 5, 780, WHITE)

                if col % 7 == 0:
                    draw_text(screen, str(col-row+1), 25, 700 + 85, y+5, WHITE)


def draw_pieces(screen, board):
    for piece in board.pieces:
        try:
            screen.blit(piece.img, piece.img_rect)
        except:
            pass


is_dragging = False
start_drag_x, start_drag_y = 0, 0
running = True
test_board = Board(SQUARE_SIZE=100)
test_board.create()
board = test_board.get_board_square()
###############################################
print(board[0][4].piece)
board[0][4].piece.update_possible_moves()
print(board[0][4].piece.possible_moves)
# print(board[0][1].piece.coordinates)
#  print(test_board.board_square[0][1].notation)
###############################################

# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Обработка нажатия кнопки мыши для всех объектов Pawn
            for piece in test_board.pieces:
                piece.handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            # Обработка отпускания кнопки мыши для всех объектов Pawn
            for piece in test_board.pieces:
                piece.handle_mouse_up(event)
        elif event.type == pygame.MOUSEMOTION:
            # Обработка перетаскивания фигур для всех объектов Pawn
            for piece in test_board.pieces:
                piece.handle_mouse_drag(event)
    # Проверяем, если перемещение происходит
    if is_dragging:
        # Обновляем координаты изображения в соответствии с записанной позицией курсора
        image_x, image_y = pygame.mouse.get_pos()[0] - start_drag_x, pygame.mouse.get_pos()[1] - start_drag_y

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка доски
    draw_chessboard()
    draw_pieces(screen=screen, board=test_board)

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(180)


pygame.quit()
