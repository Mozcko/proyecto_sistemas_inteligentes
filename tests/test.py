class ListaReversible:
    def __init__(self, lista) -> None:
        self.lista = lista

    def obtener_ultimo_y_eliminar(self):
        if self.lista:
            return self.lista.pop()
        else:
            return None

# Ejemplo de uso
mi_lista = [1, 2, 3, 4, 5]
reversible = ListaReversible(mi_lista)

print(reversible.obtener_ultimo_y_eliminar())  # Salida: 5
print(reversible.obtener_ultimo_y_eliminar())  # Salida: 4
print(reversible.obtener_ultimo_y_eliminar())  # Salida: 3

print(mi_lista)

