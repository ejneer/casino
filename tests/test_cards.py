import unittest

from ..casino import cards

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = cards.Deck()
    
    def test_deck_multiplier(self):
        deck = cards.Deck(2)
        self.assertEqual(len(deck), 104)

    def test_deal_cards_returned(self):
        first_five_cards_copy = self.deck.deck[:5]
        first_five_dealt = self.deck.deal(5)
        self.assertListEqual(first_five_cards_copy, first_five_dealt)

    def test_cards_remaining(self):
        # simulate 50 cards previously dealt
        self.deck._idx = 50
        self.assertEqual(self.deck.cards_remaining, 2)

    def test_not_enough_cards_remaining(self):
        with self.assertRaises(ValueError):
            self.deck.deal(53)

if __name__ == '__main__':
    unittest.main()
