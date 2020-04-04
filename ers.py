# References: https://stackoverflow.com/questions/1335507/keyboard-input-with-timeout-in-python

import random
from deck import Deck
from card import Card
import time
import sys
import select

def printScore(playerDeck, computerDeck):
	print("You now have " + str(len(playerDeck)) + " cards and Computer has " + str(len(computerDeck)) + " cards.")

def waitForSlap(slap, commonDeck, playerDeck, computerDeck):
	TIMEOUT = 2 # number of seconds to wait for slap
	print("You have " + str(TIMEOUT) + " seconds to slap!")

	i, o, e = select.select([sys.stdin], [], [], TIMEOUT)

	if i: # slapped
		if slap: # correct slap
			commonDeck.reverseDeck()
			playerDeck.addDeckToBottom(commonDeck)
			commonDeck.clearDeck()
			print("Yay, you correctly slapped! You win the pile.")
			printScore(playerDeck, computerDeck)
			time.sleep(3)
			return True, True
		elif not slap: # wrong slap so burn card
			# if not playerDeck.empty():
			cardToBurn = playerDeck.pop()
			commonDeck.addToBottom(cardToBurn)
			# time.sleep(3) # wait after burning card
			print("Aw man, you incorrectly slapped! You burn a card.")
			time.sleep(3)
			printScore(playerDeck, computerDeck)
			x = input("Press enter to continue.")
			# time.sleep(3)
			return False, True
	else:
		if slap: 
			print("Aw man, you missed a slap opportunity! Computer slaps and gets the pile.")
			commonDeck.reverseDeck()
			computerDeck.addDeckToBottom(commonDeck)
			commonDeck.clearDeck()
			printScore(playerDeck, computerDeck)
			time.sleep(3) # wait seconds after computer collects pile
			return True, True

	return False, False

def faceCardProcedure(playerTurn, turn, chances, commonDeck, computerDeck, playerDeck):
	faceCardPlayed = True
	if playerTurn: 
		for i in range(chances):
			print('\033[2J')
			if not computerDeck.empty():
				playedCard = computerDeck.pop()
				commonDeck.addToTop(playedCard)
				print("Computer plays:")
				playedCard.printCard()

				slap = commonDeck.double() or commonDeck.sandwich() or commonDeck.marriage()

				goodSlap, slaped = waitForSlap(slap, commonDeck, playerDeck, computerDeck)
				
				if goodSlap:
					faceCardPlayed = False
					break

				faceCardPlayed = playedCard.isFaceCard()
				if faceCardPlayed:
					turn += 1
					break
			else:
				break

		if not faceCardPlayed and not goodSlap:
			# got to the end of the chances
			print("Computer did not play any other face cards! You win the pile.")
			commonDeck.reverseDeck()
			playerDeck.addDeckToBottom(commonDeck)
			commonDeck.clearDeck()
			printScore(playerDeck, computerDeck)
			turn = 0
			time.sleep(3)

	else: 
		for i in range(chances):
			print('\033[2J')
			if not playerDeck.empty():
				playedCard = playerDeck.pop()
				commonDeck.addToTop(playedCard)
				print("You play:")
				playedCard.printCard()

				slap = commonDeck.double() or commonDeck.sandwich() or commonDeck.marriage()
				# print(slap)

				goodSlap, slapped = waitForSlap(slap, commonDeck, playerDeck, computerDeck)
				if goodSlap:
					faceCardPlayed = False
					break

				faceCardPlayed = playedCard.isFaceCard()
				if faceCardPlayed:
					turn += 1
					break
			else:
				break

		if not faceCardPlayed and not goodSlap:
			# got to the end of the chances
			print("You did not play any other face cards! Computer wins the pile.")
			commonDeck.reverseDeck()
			computerDeck.addDeckToBottom(commonDeck)
			commonDeck.clearDeck()
			printScore(playerDeck, computerDeck)
			turn = 1
			time.sleep(3)

	return turn, faceCardPlayed

def main():
	print("Hello! This is a game of Egyptian Rat Screw (ERS).")
	print("You will be playing against the computer.")
	print("To slap the deck after a card has been played, press Enter.")
	print("Computer: You go first!")

	x = input("Press enter to start.")

	deck = Deck()
	deck.shuffleDeck()
	computerDeck, playerDeck = deck.splitDeck()

	commonDeck = Deck([])

	turn = 0
	slap = False

	while not computerDeck.empty() and not playerDeck.empty():
		print('\033[2J')
		playedCard = None
		playerTurn = (turn % 2 == 0)
		if playerTurn:
			playedCard = playerDeck.pop()
			print("You play:")
		else:
			playedCard = computerDeck.pop()
			print("Computer plays:")
		
		commonDeck.addToTop(playedCard)
		playedCard.printCard()

		slap = commonDeck.double() or commonDeck.sandwich() or commonDeck.marriage()
		goodSlap, slapped = waitForSlap(slap, commonDeck, playerDeck, computerDeck)

		if slapped:
			if goodSlap:
				turn = 0
			else:
				turn = 1
			continue

		faceCardPlayed = playedCard.isFaceCard()
		# jack was played

		if faceCardPlayed:
			while faceCardPlayed:
				playerTurn = (turn % 2 == 0)
				goodSlap = False
				if playedCard.getVal() == 'J':
					turn, faceCardPlayed = faceCardProcedure(playerTurn, turn, 1, commonDeck, computerDeck, playerDeck)

				elif playedCard.getVal() == 'Q':
					turn, faceCardPlayed = faceCardProcedure(playerTurn, turn, 2, commonDeck, computerDeck, playerDeck)

				elif playedCard.getVal() == 'K':
					turn, faceCardPlayed = faceCardProcedure(playerTurn, turn, 3, commonDeck, computerDeck, playerDeck)

				elif playedCard.getVal() == 'A':
					turn, faceCardPlayed = faceCardProcedure(playerTurn, turn, 4, commonDeck, computerDeck, playerDeck)
		else:
			turn += 1

	if computerDeck.empty():
		print("You win! Wahoo!")

	if playerDeck.empty():
		print("Computer wins! Better luck next time.")


main()
