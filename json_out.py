# output_program.py
import sys
import json

def main():
    # Leer el argumento (el diccionario en formato JSON)
    dict_str = sys.argv[1]
    text = sys.argv[2]
    
    # Convertir la cadena JSON a un diccionario de Python
    my_dict = json.loads(dict_str)
    text = json.loads(text)
    # Imprimir el diccionario
    print("Diccionario recibido:", my_dict)
    print("texto:", text )

if __name__ == "__main__":
    main()
