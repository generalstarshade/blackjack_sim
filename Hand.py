class Hand:

    def __init__(self):
        self.cards = []
        self.soft = False
        self.value = 0
        self.num_splits = 0
        self.split = False
        self.surrendered = False

    def add_card(self, card):
        self.cards.append(card)
        if card == 1 and self.value < 11:
            self.soft = True
            self.value += 11
        elif self.soft and self.value + card > 21:
            self.soft = False
            self.value = self.value - 10 + card
        else:
            self.value += card

        # a hand that busts loses to everything
        if self.value > 21:
            self.value = -1

        if len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            self.split = True
            if self.cards[0] == 1:
                # for the purposes of this program, never consider pair of aces on
                # the first two cards to be soft
                self.soft = False


    def clear(self):
        self.cards = []
        self.value = 0
        self.num_splits = 0
        self.split = False
        self.surrendered = False
        self.soft = False

    def __str__(self):
        print "cards: " + str(self.cards)
        print "soft: " + str(self.soft)
        print "value: " + str(self.value)
        print "num_splits: " + str(self.num_splits)
        print "split: " + str(self.split)
        print "surrendered: " + str(self.surrendered)
        return ""

    def get_cards(self):
        return self.cards

    def get_upcard(self):
        return self.cards[0]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def is_blackjack(self):
        return 1 in self.cards and 10 in self.cards and len(self.cards) == 2 and self.num_splits == 0

    def is_soft(self):
        return self.soft

    def is_split(self):
        return self.split

    def is_surrendered(self):
        return self.surrendered

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


def hand_value(cards):

    # blackjack is the highest hand possible, higher than non-natural 21, so we make it 22
    if is_blackjack(cards):
        current_value = 22
        return current_value

    current_value = 0
    for card in cards:
        tentative_value = current_value + card
        if tentative_value > 21 and card == 11:
            tentative_value = current_value + 1
        elif tentative_value > 21:
            # player busts
            current_value = -1
            return current_value
        current_value = tentative_value

    return current_value
