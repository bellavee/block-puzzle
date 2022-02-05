import pygame as pg
import random as rnd
import pickle
import modules.grid as gd
import modules.display as dsp
import modules.player as player
import modules.functions as fnc
import modules.pieces as pcs
import modules.network as ntw

SCREENHEIGHT = 700
SCREENWIDTH = 450
screensize = (SCREENWIDTH, SCREENHEIGHT)

boardX = 65
boardY = 65

# MENU RECTS

soloButtonRect = pg.Rect(150, 318, 150, 50)
multiButtonRect = pg.Rect(150, 383, 150, 50)
quitButtonRect = pg.Rect(150, 448, 150, 45)

returnButtonRect = pg.Rect(150, 448, 150, 45)
restartButtonRect = pg.Rect(150, 405, 150, 50)
returnMenuButtonRect = pg.Rect(340, 615, 85, 30)

multiLocalButtonRect = pg.Rect(50, 230, 330, 50)
multiIAButtonRect = pg.Rect(40, 180, 200, 50)
multiOnlineButtonRect = pg.Rect(40, 280, 330, 50)

pg.init()
pg.mixer.init()

soundMenu = pg.mixer.Sound("assets/menu.wav")
soundGameOver = pg.mixer.Sound("assets/gameover.wav")
soundButton = pg.mixer.Sound("assets/button.wav")
soundPlaceable = pg.mixer.Sound("assets/placeable.wav")

screen = pg.display.set_mode(screensize)
pg.display.set_caption("PyPuzzle")


def updates(players, pieces, grid):
    """
    updates() updates the different objects needed in solo mode.
    @param players: player objects list
    @param pieces: pieces object
    @param grid: grid object
    """
    pieces.update(players)
    for i in players:
        i.update(pieces)
        for j in i.draw:
            j.update(screen)
            j.drawPiece(screen)
    grid.isThereAlignment()
    players[0].points += len(grid.linesCompleted) * 100
    grid.eraseAlignment()


def updatesMultiLocal(pieces, players, grids, screen, currentPlayer):
    """
    updates() updates the different components of multilocal function.
    :param pieces: Pieces object
    :param players: Players objects list
    :param grids: Grids objects list
    :param screen: Current window to display game on
    :param currentPlayer: Number of current player
    """
    pieces.update(players)
    for player in players:
        player.update(pieces)
        for piece in player.draw:
            piece.update(screen)
            if player == players[currentPlayer % 2]:
                piece.drawPiece(screen)
    grids[currentPlayer % 2].isThereAlignment()
    players[currentPlayer % 2].points += len(grids[currentPlayer % 2].linesCompleted) * 100
    grids[currentPlayer % 2].eraseAlignment()


def menu():
    """
    menu() is the main menu function.
    """
    soundMenu.play(-1, 0, 0)
    doContinue = True
    while doContinue:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if soloButtonRect.collidepoint(event.pos):
                    soundMenu.stop()
                    soundButton.play()
                    solo()
                if multiButtonRect.collidepoint(event.pos):
                    soundButton.play()
                    multiMenu()
                if quitButtonRect.collidepoint(event.pos):
                    fnc.quitGame()

        dsp.displayMenu(screen)
        # HOVER
        pos = pg.mouse.get_pos()
        # SOLO
        if 150 + 150 > pos[0] > 150 and 318 + 45 > pos[1] > 318:
            pg.draw.rect(screen, dsp.YELLOW, (150, 318, 150, 45))
            screen.blit(dsp.soloText, (195, 320))
        else:
            pg.draw.rect(screen, dsp.CREAM, (150, 318, 150, 45))
            screen.blit(dsp.soloText, (195, 320))
        # MULTI
        if 150 + 150 > pos[0] > 150 and 383 + 45 > pos[1] > 383:
            pg.draw.rect(screen, dsp.YELLOW, (150, 383, 150, 45))
            screen.blit(dsp.multiText, (191, 384))
        else:
            pg.draw.rect(screen, dsp.GREEN, (150, 383, 150, 45))
            screen.blit(dsp.multiText, (191, 384))
        # QUIT
        if 150 + 150 > pos[0] > 150 and 448 + 45 > pos[1] > 448:
            pg.draw.rect(screen, dsp.YELLOW, (150, 448, 150, 45))
            screen.blit(dsp.quitText, (200, 448))
        else:
            pg.draw.rect(screen, dsp.REDPINK, (150, 448, 150, 45))
            screen.blit(dsp.quitText, (200, 448))
        pg.display.flip()


