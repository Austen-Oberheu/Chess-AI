import random
import operator
import pygame

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("ChessBoard")
white,black,red = (255,255,255),(0,0,0),(255,0,0)

movePieceKey = 0
moveSquares = []

#AI turns before analyzing board
AITurnsBeforeAnalyze = 6
AITurns = 0

imageOffset = 50
whitePawn = pygame.image.load("images/white_pawn.png")
whiteBishop = pygame.image.load("images/white_bishop.png")
whiteKnight = pygame.image.load("images/white_knight.png")
whiteRook = pygame.image.load("images/white_rook.png")
whiteQueen = pygame.image.load("images/white_queen.png").convert()
whiteKing = pygame.image.load("images/white_king.png")

blackPawn = pygame.image.load("images/black_pawn.png")
blackBishop = pygame.image.load("images/black_bishop.png")
blackKnight = pygame.image.load("images/black_knight.png")
blackRook = pygame.image.load("images/black_rook.png")
blackQueen = pygame.image.load("images/black_queen.png")
blackKing = pygame.image.load("images/black_king.png")

chessBoardX = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
chessBoardY = ['8', '7', '6', '5', '4', '3', '2', '1']
cellSize = 20
#Set board size
board = [[0 for x in range(len(chessBoardX))] for y in range(len(chessBoardY))]

#Set all pieces initial postion and also will allow the game to keep track of all the pieces 
blackPieces = {'LeftRook': ['R', 0, 0], 'LeftKnight': ['H', 1, 0], 'LeftBishop': ['B', 2, 0], 'Queen': ['Q', 3, 0], 'King': ['K', 4, 0], 'RightBishop': ['B', 5, 0],
			  'RightKnight': ['H', 6, 0], 'RightRook': ['R', 7, 0], 'Pawn1': ['P', 0, 1, 0], 'Pawn2': ['P', 1, 1, 0], 'Pawn3': ['P', 2, 1, 0], 'Pawn4': ['P', 3, 1, 0], 'Pawn5': ['P', 4, 1, 0],
			 'Pawn6': ['P', 5, 1, 0], 'Pawn7': ['P', 6, 1, 0], 'Pawn8': ['P', 7, 1, 0]}

blackPossibleMoves = {'LeftRook': [], 'LeftKnight': [], 'LeftBishop': [], 'Queen': [], 'King': [], 'RightBishop': [],
			  'RightKnight': [], 'RightRook': [], 'Pawn1': [], 'Pawn2': [], 'Pawn3': [], 'Pawn4': [], 'Pawn5': [],
			 'Pawn6': [], 'Pawn7': [], 'Pawn8': []}

whitePieces = {'LeftRook': ['R', 0, 7], 'LeftKnight': ['H', 1, 7], 'LeftBishop': ['B', 2, 7], 'Queen': ['Q', 3, 7], 'King': ['K', 4, 7], 'RightBishop': ['B', 5, 7],
			  'RightKnight': ['H', 6, 7], 'RightRook': ['R', 7, 7], 'Pawn1': ['P', 0, 6, 0], 'Pawn2': ['P', 1, 6, 0], 'Pawn3': ['P', 2, 6, 0], 'Pawn4': ['P', 3, 6, 0], 'Pawn5': ['P', 4, 6, 0],
			 'Pawn6': ['P', 5, 6, 0], 'Pawn7': ['P', 6, 6, 0], 'Pawn8': ['P', 7, 6, 0]}

#If taken refers to a space that is currently occupied by an allied piece but if that piece is taken will open up
#This is entirley for the AI as right now all it looks at is the possible moves and since those spaces will not show as
#possible moves due to there being a piece there it will not account for a defensive attack

