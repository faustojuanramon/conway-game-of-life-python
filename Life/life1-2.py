import time, os, sys

vel = 0.5
n = 8
mapa = [[0 for x in range(n)] for x in range(n)]
mapa[1][1] = 1
mapa[2][1] = 1
mapa[3][1] = 1
mapa[4][1] = 1
mapa[2][2] = 1
mapa[3][3] = 1
mapa[4][4] = 1
mapa[3][4] = 1
mapa[2][4] = 1
mapa[1][4] = 1
mapa[4][4] = 1
mapa[5][5] = 1
mapa[6][7] = 1
mapa[4][6] = 1
mapa[7][7] = 1

def imprimir(mapa):
   for i in range(n):
      cad = ""
      for j in range(n):
         if(mapa[i][j] == 1):
            cad += "o "
         else:
            cad += "_ "
      print cad

def vecinas(i, j, mapa):
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
imprimir(mapa)
c = 0
while c < 30:
 if c == 6:
    mapa[2][2] = 1
    mapa[3][3] = 1
    mapa[4][4] = 1
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
 os.system('clear')
 mapa = nuevomapa
 print c
 imprimir(mapa)
 time.sleep(vel)
 c += 1





