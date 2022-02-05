import pygame as pg


def isOnGrid(pos):
    """
	isOnGrid() function check if mouse postion is on the grid or not
    @param pos: Mouse position
    @return: Boolean choose whether the mouse is on the grid or not
    """
    if 65 < pos[0] < 385 and 65 < pos[1] < 385:
        return True
    else:
        return False


def quitGame():
    """
	quitGame() quits the game.
    """
    pg.display.quit()
    quit()


def maxWeight(list):
    """
	maxWeight() determine the best choice for the AI among different moves.
    @param list: List of moves
    @return: The best move among the list
    """
    max = list[0]
    maxIndex = (0, 0)
    for i in range(len(list)):
        for j in range(1, len(list[i])):
            if list[i][j][0] > max[0][0]:
                max = list[i]
                maxIndex = (i, j)
    return (maxIndex)
