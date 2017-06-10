''' Objects used in playing card games.
'''
import itertools
import random
from collections import namedtuple

Card = namedtuple('Card', ('rank', 'suit'))


class Deck(object):
    ''' Deck(s) of cards. '''
    CARDS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    SUITS = ('H', 'D', 'C', 'S')

    def __init__(self, num_decks=1):
        self.deck = self._create_cards(num_decks)
        self.shuffle()
        self._idx = 0

    def _create_cards(self, num_decks):
        card_suit_combos = itertools.product(
            self.CARDS * num_decks, self.SUITS)
        return list(Card(x[0], x[1]) for x in card_suit_combos)

    def __len__(self):
        return len(self.deck)

    def shuffle(self):
        ''' Shuffle the deck of cards in place. '''
        random.shuffle(self.deck)

    def deal(self, num_cards=1):
        ''' Return num_cards of cards from the deck. '''
        if self.cards_remaining > num_cards:
            dealt = list(itertools.islice(self.deck,
                                          self._idx, self._idx + num_cards))
            self._idx += num_cards
            return dealt
        else:
            raise ValueError('Not enough cards remaining.')

    @property
    def cards_remaining(self):
        ''' The number of cards yet to be dealt. '''
        return len(self.deck) - self._idx


class BlackJackHand(object):
    ''' A single hand of blackjack. '''

    CARD_VALUES = dict(zip(Deck.CARDS,
                           (*range(2, 11), 10, 10, 10, 11)  # 2-10, J, Q, K, A
                           )
                       )

    def __init__(self, cards):
        self.cards = cards

    @property
    def score(self):
        ''' The numerical value of the hand. '''
        hand_score = 0
        for card in self.cards:
            if 'A' in card:
                card_score = self._handle_ace(hand_score)
            else:
                card_score = self.CARD_VALUES[card.rank]
            hand_score += card_score
        return hand_score

    def _handle_ace(self, current_hand_score):
        if current_hand_score > 10:
            return 1
        else:
            return 11
