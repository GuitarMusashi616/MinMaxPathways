import pygame
import sys
from nogrid import *
from random import randint
from time import sleep


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


def init_end(string='GAME OVER', color=(255,0,0)):
    font = pygame.font.SysFont('comicsans', 60)
    return font.render(string, 1, color)


def display_title(screen, label):
    screen.blit(label, (Config.TOP_LEFT_X + Config.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))


def display_game_over(screen, label):
    screen.blit(label, (Config.TOP_LEFT_X + Config.PLAY_WIDTH / 2 - (label.get_width() / 2), 900))


def try_stuff(n):
    grid = create_grid(n)
    constant = get_time_constant(3, True)
    play_ui(grid, True, constant)


def try_stuff_multiplayer(n):
    grid = create_grid(n)
    constant = get_time_constant(3, True)
    play_ui_multiplayer(grid, True, constant)


def try_stuff_ais(n):
    grid = create_grid(n)
    constant = get_time_constant(3, True)
    play_ais(grid, True, constant)


def play_ui(grid, is_players_turn, constant, depth=0, target_time=12):
    pygame.init()
    pygame.mixer.music.load('Pathways.mp3')
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('Pathways')
    screen = pygame.display.set_mode((Config.S_WIDTH, Config.S_HEIGHT))
    title = init_title()

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
                    if grid[r][c] == 1 or grid[r][c] == 2 or game_over:
                        break
                    grid[r][c] = 1
                    game_over = check_for_a_win(grid)
                    is_players_turn = False
            if event.type == pygame.MOUSEBUTTONUP and not is_players_turn:
                generate_computer_player_move(grid, alpha_beta, constant, target_time, depth)
                game_over = check_for_a_win(grid)
                is_players_turn = True

            if event.type == pygame.MOUSEBUTTONUP and game_over:
                score = win_loss_eval(grid)
                if score > 0:
                    end = init_end('YOU WIN', color=(0,255,0))
                    display_game_over(screen, end)
                elif score == 0:
                    end = init_end('DRAW', color=(0,0,255))
                    display_game_over(screen, end)
                else:
                    end = init_end()
                    display_game_over(screen, end)

        display_title(screen, title)
        display_grid(grid, screen)
        pygame.display.flip()


def play_ais(grid, is_players_turn, constant, depth=0, target_time=1):
    pygame.init()
    last_ticks = pygame.time.get_ticks()
    pygame.mixer.music.load('Pathways.mp3')
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('Pathways')
    screen = pygame.display.set_mode((Config.S_WIDTH, Config.S_HEIGHT))
    title = init_title()

    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if is_players_turn and pygame.time.get_ticks()-last_ticks > 100:
                generate_computer_player_move(grid, alpha_beta, constant, target_time, depth, 1)
                game_over = check_for_a_win(grid)
                is_players_turn = False
                last_ticks = pygame.time.get_ticks()

            if not is_players_turn and pygame.time.get_ticks()-last_ticks > 100:
                generate_computer_player_move(grid, alpha_beta, constant, target_time, depth)
                game_over = check_for_a_win(grid)
                is_players_turn = True
                last_ticks = pygame.time.get_ticks()

            if game_over:
                score = win_loss_eval(grid)
                if score > 0:
                    end = init_end('YOU WIN', color=(0,255,0))
                    display_game_over(screen, end)
                elif score == 0:
                    end = init_end('DRAW', color=(0,0,255))
                    display_game_over(screen, end)
                else:
                    end = init_end()
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


def play_ui_multiplayer(grid, first_players_turn, constant, depth=0):
    pygame.init()
    pygame.mixer.music.load('Pathways.mp3')
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('Pathways')
    screen = pygame.display.set_mode((Config.S_WIDTH, Config.S_HEIGHT))
    title = init_title()

    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    r, c = get_rect_clicked(grid)
                except TypeError:
                    pass
                else:
                    if grid[r][c] == 1 or grid[r][c] == 2 or game_over:
                        break
                    if first_players_turn:
                        grid[r][c] = 1
                        first_players_turn = False
                    else:
                        grid[r][c] = 2
                        first_players_turn = True
                    game_over = check_for_a_win(grid)

            if event.type == pygame.MOUSEBUTTONUP and game_over:
                score = win_loss_eval(grid)
                if score > 0:
                    end = init_end('1st Player Wins', color=(255,0,0))
                    display_game_over(screen, end)
                elif score == 0:
                    end = init_end('DRAW', color=(0,255,0))
                    display_game_over(screen, end)
                else:
                    end = init_end('2nd Player Wins', color=(0,0,255))
                    display_game_over(screen, end)

        display_title(screen, title)
        display_grid(grid, screen)
        pygame.display.flip()


if __name__ == '__main__':
    try_stuff_multiplayer(6)