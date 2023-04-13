from tkinter import *


class SelectStartPointFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        controller.bind("<ButtonRelease-1>", controller.select_start_point)
        self.controller = controller
        prompt = Label(self, text="Select Initial Point", fg='black', bg='white')
        prompt.place(x=0, y=0)
        sub_btn = Button(self, text='Confirm Start Point', command=controller.confirm_start_point, bg='white', fg='black',
                         highlightbackground='white')
        sub_btn.place(x=0, y=40)


class SelectGoalsFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        controller.bind("<ButtonRelease-1>", controller.select_goals)
        self.controller = controller
        prompt = Label(self, text="Select Goals", fg='black', bg='white')
        prompt.place(x=0, y=0)
        sub_btn = Button(self, text='Confirm Goals', command=controller.confirm_goals, bg='white', fg='black',
                         highlightbackground='white')
        sub_btn.place(x=0, y=40)

class SelectWallFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        controller.bind("<ButtonRelease-1>", controller.select_walls)
        self.controller = controller
        prompt = Label(self, text="Select Walls", fg='black', bg='white')
        prompt.place(x=0, y=0)
        sub_btn = Button(self, text='Confirm walls', command=controller.confirm_walls, bg='white',
                         fg='black',
                         highlightbackground='white')
        sub_btn.place(x=0, y=40)


class WidthAndHeightFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg="white")
        self.mazeCanvas = None
        self.controller = controller
        self.row_var = IntVar()
        self.column_var = IntVar()
        row_label = Label(self, text="Row", fg='black', bg='white')
        row_entry = Entry(self, textvariable=self.row_var, fg='black', insertbackground='black',
                          bg='white')
        column_label = Label(self, text="Column", fg='black', bg='white')
        column_entry = Entry(self, textvariable=self.column_var, fg='black', insertbackground='black',
                             bg='white')
        sub_btn = Button(self, text='Create Maze', command=self.create_maze, bg='white', fg='black',
                         highlightbackground='white')
        row_label.place(x=0, y=0)
        row_entry.place(x=100, y=0)
        column_label.place(x=0, y=30)
        column_entry.place(x=100, y=30)
        sub_btn.place(x=0, y=80)

    def create_maze(self):
        self.controller.row = self.row_var.get()
        self.controller.column = self.column_var.get()
        self.controller.draw_maze()
        self.controller.switch_frame(SelectStartPointFrame)


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mazeCanvas = None
        self.startLocation = None
        self.goals = []
        self.walls = []
        self.currentFrame = ""
        self.windowWidth = 1280
        self.windowHeight = 640
        self.squareSize = 30
        self.geometry(f"{self.windowWidth}x{self.windowHeight}")
        self.configure(bg='white')
        self.font = ('calibre', 20)
        self.row = None
        self.column = None


        self.switch_frame(WidthAndHeightFrame)



    def switch_frame(self, Frame):
        self.unbind("<ButtonRelease-1>")
        self.currentFrame = Frame.__name__
        frame = Frame(self, self)
        frame.place(x=0, y=0, width=self.windowWidth, height=150)



    def draw_maze(self):

        if self.row and self.column:
            self.mazeCanvas = Canvas(self, bg='white', width = self.squareSize * self.column + 1,
                                height=self.squareSize * self.row + 1,
                                borderwidth=0, highlightthickness=0, name="maze")
            self.mazeCanvas.place(x=50, y=150)
            self.mazeCanvas.delete("all")

            lineX = 0
            lineY = 0
            for i in range(self.row + 1):
                self.mazeCanvas.create_line(0, lineY, self.squareSize * self.column, lineY, fill="black")
                lineY += self.squareSize
            for j in range(self.column + 1):
                self.mazeCanvas.create_line(lineX, 0, lineX, self.squareSize * self.row, fill="black")
                lineX += self.squareSize
            if self.startLocation:
                x, y = self.startLocation[0] * self.squareSize, self.startLocation[1] * self.squareSize
                self.mazeCanvas.create_rectangle(x,y, x + self.squareSize, y + self.squareSize,fill="green")
            if self.goals:
                for goal in self.goals:
                    x, y = goal[0] * self.squareSize, goal[1] * self.squareSize
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize, y + self.squareSize, fill="red")
            if self.walls:
                for wall in self.walls:
                    x, y = wall[0] * self.squareSize, wall[1] * self.squareSize
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize, y + self.squareSize, fill="black")
            self.after(100,self.draw_maze)


    def select_start_point(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.squareSize
            column = mouse_x // self.squareSize
            print(mouse_x,mouse_y)
            self.startLocation = (column,row)


    def confirm_start_point(self):

        self.switch_frame(SelectGoalsFrame)
        print(self.startLocation)

    def confirm_goals(self):
        self.switch_frame(SelectWallFrame)
        print(self.goals)

    def confirm_walls(self):
        print(self.walls)
        self.export()


    def select_goals(self,event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.squareSize
            column = mouse_x // self.squareSize
            if (column,row) in self.goals:
                self.goals.remove((column,row))
            elif (column,row) != self.startLocation:
                self.goals.append((column,row))
            else:
                print("Point already occupied")

    def select_walls(self,event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.squareSize
            column = mouse_x // self.squareSize
            if (column,row) in self.walls:
                self.walls.remove((column,row))
            elif (column,row) != self.startLocation and (column,row) not in self.goals:
                self.walls.append((column,row))
            else:
                print("Point already occupied")

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


gui = GUI()

gui.mainloop()