def multiMenu():
    """
    multiMenu() is the multiplayer menu function.
    """
    dsp.displayMulti(screen)
    doContinue = True
    while doContinue:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if returnButtonRect.collidepoint(event.pos):
                    soundMenu.stop()
                    soundButton.play()
                    menu()
                elif multiLocalButtonRect.collidepoint(event.pos):
                    soundMenu.stop()
                    soundButton.play()
                    multiLocal()
                elif multiIAButtonRect.collidepoint(event.pos):
                    soundMenu.stop()
                    soundButton.play()
                    multiIA()
                elif multiOnlineButtonRect.collidepoint(event.pos):
                    soundMenu.stop()
                    soundButton.play()
                    multiOnlineClient()
        # HOVER
        pos = pg.mouse.get_pos()
        if 150 + 150 > pos[0] > 150 and 448 + 45 > pos[1] > 448:
            pg.draw.rect(screen, dsp.YELLOW, (150, 448, 150, 45))
            screen.blit(dsp.returnText, (179, 448))
        else:
            pg.draw.rect(screen, dsp.REDPINK, (150, 448, 150, 45))
            screen.blit(dsp.returnText, (179, 448))
        if 40 + 160 > pos[0] > 40 and 180 + 35 > pos[1] > 180:
            screen.blit(dsp.iaTextHover, (40, 180))
        else:
            screen.blit(dsp.iaText, (40, 180))

        if 40 + 370 > pos[0] > 40 and 230 + 35 > pos[1] > 230:
            screen.blit(dsp.localTextHover, (40, 230))
        else:
            screen.blit(dsp.localText, (40, 230))

        if 40 + 385 > pos[0] > 40 and 280 + 35 > pos[1] > 280:
            screen.blit(dsp.onlineTextHover, (40, 280))
        else:
            screen.blit(dsp.onlineText, (40, 280))
        pg.display.flip()


def gameOverSolo(player1):
    """
    gameOverSolo() is the game over menu for solo mode.
    @param player1: player object
    """
    soundGameOver.play(-1, 0, 0)
    dsp.displayGameOverSolo(screen, player1)
    doContinue = True
    while doContinue:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if restartButtonRect.collidepoint(event.pos):
                    soundGameOver.stop()
                    soundButton.play()
                    menu()
                if quitButtonRect.collidepoint(event.pos):
                    fnc.quitGame()
        # HOVER
        pos = pg.mouse.get_pos()
        if 150 + 150 > pos[0] > 150 and 383 + 45 > pos[1] > 383:
            pg.draw.rect(screen, dsp.CREAM, (150, 383, 150, 45))
            screen.blit(dsp.restart, (174, 385))
        else:
            pg.draw.rect(screen, dsp.BACKGROUNDCOLOR, (150, 383, 150, 45))
            screen.blit(dsp.restart, (174, 385))

        if 150 + 150 > pos[0] > 150 and 448 + 45 > pos[1] > 448:
            pg.draw.rect(screen, dsp.CREAM, (150, 448, 150, 45))
            screen.blit(dsp.quitText1, (200, 448))
        else:
            pg.draw.rect(screen, dsp.YELLOW, (150, 448, 150, 45))
            screen.blit(dsp.quitText1, (200, 448))
        pg.display.flip()


def gameOverMulti(players):
    """
    gameOverMulti() is the game over menu for local multiplayer mode.
    @param players: player objects list
    """
    soundGameOver.play(-1, 0, 0)
    dsp.displayGameOverMulti(screen, players)
    doContinue = True
    while doContinue:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if restartButtonRect.collidepoint(event.pos):
                    soundGameOver.stop()
                    soundButton.play()
                    menu()
                if quitButtonRect.collidepoint(event.pos):
                    fnc.quitGame()
        # HOVER
        pos = pg.mouse.get_pos()
        if 150 + 150 > pos[0] > 150 and 383 + 45 > pos[1] > 383:
            pg.draw.rect(screen, dsp.CREAM, (150, 383, 150, 45))
            screen.blit(dsp.restart, (174, 385))
        else:
            pg.draw.rect(screen, dsp.BACKGROUNDCOLOR, (150, 383, 150, 45))
            screen.blit(dsp.restart, (174, 385))

        if 150 + 150 > pos[0] > 150 and 448 + 45 > pos[1] > 448:
            pg.draw.rect(screen, dsp.CREAM, (150, 448, 150, 45))
            screen.blit(dsp.quitText1, (200, 448))
        else:
            pg.draw.rect(screen, dsp.YELLOW, (150, 448, 150, 45))
            screen.blit(dsp.quitText1, (200, 448))
        pg.display.flip()


