from gamefield import GameField
import numpy as np
from copy import deepcopy
import time



#GPU stuff
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

#Introduction
import pyfiglet
ascii_banner = pyfiglet.figlet_format("GNeuroNetWK")
print(ascii_banner)

print("Version 0.01\n"+
	"Genetic neuronal network developed by Huffliger \n" +
	"Designed to solve compute intense problems\n" +
	"Currently test boilerplate to check functionality\n" + 
	"Beat the randomness function\n\n")



ROUND_COUNT = 25000

#Data for graph
roundsCompleted = 0

if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

depth = 8
gameFieldSize = 8

#Balancing a win is 100 less worth than a loss
WINNINGSCOREADDITION = 0
WINNINGSCOREADDITION2 = 0
WINNINGSCOREADDITION3 = 0

#Losing in the next move is weighted 10x higher than in the overnext move
LOSINGSCOREADDITION = 200
LOSINGSCOREADDITION2 = 10
LOSINGSCOREADDITION3 = 1



def getMinMaxMove():
	gamesToPlay = []
	gamesToPlay1 = []
	gamesToPlay2 = []
	gamesToPlay3 = []
	gamesToPlay4 = []
	gamesToPlay5 = []
	bestPick = np.random.randint(4, 5)
	bestPickLossesScore = 100000
	#Me to play
	depth1Score = []
	depth2Score = []
	depth3Score = []
	depth4Score = []
	depth5Score = []

	moveProbabiltyScore = [2,2,2,2,2,2,2,2]



	#Me to play
	#print("Called multible times")
	for i1 in range(gameFieldSize):
		#MetoPlay
		gamesToPlay.append(deepcopy(game))
		try:
			gamesToPlay[i1].turn(i1)
			if(gamesToPlay[i1].check_winner()):
				return i1
		except:
			print("Invalid move prediction1")
		#Enemy to play 1
		for i2 in range(gameFieldSize):
			#print(str(i)+ " : "+ str(y))
			gamesToPlay1.append(deepcopy(gamesToPlay[len(gamesToPlay)-1]))
			depth1Score.append(0)
			try:
				gamesToPlay1[len(gamesToPlay1)-1].turn(i2)
				#gamesToPlay1[len(gamesToPlay1)-1].print_board()
				#print(str(gamesToPlay1[len(gamesToPlay1)-1].check_winner()))
				if(gamesToPlay1[len(gamesToPlay1)-1].check_winner() == 1):
					print("Losing in 1 on line " + str(i2+1) + " if i set " + str(i1+1))

					moveProbOption = i1
					moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION	
					#Old version
					#moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
					#if(moveProbabiltyScore[moveProbOption] >= LOSINGSCOREADDITION):
					#	moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION			
						
			except:
				print("Invalid move prediction2")

		   #Me to play 2
			for i3 in range(gameFieldSize):
				gamesToPlay2.append(deepcopy(gamesToPlay1[len(gamesToPlay1)-1]))
				depth2Score.append(0)
				try:
					gamesToPlay2[len(gamesToPlay2)-1].turn(i3)
					if(gamesToPlay2[len(gamesToPlay2)-1].check_winner() == 0):
						#print("Winning in 2 on line " + str(i3+1))
						moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
						if(moveProbabiltyScore[moveProbOption] >= WINNINGSCOREADDITION):
							moveProbabiltyScore[moveProbOption] += WINNINGSCOREADDITION		
				except:
					print("Invalid move prediction3")

				#Enemy to play 2
				for i4 in range(gameFieldSize):
					gamesToPlay3.append(deepcopy(gamesToPlay2[len(gamesToPlay2)-1]))
					depth3Score.append(0)					
					gamesToPlay3[len(gamesToPlay3)-1].turn(i4)

					if(gamesToPlay3[len(gamesToPlay3)-1].check_winner() == 1):
						print("Losing in 2 on line " + str(i4+1) + " if enemy sets " + str(i2+1) + ", (me) " + str(i3+1) + " enemy " + str(i4+1))
						moveProbOption = i1
						moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION	
						#Old version
						#moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
						#if(moveProbabiltyScore[moveProbOption] >= LOSINGSCOREADDITION2):
						#	moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION2				
					'''
					#Me to play 3
					for i5 in range(gameFieldSize):
						gamesToPlay4.append(deepcopy(gamesToPlay3[len(gamesToPlay3)-1]))
						depth4Score.append(0)
						try:
							gamesToPlay4[len(gamesToPlay4)-1].turn(i5)
							if(gamesToPlay4[len(gamesToPlay4)-1].check_winner() == 0):
								#print("Winning in 3 on line " + str(i5+1))
								moveProbOption = np.mod(len(gamesToPlay1)-1, gameFieldSize)
								if(moveProbabiltyScore[moveProbOption] >= WINNINGSCOREADDITION2):
									moveProbabiltyScore[moveProbOption] += WINNINGSCOREADDITION2	
						except:
							print("Invalid move prediction5")

						#Enemy to play 3
						for i6 in range(gameFieldSize):
							gamesToPlay5.append(deepcopy(gamesToPlay4[len(gamesToPlay4)-1]))
							depth5Score.append(0)					
							gamesToPlay5[len(gamesToPlay5)-1].turn(i6)

							if(gamesToPlay5[len(gamesToPlay5)-1].check_winner()):
								#print("Losing in 3 on line " + str(i4+1) + " if enemy sets " + str(i2+1) + ", (me) " + str(i3+1) + " enemy " + str(i4+1))
								moveProbOption = i1
								moveProbabiltyScore[moveProbOption] += LOSINGSCOREADDITION #Not sure if LOSINGADITION3 is better
							'''
		


	for x in range(gameFieldSize):
		print(moveProbabiltyScore[x])
		if(moveProbabiltyScore[x]<bestPickLossesScore):
			bestPick = x
			bestPickLossesScore = moveProbabiltyScore[x]
	return bestPick





for b in range(ROUND_COUNT-1, 0, -1):
	user = 0
	game_over = False
	game = GameField()
	while not game_over:
		game.print_board()

		if(user == 0):
			# Ask the user for input, but only accept valid turns
			valid_move = False
			while not valid_move:
				user_move = input(f"{game.which_turn()}'s Turn - pick a column (1-X): ")
				try:
					valid_move = game.turn(int(user_move)-1)
				except:
					print(f"Please choose a number between 1 and X")
			user = 1
		else:
			#MinMax function
			valid_move = False
			while not valid_move:
				minMaxMove = -2
				valid_move = game.turn(getMinMaxMove())
				print(f"Please choose a number between 1 and X | " + str(valid_move) + " is not valid.")
			user = 0


		# End the game if there is a winner
		game_over = game.check_winner()
		#print(game_over)
		#print(game.board)

		# End the game if there is a tie
		if not any(-1 in a for a in game.board):
			print("The game is a draw..")
	

	
	roundsCompleted += 1
	print("Round: " + str(roundsCompleted))