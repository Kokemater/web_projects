from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from django.http import JsonResponse
import subprocess
import os
from django.templatetags.static import static

def main(request):
    return render(request, "main.html")

def editor(request):
    return render(request, 'editor.html')

def recibir_texto(request):
    if request.method == 'POST':
        texto = request.POST.get('inputText', '')
        texto = texto[2:-2]
        generar_video_manim(texto) 
        # Genera la URL relativa del video
        video_url = os.path.join(settings.MEDIA_URL, 'videos/temp_script/480p15/new.mp4')
        return render(request, 'watch_vid.html', {'video_url': video_url})
def generar_video_manim(texto):

    with open('temp_script.py', 'w') as f:
        f.write(f"""
from manim import *

class NameofAnimation(Scene):
    def construct(self):
        text = r"{texto}"
        math_text = MathTex(text)
        self.play(Write(math_text))
        self.wait(2)
""")

    subprocess.run(['manim', '-pql', 'temp_script.py', '-o', 'new'])