#At some point will add this to the AI player to hopefully allow it to make sacrafices if there is a payoff but currently just the player has this attribute
whitePossibleMoves = {'LeftRook': [], 'LeftKnight': [], 'LeftBishop': [], 'Queen': [], 'King': [], 'RightBishop': [],
			  'RightKnight': [], 'RightRook': [], 'Pawn1': [], 'Pawn2': [], 'Pawn3': [], 'Pawn4': [], 'Pawn5': [],
			 'Pawn6': [], 'Pawn7': [], 'Pawn8': [], 'IfTaken': []}

def InitBoard():
	for y in range(len(chessBoardY)):
		for x in range(len(chessBoardX)):
			board[x][y] = '0'  

def PlacePiece(name, piece, x, y):
	board[x][y] = piece
	#print('inserting ' + name + ' at board position: ' + chessBoardX[x] + ' ' + chessBoardY[y])

def InitPieces():
	for k, v in blackPieces.items():
		PlacePiece(k, v[0], v[1], v[2])

	for k, v in whitePieces.items():
		PlacePiece(k, v[0], v[1], v[2])

def DrawBoard():
	for y in range(len(chessBoardY)):
		for x in range(len(chessBoardX)):
			print(board[x][y], end='')
		print()

def IsEnemyPiece(enemy, x, y):
	if (enemy == 'black'):
		for k, v in blackPieces.items():
			if (v[1] == x and v[2] == y):
				return True

	if (enemy == 'white'):
		for k, v in whitePieces.items():
			if (v[1] == x and v[2] == y):

				return True
	return False

def IsPieceThere(x, y):
	for k, v in whitePieces.items():
		if (v[1] == x and v[2] == y):
			return k
	return False

def RemovePiece(enemy, x, y):
	if (enemy == 'black'):
		for k, v in blackPieces.items():
			if (v[1] == x and v[2] == y):
				del blackPieces[k]
				del blackPossibleMoves[k]
				return

	if (enemy == 'white'):
		for k, v in whitePieces.items():
			if (v[1] == x and v[2] == y):
				del whitePieces[k]
				del whitePossibleMoves[k]
				return

def IsValidMove(key, x, y):
	moves = whitePossibleMoves.get(key)

	for move in range(len(moves)):
		if (x == moves[move][0] and y == moves[move][1]):
			return True
	return False

def GetPlayValue(x, y):
	for k, v in whitePieces.items():
		if (v[1] == x and v[2] == y):
			if (v[0] == 'K'):
				return 900
			if (v[0] == 'Q'):
				return 90
			if (v[0] == 'B'):
				return 30
			if (v[0] == 'H'):
				return 30
			if (v[0] == 'R'):
				return 50
			if (v[0] == 'P'):
				return 10

def GetPieceValue(piece):
	if (piece == 'King'):
		return 900
	if (piece == 'Queen'):
		return 90
	if (piece == 'LeftBishop'):
		return 30
	if (piece == 'LeftKnight'):
		return 30
	if (piece == 'LeftRook'):
		return 50
	if (piece == 'RightBishop'):
		return 30
	if (piece == 'RightKnight'):
		return 30
	if (piece == 'RightRook'):
		return 50
	if (piece == 'Pawn1'):
		return 10
	if (piece == 'Pawn2'):
		return 10
	if (piece == 'Pawn3'):
		return 10
	if (piece == 'Pawn4'):
		return 10
	if (piece == 'Pawn5'):
		return 10
	if (piece == 'Pawn6'):
		return 10
	if (piece == 'Pawn7'):
		return 10
	if (piece == 'Pawn8'):
		return 10
	else: 
		return 5

def FindPossiblePawnMoves():
#Black Pawns
	for k, v in blackPieces.items():
		if (v[0] == 'P'):
			if (v[3] == 0):
				blackPossibleMoves[k].append([v[1], v[2] + 1])
				blackPossibleMoves[k].append([v[1], v[2] + 2])
			else:
				blackPossibleMoves[k].append([v[1], v[2] + 1])

			if (v[1] + 1 < 8):
					if (board[v[1] + 1][v[2] + 1] != '0' and IsEnemyPiece('white', v[1] + 1, v[2] + 1)):
						blackPossibleMoves[k].append([v[1] + 1, v[2] + 1, GetPlayValue(v[1] + 1, v[2] + 1)])

			if (v[1] - 1 >= 0):
					if (board[v[1] - 1][v[2] + 1] != '0' and IsEnemyPiece('white', v[1] - 1, v[2] + 1)): 
						blackPossibleMoves[k].append([v[1] - 1, v[2] + 1, GetPlayValue(v[1] - 1, v[2] + 1)])
