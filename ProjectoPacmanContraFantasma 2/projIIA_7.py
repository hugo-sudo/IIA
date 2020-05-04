#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from statistics import stdev
import math
import layout
from distanceCalculator import *

def anti_scoreNosso(gState,player):    
    myPos = gState.board.getPacmanPosition()
    
    ghost = gState.board.getGhostState(1)
    ghostPos = ghost.getPosition()
    ghostPosInit = ghost.start.getPosition() 
    distance = distancia_euclidiana(myPos, ghostPos)
    pastilhas = gState.board.getCapsules()
    
    foodList = gState.board.getFood().asList()
    if ghost.scaredTimer > 0:
        return -gState.board.getScore()*120 + distance
    
    if gState.board.getNumFood() > 1 :
        x = []
        y = []
        for food in foodList:
            x.append(food[0]) 
            y.append(food[1])
        mediaX = sum(x)/len(foodList)
        mediaY = sum(y)/len(foodList)
        desvX = stdev(x)
        desvY = stdev(y)
        mostFood = (mediaX,mediaY)
        menorX = []
        maiorX = []
        for point in x:
            if point > mediaX:
                maiorX.append(point)
            if point < mediaX:
                menorX.append(point)
                
        menorY = []
        maiorY = []        
        for point in y:
            if point > mediaY:
                maiorY.append(point)
            if point < mediaY:
                menorY.append(point)
                
                
        if len(maiorY) > len(menorY) and len(maiorX) > len(menorX):
            mostFood = (mediaX+desvX,mediaY+desvY)
        elif len(maiorY) > len(menorY) and len(maiorX) < len(menorX):
            mostFood = (mediaX-desvX,mediaY+desvY)
        elif len(maiorY) < len(menorY) and len(maiorX) > len(menorX):
            mostFood = (mediaX+desvX,mediaY-desvY)
        else:
            mostFood = (mediaX-desvX,mediaY-desvY)
            
        distanceToFood = distancia_euclidiana(mostFood, ghostPos)
        return -gState.board.getScore()*100 - distance - distanceToFood * 10
    
    return -gState.board.getScore()*100 - distance
    
