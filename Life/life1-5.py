import pygame, sys, os, time
from pygame.locals import * 

#variables globales
#n: es el numero de celdas que se mostraran en pantalla
n = 36
#velocidad: es la velocidad de sleep(si no esta comentado)
velocidad = 1
color = (0,0,0)
#rectangulos: es un arreglo de n x n para los rectangulos de las celdas en pantalla
rectangulos = [[0 for x in range(n)] for x in range(n)]
#mapa: es un mapa de las celdas mostradas en pantalla que se usa para saber que celdas estan vivas o muertas
#      y para contar vecinas, me parecio mas facil usar esto para poder controlar mejor las celdas vivas y muertas
#      ya que controlar si los rect de pygame tenian un circulo o no me parecia que usaria mucha memoria.
mapa = [[0 for x in range(n)] for x in range(n)]
#listaPuntos: es una lista con las posiciones de los centros de ciertos rect de pygame para poder dibujar los circulos
#             en pantalla.
listaPuntos = []

#Este metodo cuenta vecinas de la celda de la columna "j" fila "i" creando un cuadrado que esta conformado por las celdas 
#que rodean la celda para luego con un ciclo recorrer el cuadrado con los bordes controlados contando celdas vivas y al
#final resta uno si la celda actual esta viva para que no se cuente.
def vecinas(j, i):
   cont = 0
   if(i == 0):
      ysup = i
   else:
      ysup = i - 1
   if(j == 0):
      xsup = j
   else:
      xsup = j - 1
   if(i == (n - 1)):
      yinf = i
   else:
      yinf = i + 1
   if(j == (n - 1)):
      xinf = j
   else:
      xinf = j + 1
   for x in range(xsup, xinf + 1):
      for y in range(ysup, yinf + 1):
         if(mapa[x][y] == 1):
            cont = cont + 1
   if(mapa[j][i] == 1):
      cont = cont - 1
   return cont

#Este metodo se usa al final para imprimir en consola la posicion de las ultimas celdas vivas y muertas mostradas
#en pantalla.
def imprimirmapa(mapa):
   for i in range(n):
      cad = ""
      for j in range(n):
         if(mapa[i][j] == 1):
            cad += "o "
         else:
            cad += "_ "
      print cad

#generaciones: se encarga de controlar las condiciones del juego de la vida
def generaciones(listaPuntos):
 global mapa
 nuevomapa = [[0 for x in range(n)] for x in range(n)]
 for i in range(n):
   for j in range(n):
      vecino = vecinas(j,i)
      if(mapa[j][i] == 1):
         if(vecino >= 4):
            nuevomapa[j][i] = 0
         if((vecino == 2) or (vecino == 3)):
            nuevomapa[j][i] = 1
            centroCirculo = (rectangulos[j][i].centerx, rectangulos[j][i].centery)
            listaPuntos.append(centroCirculo)
         if(vecino <= 1):
            nuevomapa[j][i] = 0
      if(mapa[j][i] == 0):
         if(vecino == 3):
            nuevomapa[j][i] = 1
            centroCirculo = (rectangulos[j][i].centerx, rectangulos[j][i].centery)
            listaPuntos.append(centroCirculo)
 mapa = nuevomapa
 return listaPuntos
#siguienteGeneracion: limpia lista de puntos y llama a generaciones para calcular la siguiente generacion.
def siguienteGeneracion(listaPuntos):
   #se borra completamente la lista de puntos para evitar que se pinten puntos no deseados
   listaPuntos[:] = []
   generaciones(listaPuntos)
   return listaPuntos

#funcion para cargar imagenes
def load_image(filename, transparent = False):
    try:
       image = pygame.image.load(filename)
    except pygame.error, message:
       raise SystemExit, message
    image = image.convert()
    if transparent:
       color = image.get_at((0,0))
       image.set_colorkey(color,RLEACCEL)
    return image 

#funcion para manipular texto en pantalla
def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font('images/DroidSans.ttf', 20)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

#inicializa pygame
pygame.init()  

#tamaño de pantalla, dimension de rectangulos, visibilidad del mouse
screen = pygame.display.set_mode((650, 750))  
dim = 650/n
pygame.mouse.set_visible(1)

#se añade titulo a la ventana
titulo = "JuegoVida"
pygame.display.set_caption(titulo)  

#Se carga la imagen de fondo y se toma el rect
#Obs: -Porque no se pone un color especifico de fondo-
#   no lo hice de esa manera porque pygame al tener un color de fondo no lo vuelve a pintar encima
#   del resto de cosas que pinto en el ciclo anterior por lo que queda manchado con restos de los 
#   dibujos anteriores y eso se mira fatal, por lo tanto opte por poner una imagen de fondo para
#   solucionar ese detalle, ya que creo que es la unica forma.
fondoI = load_image("images/fondo.png")
fondo = fondoI.get_rect()

#obtener imagen de triangulo que servira para play, up, down
img = load_image('images/play.png', True)
pauseI = load_image('images/pause.png', True)

#cambiamos tamanio y rotamos
pauseI = pygame.transform.scale(pauseI, (50,50))
botonPlayI = pygame.transform.scale(img, (50, 50))
botonUpI = pygame.transform.scale(img, (25, 25))
botonPlayI = pygame.transform.rotate(botonPlayI, -90)
botonDownI = pygame.transform.rotate(botonUpI, 180)

#obtenemos rectangulos de los botones
botonPause = pauseI.get_rect()
botonPlay = botonPlayI.get_rect()
botonUp = botonUpI.get_rect()
botonDown = botonDownI.get_rect()

#posicionamos "botones" en la posicion deseada
botonPause.centerx = 325
botonPause.centery = 680
botonPlay.centerx = 325
botonPlay.centery = 680
botonUp.centerx = 15
botonUp.centery = 667
botonDown.centerx = 16
botonDown.centery =697

#play_act: Booleano para saber si el play se ah presionado o no.
play_act = False

#ciclo principal
while True:
    #se toman los eventos(si hay) y se guardan en eventos
    eventos = pygame.event.get()  
    #recorremos eventos en busca de cualquier evento que pueda surguir
    for eventos in eventos:
           #controla el evento de cerrar la ventana
           if eventos.type == QUIT:
              imprimirmapa(mapa)
              sys.exit(0)
           if eventos.type == pygame.MOUSEBUTTONDOWN:
              pos = pygame.mouse.get_pos()
	      if(botonPlay.collidepoint(pos)):
		 if(play_act):
                    play_act = False
                    print "play = false"
                 else:
	            play_act = True
		    print "play = true"
	      for i in range(n):
                 for j in range(n):
                    if(rectangulos[j][i].collidepoint(pos)):
                        mapa[j][i] = 1
                        centroCirculo = (rectangulos[j][i].centerx, rectangulos[j][i].centery)
			listaPuntos.append(centroCirculo)
			break

    #se dibuja la imagen de fondo
    screen.blit(fondoI, fondo)
    if(play_act):
       screen.blit(pauseI, botonPause)
    else:
       screen.blit(botonPlayI, botonPlay)
    screen.blit(botonUpI, botonUp)
    screen.blit(botonDownI, botonDown)
    for i in range(n):
       for j in range(n):
          rectangulos[j][i] = pygame.draw.rect(screen, color, (i*dim, j*dim,   dim,   dim), 1)
    
    for punto in listaPuntos:
       pygame.draw.circle(screen, color, punto, dim/3) 
    if (play_act):
       siguienteGeneracion(listaPuntos)
       for punto in listaPuntos:
          pygame.draw.circle(screen, color, punto, dim/3)
    #time.sleep(velocidad)
    pygame.display.flip()
    
    
