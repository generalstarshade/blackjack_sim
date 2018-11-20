import json
import random
import os
from BasicStrategy import BasicStrategy
from Player import Player
from Hand import Hand

class Blackjack:

    self.decks = 6
    self.h17 = False
    self.num_players = 1
    self.pen = 52
    self.player_chips = 10000
    self.min_bet = 25
    self.bet_spread = [1, 2, 3, 4, 5]

    self.shoe = []
    self.players = []
    self.running_count = 0
    self.true_count = 0

    def __init__(self, config_file):

        self.load_config(config_file)
        self.shuffle_cards()


    def load_config(self, config_file):

        with open(config_file, "r") as f:
            config = json.load(f)

        self.decks = config["decks"]
        self.h17 = config["h17"]
        self.num_players = config["num_players"]
        self.pen = config["pen"]
        self.player_chips = config["player_chips"]
        self.min_bet = config["min_bet"]
        self.bet_spread = config["bet_spread"]

        # create the players
        for i in range(num_players):
            player = Player(self.player_chips, i)
            self.players.append(player)


    def shuffle_cards(self):

        # 1 is an Ace
        cards = [1]*4 + [2]*4 + [3]*4 + [4]*4 + [5]*4 + [6]*4 + [7]*4 + \
                [8]*4 + [9]*4 + [10]*16

        # shuffle the cards using os.urandom (random.shuffle is not robust enough to handle
        # long sequences, like that involving decks of cards)
        cards = cards * self.decks

        shuffled_shoe = []
        num_cards_left_to_shuffle = len(cards)

        while num_cards_left_to_shuffle > 0:
            rand_index = int(os.urandom(1)) % (num_cards_left_to_shuffle - 1)
            rand_card = cards[rand_index]
            shuffled_shoe.append(rand_card)
            del cards[rand_index]
            num_cards_left_to_shuffle -= 1

        # insert the cut card
        shuffled_shoe.insert(-self.pen, "cut")

        self.shoe = shuffled_shoe

        # burn a card
        self.deal_one_card()


    def resolve_bets(self, dealers_hand):
        for player in self.players:
            players_hand = player.get_hand()
            if dealers_hand > players_hand:
                # dealer won, take player's chips
                if players_hand.is_surrendered():
                    player.lost_chips(player.get_bet() / 2.0)
                else:
                    player.lost_chips(player.get_bet())
            elif player.get_hand() > dealers_hand:
                # player won, give player chips (and 1.5 his bet if blackjack)
                if player.get_hand().is_blackjack():
                    player.won_chips(player.get_bet() * 1.5)
                else:
                    player.won_chips(player.get_bet())
            elif dealers_hand == player.get_hand():
                # if there was a tie because dealer and player busted, dealer wins
                if dealers_hand.value == -1:
                    player.lost_chips(player.get_bet())
                pass

            player.clear_hand()

        # resolve split players by consolidating the bankroll and removing the split players
        player_split_winnings = {}
        for i in range(len(self.players)):
            player = self.players[i]

            # if we come across a split hand, take the winnings/losses of that hand and sum it
            # across all split hands belonging to a player. then we will add the final result
            # to the real player's bankroll
            if not player.is_original():
                if player_split_winnings[player.pid]:
                    player_split_winnings[player.pid] += player.chips
                else:
                    player_split_winnings[player.pid] = player.chips

            # delete the split hand now that we recorded how much was won/lost
            del self.players[i]
            i -= 1

        # add the winnings (or losses) to the split-player's bankroll
        for pid in player_split_winnings:
            self.players[pid].won_chips(player_split_winnings[pid])


    def update_count(self, card):

        count = 0
        if card <= 6 and > 1:
            count = 1
        elif card >= 10 or == 1:
            count = -1

        # update true count and running count
        self.running_count += count
        self.true_count = self.running_count / (len(self.shoe) / 52)


    def deal_one_card(self):
        card = self.shoe.pop(0)
        self.update_count(card)
        if card == "cut":
            self.end_shoe = True
            card = self.shoe.pop(0)
            self.update_count(card)
        return card


    def offer_insurance(self):

        took_insurance = False
        if self.true_count >= 3:
            # take insurance
            took_insurance = True
            for player in self.players:
                player.lost_chips(player.get_bet() / 2.0)

        return took_insurance


    def pay_insurance(self):

        for player in self.players:
            if player.get_hand().is_blackjack():
                # if player had blackjack, insurance is even money
                player.won_chips(player.bet * 1.5)
            else:
                player.won_chips(player.bet / 2.0)


    def deal(self):

        dealers_hand = Hand()

        # have the players make their bets
        for player in self.players:
            player.make_bet(self.true_count, self.min_bet, self.bet_spread)

        # deal the cards
        for i in range(2):
            for player in self.players:
                player.add_card(self.deal_one_card())

            dealers_hand.add_card(self.deal_one_card())

        # check for blackjack/offer insurance
        dealer_upcard = dealers_hand.get_upcard()
        if dealer_upcard == 10:
            if dealers_hand.is_blackjack():
                self.resolve_bets()
                return

        elif dealer_upcard == 1:
            took_insurance = self.offer_insurance()
            if dealers_hand.is_blackjack():
                if took_insurance:
                    self.pay_insurance()
                else:
                    self.resolve_bets()
                return

        # now play the hand
        self.play(dealers_hand)


    def play(dealers_hand):

        player_index = 0

        while True:
            if player_index >= len(self.players):
                break

            player = self.players[player_index]
            players_hand = player.get_hand()

            while True:
                player_decision = Strategy.optimal_play(dealers_hand, players_hand, self.true_count)

                if player_decision == "hit":
                    player.add_card(self.deal_one_card())
                    continue

                if player_decision == "stand":
                    break

                if player_decision == "double":
                    player.set_bet(player.get_bet() * 2)
                    player.add_card(self.deal_one_card())
                    break

                if player_decision == "split":
                    # add new temporary "player" to play the split hand
                    split_player = Player(0, player.pid)
                    split_player.is_original = False

                    if players_hand.num_splits == 0:
                        players_hand.num_splits = 2
                    else:
                        players_hand.num_splits += 1

                    players_split_card = players_hand.get_upcard()
                    split_player.add_card(players_split_card)
                    self.players.insert(player_index + 1, split_player)
                    player.clear_hand()
                    player.add_card(players_split_card)
                    player.add_card(self.deal_one_card())

                    # if we split aces, we do not get to hit multiple times
                    if player.get_hand().get_upcard() == 1:
                        break
                    else:
                        continue

                if player_decision == "surrender":
                    players_hand = True
                    players_hand.set_value(-1)
                    break

            player_index += 1

        # all hands have been played out, now play the dealers hand
        while (self.h17 and dealers_hand.get_value() < 17 or dealers_hand.is_soft() and dealers_hand.get_value() < 17) or \
              (not self.h17 and dealers_hand.get_value() < 17):
                  dealers_hand.add_card(self.deal_one_card())

        # resolve the bets
        self.resolve_bets()


