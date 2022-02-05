import copy as cp
import modules.functions as fnc


class Player:
    """
    Player object
    """
    def __init__(self, id=0):
        self.id = id
        self.points = 0
        self.draw = []

    def update(self, pieces):
        """
        Check if the draw is empty.
        @param pieces:
        """
        if len(self.draw) == 0:
            for i in range(3):
                self.draw.append(pieces.histories[self.id][0])
                pieces.histories[self.id].remove(pieces.histories[self.id][0])


class IA(Player):
    """
	IA Object
    """

    def __init__(self):
        Player.__init__(self)
        self.id = 1

    def determineWhatToPlay(self, grid):
        """
		Return the most accurate piece placement on grid
		:param grid: Game grid object
		:return: Array with most accurate position to place and the figure
		"""
        drawLength = len(self.draw)
        weight = [[[0, 0, 0, 0] for j in range(100)] for i in range(drawLength)]
        for piece in range(drawLength):
            cpt = 0
            for i in range(grid.size - 2):
                for j in range(grid.size - 2):
                    ghostGrid = cp.deepcopy(grid)

                    weight[piece][cpt][1] = i
                    weight[piece][cpt][2] = j
                    weight[piece][cpt][3] = self.draw[piece]

                    if ghostGrid.isPiecePlaceable(i, j, self.draw[piece].figureNumber):
                        weight[piece][cpt][0] += 1
                        ghostGrid.putPiece(i + 1, j + 1, self.draw[piece])
                        ghostGrid.isThereAlignment()
                        weight[piece][cpt][0] += len(ghostGrid.linesCompleted)
                    cpt += 1
        choice = fnc.maxWeight(weight)
        return weight[choice[0]][choice[1]]
