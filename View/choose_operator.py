from tkinter import Toplevel, NSEW, Label, StringVar, OptionMenu

import customtkinter as ctk


class ChooseOperator(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.operators = self.root.get_operators()

        self.init_widgets()
        self.root.make_resizable(self)

    def init_widgets(self):
        # Header label
        main_label = Label(self, text="Избор на оператор", bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, stick=NSEW)

        # Operator
        operator_string = StringVar(self)
        operator_string.set("Избери Оператор")
        operator_menu = OptionMenu(self, operator_string, *self.root.get_operators())
        operator_menu.configure(bg=self.root.BG_COLOR)
        operator_menu["menu"].configure(bg=self.root.BOX_COLOR)
        operator_menu.grid(row=1, column=0, sticky=NSEW)

        button = ctk.CTkButton(
            self,
            text="Потвърди Оператор",
            command=lambda: self.root.set_operator(operator_string.get()),
        )
        button.configure(font=self.root.FONT)
        button.grid(row=2, column=0, sticky=NSEW)

    def destroy(self):
        self.root.reset_panel_variable("operator")
        Toplevel.destroy(self)
