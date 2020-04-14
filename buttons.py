from gpiozero import Button
from signal import pause
import time

b = Button(2, bounce_time=0.0018, hold_time=1.5)

start = time.time()
print(start)

_in = 0
_out = 0


def released():
    global _out
    # _out = time.time_ns()
    print('released')
    # print('delta -> '+ str(_out-_in))
    # print('\n')


def pressed():
    # print('\n')
    # global _in
    # _in = time.time_ns()
    print('pressed')


def held():
    print('held')


b.when_released = released
b.when_pressed = pressed
b.when_held = held
pause()
