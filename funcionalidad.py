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
            if aux1X != None:
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
            if aux1Y != None:
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
    def __init__(self,id,color):
        self.id = id
        self.color = color
#Clases para la Interfaz
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    maxX = 7
    maxY = 10
    lCabeceras = listaCabeceras()
    nodoPrincipal = mainNodo()
    matriz = nodosEnMatriz()
    pieza = random.randint(1,6)
    changePlayer = False
    jugador = 1
    for i in range(7):
        lCabeceras.insertarX(nodoPrincipal,nodosX(i+1))

    for i in range(int(10)):
        lCabeceras.insertarY(nodoPrincipal,nodosY(i+1))
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.tablero.setRowCount(self.maxY)
        self.tablero.setColumnCount(self.maxX)
        self.tablero
        self.terminarButton.clicked.connect(self.insertarFigura)
        self.imagenFigura(self.pieza)
       

    def insertarFigura(self):
        posX = int(self.Coordenada_X.text()) - 1
        posY = int(self.Coordenada_Y.text()) - 1
        if self.jugador == 1:
            self.figuras(posX,posY,self.pieza,'yellow',self.jugador)
            if self.changePlayer:
                self.jugador = 2
                self.changePlayer = False
                self.pieza = random.randint(1,6)
        else:
            self.figuras(posX,posY,self.pieza,'red',self.jugador)
            if self.changePlayer:
                self.jugador = 1
                self.changePlayer = False
                self.pieza = random.randint(1,6)
        self.imagenFigura(self.pieza)
        

    def imagenFigura(self,idFigura):
        if idFigura == 1:
             self.image.setPixmap(QtGui.QPixmap("pieza1.png"))
        elif idFigura == 2:
            self.image.setPixmap(QtGui.QPixmap("pieza2.png"))
        elif idFigura == 3:
            self.image.setPixmap(QtGui.QPixmap("pieza3.png"))
        elif idFigura == 4:
            self.image.setPixmap(QtGui.QPixmap("pieza4.png"))
        elif idFigura == 5:
            self.image.setPixmap(QtGui.QPixmap("pieza5.png"))
        elif idFigura == 6:
            self.image.setPixmap(QtGui.QPixmap("pieza6.png"))

    def comprobarEspacio(self,posX,posY,lista):
        if posX <= self.maxX and posX > 0 and posY > 0 and posY <= self.maxY:
            aux = lista.next
            while aux.posX != int(posX):
                aux = aux.next

            if aux.down == None:
                return True
            else:
                aux2 = aux.down
                while aux2.posY != posY and aux2.down != None:
                    aux2 = aux2.down
                if aux2.posY != int(posY):
                    return True
                else:
                    return False
        else:
            return False

    def comprobarFigura(self,posX,posY,idFigura):
        var1 = True
        var2 = True
        var3 = True
        var4 = True
        var5 = True
        var6 = True
        if idFigura == 1:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX,posY+2,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX,posY+3,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX+1,posY+3,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True:
                self.changePlayer = True
                return True
        elif idFigura == 2:
            var1 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX+1,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+1,posY+2,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+1,posY+3,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX,posY+3,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True:
                self.changePlayer = True
                return True
        elif idFigura == 3:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+2,posY,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+3,posY,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True:
                self.changePlayer = True
                return True
        elif idFigura == 4:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+1,posY+1,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True:
                self.changePlayer = True
                return True
        elif idFigura == 5:
            var1 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+1,posY+1,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+2,posY,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX+2,posY+1,self.nodoPrincipal)
            var6 = self.comprobarEspacio(posX+3,posY+1,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True:
                self.changePlayer = True
                return True
        elif idFigura == 6:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX,posY+2,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX,posY+3,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX,posY+4,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True:
                self.changePlayer = True
                return True

    def figuras(self,posIX,posIY,idFigura,color,jugador):
        if idFigura == 1:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            if poderIngresar:
                while inicio != 4:
                    self.ingresarPintar(posIX,posIY+inicio," ",color)
                    self.matriz.insertar(posIX+1,posIY+inicio+1,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+inicio+1))
                    inicio+=1
                self.ingresarPintar(posIX+1,posIY+inicio-1," ",color)
                self.matriz.insertar(posIX+2,posIY+inicio,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+inicio))
        elif idFigura == 2:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            if poderIngresar:
                while inicio != 4:
                    self.ingresarPintar(posIX+1,posIY+inicio," ",color)
                    self.matriz.insertar(posIX+2,posIY+inicio+1,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+inicio+1))
                    inicio+=1
                self.ingresarPintar(posIX,posIY+inicio-1," ",color)
                self.matriz.insertar(posIX+1,posIY+inicio,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+inicio))
        elif idFigura == 3:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            if poderIngresar:
                while inicio != 4:
                    self.ingresarPintar(posIX+inicio,posIY," ",color)
                    self.matriz.insertar(posIX+inicio+1,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+inicio+1,posIY+1))
                    inicio+=1
        elif idFigura == 4:
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            if poderIngresar:
                self.ingresarPintar(posIX,posIY," ",color)
                self.matriz.insertar(posIX+1,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+1))
                
                self.ingresarPintar(posIX+1,posIY," ",color)
                self.matriz.insertar(posIX+2,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+1))

                self.ingresarPintar(posIX+1,posIY+1," ",color)
                self.matriz.insertar(posIX+2,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+2))

                self.ingresarPintar(posIX,posIY+1," ",color)
                self.matriz.insertar(posIX+1,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+2))
        elif idFigura == 5:
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            if poderIngresar:
                self.ingresarPintar(posIX+1,posIY," ",color)
                self.matriz.insertar(posIX+2,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+1))

                self.ingresarPintar(posIX+2,posIY," ",color)
                self.matriz.insertar(posIX+3,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+3,posIY+1))

                self.ingresarPintar(posIX,posIY+1," ",color)
                self.matriz.insertar(posIX+1,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+2))

                self.ingresarPintar(posIX+1,posIY+1," ",color)
                self.matriz.insertar(posIX+2,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+2))
                
                self.ingresarPintar(posIX+2,posIY+1," ",color)
                self.matriz.insertar(posIX+3,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+3,posIY+2))

                self.ingresarPintar(posIX+3,posIY+1," ",color)
                self.matriz.insertar(posIX+4,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+3,posIY+2))
        elif idFigura == 6:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            if poderIngresar:
                while inicio != 5:
                    self.ingresarPintar(posIX,posIY+inicio," ",color)
                    self.matriz.insertar(posIX+1,posIY+inicio+1,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+inicio+1))
                    inicio+=1

    def ingresarPintar(self,posIX,posIY,jugador,color):
        self.tablero.setItem(posIY, posIX, QtWidgets.QTableWidgetItem(jugador))
        self.tablero.item(posIY,posIX).setBackground(QtGui.QColor(color))
if __name__=='__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