#White Pawns
	for k, v in whitePieces.items():
		if (v[0] == 'P'):
			if (v[3] == 0):
				whitePossibleMoves[k].append([v[1], v[2] - 1])
				whitePossibleMoves[k].append([v[1], v[2] - 2])
			else:
				whitePossibleMoves[k].append([v[1], v[2] - 1])
			#The ifTaken are to account for moves that cannot currently take place but could if conditions change
			#i.e. a piece that was blocking it was captured or a piece moves into it a position that it could attack
			if (v[1] + 1 < 8):
					if (board[v[1] + 1][v[2] - 1] != '0'):
						if (IsEnemyPiece('black', v[1] + 1, v[2] - 1)):
							whitePossibleMoves[k].append([v[1] + 1, v[2] - 1])
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] + 1, v[2] - 1])
					else: 
						whitePossibleMoves['IfTaken'].append([v[1] + 1, v[2] - 1])
			if (v[1] - 1 >= 0):
					if (board[v[1] - 1][v[2] - 1] != '0'):
						if (IsEnemyPiece('black', v[1] - 1, v[2] - 1)):
							whitePossibleMoves[k].append([v[1] - 1, v[2] - 1])
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] - 1, v[2] - 1])
					else: 
						whitePossibleMoves['IfTaken'].append([v[1] - 1, v[2] - 1])

def FindPossibleRookMoves():
	for k, v in blackPieces.items():
		if (v[0] == 'R'):
			#Checks spaces below
			for spaces in range(1, len(chessBoardY) - v[2]):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] + spaces)):
							blackPossibleMoves[k].append([v[1], v[2] + spaces, GetPlayValue(v[1], v[2] + spaces)])
							break
					else: 
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] - spaces)):
							blackPossibleMoves[k].append([v[1], v[2] - spaces, GetPlayValue(v[1], v[2] - spaces)])
					else: 
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, len(chessBoardX) - v[1]):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] + spaces, v[2])):
							blackPossibleMoves[k].append([v[1] + spaces, v[2], GetPlayValue(v[1] + spaces, v[2])])
							break
					else: 
						break

				else:
					blackPossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] - spaces, v[2])):
							blackPossibleMoves[k].append([v[1] - spaces, v[2], GetPlayValue(v[1] - spaces, v[2])])
					else: 
						break

				else:
					blackPossibleMoves[k].append([v[1] - spaces, v[2]])

	for k, v in whitePieces.items():
		if (v[0] == 'R'):
			#Checks spaces below
			for spaces in range(1, len(chessBoardY) - v[2]):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] + spaces)):
							whitePossibleMoves[k].append([v[1], v[2] + spaces])
							break
					else: 
						whitePossibleMoves['IfTaken'].append([v[1], v[2] + spaces])
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(1, v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] - spaces)):
							whitePossibleMoves[k].append([v[1], v[2] - spaces])
					else: 
						whitePossibleMoves['IfTaken'].append([v[1], v[2] - spaces])
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, len(chessBoardX) - v[1]):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] + spaces, v[2])):
							whitePossibleMoves[k].append([v[1] + spaces, v[2] ])
							break
					else: 
						whitePossibleMoves['IfTaken'].append([v[1] + spaces, v[2]])
						break

				else:
					whitePossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] - spaces, v[2])):
							whitePossibleMoves[k].append([v[1] - spaces, v[2]])
					else: 
						whitePossibleMoves['IfTaken'].append([v[1] - spaces, v[2]])
						break

				else:
					whitePossibleMoves[k].append([v[1] - spaces, v[2]])

