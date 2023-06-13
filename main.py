from hardware import *
from machine import Pin
import time
import math
import random


cursor_coord = [0, 0]
rotation = 0
next_pieces = []
grid = [[(0, 0, 0) for i in range(10)] for x in range(24)]

def init_game():
    global next_pieces, cursor_coord, rotation
    # draw borders
    border_color = (69, 71, 105)
    border_color = (10, 10 ,10)
    draw_rect((1, 3), (8, 8), border_color) # hold box
    
    draw_rect((1, 10), (8, 20), border_color) # digits box
    
    draw_rect((10, 3), (21, 28), border_color) # game space
    
    draw_rect((23, 3), (30, 28), border_color) # next
    
    
    cursor_coord = [5, 1]
    rotation = 0
    next_pieces = [str(random.randint(0,6)) for x in range(6)]
    
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_pieces((26, y_coord), next_p, 0, is_grid=False)
    pixels.show()
        

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

def draw_pieces(coord, key, rotation, undraw=False, is_grid=True):
    global grid
    piece_colors = {
        "0": (103, 225, 230),
        "1": (56, 72, 214),
        "2": (222, 163, 44),
        "3": (247, 247, 87),
        "4": (88, 224, 67),
        "5": (161, 38, 209),
        "6": (217, 30, 55)

    }
    piece = get_piece(key, rotation)
    piece_coords = []
    for y in range(len(piece)):
        for x in range(len(piece[0])):
            if piece[y][x] == 1:
                piece_coords.append((x + coord[0], y + coord[1]))
    
    center_y, center_x = math.floor(len(piece)/2), math.floor(len(piece[0])/2)
    if not undraw:
        for x, y in piece_coords:
            color = piece_colors[key]
            if not is_grid:
                draw(x-center_x, y-center_y, color)
            else:
                grid[y-center_y][x-center_x] = color
    else:
        for x, y in piece_coords:
            color = piece_colors[key]
            if not is_grid:
                draw(x-center_x, y-center_y, (0,0,0))
            else:
                grid[y-center_y][x-center_x] = (0, 0, 0)

def manage_next_pieces():
    global next_pieces
    tmp_next = []
    
    draw_rect((24, 4), (29, 27), (0,0,0),border=False)

    if len(tmp_next) == 0:
        tmp_next = random_shuffle([str(x) for x in range(0, 7)])
    
    next_pieces.append(tmp_next.pop(0))
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_pieces((26, y_coord), next_p, 0, undraw=False, is_grid=False)
    draw_rect((23, 28), (30, 28), (10, 10 ,10))

def is_collide(new_cursor_coord, piece_key, rotation):
    piece = get_piece(piece_key, rotation)
    piece_coords = []
    center_y, center_x = math.floor(len(piece)/2), math.floor(len(piece[0])/2)
    
    for y in range(len(piece)):
        for x in range(len(piece[0])):
            if piece[y][x] == 1:
                piece_coords.append((x + new_cursor_coord[0]-center_x, y + new_cursor_coord[1]-center_y))
                
    # check out of bounds
    for pc_x, pc_y in piece_coords:
        if pc_x < 0 or pc_x > 9 or pc_y < 0 or pc_y > 23:
            return True
    
    # check touching floor
    return False

def game_loop():
    global rotation, cursor_coord, next_pieces
    can_move = False
    while True:
        if not can_move:
            piece_key = next_pieces.pop(0)
            manage_next_pieces()
            can_move = True

        draw_pieces(cursor_coord, piece_key, rotation, undraw=True)
        
        if joystick_moved("left") and not is_collide((cursor_coord[0]-1, cursor_coord[1]), piece_key, rotation):
            cursor_coord[0]-=1
        if joystick_moved("right") and not is_collide((cursor_coord[0]+1, cursor_coord[1]), piece_key, rotation):
            cursor_coord[0]+=1
        if joystick_moved("down") and not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation):
            cursor_coord[1] += 1
        
        if not is_collide((cursor_coord[0], cursor_coord[1]+1), piece_key, rotation):
            cursor_coord[1] += 1
        else:
            can_move = False
            cursor_coord = [5, 1]
        
        if get_button_press("rotate"):
            if not is_collide(cursor_coord, piece_key, rotation+1):
                rotation+= 1
            else:
                pass
            time.sleep(0.1)
        
        draw_pieces(cursor_coord, piece_key, rotation)
        if rotation > 3:
            rotation = 0
            time.sleep(0.1)
        
            
        
        draw_grid(grid)
        pixels.show()
        time.sleep(0.2)




init_game()
game_loop()


x = 0
y = 0

'''
while True:
    if joystick_moved("left"):
        x-=1
    if joystick_moved("right"):
        x+=1
    if joystick_moved("down"):
        y += 1
    draw(x, y, (20, 0, 64))
    pixels.show()
    
'''
"""
for i in range(1):
    pixels[i] = [0, 0, 64]
    pixels.show()
print(pixels)
for x in range(32):
    for y in range(32):
        draw(y,x,(30,10,0))
"""




