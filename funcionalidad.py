#Creacion del nodo Principal
class mainNodo:
    def __init__(self):
        self.dato = None
        self.next = None
        self.down = None

class nodosX:
    def __init__(self, data):
        self.posX = data
        self.next = None
        self.previous = None
        self.down = None

class nodosY:
    def __init__(self, data):
        self.posY = data
        self.right = None
        self.up = None
        self.down = None

class nodos:
    def __init__(self, data,posX,posY):
        self.data = data
        self.posX = posX
        self.posY = posY
        self.up = None
        self.right = None
        self.left = None
        self.down = None

#Clase para la creacion de cabeceras en X y Y
class listaCabeceras:
    def __init__(self):
        self.firstX = None
        self.firstY = None
        self.abajo = None
        self.lastX = None
        self.lastY = None

    def insertarX(self,mainNode,newNode):
        if self.firstX == None:
            newNode.previous = mainNode
            self.firstX = newNode
            mainNode.next = self.firstX
        else:
            aux = self.firstX
            while(aux.next != None):
                aux = aux.next
            newNode.previous = aux
            aux.next = newNode
        self.lastX = newNode

    def insertarY(self,mainNode,newNode):
        if self.firstY == None:
            newNode.up = mainNode
            self.firstY = newNode
            mainNode.down = self.firstY
        else:
            aux = self.firstY
            while(aux.down != None):
                aux = aux.down
            newNode.previous = aux
            aux.down = newNode
        self.lastY = newNode

    def show(self,mainNode):
        print("X:")
        aux = mainNode.next
        while(aux != None):
            print(aux.posX)
            aux = aux.next
        print("Y:")
        aux = mainNode.down
        while(aux != None):
            print(aux.posY)
            aux = aux.down
#Clase para creacion de nodos ingresados[Piezas]
class  nodosEnMatriz:
    def __init__(self):
        self.main = None

    def insertar(self,posX,posY,lista,newNode):
        #Movimiento en X
        varTemporalX = lista.next
        while(varTemporalX.posX != int(posX)):
            varTemporalX = varTemporalX.next
        listaX = varTemporalX.down

        #Insercion en X
        aux1X = listaX
        aux2X = aux1X

        while aux1X != None and int(aux1X.posY) < posY:
            aux2X = aux1X
            aux1X = aux1X.down

        if aux1X == listaX:
            listaX = newNode
        else:
            aux2X.down = newNode
        newNode.down = aux1X
        

    def show(self,posX,posY,lista):
        #Recorrido en X
        varTemporalX = lista.next

        while(varTemporalX.posX != int(posX)):
            varTemporalX = varTemporalX.next
        nodoEnX = varTemporalX.down
        
        while(nodoEnX != None):
            print(nodoEnX.posY)
            nodoEnX = nodoEnX.down
        
if __name__=='__main__':
    lCabeceras = listaCabeceras()
    nodoPrincipal = mainNodo()
    matriz = nodosEnMatriz()

    cabecerasX = input('Canidad de nodos de cabeceras en X: ')
    for i in range(int(cabecerasX)):
        lCabeceras.insertarX(nodoPrincipal,nodosX(i+1))

    cabecereasY = input('Canidad de nodos de cabeceras en Y: ')
    for i in range(int(cabecereasY)):
        lCabeceras.insertarY(nodoPrincipal,nodosY(i+1))
    
    posX = input('Ingresar valor para la posicion en X: ')
    val = input('Ingresar valor para guardar: ')
    matriz.insertar(posX,1,nodoPrincipal,nodos(val,posX,1))

    impX=input('Ingrese el valor para imprimir de la posicion X: ')
    matriz.show(impX,0,nodoPrincipal)
