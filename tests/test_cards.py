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
        self.deck.deal(50)
        self.assertEqual(self.deck.cards_remaining, 2)

    def test_not_enough_cards_remaining(self):
        with self.assertRaises(ValueError):
            self.deck.deal(53)


class TestBlackJackHand(unittest.TestCase):

    def test_hand_score_no_aces(self):
        hand = cards.BlackJackHand([cards.Card('Q', ''),
                                    cards.Card('K', '')])
        actual = hand.score
        expected = 20
        self.assertEqual(expected, actual)

    def test_hand_score_with_aces(self):
        hand = cards.BlackJackHand([cards.Card('A', ''),
                                    cards.Card('A', ''),
                                    cards.Card('7', ''),
                                    cards.Card('2', '')])
        actual = hand.score
        expected = 21
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
