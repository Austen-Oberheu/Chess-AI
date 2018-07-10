chessBoardX = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
chessBoardY = ['8', '7', '6', '5', '4', '3', '2', '1']
#Set board size
board = [[0 for x in range(len(chessBoardX))] for y in range(len(chessBoardY))]

#Set all pieces initial postion and also will allow the game to keep track of all the pieces 
blackPieces = {'LeftRook': ['R', 0, 4], 'LeftKnight': ['H', 1, 0], 'LeftBishop': ['B', 2, 3], 'Queen': ['Q', 3, 0], 'King': ['K', 4, 3], 'RightBishop': ['B', 5, 0],
			  'RightKnight': ['H', 6, 0], 'RightRook': ['R', 7, 0], 'Pawn1': ['P', 0, 1, 0], 'Pawn2': ['P', 1, 1, 0], 'Pawn3': ['P', 2, 1, 0], 'Pawn4': ['P', 3, 1, 0], 'Pawn5': ['P', 4, 1, 0],
			 'Pawn6': ['P', 5, 1, 0], 'Pawn7': ['P', 6, 1, 0], 'Pawn8': ['P', 7, 1, 0]}

blackPossibleMoves = {'LeftRook': [], 'LeftKnight': [], 'LeftBishop': [], 'Queen': [], 'King': [], 'RightBishop': [],
			  'RightKnight': [], 'RightRook': [], 'Pawn1': [], 'Pawn2': [], 'Pawn3': [], 'Pawn4': [], 'Pawn5': [],
			 'Pawn6': [], 'Pawn7': [], 'Pawn8': []}

whitePieces = {'LeftRook': ['R', 0, 7], 'LeftKnight': ['H', 1, 7], 'LeftBishop': ['B', 2, 7], 'Queen': ['Q', 3, 7], 'King': ['K', 4, 7], 'RightBishop': ['B', 5, 7],
			  'RightKnight': ['H', 6, 7], 'RightRook': ['R', 7, 7], 'Pawn1': ['P', 0, 6, 0], 'Pawn2': ['P', 1, 6, 0], 'Pawn3': ['P', 2, 6, 0], 'Pawn4': ['P', 3, 6, 0], 'Pawn5': ['P', 4, 6, 0],
			 'Pawn6': ['P', 5, 6, 0], 'Pawn7': ['P', 6, 5, 0], 'Pawn8': ['P', 7, 4, 0]}

whitePossibleMoves = {'LeftRook': [], 'LeftKnight': [], 'LeftBishop': [], 'Queen': [], 'King': [], 'RightBishop': [],
			  'RightKnight': [], 'RightRook': [], 'Pawn1': [], 'Pawn2': [], 'Pawn3': [], 'Pawn4': [], 'Pawn5': [],
			 'Pawn6': [], 'Pawn7': [], 'Pawn8': []}

def InitBoard():
	for y in range(len(chessBoardY)):
		for x in range(len(chessBoardX)):
			board[x][y] = '0'  

def PlacePiece(name, piece, x, y):
	board[x][y] = piece
	print('inserting ' + name + ' at board position: ' + chessBoardX[x] + ' ' + chessBoardY[y])

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
					if (board[v[1] + 1][v[2] + 1] != '0'):
						blackPossibleMoves[k].append([v[1] + 1, v[2] + 1])
			if (v[1] - 1 > 0):
					if (board[v[1] - 1][v[2] + 1] != '0'): 
						blackPossibleMoves[k].append([v[1] - 1, v[2] + 1])
#White Pawns
	for k, v in whitePieces.items():
		if (v[0] == 'P'):
			if (v[3] == 0):
				whitePossibleMoves[k].append([v[1], v[2] - 1])
				whitePossibleMoves[k].append([v[1], v[2] - 2])
			else:
				whitePossibleMoves[k].append([v[1], v[2] - 1])

			if (v[1] + 1 < 8):
					if (board[v[1] + 1][v[2] - 1] != '0'):
						if (IsEnemyPiece('black', v[1] + 1, v[2] - 1)):
							whitePossibleMoves[k].append([v[1] + 1, v[2] - 1])
			if (v[1] - 1 > 0):
					if (board[v[1] - 1][v[2] - 1] != '0'):
						if (IsEnemyPiece('black', v[1] - 1, v[2] - 1)):
							whitePossibleMoves[k].append([v[1] - 1, v[2] - 1])

