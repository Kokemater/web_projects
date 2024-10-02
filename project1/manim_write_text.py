from manim import *
import json
import sys

texts = sys.argv[4]
colors = sys.argv[5]
texts = json.loads(texts)
colors = json.loads(colors)
print(texts)
print(colors)

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
    print("-1...........")
    # Si se recorrió toda la cadena y no se encontró el cierre, retornar -1
    return -1


def count_letters_until_space(text, start_idx):
    count = 1
    for char in text[start_idx+1:]:
        if char in [' ', '\\n', "{", "}", '_', '^', '\\', '!',"'", '"', "(", ")"]:
            break
        count += 1
    return count
def manage_sum(text, i):
    if i +4 < len(text) and text[i + 4] == '_':
        i = i + 5
        i += find_next_closed_key(text[i:]) +1
        if i < len(text) and text[i] == '^':
            return 3
        else:
            return 2
    else:
        return 1
def find_upper(text):
    for i in range(len(text)):
        if text[i] == '^':
            return i

class ResolverEcuacion(Scene):
    def create_text_with_color(self, text=".", dictionary=dict()):
        # Almacena las posiciones ajustadas de cada palabra del diccionario
        letter_positions = []

        add_object_in_iteration = 0
        # Recorre las claves del diccionario para buscar coincidencias en el texto
        for ith_key, key in enumerate(dictionary.keys()):
            letter_positions.append([])  # Crear una lista vacía para cada clave
            i = 0
            objects_count = 0
            add_object_in_iteration = []
            remove_object_in_iteration = []
            # Analizar cada carácter en el texto para calcular posiciones
            print(f"len ={len(text)}")
            while i < len(text):
                print(f"it= {i}, n_obj = {objects_count} ,{text[i]}")

                # \frac{\frac{12x}{x}}{x}
                if text[i] in [' ', '\n', "\r", "{", "}", '_', '^']:  # Ignorar todo lo que no añada objeto matemático
                    i += 1                    
                elif text[i:i+2] == '\\,':
                    i+=2
                else:
                    if text[i: i+4] == '\\sum':
                        if manage_sum(text, i) in [1, 2, 3]:
                            i+= 4
                            objects_count +=1

                    elif text[i:i+5] == '\\frac':
                        new = find_next_closed_key(text[i+5:]) + i + 5
                        add_object_in_iteration.append(new)
                        add_object_in_iteration.append(new)
                        i += 5  # Avanza el índice al final de "\\frac"
                    elif text[i:i+5] == "\\sqrt":
                        objects_count += 2
                        i += 5
                    elif text[i:i+4] in ["\\log","\\cos", "\\sin"]:
                        objects_count +=3
                        i += 4
                    elif text[i:i+len(key)] == key:  # Detectar coincidencia con las palabras clave
                        print("!!!!!!!!!")
                        letter_positions[ith_key].append(objects_count)
                        objects_count += 1
                        i += len(key)  # Avanza el índice según la longitud de la clave
                    elif text[i] == '\\':
                        seq_length = count_letters_until_space(text, i)
                        objects_count += 1
                        i += seq_length
                    elif text[i:i+7] in ["\\right)", "\\right]","\\right|"]:
                        objects_count += 1
                        i+=7
                    elif text[i:i+5] in ["\\left(","\\left[", "\\left|"]:
                        objects_count += 1
                        i+=5
                    else:
                        objects_count += 1
                        i += 1
                if i in add_object_in_iteration:
                    objects_count+=1
                for iter, n_obj in remove_object_in_iteration:
                    if i == iter:
                        objects_count -= n_obj
                if i < len(text):
                    print(f"it= {i}, n_obj = {objects_count}, {text[i]}")
        # Crear el MathTex con el texto completo
        solution = MathTex(text)
        for i in solution[0]:
            print(i)

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
        # Crear objetos MathTex a partir de los textos
        for text in texts.values():       
            math_text.append(self.create_text_with_color(text, colors))  # Agrega cada MathTex a la lista

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
