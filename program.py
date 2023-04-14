from wall import Wall
from maze import Maze
from bfs import BFS
from dfs import DFS
from greedy_best_search import GBS
from a_star_search import ASS
from bidirectional_search import BDS
from iterative_deepening_a_star import IDA
class Program:
    def __init__(self,algorithm):
        self.algorithm = algorithm
    def readMaze(self,filename):
        file = open(filename,'r')
        mazeSize = file.readline().strip('][ \n').split(',') 
        mazeSize = [int(i) for i in mazeSize]   # convert string to integer
        initialLocation = [int(i) for i in file.readline().strip('() \n').split(',')]
        goalStates = file.readline().strip().split(' | ')
        goalStates = [state.strip(') (').split(',') for state in goalStates]
        goalStates = [[int(x) for x in state] for state in goalStates]
        walls = []
        for line in file.readlines():
            if not line.isspace():
                newWall = [int(i) for i in line.strip('() \n').split(',')]
                walls.append(Wall(*newWall))
        
        print(f"Maze size: {mazeSize}")
        print(f"Initial Location: {initialLocation}")
        print(f"Goal states: {goalStates}")
        for wall in walls:
            print(wall)
        return {"size":mazeSize,"initial":initialLocation, "goals":goalStates,"walls":walls}

    def solve(self,filename):
        mazeInfo = self.readMaze(filename)
        maze = Maze(*mazeInfo.values()) # maze or self.maze
        if self.algorithm == "bfs":
            search_algorithm = BFS(maze)
        elif self.algorithm == "dfs":
            search_algorithm = DFS(maze)
        elif self.algorithm == "gbfs":
            search_algorithm = GBS(maze)
        elif self.algorithm == "ass":
            search_algorithm = ASS(maze)
        elif self.algorithm == "bds":
            search_algorithm = BDS(maze)
        elif self.algorithm == "ida":
            search_algorithm = IDA(maze)
        result = search_algorithm.search()

        for _ in result:
            yield _


if __name__ == "__main__":
    program = Program()
    for x in program.solve("maze.txt"):
        pass
