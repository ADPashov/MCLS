import tkinter
from tkinter import Toplevel, Label, Entry, Grid, NSEW
import customtkinter as ctk


class AddCustomer(Toplevel):
    """
    This panel provides  user interface needed for adding new customers to the customer_database.
    Allows the user to input the needed customer_data for the customer and sends request to the root.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    init_widgets()
        Initializes the needed widgets for the the panel

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing
    """

    def __init__(self, root):
        """
        Contructs the AddCustomer object and initializes the widgets

         Parameters
        ----------
        root: tkinter.TK
            The object that owns and controls this panel and to whom requests are sent
        """

        Toplevel.__init__(self, root)
        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.init_widgets()
        self.root.make_resizable(self, wide_cols=[1])

    def init_widgets(self):
        """
        Initilizes all needed Label and Entry Widgets.
        Adds functionality to the button that sends request to the root for adding the customer to the customer_database

        Returns
        -------
        None
        """

        # Header label
        main_label = Label(self, text="Добавяне на нов клиент", bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # First name
        fname_label = Label(self, text="Първо Име", bg=self.root.BG_COLOR)
        fname_label.grid(row=1, column=0, sticky=NSEW)
        fname_box = Entry(self, bg=self.root.BOX_COLOR)
        fname_box.grid(row=1, column=1, sticky=NSEW)

        # Last name
        lname_label = Label(self, text="Фамилия", bg=self.root.BG_COLOR)
        lname_label.grid(row=2, column=0, sticky=NSEW)
        lname_box = Entry(self, bg=self.root.BOX_COLOR)
        lname_box.grid(row=2, column=1, sticky=NSEW)

        # Phone
        phone_label = Label(self, text="Телефон", bg=self.root.BG_COLOR)
        phone_label.grid(row=3, column=0, sticky=NSEW)
        phone_box = Entry(self, bg=self.root.BOX_COLOR)
        phone_box.grid(row=3, column=1, sticky=NSEW)

        # Skin type
        skintype_label = Label(self, text='Фототип кожа', bg=self.root.BG_COLOR)
        skintype_label.grid(row=4, column=0, sticky=NSEW)
        skintype_box = Entry(self, bg=self.root.BOX_COLOR)
        skintype_box.grid(row=4, column=1, sticky=NSEW)

        # Mail
        mail_label = Label(self, text="Имейл", bg=self.root.BG_COLOR)
        mail_label.grid(row=5, column=0, sticky=NSEW)
        mail_box = Entry(self, bg=self.root.BOX_COLOR)
        mail_box.grid(row=5, column=1, sticky=NSEW)

        # Add customer action Button
        add_button = ctk.CTkButton(self, text='Добави Клиент',
                                   command=lambda: self.root.add_customer([fname_box.get(),
                                                                           lname_box.get(),
                                                                           phone_box.get(),
                                                                           skintype_box.get(),
                                                                           mail_box.get()]))
        add_button.configure(font=self.root.FONT)
        add_button.grid(row=6, column=0, columnspan=2, sticky=NSEW)

    def destroy(self):
        self.root.reset_panel_variable('add_customer')
        Toplevel.destroy(self)
