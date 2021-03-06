import dominoes.__init__
import subprocess

# possible strategies for each of the players
f3=open('test3.txt','w') 

ai=[dominoes.players.random,dominoes.players.omniscient()]

player_list =[ai[0],ai[0],ai[0],ai[0]]
# clear the terminal before starting the series
input('Welcome! Proceeding will clear all text from this terminal session.'
      ' If you are OK with this, press enter to continue.')
subprocess.call(['tput', 'reset'])

# start a series up to `target_score`

series = dominoes.Series(target_score=100)
game = series.games[0]

# print out the possible player settings

# the game will be None once the series has ended
while game is not None:
    # clear the terminal upon starting a new game
    

    # the player holding the [6|6] plays first, in the first game. in all other
    # games, the outcome of the previous game determines the starting player.
    if len(series.games) == 1:
        print('Player {} had the [6|6] and made the first move.'.format(game.starting_player))
        f3.write('Player {} had the [6|6] and made the first move.\n'.format(game.starting_player))
    # game.result will be filled in once the game ends
    while game.result is None:
        # print the game state so that all players can see it
        print('Board:')
        f3.write('Board:')
        print(game.board)
        f3.write(str(game.board))
        for player, hand in enumerate(game.hands):
            print('Player {} hand: {} .'.format(player,hand))
            f3.write('Player {} hand: {}\n .'.format(player,hand))

        # clear the terminal upon starting a new turn
        
        # print the board so that the player can decide what to play
        print('Board:')
        f3.write('Board:')
        print(game.board)
        f3.write(str(game.board)+'\n')

        # remember whose turn it currently is.
        # we'll need it after we move on to the next player.
        turn = game.turn

        # get the setting for the current player
      

        
        current_player=player_list[game.turn]
        current_player(game)
            # print out the selected move
        print('Player {}  chose to play {} on the {} end of the board.'.format(
                game.turn,
                game.valid_moves[0][0],
                'left' if game.valid_moves[0][1] else 'right'
            ))
        f3.write('Player {}  chose to play {} on the {} end of the board.\n'.format(
                game.turn,
                game.valid_moves[0][0],
                'left' if game.valid_moves[0][1] else 'right'
            ))

            # make the selected move
        game.make_move(*game.valid_moves[0])

        # clear the terminal upon moving to the next
        # turn - no looking at the previous player's hand!
    

    # game over - move on to the next game
    print('Game over!')
    f3.write('Game over!\n')
    print(game)
    f3.write(str(game)+'\n')
    

    game = series.next_game()
    print('The current state of the series:')
    f3.write('The current state of the series:')
    print(series)
    f3.write(str(series)+'\n')

# once the series has ended, print out the winning team
winning_team, _ = max(enumerate(series.scores), key=lambda i_score: i_score[1])
print('Team {} wins!'.format(winning_team))
f3.write('Team {} wins!\n'.format(winning_team))