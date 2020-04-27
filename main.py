import json
import sys

import pygame as pg
from piece import Piece

import msvcrt
from time import time
from random import choice


def init_cells(FIELD_H, FIELD_W):
    # init cells
    cells = [[CELL_NONE for c in range(0, FIELD_W)] for r in range(0, FIELD_H)]

    # add cell walls
    for y in range(0, FIELD_H):
        cells[y][0] = CELL_WALL
        cells[y][FIELD_W-1] = CELL_WALL
    for x in range(0, FIELD_W):
        cells[FIELD_H-1][x] = CELL_WALL

    return cells


def display():
    window.fill(BACKGROUND)

    # does a similar thing that memcpy does?
    display_buffer = json.loads(json.dumps(cells))

    # add piece
    display_buffer[piece.mp_y][piece.mp_x] = piece.mp_c
    display_buffer[piece.sp_y][piece.sp_x] = piece.sp_c

    # displays cells
    # print("\n\n")
    # for row in range(0, FIELD_H):
    #     print("".join(display_buffer[row]))

    # through rows
    for i in range(len(display_buffer)):
        # through cols
        for j in range(len(display_buffer[0])):

            # non playarea squares black
            if i < 2:
                color = BACKGROUND
            elif i == 14:
                color = BACKGROUND
            elif j == 0 or j == 7:
                color = BACKGROUND
            else:
                cell = display_buffer[i][j]

                if cell == "□":
                    color = (80, 80, 80)
                elif cell == "■":
                    color = (222, 222, 222)
                elif cell == "R":
                    color = (255, 0, 0)
                elif cell == "G":
                    color = (0, 255, 0)
                elif cell == "B":
                    color = (0, 0, 255)
                elif cell == "P":
                    color = (255, 0, 255)
                elif cell == "Y":
                    color = (255, 255, 0)

                # print(i, j, cell)

            coords = (PLAYAREA_START_X + j * SQ_SIZE, PLAYAREA_START_Y + i * SQ_SIZE)
            size = (SQ_SIZE, SQ_SIZE)
            square = (coords, size)

            pg.draw.rect(window, color, square)

    # draw next
    for i in range(0, 2):
        if i == 0:
            cell = next_piece.mp_c
        else:
            cell = next_piece.sp_c

        if cell == "R":
            color = (255, 0, 0)
        elif cell == "G":
            color = (0, 255, 0)
        elif cell == "B":
            color = (0, 0, 255)
        elif cell == "P":
            color = (255, 0, 255)
        elif cell == "Y":
            color = (255, 255, 0)

        coords = ((109 * SIZE_MULTIPLIER), (46 * SIZE_MULTIPLIER) + (SQ_SIZE * i))

        size = (SQ_SIZE, SQ_SIZE)
        square = (coords, size)

        pg.draw.rect(window, color, square)

    # draw next_next
    for i in range(0, 2):
        if i == 0:
            cell = next_next_piece.mp_c
        else:
            cell = next_next_piece.sp_c

        if cell == "R":
            color = (255, 0, 0)
        elif cell == "G":
            color = (0, 255, 0)
        elif cell == "B":
            color = (0, 0, 255)
        elif cell == "P":
            color = (255, 0, 255)
        elif cell == "Y":
            color = (255, 255, 0)

        coords = ((109 * SIZE_MULTIPLIER), (90 * SIZE_MULTIPLIER) + (SQ_SIZE * i))

        size = (SQ_SIZE, SQ_SIZE)
        square = (coords, size)

        pg.draw.rect(window, color, square)

    pg.font.init()

    font = pg.font.SysFont("comicsansms", 10 * SIZE_MULTIPLIER)
    text = font.render(str(score), True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.right = 104 * SIZE_MULTIPLIER
    text_rect.bottom = 222 * SIZE_MULTIPLIER
    window.blit(text, text_rect)

    pg.display.update()


def puyo_colliding(falling_down=False):
    if falling_down:
        piece.mp_y += 1

    if cells[piece.mp_y][piece.mp_x] != CELL_NONE:
        return True
    if cells[piece.sp_y][piece.sp_x] != CELL_NONE:
        return True

    return False


def check_nearby(x, y, puyo, count):
    # only check for nearby counts if
    # # # # it hasn't been checked before
    # # # # not an empty space
    # # # # the same puyo
    if puyo == CELL_NONE or checked[y][x] or cells[y][x] != puyo:
        return count
    count += 1
    checked[y][x] = True
    for i in range(0, len(SUB_POS)):
        near_puyo_x = x + SUB_POS[i][0]
        near_puyo_y = y + SUB_POS[i][1]
        count = check_nearby(near_puyo_x, near_puyo_y, puyo, count)
    return count


def erase_puyo(x, y, puyo):
    if cells[y][x] != puyo:
        return

    cells[y][x] = CELL_NONE

    for i in range(0, len(SUB_POS)):
        near_puyo_x = x + SUB_POS[i][0]
        near_puyo_y = y + SUB_POS[i][1]
        erase_puyo(near_puyo_x, near_puyo_y, puyo)


PLAYAREA_H = 12
PLAYAREA_W = 6

# offset for playarea bottom and walls
FIELD_H = PLAYAREA_H + 3
FIELD_W = PLAYAREA_W + 2

CELL_NONE = "□"
CELL_WALL = "■"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 127, 0)

# get rid of this?
SUB_POS = [(0, -1), (-1, 0), (0, 1), (1, 0)]

