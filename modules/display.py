import pygame as pg

piecescolors = (
    (0, 0, 0),  # PREVENT A BUG
    (255, 241, 171),  # PASTEL YELLOW
    (255, 196, 196),  # PASTEL RED
    (161, 255, 170),  # PASTEL GREEN
    (186, 238, 255),  # PASTEL BLUE
    (166, 255, 236),  # GREEN MINT
    (240, 247, 244),  # CREAM
    (255, 214, 239)  # PASTEL PINK
)

BACKGROUNDCOLOR = (125, 201, 255)
BOARDCOLOR = (77, 164, 227)
CREAM = (240, 247, 244)
REDPINK = (255, 143, 137)
GREEN = (141, 232, 150)
NAVY = (7, 51, 92)
YELLOW = (255, 207, 74)
GRAY = (41, 41, 41)
RED = (219, 109, 103)
PINK = (255, 214, 239)
BLUE = (85, 169, 237)
LIGHTBLUE = (186, 233, 255)

margin = 2

pg.font.init()
font = pg.font.Font('assets/BebasNeue-Regular.ttf', 25)
bigFont = pg.font.Font('assets/BebasNeue-Regular.ttf', 100)
bigMediumFont = pg.font.Font('assets/BebasNeue-Regular.ttf', 60)
mediumFont = pg.font.Font('assets/BebasNeue-Regular.ttf', 40)
smallFont = pg.font.Font('assets/BebasNeue-Regular.ttf', 25)

gameover = bigFont.render("YOUR SCORE", True, GRAY)
gameoverShadow = bigFont.render("YOUR SCORE", True, RED)
gameoverM = bigFont.render("YOUR SCORES", True, GRAY)
gameoverShadowM = bigFont.render("YOUR SCORES", True, RED)
J1 = font.render("Player 1 : ", True, GRAY)
J2 = font.render("Player 2 : ", True, GRAY)
J1b = font.render("You : ", True, GRAY)
J2b = font.render("Opponent : ", True, GRAY)
Winner = mediumFont.render("Winner: ", True, GRAY)
VJ1 = mediumFont.render("Player 1 ", True, GRAY)
VJ2 = mediumFont.render("Player 2 ", True, GRAY)
VYou = mediumFont.render("You", True, GRAY)
VOpp = mediumFont.render("Opponent", True, GRAY)
restart = mediumFont.render("Restart", True, GRAY)

quitText1 = mediumFont.render("Quit", True, GRAY)
pypuzzle = bigFont.render("PyPuzzle", True, NAVY)

pypuzzleShadow = bigFont.render("PyPuzzle", True, BOARDCOLOR)

multiplayerText = bigMediumFont.render("MULTIPLAYER", True, NAVY)
iaText = mediumFont.render("PLAYER vs IA", True, NAVY)
localText = mediumFont.render("PLAYER 1 vs PLAYER 2 (LOCAL)", True, NAVY)
onlineText = mediumFont.render("PLAYER 1 vs PLAYER 2 (ONLINE)", True, NAVY)

iaTextHover = mediumFont.render("PLAYER vs IA", True, RED)
localTextHover = mediumFont.render("PLAYER 1 vs PLAYER 2 (LOCAL)", True, RED)
onlineTextHover = mediumFont.render("PLAYER 1 vs PLAYER 2 (ONLINE)", True, RED)
returnText = font.render("RETURN", True, NAVY)
multiplayerTextShadow = bigMediumFont.render("MULTIPLAYER", True, BOARDCOLOR)

wait = mediumFont.render("Waiting for another player..", True, NAVY)

soloText = mediumFont.render("SOLO", True, NAVY)
multiText = mediumFont.render("MULTI", True, NAVY)
quitText = mediumFont.render("QUIT", True, NAVY)
returnText = mediumFont.render("RETURN", True, NAVY)
quitText1 = mediumFont.render("Quit", True, GRAY)
restart = mediumFont.render("Restart", True, GRAY)
returnMenuText = smallFont.render("RETURN", True, NAVY)
returnMenuText1 = smallFont.render("RETURN", True, CREAM)


def displayMenu(win):
    """
    displayMenu() displays the main menu interface.
    @param win: Pygame window Surface.
    """
    win.fill(BACKGROUNDCOLOR)
    pg.draw.rect(win, BOARDCOLOR, (155, 323, 150, 45))
    pg.draw.rect(win, BOARDCOLOR, (155, 388, 150, 45))
    pg.draw.rect(win, BOARDCOLOR, (155, 453, 150, 45))

    win.blit(pypuzzleShadow, (82, 170))
    win.blit(pypuzzle, (78, 165))

    pg.draw.rect(win, LIGHTBLUE, (0, 610, 450, 30))
    pg.draw.rect(win, BLUE, (0, 640, 450, 30))
    pg.draw.rect(win, NAVY, (0, 670, 450, 30))


def displayMulti(win):
    """
    displayMulti() displays the multiplayer menu interface.
    @param win: Pygame window Surface.
    """
    win.fill(BACKGROUNDCOLOR)
    win.blit(multiplayerTextShadow, (103, 73))
    win.blit(multiplayerText, (100, 70))
    pg.draw.rect(win, BOARDCOLOR, (155, 453, 150, 45))

    pg.draw.rect(win, LIGHTBLUE, (0, 610, 450, 30))
    pg.draw.rect(win, BLUE, (0, 640, 450, 30))
    pg.draw.rect(win, NAVY, (0, 670, 450, 30))


