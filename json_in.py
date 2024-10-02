# input_program.py
import subprocess
import json

# Diccionario de ejemplo que quieres pasar
my_dict = {'a': '#ff0000', 'b': '#00ff00'}
text_2 = {'text': 'hola'}
# Convertir el diccionario a cadena JSON
dict_str = json.dumps(my_dict)
text_2 = json.dumps(text_2)

# Llamar a `output_program.py` y pasarle el diccionario como argumento
subprocess.run(['python', 'json_out.py', dict_str, text_2])
