from tkinter import *


class HomePage(Frame):
    def __init__(self, parent, controller,width,height):
        super().__init__(master=parent,width=width,height=height)
        self.controller = controller
        prompt = Label(self, text="Search Algorithm Visualizer", fg='black', bg='white')
        prompt.place(x=0, y=0)
        create_maze_btn = Button(self, text='Create Maze', command=self.create_maze, bg='white', fg='black',
                                 highlightbackground='white')
        create_maze_btn.place(x=0, y=40)

    def create_maze(self):
        self.controller.switch_frame(SelectWidthAndHeightFrame)


class SelectWidthAndHeightFrame(Frame):
    def __init__(self, parent, controller,width,height):
        lb1 = Label(parent, text="Enter Name", width=10, font=("arial", 12))
        lb1.place(x=20, y=120)
        en1 = Entry(parent)
        en1.place(x=100, y=100)


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1280x640")
        # self.configure(bg='white')
        self.switch_frame(HomePage)

    def switch_frame(self, Frame):
        frame = Frame(self, self,width=1280,height=640)
        frame.place(x=0, y=0)


gui = GUI()
gui.mainloop()