def solo():
    """
    solo() handles the solo mode of PyPuzzle.
    """
    pieces = pcs.Pieces()
    grid = gd.Grid(10, pieces)
    grid.init()
    grid.definePhysicalLimits()
    player1 = player.Player()
    players = [player1]

    currentDisplay = 'solo'
    currentlyDragging = False
    doContinue = True
    while doContinue:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if currentDisplay == 'solo':
                    for j in player1.draw:
                        if j.rect.collidepoint(event.pos) and not currentlyDragging:
                            currentlyDragging = True
                            j.dragged = True
                if returnMenuButtonRect.collidepoint(event.pos):
                    soundButton.play()
                    soundMenu.stop()
                    menu()

            elif event.type == pg.MOUSEBUTTONUP:
                if currentDisplay == 'solo':
                    if currentlyDragging:
                        for j in player1.draw:
                            if j.rect.collidepoint(event.pos):
                                currentlyDragging = False
                                j.dragged = False
                                if fnc.isOnGrid(event.pos):
                                    gridPos = ((event.pos[0] - boardX) / 32 + 1, (event.pos[1] - boardY) / 32 + 1)
                                    if grid.isPiecePlaceable(int(gridPos[0]), int(gridPos[1]), j.figureNumber):
                                        soundPlaceable.play()
                                        grid.putPiece(int(gridPos[0]), int(gridPos[1]), j)
                                        players[0].points += 30
                                        player1.draw.remove(j)

        if currentDisplay == 'solo':
            dsp.displayBoard(screen, (boardX, boardY), grid)
            updates(players, pieces, grid)
            dsp.displayDrawPieces(player1)
            dsp.displayTexts(screen, player1)
            if not grid.isDrawPlaceable(player1):
                gameOverSolo(player1)

        # HOVER
        pos = pg.mouse.get_pos()
        if 340 + 85 > pos[0] > 340 and 615 + 30 > pos[1] > 615:
            pg.draw.rect(screen, dsp.YELLOW, (340, 615, 85, 30))
            screen.blit(dsp.returnMenuText, (354, 617))
        else:
            pg.draw.rect(screen, dsp.GRAY, (340, 615, 85, 30))
            screen.blit(dsp.returnMenuText1, (354, 617))
        pg.display.flip()


def multiLocal():
    """
    multiLocal() handles the local multiplayer: player versus player. Both players's board are displayed one after
    the other on a 650x440 wide window. Creates a new window.
    """
    players = []
    grids = []
    pieces = pcs.Pieces()

    currentDisplay = 'game'

    for i in range(2):
        players.append(player.Player(i))
        grids.append(gd.Grid(10, pieces))
        grids[i].init()
        grids[i].definePhysicalLimits()

    currentPlayer = rnd.randint(0, 1)
    currentlyDragging = False

    stop = False
    while not stop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                for piece in players[currentPlayer % 2].draw:
                    if piece.rect.collidepoint(event.pos) and not currentlyDragging:
                        currentlyDragging = True
                        piece.dragged = True

            elif event.type == pg.MOUSEBUTTONUP:
                if currentDisplay == 'game':
                    if currentlyDragging:
                        for piece in players[currentPlayer % 2].draw:
                            if piece.rect.collidepoint(event.pos):
                                currentlyDragging = False
                                piece.dragged = False
                                if fnc.isOnGrid(event.pos):
                                    gridPos = ((event.pos[0] - boardX) / 32 + 1, (event.pos[1] - boardY) / 32 + 1)
                                    if grids[currentPlayer % 2].isPiecePlaceable(int(gridPos[0]), int(gridPos[1]),
                                                                                 piece.figureNumber):
                                        grids[currentPlayer % 2].putPiece(int(gridPos[0]), int(gridPos[1]), piece)
                                        players[currentPlayer % 2].draw.remove(piece)
                                        players[currentPlayer % 2].points += 30
                                        currentPlayer += 1
                                        soundPlaceable.play()
                    if returnMenuButtonRect.collidepoint(event.pos):
                        menu()
                elif currentDisplay == 'gameover':
                    if restartButtonRect.collidepoint(event.pos):
                        quit()
                        menu()
                    elif quitButtonRect.collidepoint(event.pos):
                        pg.display.quit()
                        quit()

        # INSTRUCTIONS OF LOOP ===
        if currentDisplay == 'game':
            dsp.displayBoard(screen, (boardX, boardY), grids[currentPlayer % 2])
            updatesMultiLocal(pieces, players, grids, screen, currentPlayer)
            dsp.displayDrawPieces(players[currentPlayer % 2])
            dsp.displayTexts(screen, players[currentPlayer % 2])
            if not grids[currentPlayer % 2].isDrawPlaceable(players[currentPlayer % 2]):
                currentDisplay = 'gameover'
        elif currentDisplay == 'gameover':
            gameOverMulti(players)

            # HOVER
        pos = pg.mouse.get_pos()
        if 340 + 85 > pos[0] > 340 and 615 + 30 > pos[1] > 615:
            pg.draw.rect(screen, dsp.YELLOW, (340, 615, 85, 30))
            screen.blit(dsp.returnMenuText, (354, 617))
        else:
            pg.draw.rect(screen, dsp.GRAY, (340, 615, 85, 30))
            screen.blit(dsp.returnMenuText1, (354, 617))
        pg.display.flip()


