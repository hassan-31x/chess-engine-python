import pygame
import ChessEngine

w = h = 512 # width and height of the board
squareSize = h // 8 # size of each square
images = {}

#? load images of all pieces
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK'] #list of all pieces

    for peice in pieces:
        images[peice] = pygame.transform.scale(pygame.image.load("images/" + peice + ".png"), (squareSize, squareSize))

def main():
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False #? flag variable for when a move is made so we dont have to call it everytime
    animate=False
    loadImages()
    running = True

    sqSelected = () #? keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #? keep track of player clicks (two tuples)
    gameOver=False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: #end game when quit is pressed
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN: #mouse handling on clikc
                if not gameOver:
                    location = pygame.mouse.get_pos()
                    col = location[0] // squareSize
                    row = location[1] // squareSize
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):   
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate=True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handling
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z: #? undo when z is pressed
                    gs.undoMove()
                    moveMade = True
                    animate=False
                if e.key==pygame.K_r: #reset the board when 'r' is pressed
                    gs=ChessEngine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
        if moveMade:
            if animate:
                animatingMove(gs.moveHistory[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate=False 

        drawGame(screen, gs,validMoves,sqSelected)

        if gs.checkMate:
            gameOver=True
            if gs.whiteTurn:
                showMessage(screen,'Black wins by checkmate')
            else:
                showMessage(screen,'White wins by checkmate')
        elif gs.staleMate:
            gameOver=True
            showMessage(screen,'Stalemate')
        clock.tick(60)
        pygame.display.flip()

#highlighting possible moves
def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected!=():
        r,c=sqSelected
        if gs.board[r][c][0]==('w' if gs.whiteTurn else 'b'):
            s=pygame.Surface((squareSize,squareSize))
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))
            screen.blit(s,(c*squareSize,r*squareSize))
            s.fill(pygame.Color('yellow'))
            for move in validMoves:
                if move.startRow==r and move.startCol==c:
                    screen.blit(s,(move.endCol*squareSize,move.endRow*squareSize))


def drawGame(screen, gs,validMoves,sqSelected):
    drawBoard(screen,0,0,squareSize)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen, gs.board)    

def drawBoard(screen, row, c, squareSize): #iterative
    if row == 8:
        return 

    colors = [pygame.Color("white"), pygame.Color("cyan")] #checkbox colors

    #draw the board alternating colors
    for col in range(c, 8):
        color = colors[(row + col) % 2]
        pygame.draw.rect(screen, color, pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))

    # recursion
    drawBoard(screen, row + 1, 0, squareSize)


def drawPieces(screen, board):
    #? loop through the 2D array board and draw the pieces
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


def animatingMove(move,screen,board,clock):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    coordinates=[] #list of coordinates that the animation will move through
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPersq=10 #frames to move one square
    frameCount=(abs(dR)+abs(dC))*framesPersq
    for frame in range(frameCount+1):
        r,c=(move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount)
        drawBoard(screen,0,0,squareSize)
        drawPieces(screen,board)
        #erase piece moved from ending square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare=pygame.Rect(move.endCol*squareSize,move.endRow*squareSize,squareSize,squareSize)
        pygame.draw.rect(screen,color,endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured!='--':
            screen.blit(images[move.pieceMoved],pygame.Rect(c*squareSize,r*squareSize,squareSize,squareSize))
            pygame.display.flip()
            clock.tick(60)

#? show message when game ends
def showMessage(screen,text):
    font=pygame.font.SysFont("Arial",48,True,False) #set font
    textObject=font.render(text,0,pygame.Color('Black')) #set font color
    textLocation=pygame.Rect(0,0,w,h).move(w/2-textObject.get_width()/2,h/2-textObject.get_height()/2) #draw text
    screen.blit(textObject,textLocation)


if __name__ == "__main__":
    main()