from state import State
import bisect
class IDA:
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.traversedLocation = []

    def getHeuristicValue(self, state):
        location = state.location
        values = [abs(location[0] - goal[0]) + abs(location[1] - goal[1]) for goal in self.maze.goals]
        return min(values) + len(state.parents)

    def search(self):
        success = False
        threshold = None
        while True:
            pruned_list = []
            initialState = State(location=self.maze.initialLocation, parents=[], direction="")
            self.frontier.append(initialState)
            if threshold is None:
                threshold = self.getHeuristicValue(initialState)
            print(threshold)
            self.traversedLocation = []
            while self.frontier:
                state = self.frontier.pop(0)
                self.traversedLocation.append(state.location)
                if self.maze.isGoal(state.location):
                    print("Solved")
                    success = True
                    break
                yield {"traversedList": self.traversedLocation, "success": False, "frontier": [state.location for state in self.frontier], "current":state.location}
                if self.getHeuristicValue(state) > threshold:
                    pruned_list.append(state)
                    continue
                self.expand(self.maze.getNextMoves(state), state)

            if success:
                self.displaySolution(state)
                yield {"traversedList": self.traversedLocation, "success": True, "paths": [parent.location for parent in state.parents]}
                break
            elif not pruned_list:
                print("No solution")
                yield {"traversedList": self.traversedLocation, "success": False}
                break
            else:
                threshold = self.getHeuristicValue(pruned_list[0])
                for state in pruned_list:
                    if self.getHeuristicValue(state) <= threshold:
                        threshold = self.getHeuristicValue(state)

    def expand(self, moves, parent):

        parents = parent.parents.copy()
        parents.append(parent)

        for direction in reversed(list(moves.keys())): #reversed or not
            if moves[direction] not in self.traversedLocation and State(moves[direction]) not in self.frontier: # co nen check trong self.frontier k
                self.frontier.append(State(moves[direction], parents, direction))

    def displaySolution(self, state):
        for parent in state.parents:
            print(parent.direction)
        print(state.direction)