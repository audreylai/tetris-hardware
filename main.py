from hardware import *
from machine import Pin
import time
import math
import random


cursor_coord = [0, 0]
rotation = 0
next_pieces = []

def init_game():
    global next_pieces
    # draw borders
    border_color = (69, 71, 105)
    border_color = (10, 10 ,10)
    draw_rect((1, 3), (8, 8), border_color) # hold box
    
    draw_rect((1, 10), (8, 20), border_color) # digits box
    
    draw_rect((10, 3), (21, 28), border_color) # game space
    
    draw_rect((23, 3), (30, 28), border_color)
    
    
    cursor_coord = [15, 6]
    rotation = 0
    next_pieces = [str(random.randint(0,6)) for x in range(6)]
    
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_pieces((26, y_coord), next_p, 0)
        
    


def draw_pieces(coord, key, rotation, undraw=False):
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
    piece_colors = {
        "0": (103, 225, 230),
        "1": (56, 72, 214),
        "2": (222, 163, 44),
        "3": (247, 247, 87),
        "4": (88, 224, 67),
        "5": (161, 38, 209),
        "6": (217, 30, 55)

    }
    piece = pieces[key]
    for i in range(rotation):
        piece = list(zip(*piece))
        piece = [list(reversed(x)) for x in piece]
    
    center_y, center_x = math.floor(len(piece)/2), math.floor(len(piece[0])/2)
    if not undraw:
        for x in range(len(piece[0])):
            for y in range(len(piece)):
                if piece[y][x] == 1:
                    color = piece_colors[key]
                    draw(coord[0]+x-center_x, coord[1]+y-center_y, color)
    else:
        for x in range(4):
            for y in range(4):
                draw(coord[0]+x-center_x, coord[1]+y-center_y, (0,0,0))
    pixels.show()

def manage_next_pieces():
    global next_pieces
    next_pieces.append(str(random.randint(0,6)))
    for next_p, y_coord in zip(next_pieces, range(6,27,4)):
        draw_pieces((26, y_coord), next_p, 0, True)
        draw_pieces((26, y_coord), next_p, 0)
        

def game_loop():
    global rotation, cursor_coord, next_pieces
    can_move = False
    while True:
        if not can_move:
            piece = next_pieces.pop(0)
            manage_next_pieces()
            can_move = True

        if joystick_moved("left"):
            cursor_coord[0]-=1
        if joystick_moved("right"):
            cursor_coord[0]+=1
        if joystick_moved("down"):
            cursor_coord[1] += 1
        
        if piece == "0":
            limit_x = 0
        if cursor_coord[0] > 19:
            pass
        if get_button_press("rotate"):
            rotation+= 1
            time.sleep(0.1)
        

        draw_pieces(cursor_coord, piece, rotation, True)
        draw_pieces(cursor_coord, piece, rotation)
        if rotation > 3:
            rotation = 0
        time.sleep(1)




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



