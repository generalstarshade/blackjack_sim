class Hand:

    def __init__(self):
        self.cards = []
        self.soft = False
        self.value = 0
        self.num_splits = 0
        self.can_split = False
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

        # blackjack should be considered higher than everything
        if self.is_blackjack():
            self.value = 22

        if len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            self.can_split = True
            if self.cards[0] == 1:
                # for the purposes of this program, never consider pair of aces on
                # the first two cards to be soft
                self.soft = False


    def clear(self):
        self.cards = []
        self.value = 0
        self.num_splits = 0
        self.can_split = False
        self.surrendered = False
        self.soft = False

    def __str__(self):
        s = "cards: %s\nvalue: %d\n" % (str(self.cards), self.value)
        s += "num_splits: %d" % self.num_splits
        return s

    def get_cards(self):
        return self.cards

    def get_upcard(self):
        return self.cards[0]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def incr_splits(self):
        self.num_splits += 1

    def set_splits(self, num):
        self.num_splits = num

    def is_blackjack(self):
        return 1 in self.cards and 10 in self.cards and len(self.cards) == 2 and self.num_splits == 0

    def is_soft(self):
        return self.soft

    def is_splittable(self):
        return self.can_split

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

    def __str__(self):
        s = "self.cards = " + str(self.cards) + "\nself.soft = " + str(self.soft) + "\nself.value = " + str(self.value) + "\nself.num_splits = " + str(self.num_splits) + "\nself.can_split = " + str(self.can_split) + "\nself.surrendered = " + str(self.surrendered)
        return s
