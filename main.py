# Snakes and ladders sim
from random import randint
from time import time
import multiprocessing

# player class
class Player(object):
    def __init__(self, number:int, starting_pos:int=0):
        self.position:int = starting_pos
        self.number:int = number
        self.wins:int = 0

# game board class
class Board():
    def __init__(self):
        # Dictionary key is ladder starting position and
        # value of the key is ending position of ladder
        self.ladders = {
            1 : 38,
            4 : 14,
            8 : 30,
            21 : 42,
            28 : 76,
            50 : 67,
            71 : 92,
            80 : 99
        }

        # Dictionary key is the start position of snake and
        # value of key is the ending position of snake
        self.snakes = {
            32 : 10,
            36 : 6,
            48 : 26,
            62 : 18,
            88 : 24,
            95 : 56,
            97 : 78
        }

# board object
board = Board()

# random dice roll 1-6
def roll():
    return randint(1, 6)

# snakes and ladders game sim function
def game_sim(player_data) -> int:
    # create players
    players = [Player(number, starting_pos=pos) for (number, pos) in player_data]

    # move players in order
    while True:
        for player in players:

            # roll dice
            move:int = roll()
            player.position += move

            # check if player hit ladder or snake
            # then move player to given position
            if player.position in board.ladders:
                player.position = board.ladders[player.position]

            elif player.position in board.snakes:
                player.position = board.snakes[player.position]
            
            # return winner
            if player.position >= 100:
                return player.number


# Main script
if __name__=='__main__':
    # --- simulation variables ---
    sample_size = 1_000_000
    # format: (player number, starting position) eg.
    # (1, 10) is player number one starting position 10
    player_data = [(1, 0), (2, 0)]

    # -----------------------------

    start_time = time()
    # use multiprocessing to speed up sims
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(game_sim, [player_data for _ in range(sample_size)])
    pool.close()
    pool.join()
    
    delta_time = time() - start_time
    print(f"took {round(delta_time, 2)}s")

    # count and print wins
    for (number, _) in player_data:
        wins = results.count(number)
        print(f"Player {number} won: {wins} times - {round(wins/sample_size*100, 2)}%")
