from hardware import *
from machine import Pin
import time

# while True:
#     if get_button_press("rotate"):
#         print("Button is being pressed")
#     else:
#         print("Button is not pressed")
#     time.sleep(0.1)

for x in range(32):
    for y in range(32):
        draw(y,x,(255,255,255))