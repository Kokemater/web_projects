from django.shortcuts import render
from django.conf import settings
import subprocess
import os
from django.templatetags.static import static
from manim import *
from sympy.parsing.latex import parse_latex
from sympy import symbols, lambdify
from django.http import HttpResponse
import json
import re

def main(request):
    return render(request, "main.html")

def sorting_algorithms(request):
    return render(request, "sorting_algorithms.html")

def editor(request):
    return render(request, 'editor.html')

def graph_funcs(request):
    return render(request, "grapher.html")

def machine_learning(request):
    return render(request, "machine_learning.html")

def send_sorting_algorithm(request):
    if request.method == 'POST':
        return HttpResponse("hi")
def neural_network(request):
        if request.method == 'POST':
            layers = request.POST.get('nn_create_layers', '0')
            command = ["manim", "-pqh", "manim_machine_learning.py", "Create_nn", "--", 
                    f"--layers={layers}"]
            subprocess.run(command,check=True)
            video_url = os.path.join(settings.MEDIA_URL + 'videos/manim_machine_learning/1080p60/Create_nn.mp4')
            return render(request, 'watch_vid.html', {'video_url': video_url})
def delete_spaces(texto):
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
        letter = {}
        color = {}
        latex_document = {}
        duration = {}
        # Procesar los datos enviados por POST
        for key in request.POST:
            if key.startswith("inputText"):
                textos[key] = request.POST[key]
                textos[key] = transformar_texto(textos[key])
                textos[key] = delete_spaces(textos[key])
            if key.startswith("text_attribute"):
                letter[key] = request.POST[key]
            if key.startswith("color_attribute"):
                color[key] = request.POST[key]
            if key.startswith("duration-"):
                duration[key] = request.POST[key]
            if key == "latex-content":
                latex_document[key] = request.POST[key]
                latex_document[key] = delete_spaces(latex_document[key])
        # Asocia las letras con los colores
        colors = {}
        for color_val, letter_val in zip(list(color.values()), list(letter.values())):
            colors[letter_val] = color_val
        print(duration)
        # Convertir a JSON escapado
        textos_json = json.dumps(textos)
        colors_json = json.dumps(colors)
        latex_document = json.dumps(latex_document)
        duration = json.dumps(duration)

        # Comando para ejecutar manim
        command = [
            "manim", "-pqh", "manim_write_text.py", "--",
            textos_json, colors_json, latex_document, duration
        ]
        # Ejecutar manim con subprocess
        subprocess.run(command, check=True)

        # Generar la URL del video de salida
        video_url = os.path.join(settings.MEDIA_URL + '/videos/manim_write_text/1080p60/ResolverEcuacion.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})
def transformar_texto(texto):
    # Elimina \(\ y \) del principio y del final
    if texto.startswith(r'\(') and texto.endswith(r'\)'):
        texto = texto[2:-2]  # Elimina los dos caracteres al principio y al final
    return texto

