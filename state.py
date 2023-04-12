class State:
    def __init__(self, location, parents, direction):
        self.location = location
        self.parents = parents
        self.direction = direction

    def __str__(self):
        return f"Location: {self.location}"

    def __eq__(self, other):
        return self.location == other.location
