''' Objects used in playing card games.
'''
import itertools
import random

CARDS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

class Deck(object):
    ''' Deck(s) of cards. '''

    def __init__(self, num_decks=1):
        self.deck = list(itertools.product(CARDS * num_decks, SUITS))
        self.shuffle()
        self._idx = 0

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

