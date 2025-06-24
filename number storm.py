import pygame
import random

# Constants
WIDTH, HEIGHT = 500, 550
GRID_SIZE = 4
TILE_SIZE = 100
PADDING = 10
TOP_OFFSET = 80

# Colors
WHITE = (255, 255, 240)
BLACK = (33, 33, 33)
SKY_BLUE = (135, 206, 250)
INDIGO = (75, 0, 130)
LAVENDER = (230, 230, 250)
GOLD = (255, 215, 0)

# Fonts
pygame.init()
font_large = pygame.font.SysFont('Comic Sans MS', 36, bold=True)
font_medium = pygame.font.SysFont('Verdana', 26)
font_small = pygame.font.SysFont('Verdana', 18)


def generate_board():
    nums = list(range(16))
    random.shuffle(nums)
    return [nums[i * GRID_SIZE:(i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]


def draw_grid(screen, board, moves, score):
    screen.fill(LAVENDER)
    title_text = font_large.render("NUMBER STORM", True, INDIGO)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 40))
    screen.blit(title_text, title_rect)

    offset_x = (WIDTH - ((TILE_SIZE - PADDING) * GRID_SIZE)) // 2

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = offset_x + j * TILE_SIZE
            y = i * TILE_SIZE + TOP_OFFSET
            pygame.draw.rect(screen, SKY_BLUE, (x, y, TILE_SIZE - PADDING, TILE_SIZE - PADDING), border_radius=8)
            val = board[i][j]
            if val != 0:
                num_text = font_medium.render(str(val), True, BLACK)
                num_rect = num_text.get_rect(center=(x + (TILE_SIZE - PADDING) // 2, y + (TILE_SIZE - PADDING) // 2))
                screen.blit(num_text, num_rect)

    moves_text = font_small.render(f"Moves: {moves}", True, BLACK)
    score_text = font_small.render(f"Score: {score}", True, BLACK)
    screen.blit(moves_text, (10, HEIGHT - 70))
    screen.blit(score_text, (10, HEIGHT - 45))

    pygame.draw.rect(screen, INDIGO, (WIDTH - 110, HEIGHT - 50, 90, 35), border_radius=6)
    exit_text = font_small.render("Give Up", True, GOLD)
    screen.blit(exit_text, (WIDTH - 95, HEIGHT - 45))


def find_zero(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return i, j

def show_about(screen):
    running = True
    minion_img = pygame.image.load("pngimg.com - minions_PNG72.png")
    minion_img = pygame.transform.scale(minion_img, (260, 150))

    while running:
        screen.fill(WHITE)
        title = font_large.render("About Number Storm", True, INDIGO)
        title_rect = title.get_rect(center=(WIDTH // 2, 30))
        screen.blit(title, title_rect)

        lines = [
            "Arrange numbers in increasing order (1-15).",
            "Use arrow keys to move the empty tile.",
            "Reach the goal configuration to win!",
            "",
            "Click anywhere to return to main menu."
        ]

        for i, line in enumerate(lines):
            txt = font_small.render(line, True, BLACK)
            txt_rect = txt.get_rect(center=(WIDTH // 2, 90 + i * 45))
            screen.blit(txt, txt_rect)

        screen.blit(minion_img, minion_img.get_rect(center=(WIDTH // 2, HEIGHT - 100)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.flip()
    return True

    

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Number Storm")

    # Menu screen
    menu = True
    while menu:
        screen.fill(WHITE)
        title = font_large.render("NUMBER STORM", True, INDIGO)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        start_btn = pygame.Rect(WIDTH // 2 - 75, 160, 150, 50)
        about_btn = pygame.Rect(WIDTH // 2 - 75, 230, 150, 50)
        exit_btn = pygame.Rect(WIDTH // 2 - 75, 300, 150, 50)

        pygame.draw.rect(screen, SKY_BLUE, start_btn, border_radius=8)
        pygame.draw.rect(screen, SKY_BLUE, about_btn, border_radius=8)
        pygame.draw.rect(screen, SKY_BLUE, exit_btn, border_radius=8)

        start_text = font_medium.render("Start Game", True, BLACK)
        about_text = font_medium.render("About", True, BLACK)
        exit_text = font_medium.render("Exit", True, BLACK)

        screen.blit(start_text, start_text.get_rect(center=start_btn.center))
        screen.blit(about_text, about_text.get_rect(center=about_btn.center))
        screen.blit(exit_text, exit_text.get_rect(center=exit_btn.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    game(screen)
                elif about_btn.collidepoint(event.pos):
                    if not show_about(screen):
                        menu = False
                elif exit_btn.collidepoint(event.pos):
                    menu = False


def game(screen):
    board = generate_board()
    order = [list(range(i * GRID_SIZE + 1, (i + 1) * GRID_SIZE + 1)) for i in range(GRID_SIZE)]
    order[-1][-1] = 0

    moves = 0
    score = 1000
    running = True
    while running:
        draw_grid(screen, board, moves, score - moves)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH - 110 <= event.pos[0] <= WIDTH - 20 and HEIGHT - 50 <= event.pos[1] <= HEIGHT - 15:
                    running = False
            elif event.type == pygame.KEYDOWN:
                row, col = find_zero(board)
                if event.key == pygame.K_LEFT and col < GRID_SIZE - 1:
                    board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
                    moves += 1
                elif event.key == pygame.K_RIGHT and col > 0:
                    board[row][col], board[row][col - 1] = board[row][col - 1], board[row][col]
                    moves += 1
                elif event.key == pygame.K_UP and row < GRID_SIZE - 1:
                    board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
                    moves += 1
                elif event.key == pygame.K_DOWN and row > 0:
                    board[row][col], board[row - 1][col] = board[row - 1][col], board[row][col]
                    moves += 1

        if board == order:
            screen.fill(LAVENDER)
            win_text = font_large.render("YOU WON!", True, GOLD)
            screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

main()
pygame.quit()



       
