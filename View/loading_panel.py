from tkinter import Frame, Label, NSEW


class LoadingPanel(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)

        label = Label(root, text="Зареждане...", font=root.FONT, bg=root.BG_COLOR)
        label.grid(row=0, column=0, sticky=NSEW)