def FindPossibleKnightMoves():
	#Kind of a mess but allows the code to be short relativley straigtforward
	#Basically loops over the knights moveset and after checking that everything is within bounds
	# Checks if thers is another piece there and if only if it is a enemy adds it to the availible moves
	knightMoves = [[-2, 1], [-2, -1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
	for k, v in blackPieces.items():
		if (v[0] == 'H'):
			for moves in range(len(knightMoves)):
				if ((v[1] + knightMoves[moves][0]) >= 0 and (v[1] + knightMoves[moves][0]) < 8 and (v[2] + knightMoves[moves][1]) >= 0 and (v[2] + knightMoves[moves][1]) < 8):
					if (board[v[1] + knightMoves[moves][0]][v[2] + knightMoves[moves][1]] != '0'):
						if (IsEnemyPiece('white', v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1])):
								blackPossibleMoves[k].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1], GetPlayValue(v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1])])
								
					else:
						blackPossibleMoves[k].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1]])

	for k, v in whitePieces.items():
		if (v[0] == 'H'):
			for moves in range(len(knightMoves)):
				if ((v[1] + knightMoves[moves][0]) >= 0 and (v[1] + knightMoves[moves][0]) < 8 and (v[2] + knightMoves[moves][1]) >= 0 and (v[2] + knightMoves[moves][1]) < 8):
					if (board[v[1] + knightMoves[moves][0]][v[2] + knightMoves[moves][1]] != '0'):
						if (IsEnemyPiece('black', v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1])):
								whitePossibleMoves[k].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1]])

						else: 
							whitePossibleMoves['IfTaken'].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1]])
							
						
					else:
						whitePossibleMoves[k].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1]])

def FindPossibleBishopMoves():
	for k, v in blackPieces.items():
		if (v[0] == 'B'):
			#down right diagonal
			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] + spaces < 8):
					if (board[v[1] + spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces, GetPlayValue(v[1] + spaces, v[2] + spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] - spaces >= 0):
					if (board[v[1] - spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces, GetPlayValue(v[1] - spaces, v[2] - spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] + spaces < 8):
					if (board[v[1] - spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces, GetPlayValue(v[1] - spaces, v[2] + spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] - spaces >= 0):
					if (board[v[1] + spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] - spaces, GetPlayValue(v[1] + spaces, v[2] - spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] + spaces, v[2] - spaces])

	for k, v in whitePieces.items():
		if (v[0] == 'B'):
			#down right diagonal
			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] + spaces < 8):
					if (board[v[1] + spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('black', v[1] + spaces, v[2] + spaces)):
								whitePossibleMoves[k].append([v[1] + spaces, v[2] + spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] + spaces, v[2] + spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] + spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] - spaces >= 0):
					if (board[v[1] - spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('black', v[1] - spaces, v[2] - spaces)):
								whitePossibleMoves[k].append([v[1] - spaces, v[2] - spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] - spaces, v[2] - spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] - spaces, v[2] - spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] + spaces < 8):
					if (board[v[1] - spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('black', v[1] - spaces, v[2] + spaces)):
								whitePossibleMoves[k].append([v[1] - spaces, v[2] + spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] - spaces, v[2] + spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] - spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] - spaces >= 0):
					if (board[v[1] + spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('black', v[1] + spaces, v[2] - spaces)):
								whitePossibleMoves[k].append([v[1] + spaces, v[2] - spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] + spaces, v[2] - spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] + spaces, v[2] - spaces])

