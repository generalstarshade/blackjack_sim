import sys
import os

from Blackjack import Blackjack


def main():

    if len(sys.argv) < ARGC:
        exit(1)

    num_hands_to_play = sys.argv[1]
    config_file = sys.argv[2]

    start_sim(num_hands_to_play, config_file)


def start_sim(num_hands_to_play, config_file):
    game = Blackjack(config_file)

    for hands_played in range(num_hands_to_play):
        game.deal()
        if game.end_shoe:
            game.shuffle_cards()
            game.end_shoe = False

    gather_stats(game)


def gather_stats(game):
    pass
