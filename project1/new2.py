from manim import *

class NameofAnimation(Scene):

    def construct(self):
        def write_text(self, text):
            Text = MathTex(text)
            self.play(Write(Text))
        text = r"\frac{1}{2} = 2\frac{1}{4}"
        write_text(self, text)
        