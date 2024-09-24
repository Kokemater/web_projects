from django.shortcuts import render
from django.conf import settings
import subprocess
import os
from django.templatetags.static import static

def main(request):
    return render(request, "main.html")

def editor(request):
    return render(request, 'editor.html')

def recibir_texto(request):
    if request.method == 'POST':
        textos = {}
        for key in request.POST:
            if key.startswith("inputText"):
                textos[key] = request.POST[key]
                textos[key] = transformar_texto(textos[key])
        print(":::::::::::::::::::::::::")
        print(textos)
        print(":::::::::::::::::::::::::")
        generar_video_manim(textos) 
        # Genera la URL relativa del video
        video_url = os.path.join(settings.MEDIA_URL, 'videos/temp_script/480p15/new.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})
    
def transformar_texto(texto):
    # Elimina \(\ y \) del principio y del final
    if texto.startswith(r'\(') and texto.endswith(r'\)'):
        texto = texto[2:-2]  # Elimina los dos caracteres al principio y al final
    texto = texto.replace("\\", "\\\\")  # Duplica las barras invertidas para manejo de manim
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
                self.play(Transform(math_text[i-1], math_text[i]))
            self.wait(2)
            self.remove(math_text[i-1])

        self.play(Unwrite(math_text[-1])) 
""")

    subprocess.run(['manim', '-pql', 'temp_script.py', '-o', 'new'])
