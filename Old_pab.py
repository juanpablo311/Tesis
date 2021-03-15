class probabilistic_alphabeta:
    '''
    This player repeatedly assumes the other players' hands, runs alphabeta search,
    and prefers moves that are most frequently optimal. It takes into account all
    known information to determine what hands the other players could possibly have,
    including its hand, the sizes of the other players' hands, and the moves played
    by every player, including the passes. An instance of this class must first be
    initialized before it can be called in the usual way.

    :param int start_move: move number at which to start applying this
                           player. If this player is called before the
                           specified move number, it will have no effect.
                           Moves are 0-indexed. The default is 0.
    :param int sample_size: the number of times to assign random possible
                            hands to other players and run alphabeta search
                            before deciding move preferences. By default
                            considers all hands that other players could
                            possibly have.
    :param callable player: player used to sort moves to be explored
                            in the underlying call to alphabeta search.
                            Ordering better moves first may significantly
                            reduce the amount of moves that need to be
                            explored. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var str __name__: the name of this player
    '''
    def __init__(self, start_move=0, sample_size=3, player=identity, name=None):
        self._start_move = start_move
        self._sample_size = sample_size
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        # do not perform a potentially slow operation if it is
        # too early in the game or if there is only one valid move
        if len(game.moves) < self._start_move or len(game.valid_moves) == 1:
            return

        
        
        
        hands = (game.random_possible_hands() for _ in range(self._sample_size))

        # iterate over the selected possible hands
        counter = collections.Counter()
        for h in hands:
            # do not modify the original game
            game_copy = copy.deepcopy(game)

            # set the possible hands
            game_copy.hands = h

            # for performance
            game_copy.skinny_board()

            # run alphabeta and record the optimal move
            counter.update([
                dominoes.search.alphabeta(game_copy, player=self._player)[0][0]
            ])

        # prefer moves that are more frequently optimal
        game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: -counter[m]))
