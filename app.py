import numpy as np
nombre = input("Ingrese su nombre: ")
print(f"Hola Mundo, y particularmente a {nombre}")
print(f"El seno de la longitud del nombre es: {np.sin(len(nombre))}")