def FindPossibleQueenMoves():
	for k, v in blackPieces.items():
		if (v[0] == 'Q'):
			#Checks spaces below
			for spaces in range(1, len(chessBoardY) - v[2]):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] + spaces)):
							blackPossibleMoves[k].append([v[1], v[2] + spaces, GetPlayValue(v[1], v[2] + spaces)])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] - spaces)):
							blackPossibleMoves[k].append([v[1], v[2] - spaces, GetPlayValue(v[1], v[2] - spaces)])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, len(chessBoardX) - v[1]):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] + spaces, v[2])):
							blackPossibleMoves[k].append([v[1] + spaces, v[2], GetPlayValue(v[1] + spaces, v[2])])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] - spaces, v[2])):
							blackPossibleMoves[k].append([v[1] - spaces, v[2], GetPlayValue(v[1] - spaces, v[2])])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] - spaces, v[2]])

			#down right diagonal
			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] + spaces < 8):
					if (board[v[1] + spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces, GetPlayValue(v[1] + spaces, v[2] + spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] - spaces >= 0):
					if (board[v[1] - spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces, GetPlayValue(v[1] - spaces, v[2] - spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] + spaces < 8):
					if (board[v[1] - spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces, GetPlayValue(v[1] - spaces, v[2] + spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] - spaces >= 0):
					if (board[v[1] + spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] - spaces, GetPlayValue(v[1] + spaces, v[2] - spaces)])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] + spaces, v[2] - spaces])

	for k, v in whitePieces.items():
		if (v[0] == 'Q'):
			#Checks spaces below
			for spaces in range(1, len(chessBoardY) - v[2]):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] + spaces)):
							whitePossibleMoves[k].append([v[1], v[2] + spaces])
							break
					else: 
						whitePossibleMoves['IfTaken'].append([v[1], v[2] + spaces])
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(1, v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] - spaces)):
							whitePossibleMoves[k].append([v[1], v[2] - spaces])
					else: 
						whitePossibleMoves['IfTaken'].append([v[1], v[2] - spaces])
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, len(chessBoardX) - v[1]):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] + spaces, v[2])):
							whitePossibleMoves[k].append([v[1] + spaces, v[2] ])
							break
					else: 
						whitePossibleMoves['IfTaken'].append([v[1] + spaces, v[2] ])
						break

				else:
					whitePossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] - spaces, v[2])):
							whitePossibleMoves[k].append([v[1] - spaces, v[2]])
					else: 
						whitePossibleMoves['IfTaken'].append([v[1] - spaces, v[2]])
						break

				else:
					whitePossibleMoves[k].append([v[1] - spaces, v[2]])

			#down right diagonal
			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] + spaces < 8):
					if (board[v[1] + spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('black', v[1] + spaces, v[2] + spaces)):
								whitePossibleMoves[k].append([v[1] + spaces, v[2] + spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] + spaces, v[2] + spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] + spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] - spaces >= 0):
					if (board[v[1] - spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('black', v[1] - spaces, v[2] - spaces)):
								whitePossibleMoves[k].append([v[1] - spaces, v[2] - spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] - spaces, v[2] - spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] - spaces, v[2] - spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] + spaces < 8):
					if (board[v[1] - spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('black', v[1] - spaces, v[2] + spaces)):
								whitePossibleMoves[k].append([v[1] - spaces, v[2] + spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] - spaces, v[2] + spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] - spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] - spaces >= 0):
					if (board[v[1] + spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('black', v[1] + spaces, v[2] - spaces)):
								whitePossibleMoves[k].append([v[1] + spaces, v[2] - spaces])
								break
						else: 
							whitePossibleMoves['IfTaken'].append([v[1] + spaces, v[2] - spaces])
							break
					else:
						whitePossibleMoves[k].append([v[1] + spaces, v[2] - spaces])

def FindPossibleKingMoves():
	for k, v in blackPieces.items():
		if (v[0] == 'K'):
			#Checks spaces below
			for spaces in range(1, 2):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] + spaces)):
							blackPossibleMoves[k].append([v[1], v[2] + spaces])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(1, 2):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] - spaces)):
							blackPossibleMoves[k].append([v[1], v[2] - spaces])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, 2):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] + spaces, v[2])):
							blackPossibleMoves[k].append([v[1] + spaces, v[2] ])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, 2):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] - spaces, v[2])):
							blackPossibleMoves[k].append([v[1] - spaces, v[2]])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] - spaces, v[2]])

	for k, v in whitePieces.items():
		if (v[0] == 'K'):
			#Checks spaces below
			#TODO check to make sure spaces are in range of the board index
			for spaces in range(0, 0):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] + spaces)):
							whitePossibleMoves[k].append([v[1], v[2] + spaces])
							break
					else:
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(1, 2):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] - spaces)):
							whitePossibleMoves[k].append([v[1], v[2] - spaces])
					else:
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, 2):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] + spaces, v[2])):
							whitePossibleMoves[k].append([v[1] + spaces, v[2] ])
							break
					else:
						break

				else:
					whitePossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, 2):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] - spaces, v[2])):
							whitePossibleMoves[k].append([v[1] - spaces, v[2]])
					else:
						break

				else:
					whitePossibleMoves[k].append([v[1] - spaces, v[2]])

