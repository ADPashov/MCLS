from tkinter import Toplevel, Label, Entry, NSEW, Grid
import customtkinter as ctk


class EditNote(Toplevel):
    """
    This panel provides the user interface needed for editing an existing note for the chosen customer.
    Consists of a simple info label, text box and a  two buttons.

        Attributes
        ----------
        root: tkinter.Tk
            The object that owns and controls this panel and to whom requests are sent

        customer_data: list
            The id and names of the user for whom the booking is in the: [id, first name, last name]
            
        note_data: List
            The id and the actual note contents: [id, note]

        Methods
        -------
        init_widgets()
            Initializes the needed widgets for the panel

        make_resizable()
            Allows for the widgets in the panel to keep their positions and proportions with screen resizing

         """

    def __init__(self, root, customer_data, note_data):
        """
        Constructs the EditNote object and initializes the widgets

        Parameters
        ----------
        root
            See class description
        customer_data
            See class description
        note_data
            See class description
        
        """

        Toplevel.__init__(self, root)
        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.customer_data = customer_data
        self.note_data = note_data

        self.init_widgets()
        self.root.make_resizable(self)

    def init_widgets(self):
        """
        Initializes the needed Label, Entry and Button widgets.
        Adds the corresponding functionality to the button for sending requests to root.

        Returns
        -------
        None

        """

        # Header label
        main_label = Label(self, text='Промяна на бележка за ' + self.customer_data, bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # Note text box
        note_text = Entry(self, bg=self.root.BOX_COLOR, width = len(self.note_data[1]) + 5)
        note_text.insert(0, self.note_data[1])
        note_text.grid(row=1, column=0, columnspan=2, sticky=NSEW)

        # Delete button
        delete_button = ctk.CTkButton(self, text='Изтрий бележка',
                                      command=lambda: self.root.delete_note(self.note_data[0]))
        delete_button.configure(font=self.root.FONT)
        delete_button.grid(row=2, column=0, sticky=NSEW)

        # Edit button
        edit_button = ctk.CTkButton(self, text='Промени бележка',
                                    command=lambda: self.root.edit_note([self.note_data[0], note_text.get()]))
        edit_button.configure(font=self.root.FONT)
        edit_button.grid(row=2, column=1, sticky=NSEW)

    def destroy(self):
        self.root.reset_panel_variable('edit_note')
        Toplevel.destroy(self)

    def get_max_length(self):
        length = 0
        for note in self.note_data:
            print(note)
            if len(note[1]) > length:
                length = len(note[1])
        return length
