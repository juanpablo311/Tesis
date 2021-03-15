import dominoes
from copy import copy,deepcopy
import itertools
import collections



def all_dominoes():
 return ([dominoes.Domino(i, j) for i in range(7) for j in range(i, 7)])

def alguien_paso(aja):
  for i in aja:
    if i == None:
      return True
  return False

def probabilities(game,t):
  
  #u_one es la lista de probabilidades para mis fichas
  #u_thir es la lista de probabilidades para las demas fichas
  u_one,u_third = [0]*4,[1/3]*4
  u_one[t],u_third[t]= 1,0
  my_tiles=game.hands[t]
  prob= {d:u_third if d not in my_tiles else u_one for d in all_dominoes()}
  return prob

def d_played(game):
  dominoes_played=[]
  for move in game.moves:
    if move != None:
      dominoes_played.append(move[0])
    else: dominoes_played.append(move)
  return dominoes_played


def _update_probs(game,t):
  p=probabilities(game,t)
  hands= game.hands
  L_i= list(map(lambda x: len(x),hands))
  L_i[t]=0
  dominoes_played=d_played(game)
  for d in all_dominoes():
    if d in dominoes_played:
      p[d]= [0]*4
    elif d in hands[t]:
      p[d]=[0]*4
      p[d][t]=1
    else: 
      if alguien_paso(dominoes_played):
        L_prime=deepcopy(L_i)
        for k,s in enumerate(game.missing_values()):
          if d.first in s or d.second in s:
            L_prime[k]=0
        L=sum(L_prime)
        L_f=L_prime
      else: 
        L=sum(L_i)
        L_f=L_i
      p[d]=[l/L for l in L_f]
  return p

def remaining_tiles(game):
  rem_tiles =[]
  played_tiles=[]
  for move in game.moves:
    played_tiles.append(move[0])
  for tile in all_dominoes():
    if tile not in played_tiles and tile not in game.hands[game.turn]:
      rem_tiles.append(tile)
  return rem_tiles

def evaluate(game,p):
  expectation_opp = 0
  expectation_us = 0
  turn=game.turn
  for d in p:
    if d not in d_played(game):
      probs = p[d]
      value = d.first+d.second
      expectation_opp += value*probs[(turn+1)%4] + value*probs[(turn+3)%4]
      expectation_us += value*probs[turn] + value*probs[(turn+2)%4]
  
  return expectation_opp - expectation_us 

def p_negamax_ab(game,depth,alpha,beta,player=dominoes.players.identity,t=None,p_prime=None):
  #almacena el valor inicial del turno del jugador 
  if t==None: t=game.turn
  p =_update_probs(game,t)
  
  if p_prime!=None and p!=p_prime:
    
  #Caso base
  if depth==0 or game.result!= None:
    return[], evaluate(game,p)
  best_value = -float('inf')
  for move, new_game in dominoes.search.make_moves(game,player):
    q= p[move[0]][new_game.turn-1]
    if q>0:
      moves,value =p_negamax_ab(new_game,depth-1,-alpha,-beta,player,t,p_prime=None)
      value = -q*value
      if best_value< value:
        best_moves=moves
        best_value=value
        best_moves.insert(0,move)
        alpha=max(alpha,best_value)
        if alpha>=beta:
          break
  return best_moves, best_value




g=dominoes.Game.new()
print(g)
for i in range(2):
  g.make_move(*g.valid_moves[0])
print(g)
print('moves in formato cancer')
print(g.moves)
g_prime=deepcopy(g)
moves, valor = p_negamax_ab(g_prime,2,5,1/2,player=dominoes.players.identity)

g_prime.make_move(*moves[0])
g_prime.make_move(*moves[1])
p=_update_probs(g,2)
print('ahora, si probemos qlq')
movess, valors = p_negamax_ab(g,2,5,1/2,player=dominoes.players.identity,t=None,p_prime=p)

#for item in p.items():
#print (item)

#print(p==p_prime)

'''
p=_update_probs(g,3)
print(evaluate(g,p))
p=_update_probs(g,0)
print(evaluate(g,p))
p=_update_probs(g,1)
print(evaluate(g,p))'''
'''
print(valor)
print(d_played(g))
expectation_opp = 0
expectation_us = 0
turn=g.turn
'''
'''
for d in p:
  if d not in d_played(g):
      probs = p[d]
      value = d.first+d.second
      expectation_opp += value*probs[(turn+1)%4] + value*probs[(turn+3)%4]
      expectation_us += value*probs[turn] + value*probs[(turn+2)%4]
      print(d)
      print(p[d])
      print(expectation_us)
      print(expectation_opp)
print(expectation_opp-expectation_us )
'''