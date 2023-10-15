"""
Instructions given by teacher:

Make a tree program where it gives me the options to create, insert, delete and carry out the routes.

Made by:
- Sergio Barrera Chan
- Ariel Joel Buenfil Góngora
- Juan Antonio Cel Vazquez
- Diego Monroy Minero
"""

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.derecha = None
        self.izquierda = None

class Arbol:
    # Funciones privadas
    def __init__(self, dato):
        self.raiz = Nodo(dato)

    def __agregar_recursivo(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(dato)
            else:
                self.__agregar_recursivo(nodo.izquierda, dato)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(dato)
            else:
                self.__agregar_recursivo(nodo.derecha, dato)

    def __inorden_recursivo(self, nodo):
        if nodo is not None:
            self.__inorden_recursivo(nodo.izquierda)
            print(nodo.dato, end=", ")
            self.__inorden_recursivo(nodo.derecha)

    def __preorden_recursivo(self, nodo):
        if nodo is not None:
            print(nodo.dato, end=", ")
            self.__preorden_recursivo(nodo.izquierda)
            self.__preorden_recursivo(nodo.derecha)

    def __postorden_recursivo(self, nodo):
        if nodo is not None:
            self.__postorden_recursivo(nodo.izquierda)
            self.__postorden_recursivo(nodo.derecha)
            print(nodo.dato, end=", ")

    def __buscar(self, nodo, busqueda):
        if nodo is None:
            return None
        if nodo.dato == busqueda:
            return nodo
        if busqueda < nodo.dato:
            return self.__buscar(nodo.izquierda, busqueda)
        else:
            return self.__buscar(nodo.derecha, busqueda)

    # Funciones públicas

    def agregar(self, dato):
        self.__agregar_recursivo(self.raiz, dato)

    def recorrido_inorden(self):
        print("Imprimiendo árbol inorden: ")
        self.__inorden_recursivo(self.raiz)
        print("")

    def recorrido_preorden(self):
        print("Imprimiendo árbol preorden: ")
        self.__preorden_recursivo(self.raiz)
        print("")

    def recorrido_postorden(self):
        print("Imprimiendo árbol postorden: ")
        self.__postorden_recursivo(self.raiz)
        print("")

    def buscar(self, busqueda):
        return self.__buscar(self.raiz, busqueda)
    
    def borrar(self, dato):
        # Buscamos el nodo a borrar
        nodo = self.__buscar(self.raiz, dato)

        # Si el nodo no existe, no hay nada que hacer
        if nodo is None:
            return False

        # Si el nodo no tiene hijos, simplemente lo eliminamos
        if nodo.izquierda is None and nodo.derecha is None:
            self.raiz = None
            return True

        # Si el nodo tiene un solo hijo, lo reemplazamos por su hijo
        if nodo.izquierda is None:
            self.raiz = nodo.derecha
        elif nodo.derecha is None:
            self.raiz = nodo.izquierda

        # Si el nodo tiene dos hijos, reemplazamos el nodo por su sucesor inorden
        else:
            sucesor = self.__sucesor_inorden(nodo)
            self.raiz = sucesor
            sucesor.izquierda = self.__borrar_recursivo(nodo.izquierda)

        return True

    def __sucesor_inorden(self, nodo):
        # Buscamos el sucesor inorden del nodo
        while nodo.izquierda is not None:
            nodo = nodo.izquierda

        return nodo
    
    def crear_arbol(self, datos):
        nuevo_arbol = Arbol(datos[0])
        for dato in datos[1:]:
            self.agregar(dato, nuevo_arbol)

        return nuevo_arbol

if __name__ == '__main__':
    import os; os.system('cls')
    print(f'\n{"*"*10} Creación de un nuevo árbol el cual aplica las mismas funciones sobre el que se está creando. {"*"*10}\n')
    print("Precargando un arbol sobre el cual se pueden aplicar las funciones de agregar, borrar y recorrer.")
    arbol = Arbol("Diego")
    arbol.agregar("Juan")
    arbol.agregar("Sergio")
    arbol.agregar("Ariel")

    #Agregar
    nuevo_elemento = input("Ingresa algo para agregar al árbol: ")
    arbol.agregar(nuevo_elemento)
    #Recorrido del árbol
    print('\n')
    arbol.recorrido_preorden()
    arbol.recorrido_inorden()
    arbol.recorrido_postorden()
    #Eliminar
    nodo_eliminado = input("Ingresa lo que desee eliminar del árbol: ")
    arbol.borrar(nodo_eliminado)
    nodo = arbol.buscar(nodo_eliminado)
    #Volviendo a mostrar árbol
    print('\n')
    arbol.recorrido_preorden()
    arbol.recorrido_inorden()
    arbol.recorrido_postorden()

    print(f'\n{"*"*10} Creación de un nuevo árbol el cual aplica las mismas funciones sobre el que se está creando. {"*"*10}')
    #Crear
    nuevo = input("Ingrese el nodo padre: ")
    nuevo_arbol = Arbol(nuevo)
    nuevo_arbol.crear_arbol
    #Agregar
    nuevo_elemento = input("Ingresa algo para agregar al árbol: ")
    nuevo_arbol.agregar(nuevo_elemento)
    #Recorrido del árbol
    nuevo_arbol.recorrido_preorden()
    nuevo_arbol.recorrido_inorden()
    nuevo_arbol.recorrido_postorden()
    #Eliminar
    nodo_eliminado = input("Ingresa lo que desee eliminar del árbol: ")
    nuevo_arbol.borrar(nodo_eliminado)
    nodo = nuevo_arbol.buscar(nodo_eliminado)
    #Volviendo a mostrar árbol
    nuevo_arbol.recorrido_preorden()
    nuevo_arbol.recorrido_inorden()
    nuevo_arbol.recorrido_postorden()