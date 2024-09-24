
from manim import *

class NameofAnimation(Scene):
    def construct(self):
        math_text = []

        # Crear objetos MathTex a partir de los textos
        for text in [" \\emptyset  \\cap  \\text{>}  ", " \\beth  \\imath   "]:       
            math_text.append(MathTex(text))  # Agrega cada MathTex a la lista

        # Mostrar los textos
        for i in range(len(math_text)):
            if i == 0:
                self.play(Write(math_text[i])) 
            else:
                self.play(Transform(math_text[i-1], math_text[i]))
            self.wait(2)
            self.remove(math_text[i-1])

        self.play(Unwrite(math_text[-1])) 
