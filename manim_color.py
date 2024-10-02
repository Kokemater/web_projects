from manim import *

import  re
def eliminar_espaciadores(texto):
    """
    Esta función elimina todos los caracteres espaciadores de un texto,
    incluyendo espacios, tabulaciones, saltos de línea, y retornos de carro.
    
    Args:
        texto (str): El texto del que se desea eliminar los espaciadores.
        
    Returns:
        str: El texto sin caracteres espaciadores.
    """
    # Usar una expresión regular para eliminar todos los espacios en blanco
    return re.sub(r'\s+', ' ', texto)

class VMatrixExample(Scene):
    def construct(self):
        # Define the content of the matrix
        matrix_content = r"\text{a)}\qquad\begin{vmatrix}a & b\\ a_1 & b_1\\\end{vmatrix}\neq0\quad\Rightarrow\quad\left\{\begin{array}{l}x=\xi+h\\y=\eta+k\end{array}\right.\quad,\quad h,k=\text{cte.}"
        matrix_content=  "\\text{a)}\\qquad\\begin{vmatrix}\r\na &     b\\\\\r\n        a_1 &                              b_1\\\\\r\n\\end{vmatrix}\\neq0\\quad\\Rightarrow\\quad\\                             left\\{\\begin{array}{l}\r\n        x=\\xi+h\\\\\r\n                               y=\\eta+k\r\n\\end{array}\\right.\\quad,\\quad                              h,k=\\text{cte.}"
        matrix_content = eliminar_espaciadores(matrix_content)
        # Create the MathTex object with the matrix
        matrix = MathTex(matrix_content)

        # Position the matrix in the center
        matrix.move_to(ORIGIN)

        # Add the matrix to the scene
        self.play(Write(matrix))
        self.wait(2)

# To run this, you need to use the following command:
# manim -pql your_file_name.py VMatrixExample

    