def multiIA():
    """
    multiIA() handles the local multiplayer: player versus AI. Both players's board are displayed one after
    the other.
    """
    players = [player.Player(), player.IA()]
    grids = []
    pieces = pcs.Pieces()

    for i in range(2):
        grids.append(gd.Grid(10, pieces))
        grids[i].init()
        grids[i].definePhysicalLimits()

    currentDisplay = 'game'

    currentPlayer = rnd.randint(0, 1)
    currentlyDragging = False

    stop = False
    while not stop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fnc.quitGame()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                for piece in players[currentPlayer % 2].draw:
                    if piece.rect.collidepoint(event.pos) and not currentlyDragging:
                        currentlyDragging = True
                        piece.dragged = True

            elif event.type == pg.MOUSEBUTTONUP:
                if currentDisplay == 'game':
                    if currentlyDragging:
                        for piece in players[currentPlayer % 2].draw:
                            if piece.rect.collidepoint(event.pos):
                                currentlyDragging = False
                                piece.dragged = False
                                if fnc.isOnGrid(event.pos):
                                    gridPos = ((event.pos[0] - boardX) / 32 + 1, (event.pos[1] - boardY) / 32 + 1)
                                    if grids[currentPlayer % 2].isPiecePlaceable(int(gridPos[0]), int(gridPos[1]),
                                                                                 piece.figureNumber):
                                        grids[currentPlayer % 2].putPiece(int(gridPos[0]), int(gridPos[1]), piece)
                                        players[currentPlayer % 2].draw.remove(piece)
                                        players[currentPlayer % 2].points += 30
                                        currentPlayer += 1
                                        soundPlaceable.play()
                    if returnMenuButtonRect.collidepoint(event.pos):
                        menu()
                elif currentDisplay == 'gameover':
                    if restartButtonRect.collidepoint(event.pos):
                        quit()
                        menu()
                    elif quitButtonRect.collidepoint(event.pos):
                        pg.display.quit()
                        quit()

        # INSTRUCTIONS OF LOOP ===
        if currentDisplay == 'game':
            dsp.displayBoard(screen, (boardX, boardY), grids[currentPlayer % 2])
            updatesMultiLocal(pieces, players, grids, screen, currentPlayer)
            dsp.displayDrawPieces(players[currentPlayer % 2])
            dsp.displayTextsIA(screen, players)
            if currentPlayer % 2:
                choice = players[1].determineWhatToPlay(grids[1])
                print("Choix IA:", choice)
                if choice[0] == 0:
                    currentDisplay == "gameover"
                else:
                    grids[1].putPiece(choice[1], choice[2], choice[3])
                    grids[1].print()
                    players[1].draw.remove(choice[3])
                    players[1].points += 30
                    currentPlayer += 1

            if not grids[currentPlayer % 2].isDrawPlaceable(players[currentPlayer % 2]):
                currentDisplay = 'gameover'

        elif currentDisplay == 'gameover':
            gameOverMulti(players)

        # HOVER
        pos = pg.mouse.get_pos()
        if 340 + 85 > pos[0] > 340 and 615 + 30 > pos[1] > 615:
            pg.draw.rect(screen, dsp.YELLOW, (340, 615, 85, 30))
            screen.blit(dsp.returnMenuText, (354, 617))
        else:
            pg.draw.rect(screen, dsp.GRAY, (340, 615, 85, 30))
            screen.blit(dsp.returnMenuText1, (354, 617))
        pg.display.flip()


