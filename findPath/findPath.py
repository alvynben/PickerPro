import sys
from typing import List
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

def isValidCoord(coord: List, grid: List[List]) -> bool:
    gridLength = len(grid[0])
    gridHeight = len(grid)

    return (0 <= coord[0] < gridLength) and (0 <= coord[1] < gridHeight)

#####################################################
# Parameters:                                       #
# start_coord   - [x1,y1] (len(start_coord) == 2)   #
# end_coord     - [x2,y2] (len(end_coord) == 2)     #
# grid          - [[i1,i2,i3...],...]               #
# Returns:                                          #
# Shortest distance between start_coord and         #
# end_coord                                         #
#####################################################
def shortestDist(start_coord: List, end_coord: List, grid: List[List]) -> int:
    # Check if coordinates are valid
    if (not isValidCoord(start_coord, grid)) or (not isValidCoord(end_coord, grid)):
        return -1

    matrix = Grid(matrix=grid)
    start = matrix.node(start_coord[0], start_coord[1])
    end = matrix.node(end_coord[0], end_coord[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start,end,matrix)

    # print(matrix.grid_str(path=path, start=start, end=end))
    return len(path)

#####################################################
# Parameters:                                       #
# points   - [[Xs, Ys], [Xp1, Yp1], [Xp2, Yp2],...] #
#            <Xs, Ys> refers to the starting point  #
#            <Xpi, Ypi> refers to all other points  #  
# grid     - [[i1,i2,i3...],...]                    #
# Returns:                                          #
# Order of points which results in shortest path    #
#####################################################
def findPath(points: List[List], grid: List[List]) -> List[List]:
    # Add starting point
    order = [points[0]]
    points.pop(0)

    minVal = sys.maxsize
    minInd = -1
    while points:
        # Find next nearest point
        for i in range(len(points)):
            # Compare latest point with points[i]
            dist = shortestDist(order[-1], points[i], grid)
            if dist <= minVal:
                minVal = dist
                minInd = i
        # Add shortest point to order and remove from points
        order.append(points.pop(minInd))
        minVal = sys.maxsize
    
    return order



print(findPath([[1,0], [2,14], [18,9], [11,6], [6,11]],test_grid))