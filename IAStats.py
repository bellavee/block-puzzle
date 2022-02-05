import modules.grid as gd
import modules.player as player
import modules.pieces as pcs


nbOfParties = 100

pointsPerGame = []
roundsPerGame = []
lists = [pointsPerGame, roundsPerGame]

def updates(players, pieces, grid):
    pieces.update(players)
    for i in players:
        i.update(pieces)
    grid.isThereAlignment()
    players[0].points += len(grid.linesCompleted) * 100
    grid.eraseAlignment()


def test_IA():
    pieces = pcs.Pieces()
    grid = gd.Grid(10, pieces)
    grid.init()
    grid.definePhysicalLimits()
    print("x-- FIRST GRID STATE --x")
    grid.print()
    player1 = player.IA()
    players = [player1]
    currentRound = 1
    print("x--- NEW GAME STARTING ---x")

    currentDisplay = 'ingame'
    doContinue = True
    while doContinue:
        if currentDisplay == 'ingame':
            if currentRound % 10 == 0:
                print("x--- GRID STATE ---x")
                print("Current AI points:", player1.points)
                grid.print()
            updates(players, pieces, grid)
            choice = player1.determineWhatToPlay(grid)
            grid.putPiece(choice[1], choice[2], choice[3])
            player1.draw.remove(choice[3])
            player1.points += 30
            updates(players, pieces, grid)
            if not grid.isDrawPlaceable(player1) or choice[0] == 0:
                pointsPerGame.append(player1.points)
                roundsPerGame.append(currentRound)
                print("=========================")
                print("END OF GAME: AI earned", player1.points, "points")
                print("Nb of round:", currentRound)
                doContinue = False
        currentRound += 1

def stats(list):
    meanPoints = sum(list[0])/len(list[0])
    meanRounds = sum(list[1])/len(list[1])
    print("=========================")
    print("Durant les", nbOfParties, "parties jouées par l'IA:\nPoints par partie:", list[0], "\nMoyenne:", meanPoints,"\nMin:",min(lists[0]), "\nMax:",max(lists[0]))
    print("Round par partie", list[1], "\nMoyenne:", meanRounds, "\nMin:",min(lists[1]), "\nMax:",max(lists[1]))


if __name__ == '__main__':
    for i in range(nbOfParties):
        test_IA()
    stats(lists)