def multiOnlineClient():
    """
        multiOnlineClient() handles the online multiplayer: player versus player. Both players's board are only
        displayed on their screen, only the opponent's score is displayed.
    """
    network = ntw.Network()
    try:
        network.connect()
    except:
        menu()
    cPlayer = pickle.loads(network.send("get-player"))
    oPlayer = 0 if cPlayer else 1

    pieces = pcs.Pieces()
    grid = gd.Grid(10, pieces)
    grid.init()
    grid.definePhysicalLimits()
    gamePlayer = player.Player()
    players = [gamePlayer]

    currentDisplay = "wait"
    currentGameState = "waiting"
    currentlyDragging = False
    doContinue = True
    savedpoints = 0
    playing = 1

    while doContinue:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                network.send("quit")
                fnc.quitGame()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if currentDisplay == 'game':
                    for j in gamePlayer.draw:
                        if j.rect.collidepoint(event.pos) and not currentlyDragging:
                            currentlyDragging = True
                            j.dragged = True
                if returnMenuButtonRect.collidepoint(event.pos):
                    soundButton.play()
                    soundMenu.stop()
                    network.send("quit")
                    menu()
            elif event.type == pg.MOUSEBUTTONUP:
                if currentDisplay == 'game':
                    if currentlyDragging:
                        for j in gamePlayer.draw:
                            if j.rect.collidepoint(event.pos):
                                currentlyDragging = False
                                j.dragged = False
                                if fnc.isOnGrid(event.pos):
                                    gridPos = ((event.pos[0] - boardX) / 32 + 1, (event.pos[1] - boardY) / 32 + 1)
                                    if grid.isPiecePlaceable(int(gridPos[0]), int(gridPos[1]), j.figureNumber):
                                        soundPlaceable.play()
                                        grid.putPiece(int(gridPos[0]), int(gridPos[1]), j)
                                        players[0].points += 30
                                        gamePlayer.draw.remove(j)
                                        network.send("set-points:" + str(gamePlayer.points))
                elif currentDisplay == 'gameover':
                    if restartButtonRect.collidepoint(event.pos):
                        soundButton.play()
                        network.send("quit")
                        menu()
                    elif quitButtonRect.collidepoint(event.pos):
                        network.send("quit")
                        fnc.quitGame()

        try:
            currentGameState = network.send("get-state").decode()
        except:
            currentGameState = "quit"
        if currentGameState == "waiting":
            currentDisplay = "wait"
        elif currentGameState == "quit":
            menu()
        elif currentGameState == "gameover" and not playing:
            currentDisplay = "gameover"
        elif currentGameState == "running":
            currentDisplay = 'game'
        if currentDisplay == "wait":
            dsp.displayWaitPlayers(screen)
        elif currentDisplay == "game":
            dsp.displayBoard(screen, (boardX, boardY), grid)
            updates(players, pieces, grid)
            dsp.displayDrawPieces(gamePlayer)
            try:
                otherPlayerPoints = pickle.loads(network.send("get-points"))[oPlayer]
            except:
                otherPlayerPoints = 0
            dsp.displayTextsOnline(screen, gamePlayer, otherPlayerPoints)
            if not grid.isDrawPlaceable(gamePlayer):
                playing = 0
                try:
                    points = pickle.loads(network.send("go"))
                    saved_points = points
                except:
                    points = saved_points
                dsp.displayGameOverMultiOnline(screen, points, cPlayer)

        # HOVER
        pos = pg.mouse.get_pos()
        if currentDisplay == "game" or currentDisplay == "wait":
            if 340 + 85 > pos[0] > 340 and 615 + 30 > pos[1] > 615:
                pg.draw.rect(screen, dsp.YELLOW, (340, 615, 85, 30))
                screen.blit(dsp.returnMenuText, (354, 617))
            else:
                pg.draw.rect(screen, dsp.GRAY, (340, 615, 85, 30))
                screen.blit(dsp.returnMenuText1, (354, 617))
        if currentDisplay == "gameover":
            if 150 + 150 > pos[0] > 150 and 383 + 45 > pos[1] > 383:
                pg.draw.rect(screen, dsp.CREAM, (150, 383, 150, 45))
                screen.blit(dsp.restart, (174, 385))
            else:
                pg.draw.rect(screen, dsp.BACKGROUNDCOLOR, (150, 383, 150, 45))
                screen.blit(dsp.restart, (174, 385))

            if 150 + 150 > pos[0] > 150 and 448 + 45 > pos[1] > 448:
                pg.draw.rect(screen, dsp.CREAM, (150, 448, 150, 45))
                screen.blit(dsp.quitText1, (200, 448))
            else:
                pg.draw.rect(screen, dsp.YELLOW, (150, 448, 150, 45))
                screen.blit(dsp.quitText1, (200, 448))

        pg.display.flip()


if __name__ == '__main__':
    menu()
