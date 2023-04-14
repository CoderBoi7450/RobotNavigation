from queue import Queue

from maze import Maze
from state import State


class BFS:
    def __init__(self, maze):
        self.maze = maze
        self.frontier = Queue()
        self.traversedLocation = []

    def search(self):
        initialState = State(location=self.maze.initialLocation, parents=[], direction="")
        self.frontier.put(initialState)
        self.traversedLocation = []
        success = False
        while not self.frontier.empty():
            print(self.traversedLocation)
            state = self.frontier.get()
            self.traversedLocation.append(state.location)
            if self.maze.isGoal(state.location):
                print("Solved")
                success = True
                break
            yield {"traversedList":self.traversedLocation, "frontier": [state.location for state in self.frontier.queue] , "success": False, "current": state.location}
            self.expand(self.maze.getNextMoves(state), state)

        if success:
            self.displaySolution(state)
            yield {"traversedList": self.traversedLocation, "success": True,
                   "paths": [parent.location for parent in state.parents]}
        else:
            print("No solution")
            yield {"traversedList": self.traversedLocation, "success": False,}

    def expand(self, moves, parent):

        parents = parent.parents.copy()
        parents.append(parent)

        for direction in moves:
            if moves[direction] == [1,0]:
                pass
            if moves[direction] not in self.traversedLocation and State(moves[direction]) not in self.frontier.queue:
                self.frontier.put(State(moves[direction], parents, direction))
            else:
                print("da co",moves[direction])

    def displaySolution(self, state):
        for parent in state.parents:
            print(parent.direction)
        print(state.direction)
        print(len(state.parents))
