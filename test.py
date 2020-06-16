from kivy.app import App
from kivy.lang import Builder

kv = """
<Test@AnchorLayout>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    AsyncImage:
        source: 'res/images/background/loading.gif'
        anim_delay: 0.01
Test:
"""


class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    TestApp().run()