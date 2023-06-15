from hardware import *
from machine import Pin
import time
import math
import random
from ulab import numpy


cursor_coord = [0, 0]
rotation = 0
next_pieces = []
grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]
floor_pieces = []

def init_game():
    global next_pieces, cursor_coord, rotation, floor_pieces, grid
    # draw borders
    border_color = (10, 10 ,10)
    draw_rect((1, 3), (8, 8), border_color) # hold box
    
    draw_rect((1, 10), (8, 20), border_color) # digits box
    
    draw_rect((10, 3), (21, 28), border_color) # game space
    
    draw_rect((23, 3), (30, 28), border_color) # next
    
    
    cursor_coord = [5, 1]
    rotation = 0
    next_pieces = [str(random.randint(0,6)) for x in range(6)]
    floor_pieces = []
    grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]
    
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_pieces((26, y_coord), next_p, 0, is_grid=False)
        

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

def draw_pieces(coord, key, rotation, undraw=False, is_grid=True):
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

def manage_next_pieces():
    global next_pieces
    tmp_next = []
    
    draw_rect((24, 4), (29, 27), (0,0,0), border=False)

    if len(tmp_next) == 0:
        tmp_next = random_shuffle([str(x) for x in range(0, 7)])
    
    next_pieces.append(tmp_next.pop(0))
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_pieces((26, y_coord), next_p, 0, undraw=False, is_grid=False)
    draw_rect((23, 28), (30, 28), (10, 10 ,10))

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
        
def check_is_full():
    global floor_pieces
    return any([True for fp in floor_pieces if fp[1] < 1])

def check_clear_lines():
    global floor_pieces
    for y in range(24):
        if len([fp for fp in floor_pieces if fp[1] == y]) == 10:
            print([fp for fp in floor_pieces if fp[1] == y])
            for fp in floor_pieces:
                if fp[1] == y:
                    floor_pieces.remove(fp)
            print([fp for fp in floor_pieces if fp[1] == y])
            grid.pop(y)
            grid.insert(0, [(0,0,0) for abc in range(10)])

def game_loop():
    global rotation, cursor_coord, next_pieces, floor_pieces
    can_move = False
    while True:
        if get_button_press("start") or check_is_full():
            init_game()
            can_move = False
        if not can_move:
            piece_key = next_pieces.pop(0)
            cursor_coord = [5, 1]
            manage_next_pieces()
            can_move = True

        draw_pieces(cursor_coord, piece_key, rotation, undraw=True)
        
        if joystick_moved("left") and not is_collide((cursor_coord[0]-1, cursor_coord[1]), piece_key, rotation):
            cursor_coord[0]-=1
        if joystick_moved("right") and not is_collide((cursor_coord[0]+1, cursor_coord[1]), piece_key, rotation):
            cursor_coord[0]+=1
        if joystick_moved("down") and not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation):
            cursor_coord[1] += 1
        
        if get_button_press("drop"):
            drop_piece(piece_key, rotation)
        
        if get_button_press("rotate"):
            if not is_collide(cursor_coord, piece_key, rotation + 1):
                rotation += 1
            else:
                pass
            time.sleep(0.01)
        
        if not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation, floor_only=True):
            cursor_coord[1] += 1
        else:
            for c in get_piece_coord((cursor_coord[0], cursor_coord[1]), get_piece(piece_key, rotation)):
                floor_pieces.append(c)
            can_move = False
        
        check_clear_lines()
        
        draw_pieces(cursor_coord, piece_key, rotation)
        if rotation > 3:
            rotation = 0
            time.sleep(0.1)
        
        draw_grid(grid)
        pixels.show()
        time.sleep(0.05)


init_game()
pixels.show()
game_loop()


