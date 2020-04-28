import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

import json
import pygame as pg

from piece import Piece, SUB_POS
from player import Player


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

BLACK = (0, 0, 0)
DARK_GREY = (25, 25, 25)
LIGHT_GREY = (230, 230, 230)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 127, 0)

BACKGROUND = BLACK

SIZE_MULTIPLIER = 2
SQ_SIZE = (16 * SIZE_MULTIPLIER) // 2

PLAYAREA_START_X = SQ_SIZE
PLAYAREA_START_Y = (SQ_SIZE * 2) - SIZE_MULTIPLIER
WINDOW_SIZE = (SQ_SIZE * 2 * 16, SQ_SIZE * 2 * 14)

PLAYAREA_H = 12
PLAYAREA_W = 6

# offset for playarea bottom and walls
FIELD_H = (PLAYAREA_H + 3) * 2
FIELD_W = (PLAYAREA_W + 2) * 2

CELL_NONE = " "
CELL_WALL = "█"


def init_board():
    # gameboard
    board = [[CELL_NONE for c in range(0, FIELD_W)] for r in range(0, FIELD_H)]
    for y in range(0, FIELD_H):
        board[y][0] = CELL_WALL
        board[y][1] = CELL_WALL
        board[y][FIELD_W-1] = CELL_WALL
        board[y][FIELD_W-2] = CELL_WALL
    for x in range(0, FIELD_W):
        board[FIELD_H-1][x] = CELL_WALL
        board[FIELD_H-2][x] = CELL_WALL

    return board


def display_board(console=False):
    # does a similar thing that memcpy does?
    display_buffer = json.loads(json.dumps(board))

    # PLACE MAIN PUYO ON DISPLAY BUFFER
    display_buffer[piece.mp_y][piece.mp_x] = piece.mp_c
    display_buffer[piece.mp_y][piece.mp_x + 1] = piece.mp_c
    display_buffer[piece.mp_y - 1][piece.mp_x] = piece.mp_c
    display_buffer[piece.mp_y - 1][piece.mp_x + 1] = piece.mp_c

    # PLACE PUYO ON DISPLAY BUFFER
    display_buffer[piece.sp_y][piece.sp_x] = piece.sp_c
    display_buffer[piece.sp_y][piece.sp_x + 1] = piece.sp_c
    display_buffer[piece.sp_y - 1][piece.sp_x] = piece.sp_c
    display_buffer[piece.sp_y - 1][piece.sp_x + 1] = piece.sp_c

    if console == True:
        print("\n\n")
        for i, r in enumerate(display_buffer, 0):
            row = "".join(r)
            print(f"{i:0>2} {row}")

    else:
        for i in range(4, 28):
            for j in range(2, 14):
                cell = display_buffer[i][j]

                if cell == CELL_NONE:
                    color = LIGHT_GREY
                elif cell == "R":
                    color = RED
                elif cell == "G":
                    color = GREEN
                elif cell == "B":
                    color = BLUE
                elif cell == "P":
                    color = PURPLE
                elif cell == "Y":
                    color = YELLOW

                coords = (PLAYAREA_START_X + (j - 2) * SQ_SIZE, PLAYAREA_START_Y + (i - 4) * SQ_SIZE)
                size = (SQ_SIZE, SQ_SIZE)
                square = (coords, size)

                pg.draw.rect(screen, color, square)


def set_piece():
    # PLACE MAIN PUYO ON DISPLAY BUFFER
    board[piece.mp_y][piece.mp_x] = piece.mp_c
    board[piece.mp_y][piece.mp_x + 1] = piece.mp_c
    board[piece.mp_y - 1][piece.mp_x] = piece.mp_c
    board[piece.mp_y - 1][piece.mp_x + 1] = piece.mp_c

    # PLACE PUYO ON DISPLAY BUFFER
    board[piece.sp_y][piece.sp_x] = piece.sp_c
    board[piece.sp_y][piece.sp_x + 1] = piece.sp_c
    board[piece.sp_y - 1][piece.sp_x] = piece.sp_c
    board[piece.sp_y - 1][piece.sp_x + 1] = piece.sp_c


def cant_move_here():
    if board[piece.mp_y][piece.mp_x] != CELL_NONE:
        return True
    elif board[piece.sp_y][piece.sp_x] != CELL_NONE:
        return True
    return False


def cant_keep_falling():
    if board[3][6] != CELL_NONE:
        raise Exception("GAME OVER")
    elif board[piece.mp_y + 1][piece.mp_x] != CELL_NONE:
        # print("main piece hitting", piece.mp_y, piece.mp_x, repr(board[piece.mp_y + 1][piece.mp_x]))
        return True
    elif board[piece.sp_y + 1][piece.sp_x] != CELL_NONE:
        # print("sub piece hitting", piece.sp_y, piece.sp_x, repr(board[piece.sp_y + 1][piece.sp_x]))
        return True
    return False


def check_nearby(x, y, puyo, count):
    # only check for nearby counts if
    # # # # it hasn't been checked before
    # # # # not an empty space
    # # # # the same puyo
    if puyo == CELL_NONE or checked[y][x] or board[y][x] != puyo:
        return count
    count += 1
    checked[y][x] = True
    for i in range(0, len(SUB_POS)):
        near_puyo_x = x + SUB_POS[i][0]
        near_puyo_y = y + SUB_POS[i][1]
        count = check_nearby(near_puyo_x, near_puyo_y, puyo, count)
    return count