def FindPossibleLoss():
	for bk, bv in blackPossibleMoves.items():
		for wk, wv in whitePossibleMoves.items():
			for bItem in range(len(bv)):
				for wItem in range(len(wv)):
					if (bv[bItem][0] == wv[wItem][0]):
						if (bv[bItem][1] == wv[wItem][1]):
							if (len(bv[bItem]) > 2):
								bv[bItem][2] = bv[bItem][2] - GetPieceValue(bk)
							else:
								bv[bItem].append(0 - GetPieceValue(bk))
					elif(blackPieces[bk][1] == wv[wItem][0]):
						if (blackPieces[bk][2] == wv[wItem][1]):
							if (len(bv[bItem]) > 2):
								bv[bItem][2] = bv[bItem][2] + GetPieceValue(bk)
							else:
								bv[bItem].append(GetPieceValue(bk))
					else:
						if (len(bv[bItem]) > 2):
							bv[bItem][2] = bv[bItem][2]
						else:
							bv[bItem].append(0)						

def FindPossibleMoves():
	for k, v in blackPossibleMoves.items():
		v.clear()
	for k, v in whitePossibleMoves.items():
		v.clear()

	FindPossiblePawnMoves()
	FindPossibleRookMoves()
	FindPossibleBishopMoves()
	FindPossibleKnightMoves()
	FindPossibleQueenMoves()
	FindPossibleKingMoves()

	FindPossibleLoss()

def HumanPlayTurn(piece, pieceMove):
		if (board[pieceMove[0]][pieceMove[1]] != 0):
			RemovePiece('black', pieceMove[0], pieceMove[1])

		board[whitePieces[piece][1]][whitePieces[piece][2]] = '0'
		whitePieces[piece][1] = pieceMove[0]
		whitePieces[piece][2] = pieceMove[1]
		if (piece[0] == 'P'):
			whitePieces[piece][3] = 1
		PlacePiece(' ', whitePieces[piece][0], whitePieces[piece][1], whitePieces[piece][2]) 
		movePieceKey = 0
		return True		

def ComputerPlayTurn():
	global AITurns
	moves = []
	piece = None
	pieceMove = None
	play = None
	if (AITurns > AITurnsBeforeAnalyze):
		for k, v in blackPossibleMoves.items():
			for item in range(len(v)):
				if (len(v[item]) > 2):
					moveList = v[item]
					moveValue = [k] + moveList
					moves.append(moveValue)
	if (len(moves) > 0):
		play = max(moves, key=lambda x: x[3])
		pieceMove = [play[1], play[2]]
		piece = blackPieces[play[0]]
		play = play[0]
	else:
		play = random.choice(list(blackPossibleMoves.keys()))
		while (len(blackPossibleMoves[play]) == 0):
			play = random.choice(list(blackPossibleMoves.keys()))
		piece = blackPieces[play]
		pieceMove = random.choice(list(blackPossibleMoves[play]))

	if (board[pieceMove[0]][pieceMove[1]] != 0):
				RemovePiece('white', pieceMove[0], pieceMove[1])

	board[piece[1]][piece[2]] = '0'
	blackPieces[play][1] = pieceMove[0]
	blackPieces[play][2] = pieceMove[1]
	if (piece[0] == 'P'):
		blackPieces[play][3] = 1

	PlacePiece(' ', blackPieces[play][0], blackPieces[play][1], blackPieces[play][2])
	
	AITurns += 1
				
