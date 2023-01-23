from tkinter import Toplevel, Grid, Label, Entry, NSEW
import customtkinter as ctk


class EditCustomer(Toplevel):
    """
    This panel provides the user interface needed for editing existing customers from the customer database.
    Allows the user to enter new value for every field of the customer and sends request to the root.

    ...

    Attributes
    ----------
    root: tkinter.Tk
        The object that owns and controls this panel and to whom requests are sent

    customer_data: list
        The current values for all fields of the customer in the following format:
        [id, first name, last name, phone, skin type, mail]

    Methods
    -------
    init_widgets()
        Initializes the needed Label and Entry widgets for the panel,
        also initializes the needed buttons and assigns them the corresponding actions

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing
    """

    def __init__(self, root, customer_data):
        """
        Constructs the EditCustomer object and initializes the widgets

        Parameters
        ----------
        root: tkinter.Tk
            See class description
            
        customer_data: list
            See class description
        """
        Toplevel.__init__(self, root)

        self.root = root
        self.customer_data = customer_data

        self.configure(bg=self.root.BG_COLOR)

        self.init_widgets()
        self.root.make_resizable(self, wide_cols=[1, 2])

    def init_widgets(self):
        """
        Initilizes all needed Label, Entry and Button Widgets.
        Adds the correspinding functionality to each of the buttons that sends request to the root
        for editing the value of the given field for the customer in the customer_database


        Returns
        -------
        None
        """

        # Header label
        main_label = Label(self, text="Промяна на клиент номер " + str(self.customer_data[0]), bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, columnspan=3, sticky=NSEW)

        # First name
        fname_label = Label(self, text="Първо Име", bg=self.root.BG_COLOR)
        fname_label.grid(row=1, column=0, sticky=NSEW)

        new_fname_box = Entry(self, bg=self.root.BOX_COLOR)
        new_fname_box.insert(0, self.customer_data[1])
        new_fname_box.grid(row=1, column=1, sticky=NSEW)

        fname_button = ctk.CTkButton(self, text='Промени първо име',
                                     command=lambda: self.root.edit_customer('fname',
                                                                             new_fname_box.get()))
        fname_button.configure(font=self.root.FONT)
        fname_button.grid(row=1, column=2, sticky=NSEW)

        # Last Name
        lname_label = Label(self, text="Фамилия", bg=self.root.BG_COLOR)
        lname_label.grid(row=2, column=0, sticky=NSEW)

        new_lname_box = Entry(self, bg=self.root.BOX_COLOR)
        new_lname_box.insert(0, self.customer_data[2])
        new_lname_box.grid(row=2, column=1, sticky=NSEW)

        lname_button = ctk.CTkButton(self, text='Промени Фамилия',
                                     command=lambda: self.root.edit_customer('lname',
                                                                             new_lname_box.get()))
        lname_button.configure(font=self.root.FONT)
        lname_button.grid(row=2, column=2, sticky=NSEW)

        # Phone
        phone_label = Label(self, text="Телефон", bg=self.root.BG_COLOR)
        phone_label.grid(row=3, column=0, sticky=NSEW)

        new_phone_box = Entry(self, bg=self.root.BOX_COLOR)
        new_phone_box.insert(0, str(self.customer_data[3]))
        new_phone_box.grid(row=3, column=1, sticky=NSEW)

        phone_button = ctk.CTkButton(self, text='Промени телефон',
                                     command=lambda: self.root.edit_customer('phone',
                                                                             new_phone_box.get()))
        phone_button.configure(font=self.root.FONT)
        phone_button.grid(row=3, column=2, sticky=NSEW)

        # Skin type
        skintype_label = Label(self, text='Фототип кожа', bg=self.root.BG_COLOR)
        skintype_label.grid(row=4, column=0, sticky=NSEW)

        new_skintype_box = Entry(self, bg=self.root.BOX_COLOR)
        new_skintype_box.insert(0, str(self.customer_data[4]))
        new_skintype_box.grid(row=4, column=1, sticky=NSEW)

        skintype_button = ctk.CTkButton(self, text='Промени фототип',
                                        command=lambda: self.root.edit_customer('skin_type',
                                                                                new_skintype_box.get()))
        skintype_button.configure(font=self.root.FONT)
        skintype_button.grid(row=4, column=2, sticky=NSEW)

        # Mail
        mail_label = Label(self, text="Имейл", bg=self.root.BG_COLOR)
        mail_label.grid(row=5, column=0, sticky=NSEW)

        new_mail_box = Entry(self, bg=self.root.BOX_COLOR)
        new_mail_box.insert(0, self.customer_data[5])
        new_mail_box.grid(row=5, column=1, sticky=NSEW)

        mail_button = ctk.CTkButton(self, text='Промени имейл',
                                    command=lambda: self.root.edit_customer('mail',
                                                                            new_mail_box.get()))
        mail_button.configure(font=self.root.FONT)
        mail_button.grid(row=5, column=2, sticky=NSEW)

    def destroy(self):
        self.root.reset_panel_variable('edit_customer')
        Toplevel.destroy(self)
