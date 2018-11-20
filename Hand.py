class Hand:

    self.cards = []
    self.soft = False
    self.value = 0
    self.num_splits = 0

    def __init__(self):
        pass

    def add_card(self, card):
        self.cards.append(card)
        if card == 1 and self.value < 11:
            self.soft = True
            self.value += 11
        elif self.soft and self.value > 21:
            self.soft = False
            self.value -= 10
        else:
            self.value += card

        # a hand that busts loses to everything
        if self.value > 21:
            self.value = -1


    def clear(self):
        self.cards = []

    def get_cards(self):
        return cards

    def get_upcard(self):
        return cards[0]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def is_blackjack(self):
        return 1 in self.cards and 10 in self.cards and len(cards) == 2 and num_splits == 0

    def is_soft(self):
        return self.soft

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
