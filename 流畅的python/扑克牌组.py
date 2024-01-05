import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    """
    初始化一个包含 52 张牌的牌组
    """

    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, positon):
        return self._cards[positon]

    def spades_high(self, card):
        suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
        rank_value = self.ranks.index(card.rank)
        return rank_value * len(suit_values) + suit_values[card.suit]

    def sort_card(self):
        """
        返回一个将牌组中的牌按照大小排序后的牌组
        """
        return sorted(self, key=self.spades_high)


deck = FrenchDeck()
print(deck)
print(deck.sort_card())
