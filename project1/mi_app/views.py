from django.shortcuts import render
from django.conf import settings
import subprocess
import os
from django.templatetags.static import static


def main(request):
    return render(request, "main.html")

def editor(request):
    return render(request, 'editor.html')

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
        print(color)
        print(":::::::::::::::::::::::::")

        generar_video_manim(textos) 
        # Genera la URL relativa del video
        video_url = os.path.join(settings.MEDIA_URL, 'videos/temp_script/1080p60/new.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})



def transformar_texto(texto):
    # Elimina \(\ y \) del principio y del final
    if texto.startswith(r'\(') and texto.endswith(r'\)'):
        texto = texto[2:-2]  # Elimina los dos caracteres al principio y al final
    texto = texto.replace("\\", "\\\\")  # Duplica las barras invertidas para manejo de manim
    for i in range(len(texto)):
        if texto[i] == '\n':
            return texto[:i-1]
    return texto

def generar_video_manim(textos):
    textos_str = ", ".join([f'"{text}"' for text in reversed(list(textos.values()))])  # Formato correcto para el texto

    with open('temp_script.py', 'w') as f:
        f.write(f"""
from manim import *

class NameofAnimation(Scene):
    def construct(self):
        math_text = []

        # Crear objetos MathTex a partir de los textos
        for text in [{textos_str}]:       
            math_text.append(MathTex(text))  # Agrega cada MathTex a la lista

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
