# -*- coding: utf-8 -*-
'''
Lines Extended Demo
===================

This demonstrates how to use the extended line drawing routines such
as circles, ellipses, and rectangles. You should see a static image of
labelled shapes on the screen.
'''
import random
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line, Bezier, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage

from kivy.uix.widget import Widget
from core.front import PopUpWindow
from core.helper import *


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
        self.sound_pop_1 = SoundLoader.load("res/sound/effects/pop_1.wav")
        self.sound_background.play()

        Clock.schedule_interval(self.update_score, 0)

        self.bg = AsyncImage(source='res/images/background/loading.gif', anim_delay=0.01, pos=(400, 400))

        with self.canvas:
            Color(0.1, 0.4, 0.2, .7, mode="rgb")
            self.selected_1 = RoundedRectangle(size=(0, 0))
            Color(0.2, 0.1, 0.4, .7, mode="rgb")
            self.selected_2 = RoundedRectangle(size=(0, 0))
            Color(0, 0, 0, 0, mode="rgba")
            self.temp_label_rec = Rectangle()
            self.score_text = Label(pos=(Window.width - 230, Window.height - 100),
                                    text=fix_text(str(self.score)),
                                    font_name="res/font/Far_Fanni",
                                    font_size=dp("8"),
                                    halign='left',
                                    color=[0, 0, 1, 1])
            Color(0.2, 0.5, 0.2, 1, mode="rgba")
            self.answer_connection_line = Line(width=2)
            self.score_label = Label(pos=(Window.width - 150, Window.height - 100),
                                     text=fix_text("امتیاز : "),
                                     font_name="res/font/Far_Fanni",
                                     font_size=dp("8"),
                                     halign='left',
                                     color=[0, 0, 1, 1])

            self.answer_result_line_1 = Label(pos=(50, Window.height - 100),
                                              text=fix_text(""),
                                              font_name="res/font/Far_Fanni",
                                              font_size=dp("12"),
                                              halign='left',
                                              opacity=0,
                                              color=[0, 0, 1, 1])

            self.answer_result_line_2 = Label(pos=(50, Window.height - 130),
                                              font_name="res/font/Far_Fanni",
                                              font_size=dp("12"),
                                              halign='left',
                                              opacity=1,
                                              color=[0, 0, 1, 1])

            self.answer_result_line_3 = Label(pos=(50, Window.height - 160),
                                              font_name="res/font/Far_Fanni",
                                              font_size=dp("12"),
                                              halign='left',
                                              opacity=1,
                                              color=[0, 0, 1, 1])

            Color(0.2, 0.1, 0.4, 1, mode="rgba")
            self.score_line = Line(rectangle=(0, Window.height - 100,
                                              Window.width, Window.height),
                                   )

            self.labels = [Label(pos=(-500, 0),
                                 text=fix_text("ایمان سمائی"),
                                 font_name="res/font/Far_Fanni",
                                 font_size=dp("18"),
                                 color=[0, 0.3, 0, 1]) for i in range(100, 500, 50)]

        self.available_answer_box = 3
        self.available_answer_box_runs = True
        self.selected_word = None
        self._move_word = None
        self._move_word_direction_x = 5
        self._move_word_direction_y = 3
        self.selected_word_1 = self.labels[0]
        self.selected_word_2 = self.labels[1]
        for i in self.labels:
            i.size = self.label_size(i)

        Window.clearcolor = (.9, 1, 1, 1)
        self.selected_1_is_selected = False
        self.selected_2_is_selected = False
        self.selected_1_new_pos = None
        self.selected_2_new_pos = None
        self.init_labels()

    def init_labels(self):
        for i in self.labels:
            self.appear_word_randomly(i, 0)

    #################
    # Animation
    #################
    def appear_word_randomly(self, target_object: Label, _duration):
        self.sound_pop_1.play()
        _height = 100
        x = [i for i in range(200, Window.height - 300, 100)]
        _list = random.sample(x, len(x))
        current_list = [i.pos[1] for i in self.labels]
        for i in _list:
            if i not in current_list:
                _height = i
                break
        target_object.pos = (round(Window.width * random.random() * .6), _height)
        anim = Animation(pos=(target_object.pos[0] + 20, target_object.pos[1]), duration=0.1)
        anim += Animation(pos=(target_object.pos[0] - 15, target_object.pos[1]), duration=0.1)
        anim += Animation(pos=(target_object.pos[0] + 10, target_object.pos[1]), duration=0.1)
        anim += Animation(pos=(target_object.pos[0] - 5, target_object.pos[1]), duration=0.2)
        anim += Animation(duration=_duration)
        anim += Animation(pos=target_object.pos, duration=.02)
        anim.bind(on_complete=self.recover_words_position)
        anim.start(target_object)

    def couple_answers(self):
        # self.move_word_up("selected_1")
        # self.move_word_up("selected_2")
        self.selected_1.pos = self.selected_2.pos = (-500, 0)
        self.move_word_up("selected_word_1")
        self.move_word_up("selected_word_2")
        self._couple_lines()

    def move_word_up(self, _object):
        self.pop_up_1.text = fix_text(str(self.added_score))
        target_object = self.__dict__[_object]
        new_pos = self.__dict__["selected_" + _object[-1] + "_new_pos"]
        if self.__dict__[_object].__class__ == list:
            l_size = self.label_size(target_object)
            new_pos = (new_pos[0], new_pos[1] + l_size[1])
        anim = Animation(pos=(Window.width / 2, Window.height / 2), duration=.2)
        anim += Animation(pos=new_pos, duration=.2)
        anim += Animation(duration=.5)
        anim += Animation(pos=(-500, 0), duration=0)
        anim.start(target_object)

    def _couple_lines(self):
        _points_1 = [50,
                     Window.height - 200,
                     Window.width - 50,
                     Window.height - 200]
        _points_2 = [Window.width / 2,
                     Window.height - 200,
                     Window.width / 2,
                     Window.height - 200]
        anim = Animation(points=_points_2, duration=.2)
        anim += Animation(points=_points_1, duration=.2)
        anim += Animation(points=_points_2, duration=.2)
        anim.start(self.answer_connection_line)

    def show_score_1(self):
        self.calculate_score()
        self.pop_up_1.text = fix_text(str(self.added_score))
        anim = Animation(opacity=1, duration=.4)
        anim += Animation(opacity=0, duration=.2)
        anim.start(self.pop_up_1)

    def fade_results(self, w):
        self.recover_words_position()
        if w:
            _pos = w.pos
            anim = Animation(opacity=1, duration=1)
            anim += Animation(pos=(_pos[0] + 50, _pos[1]), duration=.1)
            anim += Animation(pos=(_pos[0] - 50, _pos[1]), duration=.1)
            anim += Animation(pos=(_pos[0], _pos[1]), opacity=0, duration=.1)
            anim.bind(on_complete=self.answer_result_not_busy)
            anim.start(w)

    def answer_result_not_busy(self, *args):
        self.available_answer_box += 1

    def available_answer_result(self):
        if 0 < self.available_answer_box:
            name = "answer_result_line_" + str(4 - self.available_answer_box)
            if 3 < self.available_answer_box:
                name = None
        else:
            self.available_answer_box_runs = False
            name = None
        return name

    def move_selected(self, w, i: Label):
        _selected_pos = (i.pos[0] - 20, i.pos[1] - 20)
        _selected_size = (i.size[0] + 40, i.size[1] + 40)
        anim = Animation(pos=_selected_pos, size=_selected_size, duration=.05)
        anim.bind(on_complete=self.analyse_results)
        anim.start(w)

    #################
    # score
    #################

    def update_score(self, *args):
        if self.score < self.current_score:
            self.score += 5
            self.score_text.text = fix_text(str(self.score))

    def calculate_score(self):
        score = None
        if self.right_answer:
            score = round(1000 * random.random())
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

    # def _move_selected_1(self, *args):
    #     move_selected(self.selected_1, self.selected_word)
    #
    # def _move_selected_2(self, *args):
    #     move_selected(self.selected_2, self.selected_word)
    def recover_words_position(self, *args):
        self.sound_pop_1.stop()
        for i in self.labels:
            if i.pos[0] == -500:
                self.appear_word_randomly(i, 0.8)
                break

    def move_word(self, *args):
        self._through_label(self.selected_word_1, 1, direction_factor(self.selected_word_1)[1] * 50)
        self._through_label(self.selected_word_1, 0, direction_factor(self.selected_word_1)[0] * 40)

    def touched_words(self, touch):
        list_of_targets = self.labels
        label_index_list = []

        for key, value in enumerate(list_of_targets):
            value.size = self.label_size(value)
            rec_1 = self.temp_label_rec
            if rec_is_touched(rec_1, touch.pos):
                self.selected_word = value
                label_index_list.append(key)
                if self.selected_1_is_selected:
                    self.selected_word_1 = value
                else:
                    self.selected_word_2 = value
        return label_index_list

    def label_size(self, label: Label):
        size = (len(label.text) *
                int(label.font_size) * .7,
                int(label.font_size) * 1.2)
        self.temp_label_rec.size = size
        self.temp_label_rec.pos = label.pos
        return size

    #################
    # Results
    #################

    def analyse_results(self, *args):
        if self.selected_2_is_selected:
            self.answer_connection_line.points = [Window.width / 2,
                                                  Window.height + 50,
                                                  Window.width / 2,
                                                  Window.height + 50]
            if self.available_answer_result():
                w = self.__dict__[self.available_answer_result()]
                if self.available_answer_box == 3:
                    self.available_answer_box_runs = True
                self.available_answer_box -= 1
                w.text = self.selected_word_1.text + " = " + self.selected_word_2.text
                w.color = [0, .4, .2, 1]
                if self.available_answer_box_runs:
                    self.fade_results(w)
            else:
                self.available_answer_box = 3
            self.couple_answers()

    #################
    # Events
    #################

    def on_touch_up(self, touch):
        for i in self.touched_words(touch):
            selected_label = self.labels[i]
            if not self.selected_1_is_selected:
                self.selected_1_new_pos = Window.width - 10 - self.selected_1.size[0], Window.height - 200
                self.selected_2_new_pos = 60, Window.height - 200
                self.move_selected(self.selected_1, selected_label)
                self.selected_1_is_selected = True
                self.selected_2_is_selected = False
            else:
                self.move_selected(self.selected_2, selected_label)
                self.selected_2_is_selected = True
                self.selected_1_is_selected = False

            self.right_answer = True
            self.show_score_1()


class WordsApp(App):
    def build(self):
        root = FloatLayout()
        root.add_widget(MainLayer())
        return root


if __name__ == '__main__':
    WordsApp().run()