def UpdateBoard():
	size = 50

	#Piece Images	

	#board length, must be even
	boardLength = 8
	gameDisplay.fill(white)
	cnt = 0
	for i in range(1,boardLength+1):
		for z in range(1,boardLength+1):
			#check if current loop value is even
			if cnt % 2 == 0:
				pygame.draw.rect(gameDisplay, white,[size*z,size*i,size,size])
			else:
				pygame.draw.rect(gameDisplay, black, [size*z,size*i,size,size])
			cnt +=1
		#since theres an even number of squares go back one value
		cnt-=1
	#Add a nice boarder
	pygame.draw.rect(gameDisplay,black,[size,size,boardLength*size,boardLength*size],1)
	ShowMoves()
	for k, v in whitePieces.items():
		if (v[0] == 'P'):
			gameDisplay.blit(whitePawn, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'R'):
			gameDisplay.blit(whiteRook, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'B'):
			gameDisplay.blit(whiteBishop, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'H'):
			gameDisplay.blit(whiteKnight, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'K'):
			gameDisplay.blit(whiteKing, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'Q'):
			gameDisplay.blit(whiteQueen, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))

	for k, v in blackPieces.items():
		if (v[0] == 'P'):
			gameDisplay.blit(blackPawn, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'R'):
			gameDisplay.blit(blackRook, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'B'):
			gameDisplay.blit(blackBishop, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'H'):
			gameDisplay.blit(blackKnight, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'K'):
			gameDisplay.blit(blackKing, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
		if (v[0] == 'Q'):
			gameDisplay.blit(blackQueen, ((v[1] * imageOffset) + 45, (v[2] * imageOffset) + 45))
	
	#shows potential moves, will add this when a piece is clicked on
	#for k, v in whitePossibleMoves.items():
	#	if (k == 'Pawn1'):
	#		for items in range(len(v)):
	#			pygame.draw.rect(gameDisplay, red,[size*v[items][0] + imageOffset, size*v[items][1] + imageOffset, size, size])

def ShowMoves():
	size = 50
	moves = whitePossibleMoves.get(movePieceKey)
	if (moves != None):
		for items in range(len(moves)):
			pygame.draw.rect(gameDisplay, red,[size*moves[items][0] + imageOffset, size*moves[items][1] + imageOffset, size, size])
			moveSquares.append(moves[items])

def Main():
	InitBoard()
	InitPieces()
	DrawBoard()
	FindPossibleMoves()
	gameState = 'playing'
	gameExit = False
	humanTurn = False

	while(gameExit != True):
		while not gameExit:
			UpdateBoard()
			pygame.display.update()
			FindPossibleMoves()
			if (humanTurn == True):
				ComputerPlayTurn()
				humanTurn = False
				FindPossibleMoves()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y postions of the mouse click
					x, y = event.pos
					x = int((x - 50) / imageOffset)
					y = int((y - 50) / imageOffset)

					if (x >= 0 and x < 8 and y >= 0 and y < 8):
						global moveSquares
						global movePieceKey
						for items in range(len(moveSquares)):
							if (moveSquares[items][0] == x and moveSquares[items][1] == y):
								humanTurn = HumanPlayTurn(movePieceKey, pieceMove=[x, y])
						moveSquares = []
						movePieceKey = IsPieceThere(x, y)
					
Main()

pygame.quit()
