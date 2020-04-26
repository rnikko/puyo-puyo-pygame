import json

import msvcrt
from time import time
from random import choice


FIELD_H = 14
FIELD_W = 8

CELL_NONE = "□"
CELL_WALL = "■"
CELL_PUYO_1 = "R"
CELL_PUYO_2 = "G"
CELL_PUYO_3 = "B"
CELL_PUYO_4 = "P"
CELL_PUYO_5 = "Y"

PUYO_COLORS = [
    CELL_PUYO_1,
    CELL_PUYO_2,
    CELL_PUYO_3,
    CELL_PUYO_4,
    CELL_PUYO_5
]

PUYO_ANGLE_0 = (0, -1)
PUYO_ANGLE_90 = (-1, 0)
PUYO_ANGLE_180 = (0, 1)
PUYO_ANGLE_270 = (1, 0)

PUYO_SUB_POS = [
    PUYO_ANGLE_0,
    PUYO_ANGLE_90,
    PUYO_ANGLE_180,
    PUYO_ANGLE_270
]

PUYO_START_X = 3
PUYO_START_Y = 1

puyo_x = PUYO_START_X
puyo_y = PUYO_START_Y
puyo_angle = 0
puyo_color = choice(PUYO_COLORS)
sub_puyo_color = choice(PUYO_COLORS)

drop_puyos = False

# ms
fall_every = 500
game_tick = 0

# init cells
cells = [[CELL_NONE for c in range(0, FIELD_W)] for r in range(0, FIELD_H)]

# add cell walls
for y in range(0, FIELD_H):
    cells[y][0] = CELL_WALL
    cells[y][FIELD_W-1] = CELL_WALL
for x in range(0, FIELD_W):
    cells[FIELD_H-1][x] = CELL_WALL

def display():
    # does a similar thing that memcpy does?
    display_buffer = json.loads(json.dumps(cells))

    # add main puyo
    display_buffer[puyo_y][puyo_x] = puyo_color

    # add sub puyo
    sub_puyo_x = puyo_x + PUYO_SUB_POS[puyo_angle][0]
    sub_puyo_y = puyo_y + PUYO_SUB_POS[puyo_angle][1]
    display_buffer[sub_puyo_y][sub_puyo_x] = sub_puyo_color

    # displays cells
    print("\n\n")
    for row in range(0, FIELD_H):
        print("".join(display_buffer[row]))

def puyo_colliding(puyo_x, puyo_y, angle):
    if cells[puyo_y][puyo_x] != CELL_NONE:
        return True
    sub_puyo_x = puyo_x + PUYO_SUB_POS[puyo_angle][0]
    sub_puyo_y = puyo_y + PUYO_SUB_POS[puyo_angle][1]
    if cells[sub_puyo_y][sub_puyo_x] != CELL_NONE:
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
    for i in range(0, len(PUYO_SUB_POS)):
        near_puyo_x = x + PUYO_SUB_POS[i][0]
        near_puyo_y = y + PUYO_SUB_POS[i][1]
        count = check_nearby(near_puyo_x, near_puyo_y, puyo, count)
    return count

def erase_puyo(x, y, puyo):
    if cells[y][x] != puyo:
        return

    cells[y][x] = CELL_NONE

    for i in range(0, len(PUYO_SUB_POS)):
        near_puyo_x = x + PUYO_SUB_POS[i][0]
        near_puyo_y = y + PUYO_SUB_POS[i][1]
        erase_puyo(near_puyo_x, near_puyo_y, puyo)


while 1:
    # limit redraw interval
    game_tick += 1
    if game_tick > (fall_every * 10):
        
        if not drop_puyos:
            if not puyo_colliding(puyo_x, puyo_y + 1, puyo_angle):
                puyo_y += 1

            else:
                # set puyo on to cells master
                cells[puyo_y][puyo_x] = puyo_color
                sub_puyo_x = puyo_x + PUYO_SUB_POS[puyo_angle][0]
                sub_puyo_y = puyo_y + PUYO_SUB_POS[puyo_angle][1]
                cells[sub_puyo_y][sub_puyo_x] = sub_puyo_color

                # new piece
                puyo_x = PUYO_START_X
                puyo_y = PUYO_START_Y
                puyo_angle = 0
                puyo_color = choice(PUYO_COLORS)
                sub_puyo_color = choice(PUYO_COLORS)

                # there might be a puyo that still needs to drop
                drop_puyos = True
        
        if drop_puyos:
            #
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
                for y in range(0, FIELD_H - 1):
                    for x in range(1, FIELD_W - 1):
                        puyo = cells[y][x]

                        chain = check_nearby(x, y, puyo, 0)
                        if chain >= 4:
                            # add to user score here
                            # add_score(puyo, chain)

                            #
                            erase_puyo(x, y, puyo)

                            # lock because after clearing chains, there might be more puyos to drop
                            drop_puyos = True

            # piece can't fall anymore
            # check if 

        display()
        game_tick = 0

    if msvcrt.kbhit():
        if not drop_puyos:
            key = msvcrt.getch().decode()
            x = puyo_x
            y = puyo_y
            angle = puyo_angle

            if key == "s":
                y += 1
            # elif key == "w":
            #     y -= 1
            elif key == "d":
                x += 1
            elif key == "a":
                x -= 1
            elif key == "k":
                angle = (angle + 1) % 4
            elif key == "l":
                angle = (angle - 1) % 4

            else:
                raise Exception("exit")

            if not puyo_colliding(x, y, angle):
                puyo_x = x
                puyo_y = y
                puyo_angle = angle

        display()