def FindPossibleRookMoves():
	for k, v in blackPieces.items():
		if (v[0] == 'R'):
			#Checks spaces below
			for spaces in range(1, len(chessBoardY) - v[2]):
				if (board[v[1]][v[2] + spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] + spaces)):
							blackPossibleMoves[k].append([v[1], v[2] + spaces])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] - spaces)):
							blackPossibleMoves[k].append([v[1], v[2] - spaces])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, len(chessBoardX) - v[1]):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] + spaces, v[2])):
							blackPossibleMoves[k].append([v[1] + spaces, v[2] ])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] - spaces, v[2])):
							blackPossibleMoves[k].append([v[1] - spaces, v[2]])
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
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(1, v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] - spaces)):
							whitePossibleMoves[k].append([v[1], v[2] - spaces])
					else:
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
						break

				else:
					whitePossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] - spaces, v[2])):
							whitePossibleMoves[k].append([v[1] - spaces, v[2]])
					else:
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
								blackPossibleMoves[k].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1]])
						
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
						whitePossibleMoves[k].append([v[1] + knightMoves[moves][0], v[2] + knightMoves[moves][1]])

def FindPossibleBishopMoves():
	for k, v in blackPieces.items():
		if (v[0] == 'B'):
			#down right diagonal
			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] + spaces < 8):
					if (board[v[1] + spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] - spaces >= 0):
					if (board[v[1] - spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] + spaces < 8):
					if (board[v[1] - spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] - spaces >= 0):
					if (board[v[1] + spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] - spaces])
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
							blackPossibleMoves[k].append([v[1], v[2] + spaces])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('white', v[1], v[2] - spaces)):
							blackPossibleMoves[k].append([v[1], v[2] - spaces])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1], v[2] - spaces])

			#check spaces to right
			for spaces in range(1, len(chessBoardX) - v[1]):
				if (board[v[1] + spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] + spaces, v[2])):
							blackPossibleMoves[k].append([v[1] + spaces, v[2] ])
							break
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('white', v[1] - spaces, v[2])):
							blackPossibleMoves[k].append([v[1] - spaces, v[2]])
					else:
						break

				else:
					blackPossibleMoves[k].append([v[1] - spaces, v[2]])

			#down right diagonal
			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] + spaces < 8):
					if (board[v[1] + spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] + spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] - spaces >= 0):
					if (board[v[1] - spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] - spaces])

			for spaces in range(1, 8):
				if (v[1] - spaces >= 0 and v[2] + spaces < 8):
					if (board[v[1] - spaces][v[2] + spaces] != '0'):
						if (IsEnemyPiece('white', v[1] - spaces, v[2] + spaces)):
								blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces])
								break
						else:
							break
					else:
						blackPossibleMoves[k].append([v[1] - spaces, v[2] + spaces])

			for spaces in range(1, 8):
				if (v[1] + spaces < 8 and v[2] - spaces >= 0):
					if (board[v[1] + spaces][v[2] - spaces] != '0'):
						if (IsEnemyPiece('white', v[1] + spaces, v[2] - spaces)):
								blackPossibleMoves[k].append([v[1] + spaces, v[2] - spaces])
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
						break

				else:
					whitePossibleMoves[k].append([v[1], v[2] + spaces])
			#check spaces above
			for spaces in range(1, v[2]):
				if (board[v[1]][v[2] - spaces] != '0'):
					if (IsEnemyPiece('black', v[1], v[2] - spaces)):
							whitePossibleMoves[k].append([v[1], v[2] - spaces])
					else:
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
						break

				else:
					whitePossibleMoves[k].append([v[1] + spaces, v[2]])

			#check spaces to left
			for spaces in range(1, v[1]):
				if (board[v[1] - spaces][v[2]] != '0'):
					if (IsEnemyPiece('black', v[1] - spaces, v[2])):
							whitePossibleMoves[k].append([v[1] - spaces, v[2]])
					else:
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

def FindPossibleMoves():
	FindPossiblePawnMoves()
	FindPossibleRookMoves()
	FindPossibleBishopMoves()
	FindPossibleKnightMoves()
	FindPossibleQueenMoves()
	FindPossibleKingMoves()

InitBoard()
InitPieces()
DrawBoard()
FindPossibleMoves()

stuff
