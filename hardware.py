from machine import Pin
import time
from neopixel import Neopixel

LEDS = 30 # How many LEDs?
PIN = 28
pixels = Neopixel(LEDS, 0, PIN, "GRB")


buttons = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [21, 20, 17, 18]]


def draw(xin, yin, color):
    def pattern(r, c):
        if r <= 15:
            if c % 2 == 0: # humanly odd, computationall even
                result = (16 * c) + r
            elif c % 2 == 1: # human even, computer odd
                result = 16 * (c+1) - r - 1
        if r > 15: #top half of the board
            result = grid[r-16][c] + 512
        return result
            
            

    grid = [[ 0 for x in range(32)] for y in range(32)]
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[y][x] = pattern(y,x)
    coord = grid[yin][xin]

    pixels[coord] = color

def get_button_press(key):
    key = {
        "rotate": 0,
        "drop": 1,
        "hold": 2,
        "start": 3
    }
    
    return buttons[key].value()


