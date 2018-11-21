import sys
import os

from Blackjack import Blackjack

ARGC = 3

def main():

    if len(sys.argv) < ARGC:
        print "Usage: %s <configuration file> <number hands to play>" % (sys.argv[0])
        exit(1)

    config_file = sys.argv[1]
    num_hands_to_play = int(sys.argv[2])

    start_sim(num_hands_to_play, config_file)


def start_sim(num_hands_to_play, config_file):
    game = Blackjack(config_file)

    for hands_played in range(num_hands_to_play):
        game.deal()
        if game.end_shoe:
            game.shuffle_cards()
            game.end_shoe = False

        if (hands_played + 1) % 10000 == 0:
            print "%d hands played." % (hands_played + 1)

    gather_stats(game, num_hands_to_play)


def gather_stats(game, num_hands_to_play):

    i = 1
    for player in game.players:
        print "Player %d now has %d chips" % (i, player.chips)
        i += 1

    hands_won = game.hands_won / float(num_hands_to_play)
    hands_tied = game.hands_tied / float(num_hands_to_play)
    hands_lost = game.hands_lost / float(num_hands_to_play)

    print "Hands won : %f" % hands_won
    print "Hands tied : %f" % hands_tied
    print "Hands lost : %f" % hands_lost

main()
