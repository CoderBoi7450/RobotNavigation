from wall import Wall
from maze import Maze
from bfs import BFS
from dfs import DFS
from greedy_best_search import GBS
from a_star_search import ASS
class Program:

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
        # bfs = BFS(maze)
        # bfs.search()
        #
        # dfs = DFS(maze)
        # dfs.search()
        #
        gbs = GBS(maze)
        gbs.search()
        


if __name__ == "__main__":
    program = Program()
    program.solve("maze.txt")