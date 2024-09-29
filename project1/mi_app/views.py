from django.shortcuts import render
from django.conf import settings
import subprocess
import os
from django.templatetags.static import static
from manim import *
from sympy.parsing.latex import parse_latex
from sympy import symbols, lambdify
from django.http import HttpResponse

def main(request):
    return render(request, "main.html")

def editor(request):
    return render(request, 'editor.html')

def graficar(request):
    if request.method == 'POST':
        latex_formula = request.POST.get('latex_function', '0')
        print(latex_formula)
        x_min = float(request.POST.get('x_min', '-5'))  # Valor mínimo de x
        x_max = float(request.POST.get('x_max', '5'))  # Valor máximo de x
        y_min = float(request.POST.get('y_min', '-5'))  # Valor mínimo de y
        y_max = float(request.POST.get('y_max', '5'))  # Valor máximo de y
        # Validar que los valores mínimos no sean mayores que los máximos
        if x_min > x_max:
            return HttpResponse("Error: El valor mínimo de x no puede ser mayor que el valor máximo de x.", status=400)
        if y_min > y_max:
            return HttpResponse("Error: El valor mínimo de y no puede ser mayor que el valor máximo de y.", status=400)

        command = ["manim", "-pqh", "manim_graph.py", "LatexFunctionGraph", "--", 
                   f"--formula={latex_formula}", 
                   f"--x_min={x_min}",  f"--x_max={x_max}",  f"--y_min={y_min}",f"--y_max={y_max}"]

        print(":::::::::")
        print(latex_formula)
        print(command)
        print(":::::::::")
        subprocess.run(command,check=True)
        video_url = os.path.join(settings.MEDIA_URL, 'videos/manim_graph/1080p60/LatexFunctionGraph.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})
        


def eliminar_espacios_vacios(diccionario):
    # Usamos una lista para almacenar las claves a eliminar
    claves_a_eliminar = []

    for clave, valor in diccionario.items():
        if isinstance(valor, str) and not valor.strip():  # Verifica si el valor es una cadena vacía después de eliminar espacios
            claves_a_eliminar.append(clave)

    # Eliminamos las claves acumuladas
    for clave in claves_a_eliminar:
        del diccionario[clave]

    return diccionario
def recibir_texto(request):
    if request.method == 'POST':
        textos = {}
        letter ={}
        color = {}
        for key in request.POST:
            print(request.POST[key])
            if key.startswith("inputText"):
                textos[key] = request.POST[key]
                textos[key] = transformar_texto(textos[key])
            if key.startswith("text_attribute"):
                letter[key] = request.POST[key]
            if key.startswith("color_attribute"):
                color[key] = request.POST[key]
        colors = {}
        for color_val, letter_val in zip(list(color.values()), list(letter.values())):
            colors[letter_val] = color_val  # Asocia la letra con el color

        print(colors)

        print(":::::::::::::::::::::::::")
        print(textos)
        textos = eliminar_espacios_vacios(textos)
        print(":::::::::::::::::::::::::")

        generar_video_manim(textos,colors) 
        # Genera la URL relativa del video
        video_url = os.path.join(settings.MEDIA_URL, 'videos/temp_script/1080p60/new.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})


def transformar_texto(texto):
    # Elimina \(\ y \) del principio y del final
    if texto.startswith(r'\(') and texto.endswith(r'\)'):
        texto = texto[2:-2]  # Elimina los dos caracteres al principio y al final
    texto = texto.replace("\\", "\\\\")  # Duplica las barras invertidas para manejo de manim
    #texto = texto.replace("{", "{{")  # Duplica las barras invertidas para manejo de manim
    #texto = texto.replace("}", "}}")  # Duplica las barras invertidas para manejo de manim

    for i in range(len(texto)):
        if texto[i] == '\n':
            return texto[:i-1]
    return texto

def generar_video_manim(textos,colors_dict):
    textos_str = ", ".join([f'"{text}"' for text in list(textos.values())])  # Formato correcto para el texto
    colors_dict_str = repr(colors_dict)  # o usar str(colors_dict) si no necesitas formateo específico
    with open('temp_script.py', 'w') as f:
        f.write(f"""
from manim import *
def count_letters_until_space(text, start_idx):
    count = 1
    for char in text[start_idx+1:]:
        if char in [' ', '\\n', "{{", "}}", '_', '^']:
            break
        count += 1
    return count

class ResolverEcuacion(Scene):
    def create_text_with_color(self, text=".", dictionary=dict()):
        # Almacena las posiciones ajustadas de cada palabra del diccionario
        letter_positions = []
        n_spaces = 0
        add_object_next_iteration = False
        this_iteration = 0
        # Recorre las claves del diccionario para buscar coincidencias en el texto
        for ith_key, key in enumerate(dictionary.keys()):
            letter_positions.append([])  # Crear una lista vacía para cada clave
            i = 0
            objects_count = 0
            # Analizar cada carácter en el texto para calcular posiciones
            while i < len(text):
                if text[i:i+5] == r'\\frac':  # Detectar el comienzo de una fracción
                    add_object_next_iteration = True
                    i += 5  # Avanza el índice al final de "\\frac"
                    this_iteration = i
                elif text[i] in [' ', '\\n', "{{", "}}", '_', '^']:  # Ignorar todo lo que no añada objeto matemático
                    n_spaces += 1
                    i += 1
                    continue
                elif text[i:i+2] == '\\\\,':
                    i+=2
                    continue
                    # Avanza el índice para ignorar la secuencia completa
                elif text[i:i+len(key)] == key:  # Detectar coincidencia con las palabras clave
                    letter_positions[ith_key].append(objects_count)
                    objects_count += 1
                    i += len(key)  # Avanza el índice según la longitud de la clave
                elif text[i] == '\\\\':
                    seq_length = count_letters_until_space(text, i)
                    objects_count += 1
                    i += seq_length
                else:
                    objects_count += 1
                    i += 1
                if add_object_next_iteration and not this_iteration == i:
                    objects_count += 1  # `\\frac` agrega un nuevo objeto
                    add_object_next_iteration = False

        # Crear el MathTex con el texto completo
        solution = MathTex(text)

        # Depuración de posiciones encontradas
        print(":::::::::::::::::::::")
        print("Posiciones de las claves en el texto:", letter_positions)

        # Recorrer cada subelemento en la expresión y obtener el texto
        for ith_key, key in enumerate(dictionary.keys()):
            for position in letter_positions[ith_key]:
                if position < len(solution[0]):
                    solution[0][position].set_color(dictionary[key])
        return solution

    def construct(self):
        math_text = []

        dictionary = {colors_dict_str}
        # Crear objetos MathTex a partir de los textos
        for text in [f{textos_str}]:       
            math_text.append(self.create_text_with_color(text, dictionary))  # Agrega cada MathTex a la lista

        # Mostrar los textos
        for i in range(len(math_text)):
            if i == 0:
                self.play(Write(math_text[i])) 
            else:
                self.add_sound("mi_app/static/sounds/swap.mp3")
                self.play(Transform(math_text[i-1], math_text[i]))
            self.wait(2)
            self.remove(math_text[i-1])

        self.play(Unwrite(math_text[-1])) 
""")

    subprocess.run(['manim', '-pqh', 'temp_script.py', '-o', 'new'])


def crear_video_con_formula(latex_expr):
    # Nombre del archivo de salida
    video_filename = "graph.mp4"
    video_path = os.path.join(settings.MEDIA_ROOT, "videos", video_filename)

    # Crear y renderizar la animación con Manim
    scene = LatexFunctionGraph(latex_expr)
    scene.render()
    
    # Mover el archivo a la carpeta de medios para su descarga
    os.rename(scene.renderer.file_writer.movie_file_path, video_path)

    return video_path

class LatexFunctionGraph(Scene):
    def __init__(self, latex_expr):
        super().__init__()
        self.latex_expr = latex_expr

    def plot_tex_func(self, latex_expr):
        # Definir la expresión en LaTeX
        latex_expr_mathTex = MathTex(r"f(x) = " + latex_expr)  # Para mostrar en la pantalla

        # Convertir la expresión LaTeX en una expresión simbólica de SymPy
        sympy_expr = parse_latex(latex_expr)

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
            x_range=[-5, 5],  # Rango de los valores x
            y_range=[-5, 30],  # Rango de los valores y
            axis_config={"color": BLUE},
        )

        # Graficar la función basada en la ecuación LaTeX
        graph = ax.plot(latex_expr_func, color=RED)

        # Etiquetar la gráfica
        graph_label = ax.get_graph_label(graph, label=latex_expr_mathTex)
        self.play(Create(ax), Create(graph), Write(graph_label))

    def construct(self):
        self.plot_tex_func(self.latex_expr)
        self.wait(2)
