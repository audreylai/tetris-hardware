from hardware import *
from machine import Pin
import time
import math
import random


cursor_coord = [0, 0]
rotation = 0
next_pieces = []
grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]
floor_pieces = []
hold_piece_key = ""
game_speed = 0.1
level = 0

border_color = (10, 10 ,10)

def init_game():
    global next_pieces, cursor_coord, rotation, floor_pieces, grid, hold_piece_key
    # draw borders
    draw_rect((1, 3), (8, 8), border_color) # hold box
    
    draw_rect((1, 10), (8, 20), border_color) # digits box
    
    draw_rect((10, 3), (21, 28), border_color) # game space
    
    draw_rect((23, 3), (30, 28), border_color) # next
    
    
    cursor_coord = [5, 1]
    rotation = 0
    next_pieces = [str(random.randint(0,6)) for x in range(6)]
    floor_pieces = []
    grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]
    hold_piece_key = ""
    
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_piece((26, y_coord), next_p, 0, is_grid=False)

# piece
def get_piece(key, rotation):
    pieces = {
        "0": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
        "1": [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
        "2": [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ],
        "3": [
                [1, 1],
                [1, 1]
            ],
        "4": [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
        "5": [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
        "6": [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ],
    }
    piece = pieces[key]
    for i in range(rotation):
        piece = list(zip(*piece))
        piece = [list(reversed(x)) for x in piece]
    return piece

def get_piece_coord(coord, piece):
    center_y, center_x = math.floor(len(piece)/2), math.floor(len(piece[0])/2)
    piece_coords = []
    for y in range(len(piece)):
        for x in range(len(piece[0])):
            if piece[y][x] == 1:
                piece_coords.append((x + coord[0] - center_x, y + coord[1] - center_y))
    return piece_coords

def draw_piece(coord, key, rotation, undraw=False, is_grid=True):
    global grid
    piece_colors = {
        "0": [x*0.1 for x in (103, 225, 230)],
        "1": [x*0.1 for x in (56, 72, 214)],
        "2": [x*0.1 for x in (222, 163, 44)],
        "3": [x*0.1 for x in (247, 247, 87)],
        "4": [x*0.1 for x in (88, 224, 67)],
        "5": [x*0.1 for x in (161, 38, 209)],
        "6": [x*0.1 for x in (217, 30, 55)]
    }
    piece = get_piece(key, rotation)
    piece_coords = get_piece_coord(coord, piece)
    
    if not undraw:
        for x, y in piece_coords:
            color = piece_colors[key]
            if not is_grid:
                draw(x, y, color)
            else:
                grid[y][x] = color
    else:
        for x, y in piece_coords:
            color = piece_colors[key]
            if not is_grid:
                draw(x, y, (0,0,0))
            else:
                grid[y][x] = (0, 0, 0)


# utility
def is_collide(new_cursor_coord, piece_key, rotation, floor_only=False):
    piece = get_piece(piece_key, rotation)
    piece_coords = get_piece_coord(new_cursor_coord, piece)
    
    if not floor_only:   
        # check wall bounds
        for pc_x, pc_y in piece_coords:
            if pc_x < 0 or pc_x > 9 or pc_y < 0 or pc_y > 23:
                return True
    
    for pc in piece_coords:
        if pc[1] > 23 or pc in floor_pieces:
            return True
    

    return False

def drop_piece(piece_key, rotation):
    global floor_pieces, cursor_coord
    while not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation, floor_only=True):
        cursor_coord[1] += 1


# managment
def manage_next_pieces():
    global next_pieces
    tmp_next = []
    
    draw_rect((24, 4), (29, 27), (0,0,0), border=False)

    if len(tmp_next) == 0:
        tmp_next = random_shuffle([str(x) for x in range(0, 7)])
    
    next_pieces.append(tmp_next.pop(0))
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_piece((26, y_coord), next_p, 0, undraw=False, is_grid=False)
    draw_rect((23, 28), (30, 28), border_color)

def swap_hold_piece(new_piece):
    global hold_piece_key, next_pieces

    # swap
    if hold_piece_key == "":
        old_hold_piece_key = next_pieces.pop(0)
    else:
        old_hold_piece_key = hold_piece_key
    
    hold_piece_key = new_piece

    # redraw hold
    draw_rect((1, 3), (8, 8), border_color)
    draw_piece((4, 7), hold_piece_key, 0, is_grid=False)

    return old_hold_piece_key

def manage_level():
    global level
    
    pass

# check functions
def check_is_full():
    global floor_pieces
    return any([True for fp in floor_pieces if fp[1] < 1])

def check_clear_lines():
    global floor_pieces
    for y in range(24):
        if len([fp for fp in floor_pieces if fp[1] == y]) == 10:
            floor_pieces = [fp for fp in floor_pieces if fp[1] != y]
            grid.pop(y)
            grid.insert(0, [(0,0,0) for abc in range(10)])

def game_loop():
    global rotation, cursor_coord, next_pieces, floor_pieces, game_speed
    can_move = False
    already_hold = False

    # timers
    rotation_timer = time.time()
    hold_timer = time.time()
    move_timer = time.time()
    while True:
        if get_button_press("start") or check_is_full():
            init_game()
            can_move = False
        if not can_move:
            piece_key = next_pieces.pop(0)
            rotation = 0
            cursor_coord = [5, 1]
            manage_next_pieces()
            can_move = True

        draw_piece(cursor_coord, piece_key, rotation, undraw=True)
        
        # joystick controls
        if joystick_moved("left") and not is_collide((cursor_coord[0]-1, cursor_coord[1]), piece_key, rotation):
            cursor_coord[0]-=1
        if joystick_moved("right") and not is_collide((cursor_coord[0]+1, cursor_coord[1]), piece_key, rotation):
            cursor_coord[0]+=1
        if joystick_moved("down") and not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation):
            cursor_coord[1] += 1
        
        if get_button_press("hold") and not already_hold (time.time() - hold_timer > 0.05):
            piece_key = swap_hold_piece(piece_key)
            rotation = 0
            cursor_coord = [5, 1]
            manage_next_pieces()
            already_hold = True
            hold_timer = time.time()
        if get_button_press("drop"):
            drop_piece(piece_key, rotation)
        if get_button_press("rotate") and (time.time() - rotation_timer > 0.05):
            if not is_collide(cursor_coord, piece_key, rotation + 1):
                rotation += 1
            else:
                pass
            rotation_timer = time.time()
        
        # moving down / gravity
        if not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation, floor_only=True) and (time.time() - move_timer > game_speed):
            cursor_coord[1] += 1
            move_timer = time.time()
        else:
            for c in get_piece_coord((cursor_coord[0], cursor_coord[1]), get_piece(piece_key, rotation)):
                floor_pieces.append(c)
            can_move = False
            already_hold = False
        

        check_clear_lines()
        draw_piece(cursor_coord, piece_key, rotation)


        if rotation > 3:
            rotation = 0
        
        rotation = max(rotation_timer-time.time(), 0)
        draw_grid(grid)
        pixels.show()

if __name__ == "__main__":
    init_game()
    pixels.show()
    game_loop()