from tkinter import *

class TestFrame(Frame):
    def __init__(self, parent):
        super().__init__(master=parent, bg="black")
        test_label = Label(self,text="test",fg = "white",bg = "yellow",font = ('calibre', 20))
        test_label.place(x=0,y=0)

class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        windowWidth = 500
        windowHeight = 500
        self.geometry(f"{windowWidth}x{windowHeight}")
        self.configure(bg='white')
        self.testFrame = TestFrame(self)
        self.testFrame.place(x=0,y=0,width=200,height = 200)

gui = GUI();
gui.mainloop()