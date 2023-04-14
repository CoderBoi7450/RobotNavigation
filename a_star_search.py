
from state import State
import bisect


class ASS:
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.traversedLocation = []

    def getHeuristicValue(self, state):
        location = state.location
        values = [abs(location[0] - goal[0]) + abs(location[1] - goal[1]) for goal in self.maze.goals]
        return min(values) + len(state.parents)

    def search(self):
        initialState = State(location=self.maze.initialLocation, parents=[], direction="")
        self.frontier.append(initialState)

        self.traversedLocation = []
        success = False
        while self.frontier:
            # self.frontier.sort(reverse=True,key=self.getHeuristicValue)
            # print([self.getHeuristicValue(state) for state in self.frontier])
            state = self.frontier.pop(0)
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

        for direction in moves.keys():
            if moves[direction] not in self.traversedLocation and State(moves[direction]) not in self.frontier:
                bisect.insort_right(a=self.frontier, x=State(moves[direction], parents, direction),
                                    key=self.getHeuristicValue) #only works in python 3.11

    def displaySolution(self, state):
        for parent in state.parents:
            print(parent.direction)
        print(state.direction)
        print(len(state.parents))