def scoooreNosso(gState,player):
    foodList = gState.board.getFood().asList()
    minDistance = 0
    myPos = gState.board.getPacmanPosition()
    ghostPos = gState.board.getGhostPosition(1)
    pacGhostDist = distancia_euclidiana(myPos, ghostPos)
    pastilhas = gState.board.getCapsules()
    timer = gState.board.getGhostState(1).scaredTimer
    distObj = Distancer (gState.board.data.layout)
    
    
    """
    extra = gState.extra
    parou = False
    listaUltimasPos = extra.get('Pacman')
    
    for i in range(len(listaUltimasPos)):
        contador = 0
        for j in range(len(listaUltimasPos)):
            if listaUltimasPos[i] == listaUltimasPos[j] :
                contador += 1
        if(contador >= 6) : 
            distance = distancia_euclidiana(myPos, ghostPos)
            print("PUTINHA DO INDIANO")
            return gState.board.getScore()*100 - distance
    
    trapped = False
    if len(pastilhas) <= 2 and len(pastilhas)>0:
        for pastilha in pastilhas:
            up = gState.board.hasFood(pastilha[0],pastilha[1]+1)
            down = gState.board.hasFood(pastilha[0],pastilha[1]-1)
            right = gState.board.hasFood(pastilha[0]+1,pastilha[1])
            left = gState.board.hasFood(pastilha[0]-1,pastilha[1])
            if up or down or right or left:
                trapped = True
    """
    
    if len(pastilhas) > 4:

        if gState.board.isLose():
            #print("ENTROU CASO QUE EH LOSER COMO O INDIANO", -10000000000000000000000000000000000000000000000000000000)
            #print("*****************************************")
            return -100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

        if len(pastilhas) > 0  and len(foodList) == 1:
            #print("ENTROU CASO QUE SO HA UMA PASTILHA ", -10000000000000000000000000000000000000000000000000000000)
            #print("*****************************************")
            return -10000000000000000000000000000000000000000000000000000000

        if timer > 0:
            distance = distObj.getDistance (myPos, ghostPos)
            if(distance < timer*2):
                #print("ENTROU CASO QUE CONSEGUE COMER GHOST PELO TIMER ",gState.board.getScore()*120 - distance*10 - timer)
                #print("*****************************************")
                return gState.board.getScore()*120 - distance*10 - timer

        if pacGhostDist < 5 and len(pastilhas) > 0:
            minDistance = min([distObj.getDistance(myPos, pastilha) for pastilha in pastilhas])
            #print("ENTROU CASO QUE O FANTASMA ESTAH PERTO ",gState.board.getScore()*100 - minDistance)
            #print("*****************************************")
            return gState.board.getScore()*100 - minDistance

        if len(foodList) > 2 :
            minDistance = min([distObj.getDistance(myPos, food) for food in foodList])
        else:
            if len(pastilhas) > 1:
                minDistance = min([distObj.getDistance(myPos, pastilha) for pastilha in pastilhas])
            elif len(pastilhas) == 1: 
                minDistance = distObj.getDistance(myPos, pastilhas[0])
            elif len(foodList)>0:
                minDistance = distObj.getDistance(myPos, foodList[0])


        if len(pastilhas) > 0:
            minDistance2 = min([distObj.getDistance(myPos, pastilha) for pastilha in pastilhas])
            if minDistance > minDistance2:
                minDistance = minDistance2

        #print("ENTROU CASO BASE ",gState.board.getScore() * 100 - minDistance)
        #hhhprint("*****************************************")
        return gState.board.getScore() * 100 - minDistance
    
    else:

        if timer > 0:
            distance = distObj.getDistance(myPos, ghostPos)
            if(distance < timer*2):
                return gState.board.getScore()*120 - distance

        for position in foodList:
            if gState.board.hasFood(position[0],position[1]):
                up = gState.board.hasFood(position[0],position[1]+1)
                down = gState.board.hasFood(position[0],position[1]-1)
                right = gState.board.hasFood(position[0]+1,position[1])
                left = gState.board.hasFood(position[0]-1,position[1])
                if up==False and down==False and right==False and left==False:
                    distance = distObj.getDistance(myPos, position)
                    if distance < 10 : 
                        return gState.board.getScore()*100 - distance

        if pacGhostDist < 10 and len(pastilhas) > 0:
            minDistance = min([distObj.getDistance(myPos, pastilha) for pastilha in pastilhas])
            return gState.board.getScore()*100 - minDistance

        if len(foodList) > 0 :
            minDistance = min([distObj.getDistance(myPos, food) for food in foodList])
        if len(pastilhas) > 0:
            minDistance2 = min([distObj.getDistance(myPos, pastilha) for pastilha in pastilhas])
            if minDistance > minDistance2:
                minDistance = minDistance2


        return gState.board.getScore() * 100 - minDistance    
    
   
    
def distancia_euclidiana(ponto1, ponto2):
    dimensao = len(ponto1)
    soma = 0
    for i in range(dimensao):
        soma += math.pow(ponto1[i]-ponto2[i],2)
    return math.sqrt(soma)


def extraP_7(gState,extra):
    if extra == {}:
        n_extra ={'Pacman':[gState.getPacmanPosition()]}
        return n_extra
    else:
        pacmanList = (extra.get('Pacman')).copy()
        if(len(pacmanList)>14):
            pacmanListRemoved = pacmanList[:14]
            extra['Pacman'] = pacmanListRemoved
        n_extra= extra.copy()
        n_extra['Pacman']=[gState.getPacmanPosition()]+n_extra['Pacman']
    return n_extra

def extraF_7(gState,extra):
    if extra == {}:
        n_extra ={'Pacman':[gState.getPacmanPosition()]}
        return n_extra
    else:
        pacmanList = (extra.get('Pacman')).copy()
        if(len(pacmanList)>14):
            pacmanListRemoved = pacmanList[:14]
            extra['Pacman'] = pacmanListRemoved
        n_extra= extra.copy()
        n_extra['Pacman']=[gState.getPacmanPosition()]+n_extra['Pacman']
    return n_extra





