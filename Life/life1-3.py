import pygame, sys, os, time
from pygame.locals import * 

n = 36
velocidad = 0.5
color = (0,0,0)
rectangulos = [[0 for x in range(n)] for x in range(n)]
mapa = [[0 for x in range(n)] for x in range(n)]
listaPuntos = []

def vecinas(i, j, mapa):
   #SE CREA UN CUADRADO CON LOS BORDES CONTROLADOS PARA CONTAR CELDAS VECINAS 
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
   if(mapa[i][j] == 1):
      cont = cont - 1
   return cont

def imprimirmapa(mapa):
   for i in range(n):
      cad = ""
      for j in range(n):
         if(mapa[i][j] == 1):
            cad += "o "
         else:
            cad += "_ "
      print cad

def generaciones():
 nuevomapa = [[0 for x in range(n)] for x in range(n)]
 for i in range(n):
   for j in range(n):
      vecino = vecinas(i,j,mapa)
      #cad = str(i)+" "+str(j)+" "+str(vecin)
      #print cad
      if(mapa[i][j] == 1):
         if(vecino >= 4):
            nuevomapa[i][j] = 0
         if((vecino == 2) or (vecino == 3)):
            nuevomapa[i][j] = 1
         if(vecino <= 1):
            nuevomapa[i][j] = 0
      if(mapa[i][j] == 0):
         if(vecino == 3):
            nuevomapa[i][j] = 1
 return nuevomapa

def siguienteGeneracion():
   listaPuntos = []
   generaciones()

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

pygame.init()  

screen = pygame.display.set_mode((650, 750))  
dim = 650/n
pygame.mouse.set_visible(1)

titulo = "JuegoVida"
pygame.display.set_caption(titulo)  

fondoI = load_image("images/fondo.png")
fondo = fondoI.get_rect()

#obtener imagen de triangulo que servira para play, up, down
img = load_image('images/play.png', True)

#cambiamos tamanio y rotamos
botonPlayI = pygame.transform.scale(img, (50, 50))
botonUpI = pygame.transform.scale(img, (25, 25))
botonPlayI = pygame.transform.rotate(botonPlayI, -90)
botonDownI = pygame.transform.rotate(botonUpI, 180)

#obtenemos rectangulos de los botones
botonPlay = botonPlayI.get_rect()
botonUp = botonUpI.get_rect()
botonDown = botonDownI.get_rect()

#posicionamos "botones" en la posicion deseada
botonPlay.centerx = 325
botonPlay.centery = 680
botonUp.centerx = 15
botonUp.centery = 667
botonDown.centerx = 16
botonDown.centery =697

while True:
    play_act = False
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
	         play_act = True
	      for i in range(n):
                 for j in range(n):
                    if(rectangulos[j][i].collidepoint(pos)):
                        mapa[j][i] = 1
                        centroCirculo = (rectangulos[j][i].centerx, rectangulos[j][i].centery)
			listaPuntos.append(centroCirculo)
			break

    #se dibuja la imagen de fondo
    screen.blit(fondoI, fondo)
    screen.blit(botonPlayI, botonPlay)
    screen.blit(botonUpI, botonUp)
    screen.blit(botonDownI, botonDown)
    for i in range(n):
       for j in range(n):
          rectangulos[j][i] = pygame.draw.rect(screen, color, (i*dim, j*dim,   dim,   dim), 1)
    
    for punto in listaPuntos:
       pygame.draw.circle(screen, color, punto, dim/3) 
    if(play_act):
       siguienteGeneracion()
    #time.sleep(velocidad)
    pygame.display.flip()
    
    
