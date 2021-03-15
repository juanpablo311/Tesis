import dominoes
import subprocess



series = dominoes.Series(target_score=100)
game = series.games[0]

while game is not None:
    # clear the terminal upon starting a new game
    input('Press enter to begin game {}.'.format(len(series.games) - 1))
    subprocess.call(['tput', 'reset'])
    print (game)
    while game.result is None:
        # print the game state so that all players can see it
        print('Board:')
        print(game.board)
        
        game.make_move(*game.valid_moves[0])
    print(series.scores)

    print('Game over!')
    print(game)
  
    game = series.next_game()
    print('The current state of the series:')
    print(series)
    print(series.scores)
# once the series has ended, print out the winning team
winning_team, _ = max(enumerate(series.scores), key=lambda i_score: i_score[1])
print('Team {} wins!'.format(winning_team))