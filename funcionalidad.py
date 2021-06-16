from GameView import *
from PyQt5.QtGui import * 
import random
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
        aux2X = None
        
        while(varTemporalX.posX != int(posX)):
            varTemporalX = varTemporalX.next
        listaX = varTemporalX
        
        if listaX.down ==  None:
            listaX.down = newNode
            newNode.up = listaX
        else:
            aux1X = listaX.down
            while(aux1X != None and aux1X.posY < posY):
                aux2X = aux1X
                aux1X = aux1X.down
            if aux2X != None:
                aux2X.down = newNode
                newNode.up = aux2X
            else:
                listaX.down = newNode
                newNode.up = listaX
            aux1X.up = newNode
            newNode.down = aux1X
            
        #Movimiento en Y
        varTemporalY = lista.down
        aux2Y = None

        while(varTemporalY.posY != int(posY)):
            varTemporalY = varTemporalY.down
        listaY = varTemporalY

        if listaY.right == None:
            listaY.right = newNode
            newNode.left = listaY
        else:
            aux1Y = listaY.right
            while aux1Y != None and aux1Y.posX < posX:
                aux2Y = aux1Y
                aux1Y = aux1Y.right
            if aux2Y != None:
                aux2Y.right = newNode
                newNode.left = aux2Y
            else:
                listaY.right = newNode
                newNode.left = listaY
            aux1Y.left = newNode
            newNode.right = aux1Y
    def show(self,posX,posY,lista):
        listaCabeceraX = lista.next

        while listaCabeceraX.posX != int(posX):
            listaCabeceraX = listaCabeceraX.next
        nodosEnX = listaCabeceraX.down
        
        while int(nodosEnX.posY) < int(posY):
            nodosEnX = nodosEnX.down
        
        print(nodosEnX.data)

class figuras:
    def __init__(self,id):
        self.id = id
#Clases para la Interfaz
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    lCabeceras = listaCabeceras()
    nodoPrincipal = mainNodo()
    matriz = nodosEnMatriz()
    pieza = random.randint(1,6)
    jugador = 1
    for i in range(7):
        lCabeceras.insertarX(nodoPrincipal,nodosX(i+1))

    for i in range(int(10)):
        lCabeceras.insertarY(nodoPrincipal,nodosY(i+1))

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.tablero.setRowCount(10)
        self.tablero.setColumnCount(7)
        self.terminarButton.clicked.connect(self.insertarFigura)

    def insertarFigura(self):
        posX = int(self.Coordenada_X.text()) - 1
        posY = int(self.Coordenada_Y.text()) - 1
        if self.jugador == 1:
            self.figuras(posX,posY,self.pieza,'yellow')
            self.jugador = 2
        else:
            self.figuras(posX,posY,self.pieza,'red')
            self.jugador = 1
        self.pieza = random.randint(1,6)
    
    def figuras(self,posIX,posIY,idFigura,color):
        if idFigura == 1:
            inicio = 0
            while inicio != 4:
                self.ingresarPintar(posIX,posIY+inicio," ",color)
                inicio+=1
            self.ingresarPintar(posIX+1,posIY+inicio-1," ",color)
        elif idFigura == 2:
            inicio = 0
            while inicio != 4:
                self.ingresarPintar(posIX+1,posIY+inicio," ",color)
                inicio+=1
            self.ingresarPintar(posIX,posIY+inicio-1," ",color)
        elif idFigura == 3:
            inicio = 0
            while inicio != 4:
                self.ingresarPintar(posIX+inicio,posIY," ",color)
                inicio+=1
        elif idFigura == 4:
            self.ingresarPintar(posIX,posIY," ",color)
            self.ingresarPintar(posIX+1,posIY," ",color)
            self.ingresarPintar(posIX+1,posIY+1," ",color)
            self.ingresarPintar(posIX,posIY+1," ",color)
        elif idFigura == 5:
            self.ingresarPintar(posIX+1,posIY," ",color)
            self.ingresarPintar(posIX+2,posIY," ",color)
            self.ingresarPintar(posIX,posIY+1," ",color)
            self.ingresarPintar(posIX+1,posIY+1," ",color)
            self.ingresarPintar(posIX+2,posIY+1," ",color)
            self.ingresarPintar(posIX+3,posIY+1," ",color)
        elif idFigura == 6:
            inicio = 0
            while inicio != 5:
                self.ingresarPintar(posIX,posIY+inicio," ",color)
                inicio+=1
    def ingresarPintar(self,posIX,posIY,jugador,color):
        self.tablero.setItem(posIY, posIX, QtWidgets.QTableWidgetItem(jugador))
        self.tablero.item(posIY,posIX).setBackground(QtGui.QColor(color))
if __name__=='__main__':
    
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
