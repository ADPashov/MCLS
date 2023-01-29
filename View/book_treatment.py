from tkinter import Toplevel, Label, NSEW, StringVar, OptionMenu

import customtkinter as ctk


class BookTreatment(Toplevel):
    """
    This panel provides  user interface needed for booking treatments.
    From the system's POV this means adding treatment entries to the database.
    Allows the user to select zones and duration and sends request to the root.

    ...

    Attributes
    ----------
    customer_data: List
        List that contains the id and the names of the customer: [id, first name, last name]

    day: String
        Indicates the day part of the chosen date for which a booking will be made

    month: String
        Indicates the month part of the chosen date for which a booking will be made

    year: String
        Indicates the year part of the chosen date for which a booking will be made

    time: String
        Indicates the time at which the booking will start

    labels: List
        Contains the additional zone labels created when adding additional zones

    menus: List
        Contains the additional OptionMenu widgets created when adding additional zones

    string_vars: List
        Contains the VarString variables needed for the OptionMenus created when adding additional zones

    counter: Int
        Variable that allows for tracking the indices of widgets and in the lists above,
        as well as allowing proper placement of the book button in the grid layout

    Methods
    -------
    init_widgets()
        Initializes the needed widgets for the panel

    get_zones()
        Handles the packages functionality.

    add_zone()
        Allows for selecting multiple zones/treatments for a single treatment booking by adding and rearranging
        the needed widgets.

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing
    """

    def __init__(self, root, customer_data):
        """
        Contructs the AddCustomer object and initializes the widgets

        Parameters
        ----------
        root: tkinter.TK
            The object that owns and controls this panel and to whom requests are sent

        data: List
            The customer's id, name as well as the date for which the treatment will be booked in the following format:
            [[id, first name, last name], [day, monyh, year], time]
        """

        Toplevel.__init__(self, root)

        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        """Decomposing the data passed when creating the object"""
        self.customer_data = customer_data

        """Instance variables """
        self.labels = []
        self.menus = []
        self.string_vars = []
        self.counter = 0

        self.init_widgets()
        self.root.make_resizable(self, wide_cols=[1])

    # TODO - remove id

    def init_widgets(self):
        """
        Initializes all needed Label and Option Menu widgets, as well the needed StringVars for the booking a
        single-zone treatment. Adds functionality to the button that sends request to the root for adding the
        customer to the database. Also binds the add_zone() method to the add_button.

        Returns
        -------
        None

        """

        # Header label
        main_label = Label(
            self,
            text="Запазване на час за " + self.customer_data,
            bg=self.root.BG_COLOR,
        )
        main_label.grid(row=0, column=0, columnspan=3, sticky=NSEW)

        # Label informing the user which date and time are chosen
        data_label = Label(
            self,
            text=self.root.get_date_string()
            + ", "
            + self.root.get_current_time()
            + "ч.",
            bg=self.root.BG_COLOR,
        )
        data_label.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        # Duration label and option menu
        duration_label = Label(self, text="Продължителност: ", bg=self.root.BG_COLOR)
        duration_label.grid(row=2, column=0, sticky=NSEW)

        duration_string = StringVar(self)
        duration_string.set(list(self.root.DURATIONS.keys())[1])
        duration_chooser = OptionMenu(
            self, duration_string, *list(self.root.DURATIONS.keys())
        )
        duration_chooser.configure(bg="#FF69B4")
        duration_chooser["menu"].configure(bg=self.root.BOX_COLOR)
        duration_chooser.grid(row=2, column=1, sticky=NSEW)

        # Button for adding the needed widgets for adding additional zones
        add_button = ctk.CTkButton(
            self, text="Добави зона", command=lambda: self.add_zone()
        )
        add_button.configure(font=self.root.FONT)
        add_button.grid(row=2, column=2, sticky=NSEW)

        # Main action button
        # Instance variable as it needs to be accessed by the add_zone() method which moves its position
        # IMO, setting it to None in __init__() would not contribute to readability
        self.book_button = ctk.CTkButton(
            self,
            text="Запази Час",
            command=lambda: self.root.book_treatment(
                self.root.DURATIONS[duration_string.get()], self.get_zones()
            ),
        )
        self.book_button.configure(font=self.root.FONT)
        self.book_button.grid(row=4, column=0, columnspan=3, sticky=NSEW)
        self.add_zone()

    def get_zones(self):
        """
        Handles the package functionality.
        Goes through the selected zones and checks if any of them is a package.
        If a package is found, it is replaced with the corresponding zones.

        Returns
        -------
        zones: List
            List of zones to be sent to the root as part of the request
        """

        zones = []
        for x in [var.get() for var in self.string_vars]:
            if x in self.root.PACKAGES.keys():
                zones += self.root.PACKAGES[x]
            else:
                zones.append(x)
        return zones

    def add_zone(self):
        """
        For each new zone requested by user, a new Label and OptionMenu are created,
        along with a new StringVar for the Option Menu. Places them at the row where currently the book_button is
        and moves the button to one row below.

        Returns
        -------
        None
        """

        # Move book_button
        self.book_button.grid(row=self.counter + 4, column=0, columnspan=3, sticky=NSEW)

        # New label
        self.labels.append(Label(self, text="Зона: ", bg=self.root.BG_COLOR))
        self.labels[self.counter].grid(row=self.counter + 3, column=0)

        # Create and place new StringVar and OptionMenu
        self.string_vars.append(StringVar(self))
        self.string_vars[self.counter].set("Избор")
        self.menus.append(
            OptionMenu(
                self,
                self.string_vars[self.counter],
                *(self.root.ZONES + list(self.root.PACKAGES.keys()))
            )
        )
        self.menus[self.counter].configure(bg=self.root.BOX_COLOR)
        self.menus[self.counter]["menu"].configure(bg=self.root.BOX_COLOR)
        self.menus[self.counter].grid(row=self.counter + 3, column=1, sticky=NSEW)

        # Ensure the panes is resizable with the new widgets
        self.root.make_resizable(self, wide_cols=[1])

        # Keep track of the needed indices
        self.counter += 1

    def destroy(self):
        self.root.reset_panel_variable("book_treatment")
        Toplevel.destroy(self)
