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

def main(request):
    return render(request, "main.html")

def editor(request):
    return render(request, 'editor.html')
def graph_funcs(request):
    return render(request, "grapher.html")
def machine_learning(request):
    return render(request, "machine_learning.html")

def neural_network(request):
        if request.method == 'POST':
            print("!!!!!!!!!!!!!!!!")
            layers = request.POST.get('nn_create_layers', '0')
            command = ["manim", "-pqh", "manim_machine_learning.py", "Create_nn", "--", 
                    f"--layers={layers}"]
            subprocess.run(command,check=True)
            video_url = os.path.join(settings.MEDIA_URL + 'videos/manim_machine_learning/1080p60/Create_nn.mp4')
            return render(request, 'watch_vid.html', {'video_url': video_url})

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
        # Procesar los datos enviados por POST
        for key in request.POST:
            if key.startswith("inputText"):
                textos[key] = request.POST[key]
                textos[key] = transformar_texto(textos[key])
            if key.startswith("text_attribute"):
                letter[key] = request.POST[key]
            if key.startswith("color_attribute"):
                color[key] = request.POST[key]
        # Asocia las letras con los colores
        colors = {}
        for color_val, letter_val in zip(list(color.values()), list(letter.values())):
            colors[letter_val] = color_val

        # Convertir a JSON escapado
        textos_json = json.dumps(textos)
        colors_json = json.dumps(colors)

        # Comando para ejecutar manim
        command = [
            "manim", "-pqh", "manim_write_text.py", "--",
            textos_json, colors_json
        ]

        try:
            # Imprimir los argumentos antes de ejecutar
            print("Textos JSON:", textos_json)
            print("Colores JSON:", colors_json)
            
            # Ejecutar manim con subprocess
            subprocess.run(command, check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando manim: {e}")
            return render(request, 'error.html', {'error_message': str(e)})

        # Generar la URL del video de salida
        video_url = os.path.join(settings.MEDIA_URL + '/videos/manim_write_text/1080p60/ResolverEcuacion.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})
def transformar_texto(texto):
    # Elimina \(\ y \) del principio y del final
    if texto.startswith(r'\(') and texto.endswith(r'\)'):
        texto = texto[2:-2]  # Elimina los dos caracteres al principio y al final
    return texto