def displayBoard(win, blitCoord, grid):
    """
    displayBoard() displays the game board.
    @param win: Pygame window Surface.
    @param blitCoord: Coordinates where the game board is displayed
    @param grid: Grid Object
    """
    boxWidth = 30
    win.fill(BACKGROUNDCOLOR)
    for i in range(0, grid.size - 2):
        for j in range(0, grid.size - 2):
            cell = grid.grid[1 + i][1 + j]
            if cell != 0:
                pg.draw.rect(win, piecescolors[cell % 8], (
                    blitCoord[0] + (margin + boxWidth) * i + margin, blitCoord[1] + (margin + boxWidth) * j + margin,
                    boxWidth, boxWidth))

            else:
                pg.draw.rect(win, BOARDCOLOR, (
                    blitCoord[0] + (margin + boxWidth) * i + margin, blitCoord[1] + (margin + boxWidth) * j + margin,
                    boxWidth, boxWidth))

    pg.draw.rect(win, NAVY, (0, 670, 450, 30))
    pg.draw.rect(win, BOARDCOLOR, (345, 620, 85, 30))


def displayDrawPieces(Player):
    """
    displayDrawPieces() define the coordinates of draw's pieces.
    @param Player: Player object
    """
    j = 0
    for i in Player.draw:
        if not i.dragged:
            i.x = j
            i.y = 400
            j += 140


def displayTexts(win, Player):
    """
    displayTexts() displays the interface's texts: score and current player. Used in solo and local multiplayer.
    @param win: Pygame window Surface.
    @param Player: Player object.
    """
    score = font.render("Score: " + str(Player.points), True, NAVY)
    win.blit(score, (20, 20))
    currentPlayer = font.render("Current player: " + str(Player.id + 1), True, NAVY)
    win.blit(currentPlayer, (280, 20))


def displayTextsIA(win, Players):
    """
    displayTextsIA() displays the interface's texts: score of both player and IA.
    @param win: Pygame window Surface.
    @param Players: Player Object.
    """
    score = font.render("Score: " + str(Players[0].points), True, NAVY)
    score1 = font.render("Score IA: " + str(Players[1].points), True, NAVY)
    win.blit(score, (20, 20))
    win.blit(score1, (320, 20))


def displayTextsOnline(win, Player, points):
    """
    displayTextsOnline() displays the interface's texts: score of both player and opponent.
    @param win: Pygame window Surface.
    @param Player: Player Object.
    @param points: List of both players's points.
    """
    score = font.render("Score: " + str(Player.points), True, NAVY)
    win.blit(score, (20, 20))
    currentPlayer = font.render("Opponent's score: " + str(points), True, NAVY)
    win.blit(currentPlayer, (245, 20))


def displayGameOverSolo(win, Player):
    """
    displayGameOverSolo() displays the solo game mode's game over menu.
    @param win: Pygame window Surface.
    @param Player: Player Object.
    """
    win.fill(REDPINK)
    score = bigMediumFont.render(str(Player.points), True, GRAY)
    win.blit(score, (180, 288))
    win.blit(gameoverShadow, (45, 170))
    win.blit(gameover, (40, 165))

    pg.draw.rect(win, RED, (155, 388, 150, 45))
    pg.draw.rect(win, RED, (155, 453, 150, 45))


def displayGameOverMulti(win, Players):
    """
    displayGameOverMulti() displays the local multiplayer game mode's game over menu.
    @param win: Pygame window Surface.
    @param Players: Player objects list.
    """
    win.fill(REDPINK)

    score1 = font.render(str(Players[0].points), True, GRAY)
    win.blit(score1, (160, 253))
    win.blit(gameoverShadowM, (35, 135))
    win.blit(gameoverM, (30, 130))

    win.blit(J1, (75, 253))
    win.blit(J2, (270, 253))
    score2 = font.render(str(Players[1].points), True, GRAY)
    win.blit(score2, (355, 253))

    win.blit(Winner, (110, 310))
    if Players[0].points > Players[1].points:
        win.blit(VJ1, (230, 310))
    else:
        win.blit(VJ2, (230, 310))

    pg.draw.rect(win, RED, (155, 388, 150, 45))
    pg.draw.rect(win, RED, (155, 453, 150, 45))


def displayGameOverMultiOnline(win, points, player):
    """
    displayGameOverMultiOnline() displays the online multiplayer game mode's game over menu.
    @param win: Pygame window Surface.
    @param points: List of both players's points.
    @param player: Number of the client player.
    """
    thisPlayer = player
    otherPlayer = 0 if player else 1
    win.fill(REDPINK)
    score1 = font.render(str(points[thisPlayer]), True, GRAY)
    win.blit(score1, (120, 253))
    win.blit(gameoverShadowM, (35, 135))
    win.blit(gameoverM, (30, 130))
    win.blit(J1b, (75, 253))
    win.blit(J2b, (270, 253))
    score2 = font.render(str(points[otherPlayer]), True, GRAY)
    win.blit(score2, (365, 253))
    win.blit(Winner, (110, 310))
    if points[thisPlayer] > points[otherPlayer]:
        win.blit(VYou, (230, 310))
    else:
        win.blit(VOpp, (230, 310))

    pg.draw.rect(win, RED, (155, 388, 150, 45))
    pg.draw.rect(win, RED, (155, 453, 150, 45))


def displayWaitPlayers(win):
    """
    displayWaitPlayers() displays the "waiting for other player" screen.
    @param win: Pygame window Surface.
    """
    win.fill(BACKGROUNDCOLOR)
    win.blit(wait, (30, 300))
