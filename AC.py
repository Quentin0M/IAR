# -*- coding: utf-8 -*-
from grilles import *
import matplotlib.pyplot as plt

used_grid = copy.copy(grille1)
V = np.zeros(used_grid.shape)
W = np.zeros(tuple(list(used_grid.shape)+[8]))
gamma = .9
delta = 0
tau = 10
alphaC = .2
alphaA = .1


posx = 1
posy = 11

# transition function : 0 is north and it goes clockwise to 7 = northwest
def T(a):
    global posx, posy
    tmpx = posx
    tmpy = posy
    if a==0:
        tmpx-=1
    elif a==1:
        tmpy+=1
        tmpx-=1
    elif a==2:
        tmpy+=1
    elif a==3:
        tmpy+=1
        tmpx+=1
    elif a==4:
        tmpx+=1
    elif a==5:
        tmpy-=1
        tmpx+=1
    elif a==6:
        tmpy-=1
    elif a==7:
        tmpy-=1
        tmpx-=1
    if used_grid[tmpx,tmpy]!=0 and used_grid[tmpx,tmpy]!=3:
        return tmpx,tmpy
    return posx, posy
		

# returns a cumulated vector of P(0) to P(7) to facilitate the selection
def P():
    global tau, W, posx, posy
    p = [np.exp(W[posx,posy,a]/tau)/sum([np.exp(W[posx,posy,ap]/tau)for ap in range(8)]) for a in range(8)]
    for a in range(1,8):
        p[a]+=p[a-1]
    return p
        
        

def R(a):
    global posx, posy, used_grid
    x,y = T(a)
    if (x,y) == (posx,posy):
        return 0
    if used_grid[x, y] == 1:
        return 0
    elif used_grid[x,y] == 2:
        return 100

def update_delta(a):
    global delta
    x,y = T(a)
    delta = R(a) + gamma*V[x,y] - V[posx,posy]


def AC():
    global delta, used_grid, gamma, alphaC, alphaA, posx, posy, V, W
    time_table=np.zeros(200)
    for episode in range(200):
        posx=1
        posy=11
        t=0
        while used_grid[posx,posy] != 2:# and t<1000:
            #print W[posx,posy]
            p = P()
            choice = np.random.uniform()
            a=0
            while choice>p[a]:
                a += 1
            update_delta(a)
##            if V[posx,posy] == 0 :
##                V[posx,posy] = t-1000 
            V[posx,posy] += alphaC * delta
            W[posx,posy,a] += alphaA * delta 
            posx,posy = T(a) 
            t += 1
            #print a
            #print 'temps='+str(t)+" position = ("+str(posx)+','+str(posy)
        print "arrivé à "+str(episode)
        time_table[episode] = t
    return time_table

#time_table = AC()
##plt.plot(range(200), time_table)
##plt.show()


## Hierarchic RL

Vo = np.zeros(used_grid.shape)
# The weight of the options at a given location
WO = np.zeros(tuple(list(used_grid.shape)+[16]))
# the weight of the primitive options given the current abstract option and location
Wo = np.zeros(tuple([8]+list(used_grid.shape)+[8]))
# current active option (-1 means no option is selected)
current_option = -1

training = True

posxo = 1
posyo = 11

def available_options():
    global posxo,posyo
    if posxo < 6 and posyo < 6:
        return [0,1,2,3,4,5,6,7,8,9]
    if posxo < 7 and posyo > 6:
        return [0,1,2,3,4,5,6,7,10,11]
    if posxo > 7 and posyo > 6:
        return [0,1,2,3,4,5,6,7,12,13]
    if posxo > 6 and posyo < 6:
        return [0,1,2,3,4,5,6,7,14,15]
    # the robot is inside a door and must leave it with a primitive option
    return [0,1,2,3,4,5,6,7]

def option_target():
    global current_option
    if current_option == 0: return 3,6
    if current_option == 1: return 6,2
    if current_option == 2: return 3,6
    if current_option == 3: return 7,9
    if current_option == 4: return 7,9
    if current_option == 5: return 10,6
    if current_option == 6: return 10,6
    if current_option == 7: return 6,2

def Ro(a):
    global posxo,posyo,used_grid
    if current_option == -1:
        x,y=T(a)
        if used_grid[x,y] == 2 and not training:
            return 100
        else:
            return 0
    else:
        if (posxo,posyo)==(option_target()):
            return 100
        return 0

# returns a cumulated vector of P(0) to P(7) to facilitate the selection
def Po():
    
    global tau, Wo, posxo, posyo, current_option, WO
    if current_option == -1:
        o = available_options()
        p = [np.exp(WO[posxo,posyo,a]/tau)/sum([np.exp(WO[posxo,posyo,ap]/tau)for ap in o]) for a in o]
        for a in range(len(o)):
            p[a]+=p[a-1]
        return p
    p = [np.exp(Wo[current_option][posxo,posyo,a]/tau)/sum([np.exp(Wo[current_option][posxo,posyo,ap]/tau)for ap in range(8)]) for a in range(8)]
    p = np.asarray(p)
    for a in range(8):
        p[a]+=p[a-1]
    return p

def execute_option():
    global deltao, used_grid, gammao, alphaC, alphaA, posxo, posyo, Vo, Wo, current_option
    t = 0
    d=0
    rcum=0
    while (posxo,posyo) != (option_target()):
        p = Po()
        choice = np.random.uniform()
        a=0
        while choice>p[a]:
            a += 1
        x,y=T(a)
        reward = Ro(a)
        rcum+=reward
        d = Ro(a) + gamma*Vo[x,y] - Vo[posxo,posyo]
        Vo[posxo,posyo] += alphaC * d
        Wo[current_option][posxo,posyo,a] += alphaA * d 
        posxo,posyo = x,y 
        t += 1
    return rcum,t

def HRL():
    global deltao, used_grid, gammao, alphaC, alphaA, posxo, posyo, Vo, Wo, WO, training, current_option
    time_table=np.zeros(200)
    cpt = 0
    for episode in range(201):
        posx=1
        posy=11
        t=0
        print "episode "+str(episode)
        while used_grid[posxo,posyo] != 2 or training:# and t<1000:
            #print W[posx,posy]
            o = available_options()
            p = Po()
            choice = np.random.uniform()
            a=0
            while choice>p[a]:
                a += 1
            if a > 7:
                current_option = a - 8
                xinit,yinit = posxo,posyo
                rcum,ttot = execute_option()
                deltao = rcum + gamma**ttot * Vo[posxo,posyo] - Vo[xinit,yinit]
                Vo[xinit,yinit] += alphaC*deltao
                WO[xinit,yinit,current_option+8] += alphaA+deltao
                t += ttot
                current_option = -1
            else:
                x,y=T(a)
                deltao = Ro(a) + gamma * Vo[posxo,posyo] - Vo[x,y]
                Vo[posxo,posyo] += alphaC * deltao
                WO[posx,posy,a] += alphaA * deltao 
                posx,posy = T(a) 
                t += 1
            if training:
                cpt =t
                print "Training : "+str(cpt)
                if cpt > 50000:
                    print "Training fini"
                    t=0
                    training = False
                    break
                
        if not training: time_table[episode-1] = t
    return time_table

time_RL = AC()
time_HRL = HRL()
plt.plot(range(200), time_HRL, label = 'with options')
plt.plot(range(200), time_RL, label = 'without_option')
plt.legend(["with options","without options"])
plt.show()

used_grid = grille3
time_HRL = HRL()
plt.plot(range(200), time_HRL, label = 'with options')
time_RL = AC()
plt.plot(range(200), time_RL, label = 'without_option')
plt.show()



