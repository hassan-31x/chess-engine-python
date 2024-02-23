class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

        #? dictionary to keep track of the move functions for each piece where each value of key value pair is a function
        self.moveFunctions = {'p': self.pawnMoves, 'R': self.rookMoves, 'N': self.knightMoves,
                              'B': self.bishopMoves, 'Q': self.queenMoves, 'K': self.kingMoves}
        self.whiteTurn = True
        self.moveHistory = []
        self.whitekinglocation=(7,4)
        self.blackkinglocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        

    #takes move as parameter and executes it
    def makeMove(self, move): #for basic movements only (not for castling, or enpassant)
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveHistory.append(move)
        self.whiteTurn = not self.whiteTurn
        #update king location
        if move.pieceMoved=='wK':
            self.whitekinglocation=(move.endRow,move.endCol)
        elif move.pieceMoved=='bK':
            self.blackkinglocation=(move.endRow,move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'

        

    #undo previous move
    def undoMove(self):
        if len(self.moveHistory) != 0:
            move = self.moveHistory.pop() #remove the last move from the move history
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTurn = not self.whiteTurn
            if move.pieceMoved=='wK':
                self.whitekinglocation=(move.startRow,move.startCol)
            elif move.pieceMoved=='bK':
                self.blackkinglocation=(move.startRow,move.startCol)
        

    def getValidMoves(self):
        moves=self.getAllPossibleMoves()
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            oppmoves=self.getAllPossibleMoves()
            self.whiteTurn=not self.whiteTurn
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteTurn=not self.whiteTurn
            self.undoMove()
        if len(moves)==0: #checkmate or stalemate
            if self.inCheck()==True:
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False
        return moves
    
    def inCheck(self):
        if self.whiteTurn:
            return self.squareunderattack(self.whitekinglocation[0],self.whitekinglocation[1])
        else:
            return self.squareunderattack(self.blackkinglocation[0],self.blackkinglocation[1])

    #determine if the enemy can attack the square r,c
    def squareunderattack(self,r,c):
        self.whiteTurn=not self.whiteTurn
        oppmoves=self.getAllPossibleMoves()
        self.whiteTurn=not self.whiteTurn
        for move in oppmoves:
            if move.endRow==r and move.endCol==c:
                return True #square under attack
        return False                          



    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #r = row
            for c in range(len(self.board[r])): #c = column for each row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteTurn) or (turn == 'b' and not self.whiteTurn):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #? calls the appropriate move function based on piece type
                    
        return moves

    def pawnMoves(self, r, c, moves):
        if self.whiteTurn:
            if self.board[r-1][c] == "--": #? 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #? 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #? enemy piece to capture to the left
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #? enemy piece to capture to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def rookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #? up, left, down, right
        enemyColor = "b" if self.whiteTurn else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

        
    def knightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) #? 2.5 of all possible knight moves
        allyColor = "w" if self.whiteTurn else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def bishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #? up-left, up-right, down-left, down-right diagnols
        enemyColor = "b" if self.whiteTurn else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def queenMoves(self, r, c, moves): #? queen moves are a combination of rook and bishop moves
        self.rookMoves(r, c, moves)
        self.bishopMoves(r, c, moves)

    def kingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) #? all possible king moves (1 square in any direction)
        allyColor = "w" if self.whiteTurn else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        
class Move():
    #? maps locally used indexes to chess notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion=False
        if (self.pieceMoved=='wp' and self.endRow==0) or (self.pieceMoved=='bp' and self.endRow==7):
            self.isPawnPromotion=True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other): #! overriding the equals method
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    #? print the move in chess notation using the dictionary to map numbers to letters
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    #? helper function to get the chess notation for a square based on its row and column
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]