BACKGROUND = BLACK

SIZE_MULTIPLIER = 4
SQ_SIZE = 16 * SIZE_MULTIPLIER

PLAYAREA_START_X = (SQ_SIZE / 2) - SQ_SIZE
PLAYAREA_START_Y = (SQ_SIZE - (SQ_SIZE / 16)) - (SQ_SIZE * 2)

WINDOW_SIZE = (SQ_SIZE * 16, SQ_SIZE * 14)

CHAIN_POWER = {
    1: 4,
    2: 20,
    3: 24,
    4: 32,
    5: 48,
    6: 96,
    7: 160,
    8: 240,
    9: 320,
    10: 480,
    11: 600,
    12: 700,
    13: 800,
    14: 900
}

COLOR_BONUS = {
    0: 0,
    1: 0,
    2: 3,
    3: 6,
    4: 12,
    5: 24
}

GROUP_BONUS = {
    4: 0,
    5: 2,
    6: 3,
    7: 4,
    8: 5,
    9: 6,
    10: 7
}

chain_info = {}

piece = Piece()
next_piece = Piece()
next_next_piece = Piece()

drop_puyos = False

cells = init_cells(FIELD_H, FIELD_W)

window = pg.display.set_mode(WINDOW_SIZE)

# window title
pg.display.set_caption("puyo puyo")

chain = 0
score = 0

run = True

clock = pg.time.Clock()
fall_time = 0

while run:
    fall_time += clock.get_rawtime()
    clock.tick()

    if drop_puyos:
        fall_speed = .2

    else:
        chain_info = {}
        fall_speed = .5
        chain = 0

    # PIECE FALLING CODE
    if fall_time/1000 >= fall_speed:
        fall_time = 0

        if not drop_puyos:
            if not puyo_colliding(falling_down=True):
                pass

            else:
                if piece.mp_y <= 2:
                    raise Exception("GAME OVER")

                # undo mp_y += 1
                piece.undo()

                # set puyo on to cells master
                cells[piece.mp_y][piece.mp_x] = piece.mp_c
                cells[piece.sp_y][piece.sp_x] = piece.sp_c

                # new piece
                piece = next_piece
                next_piece = next_next_piece
                next_next_piece = Piece()

                # there might be a puyo that still needs to drop
                drop_puyos = True
            
            display()

        if drop_puyos:
            drop_puyos = False

            # if item in this cell is not none and cell under it is empty,
            # drop piece until it hits floor
            for y in range(FIELD_H - 2, -1, -1):
                for x in range(1, FIELD_W):
                    item = cells[y][x]
                    item_under = cells[y + 1][x]

                    if item != CELL_NONE and item_under == CELL_NONE:
                        cells[y + 1][x] = cells[y][x]
                        cells[y][x] = CELL_NONE
                        drop_puyos = True

            # all puyos that had to fall has fallen
            # check if there is a 4-chain of puyos present and remove from board
            # if not pieces falling down right now

            if not drop_puyos:
                checked = [[False for c in range(0, FIELD_W)] for r in range(0, FIELD_H)]

                PC = 0
                colors_cleared = []
                chain += 1

                for y in range(0, FIELD_H - 1):
                    for x in range(1, FIELD_W - 1):
                        puyo = cells[y][x]

                        if puyo == CELL_NONE or puyo == CELL_WALL:
                            continue

                        puyos_connected = check_nearby(x, y, puyo, 0)
                        if puyos_connected >= 4:
                            if puyo not in colors_cleared:
                                colors_cleared.append(puyo)
                            PC += puyos_connected

                            # add to user score here
                            # add_score(puyo, chain)

                            erase_puyo(x, y, puyo)

                            GB += 10 if puyos_connected >= 11 else GROUP_BONUS[puyos_connected]

                            # lock because after clearing chains, there might be more puyos to drop
                            drop_puyos = True

                CP = 999 if chain >= 15 else CHAIN_POWER[chain]
                CB = COLOR_BONUS[len(colors_cleared)]
                GB = 0
                score_multiplier = 1 if (CP + CB + GB) == 0 else CP + CB + GB
                chain_score = (PC * 10) * (score_multiplier)

                score += chain_score

                if chain_score > 0:
                    print(f"Chain: {chain}")
                    print(f"Cleared in Chain: {PC}")
                    print(f"Chain Power: {CP}")
                    print(f"Color Bonus: {CB} {colors_cleared}")
                    print(f"Group Power: {GB}")
                    print(f"Score Multiplier: {score_multiplier}")
                    print(f"Score Calc: (10 * {PC}) * ({CP} + {CB} + {GB})")
                    print(f"Chain Score: {chain_score}")

            # update display after we drop puyos
            display()

    for event in pg.event.get():
        # can't move if there's a blob placed + has pending blob falling down
        if event.type == pg.KEYDOWN and not drop_puyos:
            if event.key == pg.K_a:
                piece.mp_x -= 1
            elif event.key == pg.K_d:
                piece.mp_x += 1
            elif event.key == pg.K_s:
                piece.mp_y += 1
            elif event.key == pg.K_w:
                piece.mp_y -= 1

            elif event.key == pg.K_k:
                piece.angle = (piece.angle + 1) % 4
            elif event.key == pg.K_l:
                piece.angle = (piece.angle - 1) % 4

            else:
                pg.quit()

            # check for new pos collision
            if puyo_colliding():
                piece.undo()

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        display()
