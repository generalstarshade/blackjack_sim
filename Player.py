from Hand import Hand

class Player:

    self.pid = 0
    self.chips = 0
    self.hand = None
    self.bet = 0
    self.is_original = True

    def __init__(self, bankroll, pid):
        self.chips = bankroll)
        self.pid = pid
        self.hand = Hand()

    def make_bet(self, true_count, min_bet, bet_spread):

        # round true count to nearest whole number
        rounded_count = round(true_count)
        if rounded_count < 2:
            self.bet = min_bet

        if rounded_count >= 2:
            bet_spread_index = rounded_count - 1

            # use the max bet if true count exceeds bet spread granularity
            try:
                best_bet = bet_spread[bet_spread_index] * min_bet
            except IndexError:
                best_bet = bet_spread[-1]

            self.bet = best_bet


    def lost_chips(self, chips_lost):
        self.chips -= chips_lost

    def won_chips(self, chips_won):
        self.chips += chips_won

    def set_chips(self, chips):
        self.chips = chips

    def set_hand(self, hand):
        self.hand = hand

    def get_bet(self):
        return self.bet

    def set_bet(self, bet):
        self.bet = bet

    def get_chips(self):
        return chips

    def add_card(self, card):
        self.hand.add_card(card)

    def get_hand(self):
        return self.hand

    def clear_hand(self):
        self.hand.clear()
