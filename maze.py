class Maze:
    def __init__(self, size, initialLocation, goals, walls):
        self.row = size[0]
        self.column = size[1]
        self.initialLocation = initialLocation
        self.goals = goals
        self.walls = walls

    def isGoal(self, location):
        return location in self.goals

    def isWall(self, location):
        result = False
        for wall in self.walls:
            if wall.x <= location[0] < wall.x + wall.width and wall.y <= location[1] < wall.y + wall.height:
                result = True
                break
        return result

    def getNextMoves(self, state):
        moves = {}
        up = [state.location[0], state.location[1] - 1]
        if up[1] >= 0 and not self.isWall(up):
            moves["up"] = up

        left = [state.location[0] - 1, state.location[1]]
        if left[0] >= 0 and not self.isWall(left):
            moves["left"] = left

        down = [state.location[0], state.location[1] + 1]
        if down[1] < self.row and not self.isWall(down):
            moves["down"] = down

        right = [state.location[0] + 1, state.location[1]]
        if right[0] < self.column and not self.isWall(right):
            moves["right"] = right

        return moves





    # def getHeuristicValue(self,location):
    #     return abs(location.x - )


if (__name__ == "__main__"):
    from wall import Wall

    maze = Maze([5, 11], 0, 0, 0)
    maze.walls = [Wall(2, 0, 2, 2), Wall(8, 0, 1, 2), Wall(10, 0, 1, 1), Wall(2, 3, 1, 2), Wall(3, 4, 3, 1),
                  Wall(9, 3, 1, 1), Wall(8, 4, 2, 1)]
    for i in range(maze.row):
        for j in range(maze.column):
            print(j, i, end=" ")
            print(maze.isWall([j, i]), end=", ")
        print("\n")
