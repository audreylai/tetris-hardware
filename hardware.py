import time
from neopixel import Neopixel

LEDS = 30 # How many LEDs?
PIN = 28
pixels = Neopixel(LEDS, 0, PIN, "GRB")

def draw(xin, yin, color):
    def pattern(r, c):
        if r <= 7:
            if c % 2 == 0:
                result = 7 * c + c + r
            elif c % 2 == 1:
                result = 7 * (c+1) - r + c
        if r > 7: #top half of the board
            result = grid[r-8][c] + 128
        return result

    grid = [[ 0 for x in range(16)] for y in range(16)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = pattern(y,x)
    coord = grid[yin][xin]

    pixels