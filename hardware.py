from machine import Pin
import time
from neopixel import Neopixel
import random

LEDS = 1024 # How many LEDs?
PIN = 28
pixels = Neopixel(LEDS, 0, PIN, "GRB")

def pattern(r, c):
        if r <= 15:
            if c % 2 == 0: # humanly odd, computationall even
                result = (16 * c) + r
            elif c % 2 == 1: # human even, computer odd
                result = 16 * c + 15 - r 
        if r > 15: #top half of the board
            result = grid[r-16][c] + 512
        #print(r, c, result, "hi")
        return result

def draw(xin, yin, color):
    coord = pattern(yin,xin)
    pixels[coord] = color

buttons = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [21, 20, 17, 18]]
joystick = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [12, 11, 10]]

grid = [[ 0 for x in range(32)] for y in range(32)]
for y in range(len(grid)):
    for x in range(len(grid[y])):
        grid[y][x] = pattern(y,x)

def get_pixel_val(x, y):
    coord = pattern(y,x)
    return pixels[coord]

def draw_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            draw(x+11, y+4, grid[y][x])

def get_button_press(key):
    ref = {
        "rotate": 0,
        "drop": 1,
        "hold": 2,
        "start": 3
    }
    return buttons[ref[key]].value()

def joystick_moved(key):
    ref = {
        "left":0,
        "right":1,
        "down":2
    }
    return joystick[ref[key]].value()

def draw_rect(coord1, coord2, color, border=True):
    x1, y1 = coord1
    x2, y2 = coord2
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            draw(x, y, color)
    
    if border:
        draw_rect((x1+1, y1+1), (x2-1, y2-1), (0,0,0), False)

def random_shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]
    return seq

def display_text(text, x, y, color):
    bf.text(text, x, y, color=color)