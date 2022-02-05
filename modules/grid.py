import modules.logicalgate as lg


class Grid:
    """
    Grid object.
    """
    def __init__(self, size, Pieces):
        self.size = size + 2
        self.grid = []

        self.Pieces = Pieces

        self.linesCompleted = []

    def init(self):
        """
        init() method create the grid list.
        """
        for i in range(self.size):
            self.grid.append([])
            for j in range(self.size):
                self.grid[i].append(0)

    def print(self):
        """
        print() method prints the grid list on console.
        """
        for i in self.grid:
            print(i)

    def definePhysicalLimits(self):
        """
        definePhysicalLimits() method puts ones all around the grid list.
        """
        for i in range(self.size):
            self.grid[i][0] = 1
            self.grid[0][i] = 1
            self.grid[self.size - 1][i] = 1
            self.grid[i][self.size - 1] = 1

    def isPiecePlaceable(self, x, y, figure):
        """
        isPiecePlaceable() checks if a piece can be placed at specified coordinates in the grid.
        @param x: x coordinate
        @param y: y coordinate
        @param figure: figure number in pieces object
        @return: Boolean choose whether the piece can be placed or not.
        """
        x -= 2
        y -= 2
        err = 0
        for i in range(5):
            for j in range(5):
                try:
                    if not lg.nand(self.grid[x + i][y + j]//self.grid[x+i][y+j], int(self.Pieces.pieces[figure][i][j])):
                        err += 1
                except:
                    pass
        if err:
            return False
        else:
            return True

    def putPiece(self, x, y, Piece):
        """
        putPiece() method place the piece on the grid.
        @param x: x coordinate
        @param y: y coordinate
        @param Piece: Piece object.
        """
        x -= 2
        y -= 2
        for i in range(5):
            for j in range(5):
                try:
                    self.grid[x + i][y + j] += int(Piece.figure[i][j])
                except:
                    pass

    def isThereAlignment(self):
        """
        isThereAlignment() method checks if there is an alignment on the grid.
        """
        for i in range(self.size - 2):
            line = 0
            column = 0
            for j in range(self.size - 2):
                if self.grid[1 + i][1 + j]:
                    line += 1
                if self.grid[1 + j][1 + i]:
                    column += 1
            if line == self.size - 2:
                self.linesCompleted.append(['r', 1 + i])
            if column == self.size - 2:
                self.linesCompleted.append(['c', 1 + i])

    def eraseAlignment(self):
        """
        eraseAlignment() erase the alignments on the grid.
        """
        for i in self.linesCompleted:
            if i[0] == 'c':
                for j in range(self.size - 2):
                    self.grid[1 + j][i[1]] = 0
            if i[0] == 'r':
                for j in range(self.size - 2):
                    self.grid[i[1]][1 + j] = 0
            self.linesCompleted.remove(i)

    def isDrawPlaceable(self, Player):
        """
        isDrawPlaceable() checks if all the player's draw can be placed on the grid.
        @param Player: Player object
        @return: Boolean choose whether the player can play or not
        """
        err = 0
        for piece in Player.draw:
            for x in range(self.size - 2):
                for y in range(self.size - 2):
                    if not self.isPiecePlaceable(1 + x, 1 + y, piece.figureNumber):
                        err += 1
        if err == ((self.size - 2) ** 2) * len(Player.draw):
            return False
        else:
            return True
