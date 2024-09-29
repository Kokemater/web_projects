from manim import *
from sympy.parsing.latex import parse_latex
from sympy import symbols, lambdify
import sys  # Módulo para leer argumentos desde la línea de comandos

# Leer el argumento de la fórmula desde sys.argv
latex_formula = r"0"  # Valor predeterminado
x_min = -5
x_max = 5
y_min = -5
y_max = 5

# Capturar el argumento personalizado desde sys.argv
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.startswith("--formula="):
            latex_formula = arg.split("=")[1]
        if arg.startswith("--x_min="):
            x_min = float(arg.split("=")[1])
        elif arg.startswith("--x_max="):
            x_max = float(arg.split("=")[1])
        elif arg.startswith("--y_min="):
            y_min = float(arg.split("=")[1])
        elif arg.startswith("--y_max="):
            y_max = float(arg.split("=")[1])

# Clase para representar el gráfico de la función LaTeX
class LatexFunctionGraph(Scene):
    def __init__(self, latex_expr=latex_formula, **kwargs):
        super().__init__(**kwargs)
        self.latex_expr = latex_expr
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def plot_tex_func(self):
        # Definir la expresión en LaTeX para mostrarla
        latex_expr_mathTex = MathTex(r"f(x) = " + self.latex_expr)

        # Convertir la expresión LaTeX en una expresión simbólica de SymPy
        sympy_expr = parse_latex(self.latex_expr)

        # Definir la variable independiente
        x = symbols('x')

        # Convertir la expresión de SymPy en una función evaluable por Manim
        latex_expr_func = lambdify(x, sympy_expr)

        # Mostrar la expresión en la parte superior de la pantalla
        self.play(Write(latex_expr_mathTex))
        self.wait(2)

        # Mover la expresión a la esquina superior izquierda para dejar espacio a la gráfica
        latex_expr_mathTex.to_corner(UP + LEFT)

        # Definir la gráfica de la función
        ax = Axes(
            x_range=[self.x_min, self.x_max],  # Rango de los valores x
            y_range=[self.y_min, self.y_max],  # Rango de los valores y
            axis_config={"color": BLUE},
        )

        # Graficar la función basada en la ecuación LaTeX
        graph = ax.plot(latex_expr_func, color=RED)

        # Etiquetar la gráfica
        graph_label = ax.get_graph_label(graph, label=latex_expr_mathTex)
        self.play(Create(ax), Create(graph), Write(graph_label))

    def construct(self):
        self.plot_tex_func()
        self.wait(2)

# Esto asegura que se ejecute correctamente cuando se llame desde la línea de comandos
if __name__ == "__main__":
    scene = LatexFunctionGraph()
    scene.render()
