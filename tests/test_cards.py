import unittest
from unittest.mock import Mock

from casino import cards


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


class TestPokerHand(unittest.TestCase):

    def setUp(self):
        self.cards = [Mock() for _ in range(5)]
        self.hand = cards.PokerHand(self.cards)

    def test_is_high_card(self):
        ranks = ['2', '3', '5', '9', 'Q']
        suits = ['D', 'D', 'H', 'H', 'S']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        [setattr(x, 'suit', y) for x, y in zip(self.cards, suits)]
        self.assertTrue(self.hand.is_high_card)

    def test_is_pair(self):
        ranks = ['2', '2', '3', '5', '7']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_pair)

    def test_is_two_pair(self):
        ranks = ['2', '2', 'A', 'A', 'J']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_two_pair)

    def test_is_three_kind(self):
        ranks = ['2', '2', '2', '5', '7']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_three_kind)

    def test_is_straight(self):
        ranks = ['3', '4', '5', '6', '7']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_straight)

    def test_is_straight_with_ace(self):
        ranks = ['A', '2', '3', '4', '5']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_straight)

    def test_is_flush_true(self):
        [setattr(x, 'suit', 'H') for x in self.cards]
        self.assertTrue(self.hand.is_flush)

    def test_is_flush_false(self):
        [setattr(x, 'suit', 'H') for x in self.cards]
        self.cards[0].suit = 'D'
        self.assertFalse(self.hand.is_flush)

    def test_is_flush_length(self):
        # 5 cards are needed for a poker flush
        [setattr(x, 'suit', 'H') for x in self.cards]
        self.cards.pop()
        self.assertFalse(self.hand.is_flush)

    def test_is_full_house(self):
        ranks = ['3', '3', '3', 'J', 'J']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_full_house)

    def test_is_four_kind(self):
        ranks = ['A', 'A', 'A', 'A', 'K']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        self.assertTrue(self.hand.is_four_kind)

    def test_is_straight_flush(self):
        ranks = ['3', '4', '5', '6', '7']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        [setattr(x, 'suit', 'H') for x in self.cards]
        self.assertTrue(self.hand.is_straight_flush)

    def test_is_straight_flush_with_ace(self):
        ranks = ['A', '2', '3', '4', '5']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        [setattr(x, 'suit', 'H') for x in self.cards]
        self.assertTrue(self.hand.is_straight_flush)

    def test_is_royal_flush(self):
        ranks = ['10', 'J', 'Q', 'K', 'A']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]
        [setattr(x, 'suit', 'H') for x in self.cards]
        self.assertTrue(self.hand.is_royal_flush)

    def test_hand_rank_returns_highest_ranking_hand(self):
        # a full house is also a three of a kind and a pair.  The full house
        # is the highest ranking hand of the three.
        ranks = ['3', '3', '3', 'J', 'J']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, ranks)]

        # full house is 4th strongest hand
        self.assertEqual(self.hand.hand_rank, 3)


class TestHoldEmHand(unittest.TestCase):

    def setUp(self):
        self.cards = [Mock() for _ in range(2)]
        self.community_cards = [Mock() for _ in range(5)]
        self.hand = cards.HoldEmHand(self.cards, self.community_cards)

    def test_best_hand_full_community_cards(self):
        held_card_ranks = ['A', '2']
        held_card_suits = ['D', 'D']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, held_card_ranks)]
        [setattr(x, 'suit', y) for x, y in zip(self.cards, held_card_suits)]

        community_card_ranks = ['2', '2', '3', '4', '5']
        community_card_suits = ['H', 'C', 'D', 'D', 'D']
        [setattr(x, 'rank', y)
         for x, y in zip(self.community_cards, community_card_ranks)]
        [setattr(x, 'suit', y)
         for x, y in zip(self.community_cards, community_card_suits)]

        # best hand should be a straight flush
        self.assertEqual(self.hand.hand_rank, 2)

    def test_best_hand_no_community_cards(self):
        self.hand.community_cards = []

        # we've got a pair
        held_card_ranks = ['2', '2']
        held_card_suits = ['H', 'D']
        [setattr(x, 'rank', y) for x, y in zip(self.cards, held_card_ranks)]
        [setattr(x, 'suit', y) for x, y in zip(self.cards, held_card_suits)]

        self.assertEqual(self.hand.hand_rank, 8)

if __name__ == '__main__':
    unittest.main()
