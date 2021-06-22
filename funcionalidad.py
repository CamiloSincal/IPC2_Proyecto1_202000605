from pyparsing import Empty
from GameView import *
from PyQt5.QtGui import * 
import random
import threading
import time
import pydot
from PyQt5.QtWidgets import (QFileDialog, QInputDialog, QLineEdit, QMessageBox)
from xml.dom import minidom
import xml.etree.cElementTree as ET

#-------------------------------------------Partes de texto para el HTML-------------------------------------------
startHTML = '<!DOCTYPE html><html lang="en" dir="ltr"><head><meta charset="utf-8"><title>Reporte</title><link rel="stylesheet" href="style.css" type="text/css"></head><body><div id="main-container"><table><thead><tr><th>Alias Jugadores</th><th>Color</th><th>Equivocaciones</th><th>Partidas Ganadas</th></tr></thead>'
middleHTML = ''
endHTML = '</table></div></body></html>'
#-------------------------------------------Partes de texto para Graphviz------------------------------------------
startGraphText = 'digraph g{node[style="filled",fillcolor="navyblue",shape="box"]'
middleGraphText = ''
endGraphText = '}'
#--------------------------------------------Nodo Principal De La Matriz-------------------------------------------
class mainNodo:
    def __init__(self):
        self.dato = 'main Nodo'
        self.next = None
        self.down = None

#--------------------------------------------Nodos de la cabecera X-------------------------------------------
class nodosX:
    def __init__(self, data):
        self.posX = data
        self.eje = "x"
        self.next = None
        self.previous = None
        self.down = None

#--------------------------------------------Nodos de la cabecera Y-------------------------------------------
class nodosY:
    def __init__(self, data):
        self.posY = data
        self.eje = "y"
        self.right = None
        self.up = None
        self.down = None

#--------------------------------------Nodos que representan cada parte de una pieza-----------------------------
class nodos:
    def __init__(self, data,posX,posY):
        self.data = data
        self.posX = posX
        self.posY = posY
        self.up = None
        self.right = None
        self.left = None
        self.down = None

#--------------------------------------------Identificador de los primeros nodos en X,Y-------------------------------------------
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
##--------------------------------------------Matriz que almacenara los nodos-------------------------------------------
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
#--------------------------------------------Clase representa a un Jugador------------------------------------------
class jugador:
    def __init__(self,id,color,enTurno,totalPiezas,alias):
        self.id = id
        self.color = color
        self.enTurno = enTurno
        self.totalPiezas = totalPiezas
        self.intentosActuales = 2
        self.alias = alias
        self.points = 0
        self.wins = 0
        self.errors = 0


