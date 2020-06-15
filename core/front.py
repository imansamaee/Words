"""
Front module
==============

The Front module is ... :


"""
from kivy.uix.label import Label

from kivy.uix.widget import Widget


class PopUpWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.pop_up_1 = Label(pos_hint={'x': 0.5, 'y': 0.5},
                                  opacity=0,
                                  font_name="res/font/Far_Fanni",
                                  font_size="480",
                                  color=[1, 154, 23, 16])
