from manim import *
import sys

class Layer(VGroup):
    def __init__(self, n_nodes=4, n_right_steps=0, color=WHITE):
        super().__init__()
        # Crear nodos de la capa
        self.nodes = [Dot().shift(LEFT)]
        for i in range(1, n_nodes):
            self.nodes.append(Dot().next_to(self.nodes[i - 1], DOWN))
        self.add(*self.nodes)
        self.move_to(ORIGIN).shift(RIGHT * n_right_steps).set_color(color)
        if n_nodes > 10:
            self.scale(0.5)
        if n_nodes > 15:
            self.scale(0.35)

    def show_values(self, values):
        # Método para mostrar valores sobre cada nodo
        for i, value in enumerate(values):
            if i < len(self.nodes):
                text = MathTex(str(value)).next_to(self.nodes[i], RIGHT)
                self.nodes[i].add(text)

    def focus(self,index):
            node = self.nodes[index]
            return Succession(Indicate(node, scale_factor= 3))

class Connection(VGroup):
    def __init__(self, layer1, layer2):
        super().__init__()
        lines = []
        # Crear conexiones entre dos capas
        for prev_neuron in layer1.nodes:
            for next_neuron in layer2.nodes:
                line = Line(prev_neuron.get_center(), next_neuron.get_center(), stroke_width=1)
                lines.append(line)
                self.add(line)
                
    def focus(self,index):
        line = self.lines[index]
        return Succession(Indicate(line, scale_factor= 3))

class NeuralNetworkScene(Scene):
    def create_layers(self, sizes):
        # Crear las capas de la red neuronal
        layers = VGroup()
        for i, size in enumerate(sizes):
            color = YELLOW if i == 0 else (RED if i == len(sizes) - 1 else WHITE)
            layer = Layer(n_nodes=size, n_right_steps=-5 + 2 * i, color=color)
            layers.add(layer)
        layers.move_to(ORIGIN).scale(2)
        return layers

    def create_connections(self, layers):
        # Crear las conexiones entre capas
        connections = VGroup()
        for i in range(len(layers) - 1):
            connection = Connection(layers[i], layers[i + 1])
            connections.add(connection)
        return connections
# Capturar el argumento personalizado desde sys.argv

def str_to_list_numbers(text_with_numbers):
    # Eliminar espacios en blanco al principio y al final
    text_with_numbers = text_with_numbers.strip()
    
    list_of_numbers = []  # Lista para almacenar los números
    number = ""  # Usar cadena para acumular dígitos del número actual

    for char in text_with_numbers:
        if char.isdigit():  # Si el carácter es un dígito, agrégalo al número actual
            number += char
        elif number:  # Si encontramos un delimitador y ya tenemos un número acumulado
            list_of_numbers.append(int(number))  # Convertir la cadena en número y agregar a la lista
            number = ""  # Reiniciar el número

    # Agregar el último número si existe
    if number:
        list_of_numbers.append(int(number))

    return list_of_numbers


            

if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.startswith("--layers="):
            layers = arg.split("=")[1]
    print(layers)
    layers = str_to_list_numbers(layers)
    print(layers)

    
class Create_nn(NeuralNetworkScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layers = layers

    def construct(self):
        layers = self.create_layers(self.layers)  # Crear las capas
        connections = self.create_connections(layers)  # Crear las conexiones
        self.add(layers, connections)  # Añadir las capas a la escena
