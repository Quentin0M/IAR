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
            print a
            print 'temps='+str(t)+" position = ("+str(posx)+','+str(posy)
        print "arrivé à "+str(episode)
        time_table[episode] = t
    return time_table

time_table = AC()
##plt.plot(range(200), time_table)
##plt.show()


## Hierarchic RL

V = np.zeros(used_grid.shape)
W = np.zeros(tuple(list(used_grid.shape)+[8]))

# returns a cumulated vector of P(0) to P(7) to facilitate the selection
def Po():
    global tau, Wo, posxo, posyo
    p = [np.exp(W[posx,posy,a]/tau)/sum([np.exp(W[posx,posy,ap]/tau)for ap in range(16)]) for a in range(16)]
    for a in range(1,8):
        p[a]+=p[a-1]
    return p

def HRL():
    global deltao, used_grid, gammao, alphaC, alphaA, posxo, posyo, Vo, Wo
    time_table=np.zeros(200)
    for episode in range(200):
        posx=1
        posy=11
        t=0
        while used_grid[posx,posy] != 2:# and t<1000:
            #print W[posx,posy]
            p = Po()
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
            print a
            print 'temps='+str(t)+" position = ("+str(posx)+','+str(posy)
        print "arrivé à "+str(episode)
        time_table[episode] = t
    return time_table





