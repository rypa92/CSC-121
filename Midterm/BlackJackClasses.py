import random


class Card:
    cardname = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
                 11: "Jack", 12: "Queen", 13: "King"}
    suits = ["♥", "♦", "♣", "♠"]

    def __init__(self, value, suit):
        self.name = self.cardname[value]
        self.suit = suit
        self.title = "{n} of {s}".format(n=self.name, s=self.suit)
        self.score = min(value, 10)

    def __repr__(self):
        return self.title


class hand:
    def __init__(self, cards):
        self.hand = cards

    def get_scores(self):
        num_aces = sum(card.name == "Ace" for card in self.hand)
        score = sum(card.score for card in self.hand)
        return [score + i*10 for i in range(num_aces+1)]

    def possScore(self):
        return [s for s in self.get_scores() if s <= 21]

    def __repr__(self):
        return str(self.hand)

    def getCards(self):
        return str(self.hand[0])


class deck:
    new_deck = [Card(card, suit) for card in range(1, 14) for suit in ["♥", "♦", "♣", "♠"]]

    def __init__(self):
        random.shuffle(self.new_deck)

    def dealCard(self):
        return self.new_deck.pop()

    def dealHand(self):
        return hand([self.dealCard(), self.dealCard()])

    def reset(self):
        self.new_deck = [Card(card, suit) for card in range(1, 14) for suit in ["♥", "♦", "♣", "♠"]]
        random.shuffle(self.new_deck)
        return "A new deck has been shuffled!"

class player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.bet = 0
        self.wins = 0

    def new_hand(self, hand):
        self.hand = hand

    def hit(self, card):
        self.hand.hand.append(card)

    def bust(self):
        return len(self.hand.possScore()) == 0

    def scores(self):
        return self.hand.get_scores() if self.bust() else self.hand.possScore()

    def __repr__(self):
        playername = self.name + " *!BUSTED!*" if self.bust() else self.name
        return "Player Name: {p}\nMoney: ${m}\nCurrent Bet: {b}\nCards in Hand: {c}\nScore in Hand: {s}".format(p=playername, m=self.money, b=self.bet, c=self.hand, s=self.scores())


class dealer(player):
    def __init__(self, name, money):
        player.__init__(self, name, money)

    def __repr__(self):
        playername = self.name + " *!BUSTED!*" if self.bust() else self.name
        return "Player Name: {p}\nCards in Hand: [{c}, X]".format(p=playername, c=self.hand.getCards())

    def endofRoundTotal(self):
        playername = self.name + " *!BUSTED!*" if self.bust() else self.name
        return "Player Name: {p}\nCards in Hand: {c}\nScore in Hand: {s}".format(p=playername, c=self.hand, s=self.scores())
