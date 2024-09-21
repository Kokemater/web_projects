
from manim import *

class NameofAnimation(Scene):
    def construct(self):
        text = r" \frac{1}{2} \sqrt{q2}"
        math_text = MathTex(text)
        self.play(Write(math_text))
        self.wait(2)
