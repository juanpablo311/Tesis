import dominoes
import random
from copy import copy
from dominoes.juanp import all_dominoes


'''devuelve un diccionario, donde key = ficha de domino, value= [p0,p1,p2,p3] donde pi es la probablidad del i-esimo jugador'''
u_third = [0,1./3,1./3,1./3]    
u_one = [1,0,0,0]  


def probabilities(my_tiles):
  prob= {d:(copy(u_third) if d not in my_tiles else copy(u_one)) for d in all_dominoes()}
  return prob 

def _assign_prob(probabilities, domino, player):
  return probabilities[domino][player] if domino in probabilities else 1

def probability_actions(game):
#no se hace falta current player, porque valid_moves lo incluye
  p= probabilities(game.hands[game.turn])
  possible_moves = []
  '''hay que arreglar este webo, porque valid moves contine tuplas (domino,booleano) y hands solo dominos'''
  for dom in g.valid_moves:
    possible_moves.append(dom[0])
   
  def ap(d):
    return (d, _assign_prob(p,d[0], game.turn))
  return map(ap, possible_moves)

g=dominoes.Game.new(starting_player=3)
print(g)
print(g.valid_moves)
print(probabilities(g.hands[g.turn]))
print(list(probability_actions(g)))
