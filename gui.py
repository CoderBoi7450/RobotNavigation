from tkinter import *
from program import Program


class SearchPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        self.controller = controller
        Label(self, text="Breadth First Search Visualizer", fg='black', bg='white').place(x=0, y=0)
        Button(self, text='Start search', command=self.start_search, bg='white', fg='black',
               highlightbackground='white').place(x=0., y=40)
        self.algorithm = StringVar()
        Radiobutton(parent,
                    text="Breadth-First Search",
                    variable=self.algorithm,
                    command=self.change_algorithm,
                    value="bfs").place(x=40, y=80)

        Radiobutton(parent,
                    text="Depth-First Search",
                    variable=self.algorithm,
                    command=self.change_algorithm,
                    value="dfs").place(x=200, y=80)
        Radiobutton(parent,
                    text="Greedy Best-First Search",
                    variable=self.algorithm,
                    command=self.change_algorithm,
                    value="gbfs").place(x=360, y=80)
        Radiobutton(parent,
                    text="A* Search",
                    variable=self.algorithm,
                    command=self.change_algorithm,
                    value="ass").place(x=560, y=80)
        Radiobutton(parent,
                    text="Bidirectional Search (Custom Uninformed Search)",
                    variable=self.algorithm,
                    command=self.change_algorithm,
                    value="bds").place(x=660, y=80)
        Radiobutton(parent,
                    text="IDA Search (Custom Informed Search)",
                    variable=self.algorithm,
                    command=self.change_algorithm,
                    value="ida").place(x=1000, y=80)
        self.controller.import_maze()
        self.controller.draw_maze()

    def change_algorithm(self):
        print(self.algorithm.get())

    def start_search(self):
        search = Program()
        self.controller.paths = None
        self.controller.traversedLocation = None
        for result in search.solve("maze.txt"):
            self.controller.traversedLocation = result["traversedList"]
            if result["success"]:
                self.controller.paths = result["paths"]
            if result.get("frontier"):
                self.controller.frontier = result["frontier"]
            if result.get("current"):
                self.controller.current = result["current"]
            print(self.controller.traversedLocation)
            self.controller.tksleep(0.01)


class HomePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        self.controller = controller
        prompt = Label(self, text="Search Algorithm Visualizer", fg='black', bg='white')
        prompt.place(x=0, y=0)
        create_maze_btn = Button(self, text='Create Maze', command=self.create_maze, bg='white', fg='black',
                                 highlightbackground='white')
        import_btn = Button(self, text='Import Maze', command=self.import_maze, bg='white', fg='black',
                            highlightbackground='white')
        search_btn = Button(self, text='Search', command=self.search, bg='white', fg='black',
                            highlightbackground='white')
        create_maze_btn.place(x=0, y=40)
        import_btn.place(x=150, y=40)
        search_btn.place(x=300, y=40)

    def create_maze(self):
        self.controller.switch_frame(SelectWidthAndHeightFrame)

    def import_maze(self):
        self.controller.switch_frame(ImportPage)

    def search(self):
        self.controller.switch_frame(SearchPage)


class ImportPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        self.controller = controller
        prompt = Label(self, text="Imported from maze.txt file", fg='black', bg='white')
        prompt.place(x=0, y=0)
        self.controller.import_maze()
        self.controller.draw_maze()


class SelectStartPointFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        controller.bind("<ButtonRelease-1>", self.select_start_point)
        self.controller = controller
        prompt = Label(self, text="Select Initial Point", fg='black', bg='white')
        prompt.place(x=0, y=0)
        sub_btn = Button(self, text='Confirm Start Point', command=self.confirm_start_point, bg='white', fg='black',
                         highlightbackground='white')
        sub_btn.place(x=0, y=40)

    def confirm_start_point(self):
        self.controller.switch_frame(SelectGoalsFrame)

    def select_start_point(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            self.controller.startLocation = (column, row)


class SelectGoalsFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        controller.bind("<ButtonRelease-1>", self.select_goals)
        self.controller = controller
        prompt = Label(self, text="Select Goals", fg='black', bg='white')
        prompt.place(x=0, y=0)
        sub_btn = Button(self, text='Confirm Goals', command=self.confirm_goals, bg='white', fg='black',
                         highlightbackground='white')
        sub_btn.place(x=0, y=40)

    def confirm_goals(self):
        self.controller.switch_frame(SelectWallFrame)

    def select_goals(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            if (column, row) in self.controller.goals:
                self.controller.goals.remove((column, row))
            elif (column, row) != self.controller.startLocation:
                self.controller.goals.append((column, row))
            else:
                print("Point already occupied")


class SelectWallFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        controller.bind("<ButtonRelease-1>", self.select_walls)
        self.controller = controller
        prompt = Label(self, text="Select Walls", fg='black', bg='white')
        prompt.place(x=0, y=0)
        sub_btn = Button(self, text='Export', command=self.confirm_walls, bg='white',
                         fg='black',
                         highlightbackground='white')
        sub_btn.place(x=0, y=40)

    def confirm_walls(self):
        self.controller.export()

    def select_walls(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            if (column, row) in self.controller.walls:
                self.controller.walls.remove((column, row))
            elif (column, row) != self.controller.startLocation and (column, row) not in self.controller.goals:
                self.controller.walls.append((column, row))
            else:
                print("Point already occupied")


class SelectWidthAndHeightFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")

        # self.mazeCanvas = None
        self.controller = controller
        self.row_var = IntVar()
        self.column_var = IntVar()
        row_label = Label(parent, text="Row", fg='black', bg='white')
        row_entry = Entry(parent, textvariable=self.row_var, fg='black', insertbackground='black',
                          bg='white')
        column_label = Label(parent, text="Column", fg='black', bg='white')
        column_entry = Entry(parent, textvariable=self.column_var, fg='black', insertbackground='black',
                             bg='white')
        sub_btn = Button(parent, text='Confirm Size', command=self.confirm_size, bg='white', fg='black',
                         highlightbackground='white')
        row_label.place(x=0, y=0)
        row_entry.place(x=100, y=0)
        column_label.place(x=0, y=30)
        column_entry.place(x=100, y=30)
        sub_btn.place(x=0, y=80)

    def confirm_size(self):
        self.controller.row = self.row_var.get()
        self.controller.column = self.column_var.get()
        self.controller.draw_maze()
        self.controller.switch_frame(SelectStartPointFrame)


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paths = None
        self.mazeCanvas = None
        self.startLocation = None
        self.frontier = []
        self.goals = []
        self.current = None

        self.walls = []
        self.traversedLocation = []
        self.currentFrame = ""
        self.windowWidth = 1280
        self.windowHeight = 1280
        self.squareSize = 30
        self.geometry(f"{self.windowWidth}x{self.windowHeight}")
        self.configure(bg='white')
        self.font = ('calibre', 20)
        self.row = None
        self.column = None
        self.switch_frame(HomePage)

    def switch_frame(self, Frame):
        self.unbind("<ButtonRelease-1>")
        self.currentFrame = Frame.__name__
        frame = Frame(self, self)
        frame.place(x=0, y=0, width=self.windowWidth, height=150)

    def draw_maze(self):
        if self.row and self.column:
            self.mazeCanvas = Canvas(self, bg='white', width=self.squareSize * self.column + 1,
                                     height=self.squareSize * self.row + 1,
                                     borderwidth=0, highlightthickness=0, name="maze")
            self.mazeCanvas.place(x=50, y=150)
            self.mazeCanvas.delete("all")

            lineX = 0
            lineY = 0
            for i in range(self.row + 1):
                self.mazeCanvas.create_line(0, lineY, self.squareSize * self.column, lineY, fill="black", width=1)
                lineY += self.squareSize
            for j in range(self.column + 1):
                self.mazeCanvas.create_line(lineX, 0, lineX, self.squareSize * self.row, fill="black", width=1)
                lineX += self.squareSize

            if self.frontier:
                for location in self.frontier:
                    x, y = location[0] * self.squareSize + 1, location[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="#ADD8E6")

            if self.traversedLocation:
                for location in self.traversedLocation:
                    x, y = location[0] * self.squareSize + 1, location[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="#241571")

            if self.current:
                x, y = self.current[0] * self.squareSize + 1, self.current[1] * self.squareSize + 1
                self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                 fill="#F58025")
            if self.paths:
                for path in self.paths:
                    x, y = path[0] * self.squareSize + 1, path[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="yellow")
            if self.goals:
                for goal in self.goals:
                    x, y = goal[0] * self.squareSize + 1, goal[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="green")

            if self.walls:
                for wall in self.walls:
                    x, y = wall[0] * self.squareSize + 1, wall[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="black")

            if self.startLocation:
                x, y = self.startLocation[0] * self.squareSize + 1, self.startLocation[1] * self.squareSize + 1
                self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2, fill="red")
            self.after(100, self.draw_maze)

    def export(self):
        with open("maze.txt", "w") as file:
            file.write(f"[{self.row},{self.column}]\n")
            file.write(f"({self.startLocation[0]},{self.startLocation[1]})\n")
            for index in range(len(self.goals)):
                goal = self.goals[index]
                file.write(f"({goal[0]},{goal[1]})")
                if index != len(self.goals) - 1:
                    file.write(" | ")
            file.write("\n")
            for index in range(len(self.walls)):
                wall = self.walls[index]
                file.write(f"({wall[0]},{wall[1]},1,1)")
                if index != len(self.walls) - 1:
                    file.write("\n")

    def import_maze(self):
        with open("maze.txt", "r") as file:
            mazeSize = file.readline().strip('][ \n').split(',')
            mazeSize = [int(i) for i in mazeSize]
            self.row, self.column = mazeSize[0], mazeSize[1]
            initialLocation = [int(i) for i in file.readline().strip('() \n').split(',')]
            self.startLocation = (initialLocation[0], initialLocation[1])
            goalStates = file.readline().strip().split(' | ')
            goalStates = [state.strip(') (').split(',') for state in goalStates]
            goalStates = [[int(x) for x in state] for state in goalStates]
            self.goals = []
            for goal in goalStates:
                self.goals.append(goal)
            walls = []
            for line in file.readlines():
                if not line.isspace():
                    newWall = [int(i) for i in line.strip('() \n').split(',')]
                    for i in range(newWall[2]):
                        for j in range(newWall[3]):
                            walls.append((newWall[0] + i, newWall[1] + j))
            self.walls = []
            for wall in walls:
                self.walls.append(wall)


def tksleep(self, time: float) -> None:
    """
    Emulating `time.sleep(seconds)`
    Created by TheLizzard, inspired by Thingamabobs
    """
    self.after(int(time * 1000), self.quit)
    self.mainloop()


Misc.tksleep = tksleep

gui = GUI()
gui.mainloop()
