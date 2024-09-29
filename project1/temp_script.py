
from manim import *
def count_letters_until_space(text, start_idx):
    count = 1
    for char in text[start_idx+1:]:
        if char in [' ', '\n', "{", "}", '_', '^']:
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
                if text[i:i+5] == r'\frac':  # Detectar el comienzo de una fracción
                    add_object_next_iteration = True
                    i += 5  # Avanza el índice al final de "\frac"
                    this_iteration = i
                elif text[i] in [' ', '\n', "{", "}", '_', '^']:  # Ignorar todo lo que no añada objeto matemático
                    n_spaces += 1
                    i += 1
                    continue
                elif text[i:i+2] == '\\,':
                    i+=2
                    continue
                    # Avanza el índice para ignorar la secuencia completa
                elif text[i:i+len(key)] == key:  # Detectar coincidencia con las palabras clave
                    letter_positions[ith_key].append(objects_count)
                    objects_count += 1
                    i += len(key)  # Avanza el índice según la longitud de la clave
                elif text[i] == '\\':
                    seq_length = count_letters_until_space(text, i)
                    objects_count += 1
                    i += seq_length
                else:
                    objects_count += 1
                    i += 1
                if add_object_next_iteration and not this_iteration == i:
                    objects_count += 1  # `\frac` agrega un nuevo objeto
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

        dictionary = {'p': '#bbff00', 'n': '#00c0f0'}
        # Crear objetos MathTex a partir de los textos
        for text in [f" p = np", " p -np = 0", " p(1 -n) = 0", " p = 0, n = 1", " q.e.d"]:       
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
