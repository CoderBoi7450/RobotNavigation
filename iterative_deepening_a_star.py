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
                if self.getHeuristicValue(state) > threshold:
                    pruned_list.append(state)
                    continue

                self.expand(self.maze.getNextMoves(state), state)

            if success:
                self.displaySolution(state)
                break
            elif not pruned_list:
                print("No solution")
                break
            else:
                threshold = self.getHeuristicValue(pruned_list[0])
                for state in pruned_list:
                    if self.getHeuristicValue(state) <= threshold:
                        threshold = self.getHeuristicValue(state)

    def expand(self, moves, parent):

        parents = parent.parents.copy()
        parents.append(parent)

        for direction in moves.keys():
            if moves[direction] not in self.traversedLocation:
                self.frontier.append(State(moves[direction], parents, direction))

    def displaySolution(self, state):
        for parent in state.parents:
            print(parent.direction)
        print(state.direction)