from queue import Queue

from state import State

class BDS:
    def __init__(self, maze):
        self.maze = maze
        self.src_frontier = Queue()
        self.des_frontier = Queue()

        self.src_visited = []
        self.des_visited = []

    def check_intersect(self):
        for state in self.src_visited:
            if state in self.des_visited:
                return state.location
        return -1

    def reflect_des_direction(self,direction):
        if direction == "right":
            return "left"
        elif direction == "left":
            return "right"
        elif direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        else:
            return ""

    def get_path(self,intersecting_location):
        for state in self.src_visited:
            if intersecting_location == state.location:
                src_state = state
        for state in self.des_visited:
            if intersecting_location == state.location:
                des_state = state;
        path = []
        for parent in src_state.parents:
            path.append(parent.location)
        path.append(intersecting_location)
        for parent in des_state.parents:
            path.append(parent.location)
        return path

    def displaySolution(self, intersecting_location):
        src_state = None
        for state in self.src_visited:
            if intersecting_location == state.location:
                src_state = state
        for parent in src_state.parents:
            print(parent.direction)
        print(src_state.direction)

        des_state = None
        for state in self.des_visited:
            if intersecting_location == state.location:
                des_state = state
        print(self.reflect_des_direction(des_state.direction))
        for parent in reversed(des_state.parents):
            print(self.reflect_des_direction(parent.direction))


    def search(self):
        initialState = State(location=self.maze.initialLocation, parents=[], direction="")
        self.src_frontier.put(initialState)
        goalState = State(location=self.maze.goals[0], parents=[], direction="")
        self.des_frontier.put(goalState)
        intersecting_location = -1
        while not self.src_frontier.empty() and not self.des_frontier.empty():
            src_state = self.src_frontier.get()
            self.src_visited.append(src_state)
            des_state = self.des_frontier.get()
            self.des_visited.append(des_state)
            intersecting_location = self.check_intersect()
            if intersecting_location != -1:
                print(intersecting_location)
                print("Solved")
                break
            yield {"traversedList": [state.location for state in self.src_visited] + [state.location for state in self.des_visited],"success" : False}
            self.expand(self.maze.getNextMoves(src_state), src_state, "forward")
            self.expand(self.maze.getNextMoves(des_state), des_state, "backward")

        if intersecting_location != -1:
            yield {"traversedList": [state.location for state in self.src_visited] + [state.location for state in self.des_visited], "success": True,
                   "paths": self.get_path(intersecting_location)}
            self.displaySolution(intersecting_location)
        else:
            yield {"traveresedList" : [state.location for state in self.src_visited] + [state.location for state in self.des_visited], "success": False}
            print("No solution")

    def check_location_visited(self, location, visited_list):
        for state in visited_list:
            if location == state.location:
                return True
        return False


    def expand(self, moves, parent, direction):
        parents = parent.parents.copy()
        parents.append(parent)
        if direction == "forward":
            for direction in moves:
                if not self.check_location_visited(moves[direction], self.src_visited + list(self.src_frontier.queue)):
                    self.src_frontier.put(State(moves[direction], parents, direction))
        elif direction == "backward":
            for direction in moves:
                if not self.check_location_visited(moves[direction], self.des_visited + list(self.des_frontier.queue)):
                    self.des_frontier.put(State(moves[direction], parents, direction))
