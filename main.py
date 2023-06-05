from hardware import *
from machine import Pin
import time

def init_game():
    border_color = (69, 71, 105)
    border_color = (10, 10 ,10)
    draw_rect((1, 3), (8, 8), border_color) # hold box
    
    draw_rect((1, 10), (8, 20), border_color) # digits box
    
    draw_rect((10, 3), (21, 28), border_color) # game space
    
    draw_rect((23, 3), (30, 28), border_color)


def draw_pieces(coord, key, rotation):
    pieces = {
        "0": [
                [1, 1, 1, 1]
            ],
        "1": [
                [1, 0, 0],
                [1, 1, 1]
            ],
        "2": [
                [0, 0, 1],
                [1, 1, 1]
            ],
        "3": [
                [1, 1, 0],
                [1, 1, 0]
            ],
        "4": [
                [0, 1, 1],
                [1, 1, 0]
            ],
        "5": [
                [0, 1, 0],
                [1, 1, 1]
            ],
        "6": [
                [1, 1, 0],
                [0, 1, 1]
            ],
    }
    piece = pieces[key]
    for i in range(rotation):
        # piece = list(zip(*piece))
        # piece = [list(reversed(x)) for x in piece]
        piece = list(list(x) for x in zip(*piece))[::-1]
    

    for x in range(len(piece[0])):
        for y in range(len(piece)):
            if piece[y][x] == 1:
                draw(coord[0]+x, coord[1]+y, (10, 10, 100))
    pixels.show()




init_game()
for i in range(4):
    draw_pieces((11,4), "0", i)
    time.sleep(1)
    draw_rect((11,4), (15,8), (0,0,0), False)


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