def erase_puyo(x, y, puyo):
    if board[y][x] != puyo:
        return

    board[y][x] = CELL_NONE
    board[y][x + 1] = CELL_NONE
    board[y - 1][x] = CELL_NONE
    board[y - 1][x + 1] = CELL_NONE

    for i in range(0, len(SUB_POS)):
        near_puyo_x = x + SUB_POS[i][0]
        near_puyo_y = y + SUB_POS[i][1]
        erase_puyo(near_puyo_x, near_puyo_y, puyo)


piece = Piece()
n_piece = Piece()
nn_piece = Piece()

# movement
p_dx = 0
p_dy = 0

chain = 0
score = 0
total_chain = 0

fall_speed = 60
board = init_board()
drop_puyos = False

pg.init()
pg.display.set_caption("??????????")

screen = pg.display.set_mode(WINDOW_SIZE)
screen.fill(BACKGROUND)

run = True

frame = 0
clock = pg.time.Clock()


while run:
    if not drop_puyos:        
        chain = 0

        if cant_keep_falling():
            set_piece()
            piece = n_piece
            n_piece = nn_piece
            nn_piece = Piece()

            drop_puyos = True

    if drop_puyos:
            drop_puyos = False

            # if item in this cell is not none and cell under it is empty,
            # drop piece until it hits floor
            for y in range(FIELD_H - 3, 3, -2):
                for x in range(2, FIELD_W - 3):
                    item = board[y][x]
                    item_under = board[y + 2][x]

                    if item != CELL_NONE and item_under == CELL_NONE:
                        # moves piece down
                        board[y + 1][x] = item
                        board[y + 1][x + 1] = item
                        board[y + 2][x] = item
                        board[y + 2][x + 1] = item
                        # sets previous coord to none
                        board[y][x] = CELL_NONE
                        board[y][x + 1] = CELL_NONE
                        board[y - 1][x] = CELL_NONE
                        board[y - 1][x + 1] = CELL_NONE
                        drop_puyos = True

            # all puyos that had to fall has fallen
            # check if there is a 4-chain of puyos present and remove from board
            # if not pieces falling down right now

            if not drop_puyos:
                checked = [[False for c in range(0, FIELD_W)] for r in range(0, FIELD_H)]

                PC = 0
                GB = 0
                colors_cleared = []
                chain += 1

                for y in range(5, FIELD_H - 2, 2):
                    for x in range(2, FIELD_W - 3, 2):
                        puyo = board[y][x]

                        if puyo == CELL_NONE or puyo == CELL_WALL:
                            continue

                        puyos_connected = check_nearby(x, y, puyo, 0)
                        if puyos_connected >= 4:
                            erase_puyo(x, y, puyo)
                            drop_puyos = True

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
                score_multiplier = 1 if (CP + CB + GB) == 0 else CP + CB + GB
                chain_score = (PC * 10) * (score_multiplier)

                score += chain_score

                if chain_score > 0:
                    total_chain += 1

                    print(f"Chain: {chain}")
                    print(f"Cleared in Chain: {PC}")
                    print(f"Chain Power: {CP}")
                    print(f"Color Bonus: {CB} {colors_cleared}")
                    print(f"Group Bonus: {GB}")
                    print(f"Score Multiplier: {score_multiplier}")
                    print(f"Score Calc: (10 * {PC}) * ({CP} + {CB} + {GB})")
                    print(f"Chain Score: {chain_score}\n")

    # controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.KEYDOWN and not drop_puyos:
            # moving piece
            if event.key == pg.K_a:
                p_dx = -2
            elif event.key == pg.K_d:
                p_dx = 2
            elif event.key == pg.K_s:
                p_dy = 2
            elif event.key == pg.K_w:
                # p_dy = -2
                pass

            # rotating piece
            elif event.key == pg.K_k:
                piece.angle = (piece.angle + 1) % 4
                p_dx = 0
                p_dy = 0
            elif event.key == pg.K_l:
                piece.angle = (piece.angle - 1) % 4
                p_dx = 0
                p_dy = 0

            else:
                run = False

        elif event.type == pg.KEYUP:
            if event.key == pg.K_a or event.key == pg.K_d:
                p_dx = 0
            elif event.key == pg.K_w or event.key == pg.K_s:
                p_dy = 0

    # APPLY MOVEMENT TO PIECE (only every nth frame)
    # check collision here, if good, add
    moving_piece = p_dy != 0 or p_dx != 0
    if frame % 4 == 0 and moving_piece:
        if piece.mp_y % 2 == 0 and p_dy != 0:
            piece.mp_y -= 1

        piece.mp_y += p_dy
        piece.mp_x += p_dx

    # drop piece every (nth frame)
    if frame % 45 == 0 and p_dy == 0:
        piece.mp_y += 1

    # piece bounce
    if piece.sp_x == 14 and piece.angle == 3:
        piece.sp_x -= 2
        piece.mp_x -= 2
    elif piece.sp_x == 0 and piece.angle == 1:
        piece.sp_x += 2
        piece.mp_x += 2
    elif piece.sp_y >= 28 and piece.angle == 2:
        piece.sp_y -= 2
        piece.mp_y -= 2

    if cant_move_here():
        piece.undo()

    # draw and update screen
    display_board(console=False)
    pg.display.flip()

    frame += 1
    clock.tick(60)
    

print(f"Score: {score}")
print(f"Total Chains: {total_chain}")
pg.quit()
