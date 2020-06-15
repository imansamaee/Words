# -*- coding: utf-8 -*-
'''
Lines Extended Demo
===================

This demonstrates how to use the extended line drawing routines such
as circles, ellipses, and rectangles. You should see a static image of
labelled shapes on the screen.
'''
from random import Random, random

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line, Bezier, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.gridlayout import GridLayout

from kivy.uix.widget import Widget
from core.front import PopUpWindow
from core.helper import *

touch_circle_size = 40


class MainLayer(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_i = 0
        self.score = 0
        self.added_score = 0
        self.current_score = 0
        self.right_answer = False
        self.pop_up_1 = PopUpWindow()
        # sound:
        self.sound_background = SoundLoader.load("res/sound/word/start_action.wav")
        self.sound_hit = SoundLoader.load("res/sound/effects/beep.ogg")
        self.sound_background.play()
        self.selected_1_is_selected = False
        self.selected_2_is_selected = False

        Clock.schedule_interval(self.update_score, 0)

        with self.canvas:
            Color(0, .1, 2, 1, mode="rgba")
            self.selected_1 = RoundedRectangle(size=(0, 0))
            Color(0, 1, 0, 1, mode="rgba")
            self.selected_2 = RoundedRectangle(size=(0, 0))
            Color(0, 0, 0, 0, mode="rgba")
            self.temp_label_rec = Rectangle(size=(0, 0))

            self.score_text = Label(pos=(Window.width - 230, Window.height - 100),
                                    text=fix_text(str(self.score)),
                                    font_name="res/font/Far_Fanni",
                                    font_size="24",
                                    halign='left',
                                    color=[0, 0, 1, 1])
            self.score_label = Label(pos=(Window.width - 150, Window.height - 100),
                                     text=fix_text("امتیاز : "),
                                     font_name="res/font/Far_Fanni",
                                     font_size="24",
                                     halign='left',
                                     color=[0, 0, 1, 1])

            self.answer_result = Label(pos=(150, Window.height - 100),
                                       text=fix_text(""),
                                       font_name="res/font/Far_Fanni",
                                       font_size="24",
                                       halign='left',
                                       color=[0, 0, 1, 1])

            Color(160, 92, 56, 1, mode="rgba")
            self.score_line = Line(rectangle=(0, Window.height - 100,
                                              Window.width, Window.height),
                                   )

            self.main_word = Label(pos=(20, 600),
                                   text=fix_text("سارا بیات"),
                                   font_name="res/font/Far_Fanni",
                                   font_size="24",
                                   color=[1, 0, 1, 1])

            self.syn_word = Label(pos=(50, 150),
                                  text=fix_text("ایمان سمائی"),
                                  font_name="res/font/Far_Fanni",
                                  font_size="24",
                                  color=[1, 0, 1, 1])
        self.selected_word = self.main_word
        self._move_word = None
        self._move_word_direction_x = 5
        self._move_word_direction_y = 3
        self.main_word.size = self.label_size(self.main_word)
        self.syn_word.size = self.label_size(self.syn_word)
        Window.clearcolor = (.9, 1, 1, 1)

    #################
    # score
    #################

    def update_score(self, *args):
        if self.score < self.current_score:
            self.score += 5
            self.score_text.text = fix_text(str(self.score))

    def show_score_1(self):
        self.calculate_score()
        self.pop_up_1.text = fix_text(str(self.added_score))
        anim = Animation(opacity=1, duration=.4)
        anim += Animation(opacity=0, duration=.2)
        anim.start(self.pop_up_1)

    def calculate_score(self):
        score = None
        if self.right_answer:
            score = round(1000 * random())
            self.current_score = self.score + score
            self.added_score = score
        self.right_answer = False
        return score

    #################
    # Sound
    #################

    def change_background_sound(self, sound_url):
        self.sound_background.stop()
        self.sound_background = SoundLoader.load(sound_url)
        self.sound_background.play()

    #################
    # position
    #################

    def _move_selected_1(self, *args):
        move_selected(self.selected_1, self.selected_word)

    def _move_selected_2(self, *args):
        move_selected(self.selected_2, self.selected_word)

    def move_word(self, *args):
        self._through_label(self.main_word, 1, direction_factor(self.main_word)[1] * 50)
        self._through_label(self.main_word, 0, direction_factor(self.main_word)[0] * 40)

    def animate(self):
        self._move_word = Clock.schedule_interval(
            self.move_word, 0)

    def touched_words(self, touch):
        list_of_targets = [self.main_word, self.syn_word]
        list_of_touched_elements = []

        for i in list_of_targets:
            i.size = self.label_size(i)
            rec_1 = self.temp_label_rec
            if rec_is_touched(rec_1, touch.pos):
                self.selected_word = i
                list_of_touched_elements.append(i)
        return list_of_touched_elements

    def label_size(self, label: Label):
        size = (len(label.text) *
                int(label.font_size) * .6,
                int(label.font_size) * .8)
        self.temp_label_rec.size = size
        self.temp_label_rec.pos = label.pos
        return size

    def through_syn_word_up(self, *args):
        self._through_label(self.syn_word, 1, direction_factor(self.syn_word)[1] * 50)
        self._through_label(self.syn_word, 0, direction_factor(self.syn_word)[0] * 40)

    def _through_label(self, label: Label, direction, velocity, *args):
        _size = self.label_size(label)
        _pos = label.pos
        if _pos[direction] + _size[direction] / 2 < Window.width:
            label.pos[direction] += velocity

    #################
    # Results
    #################

    def analyse_results(self, *args):
        print("okk")
        if self.selected_2_is_selected:
            self.answer_result.text = self.main_word.text + " = " + self.syn_word.text
            self.answer_result.color = [0, .4, .2, 1]
            self.fade_results()

    def fade_results(self):
        w = self.answer_result
        w.opacity = 1
        _pos = self.answer_result.pos
        anim = Animation (duration=1)
        anim += Animation(pos=(_pos[0] + 50, _pos[1]), duration=.1)
        anim += Animation(pos=(_pos[0] - 50, _pos[1]), duration=.1)
        anim += Animation(pos=(_pos[0], _pos[1]), opacity=0, duration=.5)
        # anim.bind(on_complete=self.analyse_results)
        anim.start(w)



    #################
    # Events
    #################

    def on_touch_up(self, touch):

        for i in self.touched_words(touch):
            if not self.selected_1_is_selected:
                self.move_selected(self.selected_1, i)
                self.selected_1_is_selected = True
                self.selected_2_is_selected = False
            else:
                self.move_selected(self.selected_2, i)
                self.selected_2_is_selected = True
                self.selected_1_is_selected = False

            self.right_answer = True
            self.show_score_1()

    def move_selected(self, w, i: Label):
        _selected_pos = (i.pos[0] - 20, i.pos[1] - 20)
        _selected_size = (i.size[0] + 40, i.size[1] + 40)
        anim = Animation(pos=_selected_pos, size=_selected_size, duration=.05)
        anim.bind(on_complete=self.analyse_results)
        anim.start(w)


class WordsApp(App):
    def build(self):
        root = FloatLayout()
        root.add_widget(MainLayer())
        return root


if __name__ == '__main__':
    WordsApp().run()
