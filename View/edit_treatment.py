from tkinter import Toplevel, Label, NSEW, StringVar, OptionMenu

import customtkinter as ctk


# TODO - remove id


class EditTreatment(Toplevel):
    """
    This panel provides the user interface needed for editing existing future treatments containing single zone.
    Allows the user to enter new zone, date, time and duration for the given treatment and sends request to root.

    Attributes
    ----------
    root: tkinter.Tk
        The object that owns and controls this panel and to whom requests are sent

    customer_data: list
        The id and names of the user for whom the booking is in the: [id, first name last name]

    date: List
        The date for which the treatment is currently booked: [day, month, year]

    time: String
        The time for which the treatment is currently booked

    treatment_data: List
        The specific details of the treatment. [treatment ID, zone, duration, ids of fillers]
        Fillers are such entries in the database that are empty and represent treatments
        with duration bigger than 1 slot. Not used in this class, but needed when sending the request.

    Methods
    -------
    init_widgets()
        Initializes the needed widgets for the panel

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing

    """

    def __init__(self, root, customer_data, treatment_data):
        """
        Constructs the EditTreatment object and initializes the widgets

        Parameters
        ----------
        root
            See class description
        customer_data
            See class description
        date
            See class description
        time
            See class description
        treatment_data
            See class description
        """

        Toplevel.__init__(self, root)
        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.date = self.root.get_current_date()
        self.time = self.root.get_current_time()

        self.customer_data = customer_data
        self.treatment_data = treatment_data

        self.init_widgets()
        self.root.make_resizable(self)

    def init_widgets(self):
        """
        Initializes the needed Label, OptionMenu(along with their corresponding StringVars) and Button widgets.
        Adds the corresponding functionality to the buttons for sending requests to root.

        Returns
        -------
        None

        """

        # Header label
        main_label = Label(
            self,
            text="Промяна на процедура "
            + self.treatment_data[1]
            + " на"
            + self.customer_data
            + " от "
            + self.time
            + " на "
            + self.root.get_date_string(),
            bg=self.root.BG_COLOR,
        )
        main_label.grid(row=0, column=0, columnspan=7, sticky=NSEW)

        zone_label = Label(self, text="Нова зона: ", bg=self.root.BG_COLOR)
        zone_label.grid(row=1, column=0, sticky=NSEW)

        # Zone widgets
        zone_string = StringVar(self)
        zone_string.set("Избор")

        new_zone = OptionMenu(self, zone_string, *self.root.ZONES)
        new_zone.configure(bg=self.root.BOX_COLOR)
        new_zone["menu"].configure(bg=self.root.BOX_COLOR)
        new_zone.grid(row=2, column=0, sticky=NSEW)

        # Date widgets
        date_label = Label(self, text="Нова дата: ", bg=self.root.BG_COLOR)
        date_label.grid(row=1, column=1, columnspan=3, sticky=NSEW)

        # Day
        day_string = StringVar(self)
        day_string.set(self.date[0])
        new_day = OptionMenu(self, day_string, *self.root.DAYS)
        new_day.configure(bg=self.root.BOX_COLOR)
        new_day["menu"].configure(bg=self.root.BOX_COLOR)
        new_day.grid(row=2, column=1, sticky=NSEW)

        # Month
        month_string = StringVar(self)
        month_string.set(self.root.MONTHS[self.date[1]])
        new_month = OptionMenu(self, month_string, *self.root.MONTHS.values())
        new_month.configure(bg=self.root.BOX_COLOR)
        new_month["menu"].configure(bg=self.root.BOX_COLOR)
        new_month.grid(row=2, column=2, sticky=NSEW)

        # Year
        year_string = StringVar(self)
        year_string.set(self.date[2])
        new_year = OptionMenu(self, year_string, *[str(x) for x in self.root.YEARS])
        new_year.configure(bg=self.root.BOX_COLOR)
        new_year["menu"].configure(bg=self.root.BOX_COLOR)
        new_year.grid(row=2, column=3, sticky=NSEW)

        # Time widgets
        time_label = Label(self, text="Нов час: ", bg=self.root.BG_COLOR)
        time_label.grid(row=1, column=4, sticky=NSEW)

        time_string = StringVar(self)
        time_string.set(self.time)
        new_time = OptionMenu(self, time_string, *self.root.TIMES[1:])
        new_time.configure(bg=self.root.BOX_COLOR)
        new_time["menu"].configure(bg=self.root.BOX_COLOR)
        new_time.grid(row=2, column=4, sticky=NSEW)

        # Duration widgets
        duration_label = Label(
            self, text="Нова продължителност: ", bg=self.root.BG_COLOR
        )
        duration_label.grid(row=1, column=5, sticky=NSEW)

        duration_string = StringVar(self)
        duration_string.set(
            list(self.root.DURATIONS.keys())[self.treatment_data[2] - 1]
        )
        new_duration = OptionMenu(self, duration_string, *self.root.DURATIONS.keys())
        new_duration.configure(bg=self.root.BOX_COLOR)
        new_duration["menu"].configure(bg=self.root.BOX_COLOR)
        new_duration.grid(row=2, column=5, sticky=NSEW)
        delete_button = ctk.CTkButton(
            self,
            text="Изтрий Процедура",
            command=lambda: self.root.delete_treatments([self.treatment_data[0]]),
        )
        delete_button.configure(font=self.root.FONT)
        delete_button.grid(row=3, column=6, sticky=NSEW)

        complete_button = ctk.CTkButton(
            self,
            text="Завърши Процедура",
            command=lambda: self.root.show_panel(
                "complete_treatment",
                [
                    self.customer_data,
                    [[self.treatment_data[0]], [self.treatment_data[1]]],
                ],
            ),
        )
        complete_button.configure(font=self.root.FONT)
        complete_button.grid(row=3, column=1, columnspan=5, sticky=NSEW)

        edit_button = ctk.CTkButton(
            self,
            text="Промени Процедура",
            command=lambda: self.root.edit_treatments(
                [
                    [self.treatment_data[0]],
                    [self.treatment_data[1]],
                    [
                        day_string.get(),
                        [
                            k
                            for k, v in self.root.MONTHS.items()
                            if v == month_string.get()
                        ][0],
                        year_string.get(),
                    ],
                    time_string.get(),
                    self.root.DURATIONS[duration_string.get()],
                ]
            ),
        )

        edit_button.configure(font=self.root.FONT)
        edit_button.grid(row=2, column=6, sticky=NSEW)

        new_zone_button = ctk.CTkButton(
            self,
            text="Добавяне на нова зона",
            command=lambda: self.root.add_new_zone(zone_string.get()),
        )
        new_zone_button.configure(font=self.root.FONT)
        new_zone_button.grid(row=3, column=0, sticky=NSEW)

    def destroy(self):
        self.root.reset_panel_variable("edit_treatment")
        Toplevel.destroy(self)
