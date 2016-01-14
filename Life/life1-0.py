import time, os, sys

vel = 1
mapa = [[0 for x in range(8)] for x in range(8)]
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
#mapa[][] = 1

def imprimir(mapa):
   for i in range(8):
      cad = ""
      for j in range(8):
         cad += str(mapa[i][j]) + "  "
      print cad

def vecinas(i, j, mapa):
   cont = 0
   if(i>0 and j>0):
      if(mapa[i-1][j-1] == 1):
         cont +=1
      if(mapa[i-1][j] == 1):
         cont +=1
      if(mapa[i-1][j+1] == 1):
         cont +=1
      if(mapa[i][j-1] == 1):
         cont +=1
      if(mapa[i][j+1] == 1):
         cont +=1
      if(mapa[i+1][j-1] == 1):
         cont +=1
      if(mapa[i+1][j] == 1):
         cont +=1
      if(mapa[i+1][j+1] == 1):
         cont +=1
   return cont
imprimir(mapa)
c = 0
while c < 3:
 for i in range(7):
   for j in range(7):
      vecin = vecinas(i,j,mapa)
      cad = str(i)+" "+str(j)+" "+str(vecin)
      print cad
      if(mapa[i][j] == 1):
         if(vecin >= 4):
            mapa[i][j] = 0
         if((vecin == 2) or (vecin == 3)):
            mapa[i][j] = 1
         if(vecin <= 1):
            mapa[i][j] = 0
      if(mapa[i][j] == 0):
         if(vecin == 3):
            mapa[i][j] = 1
 #os.system('clear')
 print c
 imprimir(mapa)
 time.sleep(vel)
 c += 1





