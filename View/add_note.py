from tkinter import Toplevel, NSEW, Label, Text, Grid
import customtkinter as ctk


class AddNote(Toplevel):
    """
    This panel provides the user interface needed for adding a note to the chosen customer.
    Consists of a simple info label, text box and a button.

    Attributes
    ----------
    root: tkinter.Tk
        The object that owns and controls this panel and to whom requests are sent

    customer_data: list
        The id and names of the user for whom the booking is in the: [id, first name, last name]

    Methods
    -------
    init_widgets()
        Initializes the needed widgets for the panel

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing

     """
    def __init__(self, root, customer_data):
        """
        Constructs the AddNote object and initializes the widgets

        Parameters
        ----------
        root
            See class description
        customer_data
            See class description
        """

        Toplevel.__init__(self, root)
        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.customer_data = customer_data

        self.init_widgets()
        self.root.make_resizable(self)

    def init_widgets(self):
        """
        Initializes the needed Label, Text Button widgets.
        Adds the corresponding functionality to the button for sending requests to root.

        Returns
        -------
        None

        """

        # Header label
        main_label = Label(self, text='Добавяне на бележка за ' + self.customer_data, bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, stick=NSEW)

        # Note contents box
        note_box = Text(self, height=2, width=60, bg=self.root.BOX_COLOR)
        note_box.grid(row=1, column=0, sticky=NSEW)

        # Button
        note_button = ctk.CTkButton(self, text='Добави бележка',
                                    command=lambda: self.root.add_note(note_box.get('1.0', 'end-1c')))
        note_button.configure(font=self.root.FONT)
        note_button.grid(row=2, column=0, sticky=NSEW)


    def destroy(self):
        self.root.reset_panel_variable('add_note')
        Toplevel.destroy(self)


