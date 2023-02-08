from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

test_grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

def isValidCoord(coord: list, grid: list[list]) -> bool:
    gridLength = len(grid[0])
    gridHeight = len(grid)

    return (0 <= coord[0] < gridLength) and (0 <= coord[1] < gridHeight)

#####################################################
# Parameters:                                       #
# start_coord   - [x1,y1] (len(start_coord) == 2)   #
# end_coord     - [x2,y2] (len(end_coord) == 2)     #
# grid          - [[i1,i2,i3...],...]               #
#####################################################
def pathfinding(start_coord: list, end_coord: list, grid: list[list]) -> int:
    # Check if coordinates are valid
    if (not isValidCoord(start_coord, grid)) or (not isValidCoord(end_coord, grid)):
        return -1

    matrix = Grid(matrix=grid)
    start = matrix.node(start_coord[0], start_coord[1])
    end = matrix.node(end_coord[0], end_coord[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start,end,matrix)

    print(matrix.grid_str(path=path, start=start, end=end))
    return len(path)

print(pathfinding([1,0],[11,6],test_grid))