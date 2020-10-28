import pygame
import sys
from nogrid import *
from random import randint

class Config:
    S_WIDTH = 1920
    S_HEIGHT = 1080
    PLAY_WIDTH = 600
    PLAY_HEIGHT = 600

    TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2  # middle aligned
    TOP_LEFT_Y = 200  # pixels from top


def init_title():
    font = pygame.font.SysFont('comicsans', 60)
    return font.render('PATHWAYS', 1, (255, 255, 255))


def init_end():
    font = pygame.font.SysFont('comicsans', 60)
    return font.render('GAME OVER', 1, (255, 0, 0))


def display_title(screen, label):
    screen.blit(label, (Config.TOP_LEFT_X + Config.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))


def display_game_over(screen, label):
    screen.blit(label, (Config.TOP_LEFT_X + Config.PLAY_WIDTH / 2 - (label.get_width() / 2), 900))


def try_stuff(n):
    pygame.init()
    pygame.display.set_caption('Pathways')
    screen = pygame.display.set_mode((Config.S_WIDTH, Config.S_HEIGHT))
    grid = create_grid(n)
    constant = get_time_constant(4, True)
    title = init_title()
    end = init_end()

    is_players_turn = True
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if is_players_turn and event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    r, c = get_rect_clicked(grid)
                except TypeError:
                    pass
                else:
                    grid[r][c] = 1
                    game_over = check_for_a_win(grid)
                    is_players_turn = False
            if event.type == pygame.MOUSEBUTTONUP and not is_players_turn:
                generate_computer_player_move(grid, alpha_beta, constant, 1)
                game_over = check_for_a_win(grid)
                is_players_turn = True

            if event.type == pygame.MOUSEBUTTONUP and game_over:
                display_game_over(screen, end)

        display_title(screen, title)
        display_grid(grid, screen)
        pygame.display.flip()


def display_grid(grid, screen):
    block_width = Config.PLAY_WIDTH // grid.shape[0]
    block_height = Config.PLAY_HEIGHT // grid.shape[1]
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            rect = pygame.draw.rect(screen, (128, 128, 128), (Config.TOP_LEFT_X+c*block_width, Config.TOP_LEFT_Y+r*block_height, block_width, block_height), 1)
            if grid[r][c] == 1 or grid[r][c] == 2:
                color = (255, 0, 0) if grid[r][c] == 1 else (0, 0, 255)
                rect.top += 1
                rect.left += 1
                rect.width -= 2
                rect.height -= 2
                pygame.draw.rect(screen, color, rect)


def get_rect_clicked(grid):
    pos = pygame.mouse.get_pos()
    block_width = Config.PLAY_WIDTH // grid.shape[0]
    block_height = Config.PLAY_HEIGHT // grid.shape[1]
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            rect = pygame.Rect(Config.TOP_LEFT_X + c * block_width, Config.TOP_LEFT_Y + r * block_height, block_width, block_height)
            if rect.collidepoint(pos):
                return r, c


if __name__ == '__main__':
    try_stuff(5)