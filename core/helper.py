"""

Useful functions stored here.

"""
from arabic_reshaper import arabic_reshaper
import bidi.algorithm
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Line
from kivy.uix.label import Label


def rec_colliding(rec_1, rec_2):
    if rec_1.pos[0] - rec_2.size[0] / 2 < rec_2.pos[0] + rec_2.size[0] / 2 \
            and rec_2.pos[0] - rec_1.size[0] / 2 < rec_1.pos[0] + rec_1.size[0] / 2 \
            and rec_1.pos[1] + rec_1.size[1] / 2 > rec_2.pos[1] - rec_1.size[1] / 2 \
            and rec_2.pos[1] + rec_2.size[1] / 2 > rec_1.pos[1] - rec_2.size[1] / 2:
        colling = True
    else:
        colling = False
    return colling


def rec_is_touched(rec_1, touch_pos):
    colling = False
    if rec_1.pos[0] < touch_pos[0] < rec_1.pos[0] + rec_1.size[0] and \
            rec_1.pos[1] < touch_pos[1] < rec_1.pos[1] + rec_1.size[1]:
        colling = True
    return colling


# moving


def direction_factor(label: Label, *args):
    if label.pos[1] > Window.width or label.pos[1] < 0:
        x_d = -1
    else:
        x_d = 1
    if label.pos[0] > Window.height or label.pos[0] < 0:
        y_d = -1
    else:
        y_d = 1
    return x_d, y_d


def moving_dash_lines(line, factor: int):
    if line.dash_offset < factor + 1:
        line.dash_length = 50
        line.dash_offset = 50
    line.dash_length += factor
    line.dash_offset -= factor





def fix_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = bidi.algorithm.get_display(reshaped_text)
    return bidi_text
