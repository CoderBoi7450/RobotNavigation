from queue import Queue

from maze import Maze
from state import State


class DFS:
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.traversedLocation = []

    def search(self):
        initialState = State(location=self.maze.initialLocation, parents=[], direction="")
        self.frontier.append(initialState)
        self.traversedLocation = []
        success = False
        while self.frontier:
            state = self.frontier.pop()
            self.traversedLocation.append(state.location)
            if self.maze.isGoal(state.location):
                print("Solved")
                success = True
                break
            yield {"traversedList": self.traversedLocation, "success": False, "frontier": [state.location for state in self.frontier]}
            self.expand(self.maze.getNextMoves(state), state)

        if success:
            self.displaySolution(state)
            yield {"traversedList": self.traversedLocation, "success": True,
                   "paths": [parent.location for parent in state.parents]}
        else:
            print("No solution")
            yield {"traversedList": self.traversedLocation, "success": False}

    def expand(self, moves, parent):

        parents = parent.parents.copy()
        parents.append(parent)

        for direction in reversed(list(moves.keys())):
            if moves[direction] not in self.traversedLocation:
                self.frontier.append(State(moves[direction], parents, direction))

    def displaySolution(self, state):
        for parent in state.parents:
            print(parent.direction)
        print(state.direction)
