import dominoes 
import random
import copy
import itertools

def minimax(game):
  game_copy = copy.deepcopy(game)

    # for performance
  game_copy.skinny_board()
  moves, _ = dominoes.search.alphabeta(game_copy)
  return(moves[0])

#Función que indica cuantas de piezas de cada numero se tiene. Devuelve lista de tamaño 7
def num_counter(hand):
  count=[]
  for i in range(7):
    j=0
    for d in hand:
      if i in d:
        j+=1
    count.append(j)
  return(count)

def how_many(hand,value):
  return num_counter(hand)[value]

def strong_hand(hand,fuerte=4,acompaña=3):
  c1,c2,c3= False, False,True
  k1,k2= None, None
  repetition=num_counter(hand)
  if 0 in repetition: c3= False 
  for piece,rep in enumerate(repetition):
    if rep>=fuerte: c1,k1= True,piece
    elif rep>=acompaña: c2, k2=True, piece
    
  if (k1==None or k2 == None):
    return False
  elif (k1<k2): ficha=(k1,k2) 
  elif (k1>k2): ficha=(k2,k1)
  if (c1 and c2  and c3 and dominoes.Domino(*ficha)in hand): return True
  else: return False 

'''g=dominoes.Game.new(starting_player=3)
print(g)
for i in range(12):
  g.make_move(*g.valid_moves[0])
  print(g.board)
print(g)
print(g.moves)
'''


'''devuelve un arreglo una lista donde lista[i], es una lista con las jugadas realizadas por el i-esimo jugador'''

def track_players_moves(game):
  jugadas=[[],[],[],[]]
  #b=dominoes.board
  i=game.starting_player
  for k,piece in enumerate(game.moves):
    jugadas[(i+k)%4].append(piece[0])  
  return(jugadas)

class ES:
  def __init__(self):
    pass
  def __call__(game):
    game.valid_moves=game.valid_moves


#def ES_Make_move(game,player=ES()):


def all_dominoes():
 return ([dominoes.Domino(i, j) for i in range(7) for j in range(i, 7)])


def remaining_tiles(game):
  rem_tiles =[]
  played_tiles=[]
  for move in game.moves:
    played_tiles.append(move[0])
  for tile in all_dominoes():
    if tile not in played_tiles and tile not in game.hands[game.turn]:
      rem_tiles.append(tile)
  return rem_tiles

u_third = [0,1./3,1./3,1./3]    
u_one = [1,0,0,0]   

def probabilities(my_tiles):
  
  prob= {d:(copy(u_third) if d not in my_tiles else copy(u_one)) for d in all_dominoes()}
  
  return prob 

def _assign_prob(probabilities, domino, player):
  return probabilities[domino][player] if domino in probabilities else 1

def how_many_turns(game):
  return len(game.moves)

#Función que devuelve los movimientos realizados por cada jugador en formato "util" 
#Esta función combina Jp_moves() y track_players_moves()

def player_moves(game):
  jugadas=[[],[],[],[]]
  i=game.starting_player
  b2=dominoes.SkinnyBoard()
  game_moves=game.moves
  #Agrega el primer movimiento
  tile_1= game_moves[0][0]
  first_play= (tile_1,(tile_1.first,tile_1.second),(None,None))
  jugadas[i].append(first_play)
  b2.add(*game_moves[0])
  # Para el segundo movimiento en adelante:
  for k,move in enumerate(game_moves[1:],start=1):
    b1=copy.deepcopy(b2)
    if move != None:
      b2.add(*move)
    if b2._left != b1._left :
      v,w=b2._left,b1._left
    elif b2._right != b1._right:
      v,w=b2._right,b1._right
    else: v,w=None,None
    if move != None:
      jugada= (move[0],v,w)
    else: 
      jugada=(None) 
    jugadas[(i+k)%4].append(jugada)  
  return(jugadas)

# devuelva la lista de jugadas realizadas en formato util (d,a,c) d: ficha jugada, a:extremo que se abre, c: piedra que se castiga
def Jp_moves(game):
  b2=dominoes.SkinnyBoard()
  jugadas=[]
  
  game_moves=game.moves
  #primera jugada
  tile_1= game_moves[0][0]
  first_play= (tile_1,(tile_1.first,tile_1.second),(None,None))
  jugadas.append(first_play)
  b2.add(*game_moves[0])
  
  for move in game_moves[1:]:

    b1=copy.deepcopy(b2)
    if move != None:
      b2.add(*move)
    if b2._left != b1._left :
      v,w=b2._left,b1._left
    elif b2._right != b1._right:
      v,w=b2._right,b1._right
    else: v,w=None,None
    if move != None:
      jugada= (move[0],v,w)
    else: 
      jugada=(None)
    jugadas.append(jugada)
  return jugadas

def combinando(elementos,tamaños):
  try:
    tamaño= tamaños[0]
  except IndexError:
    yield()
    return
  tamaños=tamaños[1:]
  for partition in itertools.combinations(elementos,tamaño):
    particioncita= elementos.difference(set(partition))
    for minipart in combinando(particioncita,tamaños):
      yield (partition,)+ minipart