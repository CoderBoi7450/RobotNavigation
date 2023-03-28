class Wall:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f"Wall object at x: {self.x}, y: {self.y} with width: {self.width}, height: {self.height}"