#--------------------------------------------Clase del tablero de juego-------------------------------------------
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    nodoPrincipal = mainNodo()
    lCabeceras = listaCabeceras()
    matriz = nodosEnMatriz()
    pieza = random.randint(1,6)
    #Creacion de Jugadores
    Tpiezas = 0
    jugador1 = jugador(1,'yellow',True,Tpiezas,"J1")
    jugador2 = jugador(2,'yellow',True,Tpiezas,"J2")
    #Tiempo
    maxTiempo = 1
    maxX = 0
    maxY = 0
    tiempo = maxTiempo
    changePlayer = False
    #Continuar juego
    playing = False
    #Variables que indican que cierta pieza puede seguir colocandose
    pieza1 = True
    pieza2 = True
    pieza3 = True
    pieza4 = True
    pieza5 = True
    pieza6 = True
    

    def camiboJugador(self):
        if self.playing:
            if self.jugador1.enTurno:
                self.jugador1.enTurno = False
                self.jugador1.intentosActuales = 2
                self.jugador2.enTurno = True
                self.intentos.setText(str(self.jugador2.intentosActuales))
                self.playerName.setText(self.jugador2.alias)
                self.numPiezas.setText(str(self.jugador2.totalPiezas))
                self.ptsJugador.setText(str(self.jugador2.points))
                self.tiempo = self.maxTiempo
                self.pieza = random.randint(1,6)
            else:
                self.jugador2.enTurno = False
                self.jugador2.intentosActuales = 2
                self.jugador1.enTurno = True
                self.intentos.setText(str(self.jugador1.intentosActuales))
                self.tiempo = self.maxTiempo
                self.playerName.setText(self.jugador1.alias)
                self.numPiezas.setText(str(self.jugador1.totalPiezas))
                self.ptsJugador.setText(str(self.jugador1.points))
                self.pieza = random.randint(1,6)
            self.imagenFigura(self.pieza)
           

    def startGame(self):
        self.winMessage.setText("")
        winsJ1 = self.jugador1.wins
        winsJ2 = self.jugador2.wins
        
        Errors1 = self.jugador1.errors
        Errors2 = self.jugador2.errors

        self.tablero.setRowCount(0)
        self.tablero.setColumnCount(0)
        color1 = self.colorPlayer(str(self.colorP1.currentText()))
        color2 = self.colorPlayer(str(self.colorP2.currentText()))
        
        nick1 = self.nick1.text()
        nick2 = self.nick2.text()

        self.maxX = int(self.newX.text())  
        self.maxY = int(self.newY.text())
        
        self.maxTiempo = int(self.timePerPlayer.text())

        if color1 == color2 or nick1 == nick2:
            QMessageBox.about(self,"Advertencia","Colores o nombres repetidos")
        elif self.maxTiempo > 60:
            QMessageBox.about(self,"Advertencia","El tiempo no puede ser mayor a 60")
        elif self.maxX < 4 and self.maxY < 4:
            QMessageBox.about(self,"Advertencia","El tablero debe ser de mínimo 4x4")
        else:
            self.nodoPrincipal = mainNodo()
            self.lCabeceras = listaCabeceras()
            self.matriz = nodosEnMatriz()
            self.pieza = random.randint(1,6)
            self.imagenFigura(self.pieza)
            self.playing = True
            
            for i in range(self.maxX):
                self.lCabeceras.insertarX(self.nodoPrincipal,nodosX(i+1))

            for i in range(int(self.maxY)):
                self.lCabeceras.insertarY(self.nodoPrincipal,nodosY(i+1))  
            

            self.tablero.setRowCount(self.maxY)
            self.tablero.setColumnCount(self.maxX)

            horizontal = self.tablero.horizontalHeader()   
            vertical = self.tablero.verticalHeader()
            for i in range(self.maxX):
                horizontal.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

            for i in range(self.maxY):
                vertical.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                
            self.Tpiezas = int(self.totalPerPlayer.text())

            self.jugador1 = jugador(1,color1,True,self.Tpiezas,nick1)
            self.jugador2 = jugador(2,color2,False,self.Tpiezas,nick2)

            self.jugador1.wins = winsJ1
            self.jugador2.wins = winsJ2

            self.jugador1.errors = Errors1
            self.jugador2.errors = Errors2
            
            thread = threading.Thread(target=self.temporizador)
            thread2 = threading.Thread(target=self.cambioPorTiempo)
            thread3 = threading.Thread(target=self.winGame)
            
            thread3.start()
            thread.start()
            thread2.start()
            
    def colorPlayer(self,colorES):
        if colorES == "Azul":
            return "blue"
        elif colorES == "Rojo":
            return "red"
        elif colorES == "Amarillo":
            return "yellow"
        elif colorES == "Verde":
            return "green"
    
    def colorPlayerES(self,colorIN):
        if colorIN == "blue":
            return "Azul"
        elif colorIN == "red":
            return "Rojo"
        elif colorIN == "yellow":
            return "Amarillo"
        elif colorIN == "green":
            return "Verde"
    def __init__(self,*args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.tablero
        self.terminarButton.clicked.connect(self.insertarFigura)
        self.pasarTurno.clicked.connect(self.camiboJugador)
        self.newGameStart.clicked.connect(self.startGame)
        self.newReporte.clicked.connect(self.generarReporte)
        self.openButton.clicked.connect(self.abrirArchivo)
        self.saveButton.clicked.connect(self.guardarArchivo)
        self.imagenFigura(self.pieza)
        self.numPiezas.setText(str(self.jugador1.totalPiezas))
        self.playerTimer.setText(str(self.tiempo))
        self.intentos.setText(str(self.jugador1.intentosActuales))
        self.playerName.setText(self.jugador1.alias)
        
    def abrirArchivo(self):
        fileName = QFileDialog.getOpenFileName()
        direc = fileName[0]
        
        documento = minidom.parse(direc)
        matrizCompleta = documento.getElementsByTagName('imagen')
        columnas = documento.getElementsByTagName('columnas')[0].firstChild.data
        filas = documento.getElementsByTagName('filas')[0].firstChild.data
        colorname1 = documento.getElementsByTagName('color1')[0].firstChild.data
        colorname2 = documento.getElementsByTagName('color2')[0].firstChild.data
        
        if direc != "":
            
            self.winMessage.setText("")

            self.tablero.setRowCount(0)
            self.tablero.setColumnCount(0)

            color1 = self.colorPlayer(str(colorname1))
            color2 = self.colorPlayer(str(colorname2))
            
            nick1 = str(colorname1)
            nick2 = str(colorname2)

            self.maxX = int(filas)
            self.maxY = int(columnas)
            
            self.maxTiempo = 60

            self.tablero.setRowCount(0)
            self.tablero.setColumnCount(0)

            self.tablero.setRowCount(self.maxY)
            self.tablero.setColumnCount(self.maxX)
        
            horizontal = self.tablero.horizontalHeader()   
            vertical = self.tablero.verticalHeader()
            for i in range(self.maxX):
                horizontal.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

            for i in range(self.maxY):
                vertical.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            
            for elemento in matrizCompleta:
                texto = elemento.firstChild.data

            #separo el texto
            for j in texto:
                separacion = texto.split(" ")
            for elem in separacion:
                if elem == '':
                    separacion.remove('')
            
            self.nodoPrincipal = mainNodo()
            self.lCabeceras = listaCabeceras()
            self.matriz = nodosEnMatriz()
            self.pieza = random.randint(1,6)
            self.imagenFigura(self.pieza)
            self.playing = True

            for i in range(self.maxX):
                self.lCabeceras.insertarX(self.nodoPrincipal,nodosX(i+1))

            for i in range(int(self.maxY)):
                self.lCabeceras.insertarY(self.nodoPrincipal,nodosY(i+1))  
            
            #Reccorro cada elemento
            inicio = 0
            while(inicio != int(filas)):
                if(separacion[inicio] != ""):
                    for c in range(int(columnas)):
                        if(separacion[inicio][c] != "-"):
                            if separacion[inicio][c] == "1":
                                self.ingresarPintar(c,inicio," ",color1)
                            elif separacion[inicio][c] == "2":
                                self.ingresarPintar(c,inicio," ",color2)
                            
                            self.matriz.insertar(c+1,inicio+1,self.nodoPrincipal,nodos(separacion[inicio][c],c+1,inicio+1))
                inicio+=1
            
            num1,okPressed1 = QInputDialog.getInt(self, nick1,"Cantidad de piezas restantes:", 0, 0, 100, 1)
            num2,okPressed2 = QInputDialog.getInt(self, nick2,"Cantidad de piezas restantes:", 0, 0, 100, 1)

            x = 0
            y = 0
            
            while x != self.maxX:
                while y != self.maxY:
                    for fig in range(6):
                        self.comprobarFigura(x+1,y+1,fig+1)
                        if self.comprobarFigura(x+1,y+1,fig+1) != True:
                            self.agregarPuntosInCharge(self.comprobarFigura(x+1,y+1,fig+1))
                            break
                    y+=1
                x += 1

            if okPressed1:
                self.jugador1 = jugador(1,color1,True,num1,nick1)
            
            if okPressed2:
                self.jugador2 = jugador(2,color2,False,num2,nick2)

            self.jugador1.wins = 0
            self.jugador2.wins = 0

            self.jugador1.errors = 0
            self.jugador2.errors = 0
            
            thread = threading.Thread(target=self.temporizador)
            thread2 = threading.Thread(target=self.cambioPorTiempo)
            thread3 = threading.Thread(target=self.winGame)
            
            thread3.start()
            thread.start()
            thread2.start()
            
    def guardarArchivo(self):
        #Variable que almacenar el "Texto" de la matriz
        matrizT = ''
        #Recorro la matriz
        inicioY = self.nodoPrincipal.down
        while inicioY != None:
            if inicioY.right == None:
                for elm in range(self.maxX-1):
                    matrizT += '-'
                matrizT += '- '
            else:
                nodosI = inicioY.right
                if nodosI.posX != 1:
                    difI = nodosI.posX - 1
                    Cinicial = 1
                    while Cinicial <= difI:
                        matrizT += '-'
                        Cinicial+=1

                while nodosI.right != None:
                    pos1 = nodosI.posX
                    pos2 = nodosI.right.posX
                    matrizT += str(nodosI.data)
                    mdif = pos2-pos1
                    if mdif != 1:
                        numEsp = 1
                        while numEsp <= mdif-1:
                            matrizT += '-'
                            numEsp+=1
                    nodosI = nodosI.right
                matrizT += str(nodosI.data)

                if nodosI.posX < self.maxX:
                    dif2 = self.maxX-nodosI.posX
                    Cinicial2 = 1
                    while Cinicial2 <= dif2:
                        matrizT+="-"
                        Cinicial2+=1
                matrizT+=' '
            inicioY = inicioY.down
        #Creacion de las primeras
        raiz = ET.Element('matrices')
        matriz = ET.SubElement(raiz,'matriz')
        archivename = ET.SubElement(matriz,'nombre')
        archivename.text = self.nameSave.text()
        archiveN = self.nameSave.text()+'.xml'
        numFilas = ET.SubElement(matriz,'filas')
        numFilas.text = str(self.maxX)
        numColumna = ET.SubElement(matriz,'columnas')
        numColumna.text = str(self.maxY)
        nomCol1 = ET.SubElement(matriz,'color1')
        nomCol1.text = self.colorPlayerES(str(self.jugador1.color))
        nomCol2 = ET.SubElement(matriz,'color2')
        nomCol2.text = self.colorPlayerES(str(self.jugador2.color))
        img = ET.SubElement(matriz,'imagen')
        img.text = matrizT
        data = ET.tostring(raiz)
        documento = open(archiveN,"wb")
        documento.write(data)

    def closeEvent(self, event):
        respuesta = QMessageBox.question(self, 'Cerrar Juego', '¿Quieres Salir del juego?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.playing = False
            event.accept()
        else:
            event.ignore()

    def winGame(self):
        while self.playing:
            self.comprobarPosibilidad()
            #Verifico si algún jugador se quedo sin piezas
            if self.jugador1.totalPiezas == 0 or self.jugador2.totalPiezas == 0:
                if self.jugador1.totalPiezas == 0:
                    self.winMessage.setText(str(self.jugador1.alias)+" GANÓ")
                    self.jugador1.wins +=1
                else:
                    self.winMessage.setText(str(self.jugador2.alias)+" GANÓ")
                    self.jugador2.wins +=1
                self.playing = False
            #Verifico si todas las piezas no se pueden colocar para dar fin al juego
            if self.pieza1 == False and self.pieza2 == False and self.pieza3 == False and self.pieza4 == False and self.pieza5 == False and self.pieza6 == False:
                if self.jugador1.points > self.jugador2.points:
                    self.winMessage.setText(str(self.jugador1.alias)+" GANÓ")
                    self.jugador1.wins +=1
                elif self.jugador2.points > self.jugador1.points:
                    self.winMessage.setText(str(self.jugador2.alias)+" GANÓ")
                    self.jugador2.wins +=1
                else:
                    self.winMessage.setText("FUE UN EMPATE")
                self.playing = False
        
        
    def createHTML(self):
        global startHTML
        global middleHTML
        global endHTML
        middleHTML = ''
        file = open('reporteHTML.html','w')
        #Datos Jugador1
        middleHTML += '<tr>'+'<td>'+str(self.jugador1.alias)+'</td>'+'<td>'+self.colorPlayerES(str(self.jugador1.color))+'</td>'+'<td>'+str(self.jugador1.errors)+'</td>'+'<td>'+str(self.jugador1.wins)+'</td>'+'</tr>'
        #Datos Jugador2
        middleHTML += '<tr>'+'<td>'+str(self.jugador2.alias)+'</td>'+'<td>'+self.colorPlayerES(str(self.jugador2.color))+'</td>'+'<td>'+str(self.jugador2.errors)+'</td>'+'<td>'+str(self.jugador2.wins)+'</td>'+'</tr>'
        middleHTML += '<img src="matriz.png">'
        text = startHTML + middleHTML +endHTML
        file.write(text)
        file.close()
    
    def createGraph(self):
        global startGraphText
        global middleGraphText
        global endGraphText
        middleGraphText = ''
        file = open('matriz.dot','w')
        middleGraphText += 'mainNode[label='+'"'+self.nodoPrincipal.dato+'"'+'fontcolor="white"]'
        #Agrego los nodos en X existentes
        aux = self.nodoPrincipal.next
        while aux != None:
            if aux.down != None:
                middleGraphText += 'node'+str(aux.posX)+'x[label="'+str(aux.posX)+'x",fontcolor="white"]'
            aux = aux.next
        
        #Agrego los nodos en Y existentes
        aux2 = self.nodoPrincipal.down
        while aux2 != None:
            if aux2.right != None:
                middleGraphText += 'node'+str(aux2.posY)+'y[label="'+str(aux2.posY)+'y",fontcolor="white"]\n'
            aux2 = aux2.down

        #Agrego los nodos correspondientes tomando como base el eje X 
        recX = self.nodoPrincipal.next
        while recX != None:
            if recX.down != None:
                recAbajo = recX.down
                while recAbajo != None:
                    middleGraphText += 'node'+str(recAbajo.posX)+str(recAbajo.posY)+'[label="'+str(recAbajo.posX)+','+str(recAbajo.posY)+'",fontcolor="white"]\n'
                    recAbajo = recAbajo.down
            recX = recX.next

        #Creo las relaciones entre nodos en X
        posI = self.nodoPrincipal.next
        pos2 = posI.next 

        primerX = self.nodoPrincipal.next
        while primerX != None:
            if(primerX.down != None):
                break
            primerX = primerX.next

        middleGraphText += 'mainNode->node'+str(primerX.posX)+'x\n'
        middleGraphText += 'node'+str(primerX.posX)+'x->mainNode\n'
        
        while posI != None and pos2 != None:
            if posI.down != None and pos2.down != None:
                middleGraphText += 'node'+str(posI.posX)+'x->'+'node'+str(pos2.posX)+'x\n'
                middleGraphText += 'node'+str(pos2.posX)+'x->'+'node'+str(posI.posX)+'x\n'
                posI = posI.next
                pos2 = posI.next
            elif posI.down != None and pos2.down == None:
                pos2 = pos2.next
            elif posI.down == None and pos2.down != None:
                posI = pos2
                pos2 = pos2.next
            elif posI.down == None and pos2.down == None:
                posI = posI.next
                pos2 = posI.next
                
        middleGraphText +='{rank="same";'

        aux = self.nodoPrincipal.next
        while aux !=None:
            if aux.down != None:
                middleGraphText += 'node'+str(aux.posX)+'x;'
            aux = aux.next

        middleGraphText +='mainNode}\n'

        #Creo las relaciones entre nodos en Y
        posIY = self.nodoPrincipal.down
        pos2Y = posIY.down 

        primerY = self.nodoPrincipal.down
        while primerY != None:
            if(primerY.right != None):
                break
            primerY = primerY.down

        middleGraphText += 'mainNode->node'+str(primerY.posY)+'y\n'
        middleGraphText += 'node'+str(primerY.posY)+'y->mainNode\n'
        while posIY != None and pos2Y != None:
            if posIY.right != None and pos2Y.right != None:
                middleGraphText += 'node'+str(posIY.posY)+'y->'+'node'+str(pos2Y.posY)+'y\n'
                middleGraphText += 'node'+str(pos2Y.posY)+'y->'+'node'+str(posIY.posY)+'y\n'
                posIY = posIY.down
                pos2Y = posIY.down
            elif posIY.right != None and pos2Y.right == None:
                pos2Y = pos2Y.down
            elif posIY.right == None and pos2Y.right != None:
                posIY = pos2Y
                pos2Y = pos2Y.down
            elif posIY.right == None and pos2Y.right == None:
                posIY = posIY.down
                pos2Y = posIY.down
        #Creo las relaciones entre los otros nodos
        inicioX = self.nodoPrincipal.next
        
        while inicioX != None:
            if inicioX.down != None:
                pos1N = inicioX.down
                pos2N = pos1N.down
                middleGraphText += 'node'+str(inicioX.posX)+'x->'+'node'+str(pos1N.posX)+str(pos1N.posY)+'\n'
                middleGraphText += 'node'+str(pos1N.posX)+str(pos1N.posY)+'->'+'node'+str(inicioX.posX)+'x\n'
                while pos2N !=None:
                    if pos2N != None:
                        middleGraphText += 'node'+str(pos1N.posX)+str(pos1N.posY)+'->'+'node'+str(pos2N.posX)+str(pos2N.posY)+'\n'
                        middleGraphText += 'node'+str(pos2N.posX)+str(pos2N.posY)+'->'+'node'+str(pos1N.posX)+str(pos1N.posY)+'\n'
                        pos1N = pos1N.down  
                        pos2N = pos1N.down
            inicioX = inicioX.next

        
        
        text = startGraphText + middleGraphText + endGraphText
        file.write(text)
        file.close()
        (graph,) = pydot.graph_from_dot_file('matriz.dot')
        graph.write_png('matriz.png')

    def generarReporte(self):
        self.createGraph()
        self.createHTML()

    def comprobarPosibilidad(self):
        #Verifico si se puede [Pieza 1]
        for i in range(self.maxX-1):
            for j in range(self.maxY-3):
                espacio = self.comprobarFigura(i+1,j+1,1)
                jugador1P = self.comprobarEsquinas(i+1,j+1,1,self.jugador1.id)
                jugador2P = self.comprobarEsquinas(i+1,j+1,1,self.jugador2.id)
                if jugador1P and espacio:
                    self.pieza1 = True
                    break
                elif jugador2P and espacio:
                    self.pieza1 = True
                    break
                else:
                    self.pieza1 = False
            else:
                continue
            break

        #Verifico si se puede [Pieza 2]
        for i in range(self.maxX-1):
            for j in range(self.maxY-3):
                espacio = self.comprobarFigura(i+1,j+1,2)
                jugador1P = self.comprobarEsquinas(i+1,j+1,2,self.jugador1.id)
                jugador2P = self.comprobarEsquinas(i+1,j+1,2,self.jugador2.id)
                if jugador1P and espacio:
                    self.pieza2= True
                    break
                elif jugador2P and espacio:
                    self.pieza2 = True
                    break
                else:
                    self.pieza2 = False
            else:
                continue
            break
        #Verifico si se puede [Pieza 3]
        for i in range(self.maxX-3):
            for j in range(self.maxY):
                espacio = self.comprobarFigura(i+1,j+1,3)
                jugador1P = self.comprobarEsquinas(i+1,j+1,3,self.jugador1.id)
                jugador2P = self.comprobarEsquinas(i+1,j+1,3,self.jugador2.id)
                if jugador1P and espacio:
                    self.pieza3= True
                    break
                elif jugador2P and espacio:
                    self.pieza3 = True
                    break
                else:
                    self.pieza3 = False
            else:
                continue
            break
        
        #Verifico si se puede [Pieza 4]
        for i in range(self.maxX-1):
            for j in range(self.maxY-1):
                espacio = self.comprobarFigura(i+1,j+1,4)
                jugador1P = self.comprobarEsquinas(i+1,j+1,4,self.jugador1.id)
                jugador2P = self.comprobarEsquinas(i+1,j+1,4,self.jugador2.id)
                if jugador1P and espacio:
                    self.pieza4= True
                    break
                elif jugador2P and espacio:
                    self.pieza4 = True
                    break
                else:
                    self.pieza4 = False
            else:
                continue
            break
        
        #Verifico si se puede [Pieza 5]
        for i in range(self.maxX-3):
            for j in range(self.maxY-1):
                espacio = self.comprobarFigura(i+1,j+1,5)
                jugador1P = self.comprobarEsquinas(i+1,j+1,5,self.jugador1.id)
                jugador2P = self.comprobarEsquinas(i+1,j+1,5,self.jugador2.id)
                if jugador1P and espacio:
                    self.pieza5= True
                    break
                elif jugador2P and espacio:
                    self.pieza5 = True
                    break
                else:
                    self.pieza5 = False
            else:
                continue
            break

        #Verifico si se puede [Pieza 6]
        if self.maxY < 5:
            self.pieza6 = False

        for i in range(self.maxX):
            for j in range(self.maxY-4):
                espacio = self.comprobarFigura(i+1,j+1,6)
                jugador1P = self.comprobarEsquinas(i+1,j+1,6,self.jugador1.id)
                jugador2P = self.comprobarEsquinas(i+1,j+1,6,self.jugador2.id)
                if jugador1P and espacio:
                    self.pieza6= True
                    break
                elif jugador2P and espacio:
                    self.pieza6 = True
                    break
                else:
                    self.pieza6 = False
            else:
                continue
            break

    def temporizador(self): 
        while self.tiempo != 0 and self.playing:
            self.tiempo -= 1
            self.playerTimer.setText(str(self.tiempo))
            time.sleep(1)
        
    def cambioPorTiempo(self):
        while self.playing:
            if self.tiempo == 0:
                self.imagenFigura(self.pieza)
                self.tiempo = self.maxTiempo
                self.camiboJugador()

    def insertarFigura(self):
        if self.playing:
            if self.Coordenada_X.text() != "" and self.Coordenada_Y.text() != "":
                posX = int(self.Coordenada_X.text()) - 1
                posY = int(self.Coordenada_Y.text()) - 1
                if self.jugador1.enTurno:
                    if self.jugador1.totalPiezas != 0:
                        self.figuras(posX,posY,self.pieza,self.jugador1.color,self.jugador1.id,self.jugador1)
                        if self.changePlayer:
                            self.jugador1.totalPiezas -= 1
                            self.camiboJugador()
                            self.changePlayer = False
                            self.tiempo = self.maxTiempo
                else:
                    if self.jugador2.totalPiezas != 0:
                        self.figuras(posX,posY,self.pieza,self.jugador2.color,self.jugador2.id,self.jugador2)
                        if self.changePlayer:
                            self.jugador2.totalPiezas -= 1
                            self.camiboJugador()
                            self.changePlayer = False
                            self.tiempo = self.maxTiempo
                self.imagenFigura(self.pieza)
            else:
                QMessageBox.about(self,"Advertencia","¡No se ingresaron todas las coordenadas!")
        

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
    
    def sideS(self,posX,posY,lista,jugador):
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
                elif aux2.posY == int(posY) and aux2.data != jugador:
                    return True
                else:
                    return False
        else:
            return True

    def comprobarEsquinas(self,posX,posY,idFigura,jugador):
        var1 = True
        var2 = True
        var3 = True
        var4 = True
        var5 = True
        var6 = True
        var7 = True
        var8 = True
        var9 = True
        var10 = True
        var11 = True
        var12 = True
        if idFigura == 1:
            var1 = self.sideS(posX,posY-1,self.nodoPrincipal,jugador)
            var2 = self.sideS(posX+1,posY,self.nodoPrincipal,jugador)
            var3 = self.sideS(posX-1,posY,self.nodoPrincipal,jugador)
            var4 = self.sideS(posX+1,posY+1,self.nodoPrincipal,jugador)
            var5 = self.sideS(posX-1,posY+1,self.nodoPrincipal,jugador)
            var6 = self.sideS(posX+1,posY+2,self.nodoPrincipal,jugador)
            var7 = self.sideS(posX-1,posY+2,self.nodoPrincipal,jugador)
            var8 = self.sideS(posX-1,posY+3,self.nodoPrincipal,jugador)
            var9 = self.sideS(posX,posY+4,self.nodoPrincipal,jugador)
            var10 = self.sideS(posX+1,posY+4,self.nodoPrincipal,jugador)
            var11 = self.sideS(posX+2,posY+3,self.nodoPrincipal,jugador)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True and var7 == True and var8 == True and var9 == True and var10 == True and var11 == True:
                return True
            
        elif idFigura == 2:
            var1 = self.sideS(posX+1,posY-1,self.nodoPrincipal,jugador)
            var2 = self.sideS(posX,posY,self.nodoPrincipal,jugador)
            var3 = self.sideS(posX+2,posY,self.nodoPrincipal,jugador)
            var4 = self.sideS(posX,posY+1,self.nodoPrincipal,jugador)
            var5 = self.sideS(posX+2,posY+1,self.nodoPrincipal,jugador)
            var6 = self.sideS(posX,posY+2,self.nodoPrincipal,jugador)
            var7 = self.sideS(posX+2,posY+2,self.nodoPrincipal,jugador)
            var8 = self.sideS(posX+2,posY+3,self.nodoPrincipal,jugador)
            var9 = self.sideS(posX-1,posY+3,self.nodoPrincipal,jugador)
            var10 = self.sideS(posX,posY+4,self.nodoPrincipal,jugador)
            var11 = self.sideS(posX+1,posY+4,self.nodoPrincipal,jugador)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True and var7 == True and var8 == True and var9 == True and var10 == True and var11 == True :
                return True
        elif idFigura == 3:
            var1 = self.sideS(posX,posY-1,self.nodoPrincipal,jugador)
            var2 = self.sideS(posX,posY+1,self.nodoPrincipal,jugador)
            var3 = self.sideS(posX+1,posY-1,self.nodoPrincipal,jugador)
            var4 = self.sideS(posX+1,posY+1,self.nodoPrincipal,jugador)
            var5 = self.sideS(posX+2,posY-1,self.nodoPrincipal,jugador)
            var6 = self.sideS(posX+2,posY+1,self.nodoPrincipal,jugador)
            var7 = self.sideS(posX+3,posY-1,self.nodoPrincipal,jugador)
            var8 = self.sideS(posX+3,posY+1,self.nodoPrincipal,jugador)
            var9 = self.sideS(posX-1,posY,self.nodoPrincipal,jugador)
            var10 = self.sideS(posX+4,posY,self.nodoPrincipal,jugador)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True and var7 == True and var8 == True and var9 == True and var10 == True:
                return True
        elif idFigura == 4:
            var1 = self.sideS(posX,posY-1,self.nodoPrincipal,jugador)
            var2 = self.sideS(posX-1,posY,self.nodoPrincipal,jugador)
            var3 = self.sideS(posX+1,posY-1,self.nodoPrincipal,jugador)
            var4 = self.sideS(posX+2,posY,self.nodoPrincipal,jugador)
            var5 = self.sideS(posX-1,posY+1,self.nodoPrincipal,jugador)
            var6 = self.sideS(posX,posY+2,self.nodoPrincipal,jugador)
            var7 = self.sideS(posX+1,posY+2,self.nodoPrincipal,jugador)
            var8 = self.sideS(posX+2 ,posY+1,self.nodoPrincipal,jugador)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True and var7 == True and var8 == True:
                return True
        elif idFigura == 5:
            var1 = self.sideS(posX,posY,self.nodoPrincipal,jugador)
            var2 = self.sideS(posX-1,posY+1,self.nodoPrincipal,jugador)
            var3 = self.sideS(posX+1,posY-1,self.nodoPrincipal,jugador)
            var4 = self.sideS(posX+2,posY-1,self.nodoPrincipal,jugador)
            var5 = self.sideS(posX+3,posY,self.nodoPrincipal,jugador)
            var6 = self.sideS(posX,posY+2,self.nodoPrincipal,jugador)
            var7 = self.sideS(posX+1,posY+2,self.nodoPrincipal,jugador)
            var8 = self.sideS(posX+2,posY+2,self.nodoPrincipal,jugador)
            var9 = self.sideS(posX+3,posY+2,self.nodoPrincipal,jugador)
            var9 = self.sideS(posX+4,posY+1,self.nodoPrincipal,jugador)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True and var7 == True and var8 == True and var9:
                return True
        elif idFigura == 6:
            var1 = self.sideS(posX,posY-1,self.nodoPrincipal,jugador)
            var2 = self.sideS(posX-1,posY,self.nodoPrincipal,jugador)
            var3 = self.sideS(posX+1,posY,self.nodoPrincipal,jugador)
            var4 = self.sideS(posX-1,posY+1,self.nodoPrincipal,jugador)
            var5 = self.sideS(posX+1,posY+1,self.nodoPrincipal,jugador)
            var6 = self.sideS(posX-1,posY+2,self.nodoPrincipal,jugador)
            var7 = self.sideS(posX+1,posY+2,self.nodoPrincipal,jugador)
            var8 = self.sideS(posX-1,posY+3,self.nodoPrincipal,jugador)
            var9 = self.sideS(posX+1,posY+3,self.nodoPrincipal,jugador)
            var10 = self.sideS(posX-1,posY+4,self.nodoPrincipal,jugador)
            var11 = self.sideS(posX+1,posY+4,self.nodoPrincipal,jugador)
            var12 = self.sideS(posX,posY+5,self.nodoPrincipal,jugador)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True and var7 == True and var8 == True and var9  and var10 == True and var11  and var12 == True:
                return True

    def agregarPuntosInCharge(self,player):
        if player == 1:
            self.jugador1.points +=1
        elif player == 2:
            self.jugador2.points +=1
            
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
                return True
            elif var1 !=True and var2 !=True and var3 !=True and var4 !=True and var5 !=True:
                
                return var1
        elif idFigura == 2:
            var1 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX+1,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+1,posY+2,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+1,posY+3,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX,posY+3,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True:
                return True
            elif var1 !=True and var2 !=True and var3 !=True and var4 !=True and var5 !=True:
                return var1

        elif idFigura == 3:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+2,posY,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+3,posY,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True:
                return True
            elif var1 !=True and var2 !=True and var3 !=True and var4 !=True:
                return var1

        elif idFigura == 4:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+1,posY+1,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True:
                return True
            elif var1 !=True and var2 !=True and var3 !=True and var4 !=True:
                return var1

        elif idFigura == 5:
            var1 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX+1,posY,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX+1,posY+1,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX+2,posY,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX+2,posY+1,self.nodoPrincipal)
            var6 = self.comprobarEspacio(posX+3,posY+1,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True and var6 == True:
                return True
            elif var1 !=True and var2 !=True and var3 !=True and var4 !=True and var5 !=True and var6 !=True:
                return var1

        elif idFigura == 6:
            var1 = self.comprobarEspacio(posX,posY,self.nodoPrincipal)
            var2 = self.comprobarEspacio(posX,posY+1,self.nodoPrincipal)
            var3 = self.comprobarEspacio(posX,posY+2,self.nodoPrincipal)
            var4 = self.comprobarEspacio(posX,posY+3,self.nodoPrincipal)
            var5 = self.comprobarEspacio(posX,posY+4,self.nodoPrincipal)
            if var1 == True and var2 == True and var3 == True and var4 == True and var5 == True:
                return True
            elif var1 !=True and var2 !=True and var3 !=True and var4 !=True and var5 !=True:
                return var1

    def figuras(self,posIX,posIY,idFigura,color,jugador,player):
        if idFigura == 1:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            esquinasC = self.comprobarEsquinas(posIX+1,posIY+1,idFigura,jugador)
            if poderIngresar and esquinasC:
                while inicio != 4:
                    self.ingresarPintar(posIX,posIY+inicio," ",color)
                    self.matriz.insertar(posIX+1,posIY+inicio+1,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+inicio+1))
                    inicio+=1
                self.ingresarPintar(posIX+1,posIY+inicio-1," ",color)
                self.matriz.insertar(posIX+2,posIY+inicio,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+inicio))
                player.points +=1
                self.changePlayer = True
            else:
                QMessageBox.about(self,"Advertencia","¡La pieza no se puede colocar en esa posición!")
                if player.intentosActuales != 1:
                    player.intentosActuales -=1
                    self.intentos.setText(str(player.intentosActuales))
                else:
                    self.camiboJugador()
                    player.errors+=1
        elif idFigura == 2:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            esquinasC = self.comprobarEsquinas(posIX+1,posIY+1,idFigura,jugador)
            if poderIngresar and esquinasC:
                while inicio != 4:
                    self.ingresarPintar(posIX+1,posIY+inicio," ",color)
                    self.matriz.insertar(posIX+2,posIY+inicio+1,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+inicio+1))
                    inicio+=1
                self.ingresarPintar(posIX,posIY+inicio-1," ",color)
                self.matriz.insertar(posIX+1,posIY+inicio,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+inicio))
                player.points +=1
                self.changePlayer = True
            else:
                QMessageBox.about(self,"Advertencia","¡La pieza no se puede colocar en esa posición!")
                if player.intentosActuales != 1:
                    player.intentosActuales -=1
                    self.intentos.setText(str(player.intentosActuales))
                else:
                    self.camiboJugador()
                player.errors+=1
        elif idFigura == 3:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            esquinasC = self.comprobarEsquinas(posIX+1,posIY+1,idFigura,jugador)
            if poderIngresar and esquinasC:
                while inicio != 4:
                    self.ingresarPintar(posIX+inicio,posIY," ",color)
                    self.matriz.insertar(posIX+inicio+1,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+inicio+1,posIY+1))
                    inicio+=1
                player.points +=1
                self.changePlayer = True
            else:
                QMessageBox.about(self,"Advertencia","¡La pieza no se puede colocar en esa posición!")
                if player.intentosActuales != 1:
                    player.intentosActuales -=1
                    self.intentos.setText(str(player.intentosActuales))
                else:
                    self.camiboJugador()
                player.errors+=1
        elif idFigura == 4:
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            esquinasC = self.comprobarEsquinas(posIX+1,posIY+1,idFigura,jugador)
            if poderIngresar and esquinasC:
                self.ingresarPintar(posIX,posIY," ",color)
                self.matriz.insertar(posIX+1,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+1))
                
                self.ingresarPintar(posIX+1,posIY," ",color)
                self.matriz.insertar(posIX+2,posIY+1,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+1))

                self.ingresarPintar(posIX+1,posIY+1," ",color)
                self.matriz.insertar(posIX+2,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+2,posIY+2))

                self.ingresarPintar(posIX,posIY+1," ",color)
                self.matriz.insertar(posIX+1,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+2))
                player.points +=1
                self.changePlayer = True
            else:
                QMessageBox.about(self,"Advertencia","¡La pieza no se puede colocar en esa posición!")
                if player.intentosActuales != 1:
                    player.intentosActuales -=1
                    self.intentos.setText(str(player.intentosActuales))
                else:
                    self.camiboJugador()
                player.errors+=1
        elif idFigura == 5:
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            esquinasC = self.comprobarEsquinas(posIX+1,posIY+1,idFigura,jugador)
            if poderIngresar and esquinasC:
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
                self.matriz.insertar(posIX+4,posIY+2,self.nodoPrincipal,nodos(jugador,posIX+4,posIY+2))
                player.points +=1
                self.changePlayer = True
            else:
                QMessageBox.about(self,"Advertencia","¡La pieza no se puede colocar en esa posición!")
                if player.intentosActuales != 1:
                    player.intentosActuales -=1
                    self.intentos.setText(str(player.intentosActuales))
                else:
                    self.camiboJugador()
                player.errors+=1
        elif idFigura == 6:
            inicio = 0
            poderIngresar = self.comprobarFigura(posIX+1,posIY+1,idFigura)
            esquinasC = self.comprobarEsquinas(posIX+1,posIY+1,idFigura,jugador)
            if poderIngresar and esquinasC:
                while inicio != 5:
                    self.ingresarPintar(posIX,posIY+inicio," ",color)
                    self.matriz.insertar(posIX+1,posIY+inicio+1,self.nodoPrincipal,nodos(jugador,posIX+1,posIY+inicio+1))
                    inicio+=1
                player.points +=1
                self.changePlayer = True
            else:
                QMessageBox.about(self,"Advertencia","¡La pieza no se puede colocar en esa posición!")
                if player.intentosActuales != 1:
                    player.intentosActuales -=1
                    self.intentos.setText(str(player.intentosActuales))
                else:
                    self.camiboJugador()
                player.errors+=1
                
    def ingresarPintar(self,posIX,posIY,jugador,color):
        self.tablero.setItem(posIY, posIX, QtWidgets.QTableWidgetItem(jugador))
        self.tablero.item(posIY,posIX).setBackground(QtGui.QColor(color))

if __name__=='__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
