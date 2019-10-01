class Strategy:

    def __init__(self):

        self.hard_hand_table = \
        [
          ["hit","hit","hit","hit","hit","hit","hit","hit","hit","hit"],
          ["hit","hit","hit","hit","hit","hit","hit","hit","hit","hit"],
          ["hit","hit","hit","hit","hit","hit","hit","hit","hit","hit"],
          ["hit","hit","hit","hit","hit","hit","hit","hit","hit","hit"],
          ["hit","hit","hit","hit","hit","hit","hit","hit","hit","hit"],
          ["hit","double/hit","double/hit","double/hit","double/hit","hit","hit","hit","hit","hit"],
          ["double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","hit","hit"],
          ["double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit"],
          ["hit","hit","stand","stand","stand","hit","hit","hit","hit","hit"],
          ["stand","stand","stand","stand","stand","hit","hit","hit","hit","hit"],
          ["stand","stand","stand","stand","stand","hit","hit","hit","hit","hit"],
          ["stand","stand","stand","stand","stand","hit","hit","hit","surrender/hit","surrender/hit"],
          ["stand","stand","stand","stand","stand","hit","hit","surrender/hit","surrender/hit","surrender/hit"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","surrender/stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"]
        ]

        self.soft_hand_table = \
        [
          ["hit","hit","hit","double/hit","double/hit","hit","hit","hit","hit","hit"],
          ["hit","hit","hit","double/hit","double/hit","hit","hit","hit","hit","hit"],
          ["hit","hit","double/hit","double/hit","double/hit","hit","hit","hit","hit","hit"],
          ["hit","hit","double/hit","double/hit","double/hit","hit","hit","hit","hit","hit"],
          ["hit","double/hit","double/hit","double/hit","double/hit","hit","hit","hit","hit","hit"],
          ["double/stand","double/stand","double/stand","double/stand","double/stand","stand","stand","hit","hit","hit"],
          ["stand","stand","stand","stand","double/stand","stand","stand","stand","stand","stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"]
        ]

        self.split_hand_table = \
        [
          ["split","split","split","split","split","split","hit","hit","hit","hit"],
          ["split","split","split","split","split","split","hit","hit","hit","hit"],
          ["hit","hit","hit","split","split","hit","hit","hit","hit","hit"],
          ["double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","double/hit","hit","hit"],
          ["split","split","split","split","split","hit","hit","hit","hit","hit"],
          ["split","split","split","split","split","split","hit","hit","hit","hit"],
          ["split","split","split","split","split","split","split","split","split","surrender"],
          ["split","split","split","split","split","stand","split","split","stand","stand"],
          ["stand","stand","stand","stand","stand","stand","stand","stand","stand","stand"],
          ["split","split","split","split","split","split","split","split","split","split"]
        ]

    def optimal_play(self, dealers_hand, players_hand, true_count):
        dealers_upcard = dealers_hand.get_upcard()
        players_value = players_hand.get_value()
        players_upcard = players_hand.get_upcard()

        best_move = self.get_deviation(dealers_hand, players_hand, true_count)
        if best_move:
            return best_move

        # for the sake of this file, A will be represented as 11
        if dealers_upcard == 1:
            dealers_upcard = 11

        # the point of the indexes is to allow for easy indexing into the arrays above. for example, there
        # is no data for soft hand of 9 because that's impossible. thus, to access soft 13 row, you need to
        # access the 0th element in the array, so we decrement the index by 13 to do this cleanly
        table = None
        dealer_offset_idx = -2
        player_offset_idx = 0

        # determine from which table we should use and adjust the table index
        best_move = ""
        try:
            if players_hand.is_soft():
                player_offset_idx = -13
                best_move = self.soft_hand_table[players_value + player_offset_idx][dealers_upcard + dealer_offset_idx]
            elif players_hand.is_splittable():
                player_offset_idx = -2
                best_move = self.split_hand_table[players_upcard + player_offset_idx][dealers_upcard + dealer_offset_idx]
            else:
                player_offset_idx = -4
                best_move = self.hard_hand_table[players_value + player_offset_idx][dealers_upcard + dealer_offset_idx]

        except IndexError:
            print players_hand
            print dealers_hand
            exit(0)

        # check if we can actually double or surrender if that's the recommended move. If not, do the alternate option
        if "/" in best_move:
            if len(players_hand.get_cards()) > 2:
                best_move = best_move.split("/")[1]
            else:
                best_move = best_move.split("/")[0]

        # if it's a split, check that we can actually split (can't split more than 4 hands). If not, go to hard hand table
        elif best_move == "split" and players_hand.num_splits >= 4:
            player_offset_idx = -4
            best_move = self.hard_hand_table[players_value + player_offset_idx][dealers_upcard + dealer_offset_idx]

            if "/" in best_move:
                if len(players_hand.get_cards()) > 2:
                    best_move = best_move.split("/")[1]
                else:
                    best_move = best_move.split("/")[0]


        return best_move


    def get_deviation(self, dealers_hand, players_hand, tc):

        players_value = players_hand.get_value()
        players_cards = players_hand.get_cards()
        dealers_value = dealers_hand.get_value()

        if players_value == 16 and dealers_value == 10:
            if tc < -1:
                return "hit"
            if tc > -1 and tc < 1:
                if len(players_cards) > 2:
                    return "hit"
                else:
                    return "surrender"
            if tc >= 1:
                if len(players_cards) > 2:
                    return "stand"
                else:
                    return "surrender"

        elif players_value == 15 and dealers_value == 10:
            if tc < 0:
                return "hit"
            if tc < 5:
                if len(players_cards) > 2:
                    return "hit"
                else:
                    return "surrender"
            if tc >= 5:
                if len(players_cards) > 2:
                    return "stand"
                else:
                    return "surrender"

        elif players_cards[0] == 10 and players_cards[1] == 10 and len(players_cards) == 2 and dealers_value == 5:
            if tc >= 6 and players_hand.num_splits < 4:
                return "split"
            else:
                return "stand"

        elif players_cards[0] == 10 and players_cards[1] == 10 and len(players_cards) == 2 and dealers_value == 6:
            if tc >= 5 and players_hand.num_splits < 4:
                return "split"
            else:
                return "stand"

        elif players_value == 10 and len(players_cards) == 2 and dealers_value == 10:
            if tc >= 5:
                return "double"
            else:
                return "hit"

        elif players_value == 12 and dealers_value == 3:
            if tc > 2:
                return "stand"
            else:
                return "hit"

        elif players_value == 12 and dealers_value == 2:
            if tc > 3:
                return "stand"
            else:
                return "hit"

        elif players_value == 9 and len(players_cards) == 2 and dealers_value == 2:
            if tc > 2:
                return "double"
            else:
                return "hit"

        elif players_value == 10 and len(players_cards) == 2 and dealers_value == 1:
            if tc >= 5:
                return "double"
            else:
                return "hit"

        elif players_value == 9 and len(players_cards) == 2 and dealers_value == 7:
            if tc >= 3:
                return "double"
            else:
                return "hit"

        elif players_value == 16 and dealers_value == 9:
            if tc < -1:
                return "hit"
            if tc < 6:
                if len(players_cards) > 2:
                    return "hit"
                else:
                    return "surrender"
            if tc >= 6:
                if len(players_cards) > 2:
                    return "stand"
                else:
                    return "surrender"

        elif players_value == 13 and dealers_value == 2:
            if tc <= -2:
                return "hit"
            else:
                return "stand"

        elif players_value == 12 and dealers_value == 4:
            if tc <= -1:
                return "hit"
            else:
                return "stand"

        elif players_value == 12 and dealers_value == 5:
            if tc <= -3:
                return "hit"
            else:
                return "stand"

        elif players_value == 12 and dealers_value == 6:
            if tc <= -2:
                return "hit"
            else:
                return "stand"

        elif players_value == 13 and dealers_value == 3:
            if tc <= -3:
                return "hit"
            else:
                return "stand"

        else:
            return None
