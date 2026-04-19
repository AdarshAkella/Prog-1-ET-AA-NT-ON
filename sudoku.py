from sudoku_generator import Board, Cell
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 540, 600
CELL_SIZE =WIDTH // 9
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

def select_difficulty():
    font = pygame.font.Font(None, 36)
    font_big = pygame.font.Font(None, 50)
    text_welcome = font_big.render("Welcome To Sudoku", True, WHITE)
    text_game_mode = font.render("Select Game Mode:", True, WHITE)
    text_easy = font.render("Easy", True, RED)
    text_medium = font.render("Medium", True, GREEN)
    text_hard = font.render("Hard", True, WHITE)

    screen.blit(text_welcome, (WIDTH // 4 - text_easy.get_width() // 2, HEIGHT - 500))
    screen.blit(text_game_mode, (WIDTH // 4 - text_easy.get_width() // 3, HEIGHT - 350))

    screen.blit(text_easy, (WIDTH // 3 - text_easy.get_width() // 2, HEIGHT - 300))
    screen.blit(text_medium, (WIDTH // 2 - text_medium.get_width() // 2, HEIGHT - 300))
    screen.blit(text_hard, (2 * WIDTH // 3 - text_hard.get_width() // 2, HEIGHT - 300))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 3 > mouse_x:
                    return "easy"
                elif WIDTH // 3 < mouse_x < 2 * WIDTH // 3:
                    return "medium"
                elif mouse_x > 2 * WIDTH // 3:
                    return "hard"

def draw_buttons():
    font = pygame.font.Font(None, 30)
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 60, WIDTH // 3, 60))
    pygame.draw.rect(screen, BLUE, (WIDTH // 3, HEIGHT - 60, WIDTH // 3, 60))
    pygame.draw.rect(screen, BLUE, (2 * WIDTH // 3, HEIGHT - 60, WIDTH // 3, 60))

    reset_text = font.render("Reset", True, WHITE)
    restart_text = font.render("Restart", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)

    screen.blit(reset_text, (WIDTH // 6 - reset_text.get_width() // 2, HEIGHT - 40))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 40))
    screen.blit(exit_text, (5 * WIDTH // 6 - exit_text.get_width() // 2, HEIGHT - 40))

def draw_game_over():
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over :(", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def draw_game_win():
    font = pygame.font.Font(None, 48)
    text = font.render("Game Won!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_state = "start"
selected_cell = None
difficulty = None

clock = pygame.time.Clock()
row = 0
col = 0
org_board = None


while True:
    if game_state == "start":
        screen.fill(BLACK)
        pygame.display.set_caption("Sudoku Game")
        difficulty = select_difficulty()
        screen.fill(WHITE)
        board = Board(540, 600, screen, difficulty)
        pygame.display.set_caption("Sudoku Game (" + difficulty + ")")
        org_board = board.org_board
        board.draw()
        game_state = "playing"
    elif game_state == "playing":
        board.draw()
        draw_buttons()
        if selected_cell:
            board.select(row, col)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_x, mouse_y = pygame.mouse.get_pos()
                 if mouse_y > WIDTH:
                     row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
                     selected_cell = (row, col)
                     if row == 9:
                         if col == 7:
                          pygame.quit()
                          sys.exit()
                         elif col == 4:
                             game_state = "start"
                         elif col == 1:
                             board.reset_to_original()
                             board.draw()
                 else:
                     row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
                     selected_cell = (row, col)
            elif event.type == pygame.KEYDOWN and selected_cell:
                 if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                                  pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]:
                    if 0 <= row <= 8 and 0 <= col <= 8:
                        if org_board[row][col] == 0:
                            board.sketch(int(event.unicode))
                            board.draw()
                 elif event.key in [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]:
                     if event.key == pygame.K_DOWN :
                        if row < 9:
                            row += 1
                     elif event.key == pygame.K_UP:
                         if row > -1:
                             row -= 1
                     elif event.key == pygame.K_LEFT:
                         if col > -1:
                             col -= 1
                     elif event.key == pygame.K_RIGHT:
                         if col < 9:
                             col += 1
                     selected_cell = (row, col)
                 elif event.key == pygame.K_BACKSPACE:
                     if 0 <= row <= 8 and 0 <= col <= 8:
                         if org_board[row][col] == 0:
                             board.clear()
                             board.draw()
                 elif event.key == pygame.K_RETURN:
                     if board.is_full():
                        if board.check_board():
                            screen.fill(WHITE)
                            draw_game_win()
                            game_state = "start"
                        else:
                            screen.fill(WHITE)
                            draw_game_over()
                            game_state = "start"
        pygame.display.flip()
        clock.tick(FPS)






