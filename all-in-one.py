import pygame
import sys
import random
from pygame.locals import *
import cv2
from cvzone.HandTrackingModule import HandDetector
from PIL import Image as im

BOARDWIDTH = 2  # number of columns in the board
BOARDHEIGHT = 2  # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 1040
WINDOWHEIGHT = 680
FPS = 30
BLANK = None

#        R    G    B
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0,  50, 255)
DARKTURQUOISE = (3,  54,  73)
GREEN = (0, 204,   0)
RED = (255, 0, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int(
    (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
mode = "MANUAL"
isPlaying = False


def main():
    global isPlaying, seconds,start_ticks, allMoves, mainBoard, mode, XMARGIN, YMARGIN, BOARDWIDTH, BOARDHEIGHT, FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, LEVEL1_SURF, LEVEL1_RECT, LEVEL2_SURF, LEVEL2_RECT, LEVEL3_SURF, LEVEL3_RECT, LEVEL4_SURF, LEVEL4_RECT, IDS_SURF, IDS_RECT, GESTURE_SURF, GESTURE_RECT, MANUAL_SURF, MANUAL_RECT, TIMER_SURF, TIMER_RECT
    pygame.init()
    start_ticks = pygame.time.get_ticks()
    seconds = 0.0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText(
        'Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
    NEW_SURF,   NEW_RECT = makeText(
        'New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    SOLVE_SURF, SOLVE_RECT = makeText(
        'Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    LEVEL1_SURF, LEVEL1_RECT = makeText(
        "Level1 (2X2)",    TEXTCOLOR, TILECOLOR, 20, WINDOWHEIGHT - 150)
    LEVEL2_SURF, LEVEL2_RECT = makeText(
        "Level2 (3X3)",    TEXTCOLOR, TILECOLOR, 20, WINDOWHEIGHT - 120)
    LEVEL3_SURF, LEVEL3_RECT = makeText(
        "Level3 (4X4)",    TEXTCOLOR, TILECOLOR, 20, WINDOWHEIGHT - 90)
    LEVEL4_SURF, LEVEL4_RECT = makeText(
        "Level4 (5X5)",    TEXTCOLOR, TILECOLOR, 20, WINDOWHEIGHT - 60)
    GESTURE_SURF, GESTURE_RECT = makeText(
        "Play Using Hand Gestures",   TEXTCOLOR, TILECOLOR, WINDOWWIDTH//2-150, 90)
    MANUAL_SURF, MANUAL_RECT = makeText(
        "Play Using Keyboard and Mouse",   TEXTCOLOR, TILECOLOR, WINDOWWIDTH//2-150, 60)
    IDS_SURF, IDS_RECT = makeText(
        "IDS: 1804011, 1804016, 1804017", TEXTCOLOR, BGCOLOR, WINDOWWIDTH//2-150, WINDOWHEIGHT-30)

    mainBoard, solutionSeq = generateNewPuzzle(0)
    # a solved board is the same as the board in a start state.
    SOLVEDBOARD = getStartingBoard()
    allMoves = []  # list of moves made from the solved configuration

    while True:  # main game loop
        slideTo = None  # the direction, if any, a tile should slide
        # contains the message to show in the upper left corner.
        msg = 'Click tile or press arrow keys to slide.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(
                    mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        # clicked on Reset button
                        isPlaying = False
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                        
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(
                            30)  
                        # clicked on New Game button
                        allMoves = []
                        isPlaying = True
                        pygame.init()
                        start_ticks = pygame.time.get_ticks()
                    elif SOLVE_RECT.collidepoint(event.pos):
                        # clicked on Solve button
                        isPlaying = False
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                        
                    elif LEVEL1_RECT.collidepoint(event.pos):
                        # clicked on Level1 button
                        isPlaying = False
                        BOARDWIDTH = 2
                        BOARDHEIGHT = 2
                        XMARGIN = int(
                            (WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                        YMARGIN = int(
                            (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
                        mainBoard, solutionSeq = generateNewPuzzle(2*15)
                        SOLVEDBOARD = getStartingBoard()
                        allMoves = []
                        isPlaying = True
                        pygame.init()
                        start_ticks = pygame.time.get_ticks()
                    elif LEVEL2_RECT.collidepoint(event.pos):
                        # clicked on Level2 button
                        isPlaying = False
                        BOARDWIDTH = 3
                        BOARDHEIGHT = 3
                        XMARGIN = int(
                            (WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                        YMARGIN = int(
                            (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
                        mainBoard, solutionSeq = generateNewPuzzle(3*15)
                        SOLVEDBOARD = getStartingBoard()
                        allMoves = []
                        isPlaying = True
                        pygame.init()
                        start_ticks = pygame.time.get_ticks()
                    elif LEVEL3_RECT.collidepoint(event.pos):
                        # clicked on Level3 button
                        isPlaying = False
                        BOARDWIDTH = 4
                        BOARDHEIGHT = 4
                        XMARGIN = int(
                            (WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                        YMARGIN = int(
                            (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
                        mainBoard, solutionSeq = generateNewPuzzle(4*15)
                        SOLVEDBOARD = getStartingBoard()
                        allMoves = []
                        isPlaying = True
                        pygame.init()
                        start_ticks = pygame.time.get_ticks()
                    elif LEVEL4_RECT.collidepoint(event.pos):
                        # clicked on Level4 button
                        isPlaying = False
                        BOARDWIDTH = 5
                        BOARDHEIGHT = 5
                        XMARGIN = int(
                            (WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                        YMARGIN = int(
                            (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
                        mainBoard, solutionSeq = generateNewPuzzle(5*15)
                        SOLVEDBOARD = getStartingBoard()
                        allMoves = []
                        isPlaying = True
                        pygame.init()
                        start_ticks = pygame.time.get_ticks()

                    elif MANUAL_RECT.collidepoint(event.pos):
                        # clicked on Manual Mode button
                        mode = "MANUAL"
                        MODE_SURF, MODE_RECT = makeText(
                            "Mode: Manual", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 30)
                        DISPLAYSURF.blit(MODE_SURF, MODE_RECT)
                    elif GESTURE_RECT.collidepoint(event.pos):
                        # clicked on Gestures Mode button
                        mode = "HAND"

                elif mode == "MANUAL":
                    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP and mode == "MANUAL":
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if mode == "HAND":
            MODE_SURF, MODE_RECT = makeText(
                "Mode: Hand Gestures", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 30)
            DISPLAYSURF.blit(MODE_SURF, MODE_RECT)
            INS_SURF, INS_RECT = makeText(
                "1 finger --> UP", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 60)
            DISPLAYSURF.blit(INS_SURF, INS_RECT)
            INS_SURF, INS_RECT = makeText(
                "2 fingers --> DOWN", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 90)
            DISPLAYSURF.blit(INS_SURF, INS_RECT)
            INS_SURF, INS_RECT = makeText(
                "3 fingers --> RIGHT", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 120)
            DISPLAYSURF.blit(INS_SURF, INS_RECT)
            INS_SURF, INS_RECT = makeText(
                "4 fingers --> LEFT", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 150)
            DISPLAYSURF.blit(INS_SURF, INS_RECT)
            fingers, hands = NoOfFingers()
            # print(fingers)
            if hands != 0:
                if fingers == 1 and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif fingers == 2 and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
                elif fingers == 3 and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif fingers == 4 and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
        if slideTo:
            # show slide on screen
            slideAnimation(mainBoard, slideTo,
                           'Click tile or press arrow keys to slide.', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)  # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        seconds = (pygame.time.get_ticks()-start_ticks)//1000
        # await asyncio.sleep(0)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky +
                                             1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky -
                                             1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx +
                                     1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx -
                                     1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR,
                     (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + \
        adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    TIMER_SURF, TIMER_RECT = makeText(
        "Timer: "+str(seconds)+" s", TEXTCOLOR, BGCOLOR, 50, 60)
    
    if isPlaying:
        DISPLAYSURF.blit(TIMER_SURF, TIMER_RECT)
    if mode == "MANUAL":
        MODE_SURF, MODE_RECT = makeText(
            "Mode: Manual", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 30)
        DISPLAYSURF.blit(MODE_SURF, MODE_RECT)
    else:
        MODE_SURF, MODE_RECT = makeText(
            "Mode: Hand Gestures", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 30)
        DISPLAYSURF.blit(MODE_SURF, MODE_RECT)
        INS_SURF, INS_RECT = makeText(
            "1 finger --> UP", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 60)
        DISPLAYSURF.blit(INS_SURF, INS_RECT)
        INS_SURF, INS_RECT = makeText(
            "2 fingers --> DOWN", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 90)
        DISPLAYSURF.blit(INS_SURF, INS_RECT)
        INS_SURF, INS_RECT = makeText(
            "3 fingers --> RIGHT", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 120)
        DISPLAYSURF.blit(INS_SURF, INS_RECT)
        INS_SURF, INS_RECT = makeText(
            "4 fingers --> LEFT", MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 220, 150)
        DISPLAYSURF.blit(INS_SURF, INS_RECT)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5,
                     top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(LEVEL1_SURF, LEVEL1_RECT)
    DISPLAYSURF.blit(LEVEL2_SURF, LEVEL2_RECT)
    DISPLAYSURF.blit(LEVEL3_SURF, LEVEL3_RECT)
    DISPLAYSURF.blit(LEVEL4_SURF, LEVEL4_RECT)
    DISPLAYSURF.blit(GESTURE_SURF, GESTURE_RECT)
    DISPLAYSURF.blit(MANUAL_SURF, MANUAL_RECT)
    DISPLAYSURF.blit(IDS_SURF, IDS_RECT)
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft,
                     moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...',
                       animationSpeed=int(TILESIZE / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:]  # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '',
                       animationSpeed=int(TILESIZE / 8))
        makeMove(board, oppositeMove)


def NoOfFingers():
    wCam, hCam = 1, 5
    cap = cv2.VideoCapture(0)
    cap.set(1, wCam)
    cap.set(2, hCam)
    pTime = 0

    detector = HandDetector(detectionCon=0.70, maxHands=1)

    success, img = cap.read()
    hands, img = detector.findHands(img)
    vdo = cv2.imshow("Video", img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    return 0,0
    if len(hands) != 0:

        fingers = detector.fingersUp(hands[0])

        noOfFingers = fingers.count(1)
        print(noOfFingers)
        # print("From Function Called")
        return (noOfFingers, len(hands))
    return (0, 0)


if __name__ == '__main__':
    main()
