class Card:
	def __init__(self, suit, val):
		self.suit = suit
		self.val = val

	def getSuit(self):
		return self.suit

	def getVal(self):
		return self.val

	def printCard(self):
		print(self.val)

	def isFaceCard(self):
		return self.val == 'J' or self.val == 'Q' or self.val == 'K' or self.val == 'A'