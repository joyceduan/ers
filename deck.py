from card import Card
import random

class Deck:
	def __init__(self, deck=None):
		if deck is None:
			self.deck = []
			suits = ["D", "H", "C", "S"]
			vals = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
			fullDeck = []

			for val in vals:
				for suit in suits:
					card = Card(suit, val)
					self.deck.append(card)
		else:
			self.deck = deck

	def __len__(self):
		return len(self.deck)

	def __getitem__(self, pos):
		return self.deck[pos]

	def printDeck(self):
		for card in self.deck:
			print(card.val + card.suit) # print on the same line

	def shuffleDeck(self):
		random.shuffle(self.deck)

	def reverseDeck(self):
		self.deck = list(reversed(self.deck))

	def splitDeck(self):
		halfway = len(self.deck)//2
		first = Deck(self.deck[:halfway])
		second = Deck(self.deck[halfway:])
		return first, second

	def addDeckToBottom(self, deckToAdd):
		self.deck = deckToAdd.deck + self.deck

	def clearDeck(self):
		self.deck = []

	def pop(self):
		return self.deck.pop(-1)

	def empty(self):
		return len(self.deck) == 0

	def addToTop(self, card):
		self.deck.append(card)

	def addToBottom(self, card):
		self.deck = [card] + self.deck

	def sandwich(self):
		if len(self.deck) >= 3:
			return self.deck[-1].getVal() == self.deck[-3].getVal()
		else:
			return False

	def double(self):
		if len(self.deck) >= 2:
			return self.deck[-1].getVal() == self.deck[-2].getVal()
		else:
			return False

	def marriage(self):
		if len(self.deck) >= 2:
			return (self.deck[-1].getVal() == 'K' and self.deck[-2].getVal() == 'Q') or (self.deck[-1].getVal() == 'Q' and self.deck[-2].getVal() == 'K')
		else:
			return False


