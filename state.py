class State:
    def __init__(self,location,parents,direction):
        self.location = location
        self.parents = parents
        self.direction = direction
    def __str__(self):
        return f"State object with parent: {self.parents}"