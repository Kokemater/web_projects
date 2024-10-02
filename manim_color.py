from manim import *

class Test(Scene):
    def construct(self):
        formula = MathTex("\\sum_{n=1}^{\infty}")
        formula[0][0].set_color(RED)
        formula[0][1].set_color(GREEN)
        formula[0][2].set_color(BLUE)
        self.add(formula)

def find_next_closed_key(expr):
    """{x^2}, return 4
    {x_{2} + 1} return 10
    """
    open_braces = 0
    for i in range(len(expr)):
        if expr[i] == '{':
            open_braces += 1  # Aumentar contador cuando se encuentra '{'
        elif expr[i] == '}':
            open_braces -= 1  # Disminuir contador cuando se encuentra '}'
        if open_braces == 0:
            return i
    # Si se recorrió toda la cadena y no se encontró el cierre, retornar -1
    return -1


    

