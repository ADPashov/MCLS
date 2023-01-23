from tkinter import Toplevel, NSEW, StringVar, OptionMenu, Label, Grid
import customtkinter as ctk


class EditMulti(Toplevel):
    """
    This panel provides the user interface needed for editing existing future treatments containing more than one zone.
    Allows for two types of changes - the whole booking with all the treatments it includes or only a single zone.
    The whole booking can be deleted or moved to another day/time.
    For single zones, they could either be singularly moved to another day/time as a new treament for a single zone,
    or the given zone could be removed from booking.

    Attributes
    ----------
    root: tkinter.Tk
        The object that owns and controls this panel and to whom requests are sent

    customer_data: list
        The id and names of the user for whom the booking is in the: [id, first name, last name]

    date: List
        The date for which the treatment is currently booked: [day, month, year]

    time: String
        The time for which the treatment is currently booked

    treatments: List(Tuple)
        A list of tuples, where each tuple represents the id and the zone for each entry in the multi booking.
        [(id1, zone1), (id2,zone2),....]
    duration: Int
        The duration of the whole multi booking represented in number of slots it occupies
    fillers: List
        dfdsfa
    index_first: Int
        The index of the first entry of the multi booking in the daily schedule.

        When a single zone is moved/deleted, a request is sent as if the first entry of this booking is clicked in order
        to show a new edit booking windows(edit_treatment if only one zone is left or
        edit_multi if more than zone remain).
        The first index is kept track of as clicking any of the single entries in the daily schedule should
        show the same edit_multi window. If we keep track of the one clicked, the functionalities will properly
        only when the first entry is clicked. All other clicks are guaranteed to give problems when moving/deleting
        single zones.

    Methods
    -------
    init_widgets_all()
        Responsible for creating the widgets needed for editing the whole booking together.

    init_widgets_single()
        Responsible for creating the widgets needed for editing single entries from the whole booking.

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing

    """

    def __init__(self, root, customer_data, treatment_ids, treatment_zones, duration):
        """
        Constructs the EditMulti object and initializes the widgets.

        Since this panel is with much longer code for initializing all widgets,
        the init_widgets method is split into two parts.

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
        treatments
            See class description
        duration
            See class description
        index_first
            See class description

        """
        Toplevel.__init__(self, root)

        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.customer_data = customer_data
        self.date = self.root.get_current_date()
        self.time = self.root.get_current_time()
        self.treatment_ids = treatment_ids
        self.treatment_zones = treatment_zones
        self.duration = duration

        self.init_widgets_all()
        self.init_widgets_single()
        self.root.make_resizable(self)

    def init_widgets_all(self):
        """
        The first part of the widget initialization.

        In this method the header and info labels are initialized. Along with them, the OptionMenu(with their VarString)
        and Buttons for rescheduling/deleting the whole booking are also placed.
        The corresponding functionalities are bound to the buttons, so they can send requests to the root.

        Returns
        -------
        None

        """

        # Header Label
        main_label = Label(self, text='Промяна на резервация за няколко зони', bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, columnspan=6, sticky=NSEW)

        # Info labels for name, date, time, duration and zone count
        name_label = Label(self, text='Клиент: ' + self.customer_data, bg=self.root.BG_COLOR)
        name_label.grid(row=1, column=0, sticky=NSEW)

        date_label = Label(self, text='Дата: ', bg=self.root.BG_COLOR)
        date_label.grid(row=1, column=1, columnspan=3, sticky=NSEW)

        time_label = Label(self, text='Час: ', bg=self.root.BG_COLOR)
        time_label.grid(row=1, column=4, sticky=NSEW)

        duration_label = Label(self, text='Продължителност: ', bg=self.root.BG_COLOR)
        duration_label.grid(row=1, column=5, sticky=NSEW)

        count_label = Label(self, text='Брой зони: ' + str(len(self.treatment_ids)), bg=self.root.BG_COLOR)
        count_label.grid(row=2, column=0, sticky=NSEW)

        # Widgets for editing all treatments simultaneously

        # Day
        day_string = StringVar(self)
        day_string.set(self.date[0])
        new_day = OptionMenu(self, day_string, *self.root.DAYS)
        new_day.configure(bg=self.root.BOX_COLOR)
        new_day['menu'].configure(bg=self.root.BOX_COLOR)
        new_day.grid(row=2, column=1, sticky=NSEW)

        # Month
        month_string = StringVar(self)
        month_string.set(self.root.MONTHS[self.date[1]])
        new_month = OptionMenu(self, month_string, *self.root.MONTHS.values())
        new_month.configure(bg=self.root.BOX_COLOR)
        new_month['menu'].configure(bg=self.root.BOX_COLOR)
        new_month.grid(row=2, column=2, sticky=NSEW)

        # Year
        year_string = StringVar(self)
        year_string.set(self.date[2])
        new_year = OptionMenu(self, year_string, *self.root.YEARS)
        new_year.configure(bg=self.root.BOX_COLOR)
        new_year['menu'].configure(bg=self.root.BOX_COLOR)
        new_year.grid(row=2, column=3, sticky=NSEW)

        # Time
        time_string = StringVar(self)
        time_string.set(self.time)
        new_time = OptionMenu(self, time_string, *self.root.TIMES[1:])
        new_time.configure(bg=self.root.BOX_COLOR)
        new_time['menu'].configure(bg=self.root.BOX_COLOR)
        new_time.grid(row=2, column=4, sticky=NSEW)

        # Duration
        duration_string = StringVar(self)
        duration_string.set(list(self.root.DURATIONS.keys())[self.duration - 1])
        new_duration = OptionMenu(self, duration_string, *self.root.DURATIONS.keys())
        new_duration.configure(bg=self.root.BOX_COLOR)
        new_duration['menu'].configure(bg=self.root.BOX_COLOR)
        new_duration.grid(row=2, column=5, sticky=NSEW)

        # Complete button
        complete_all_button = ctk.CTkButton(self, text='Завършване на всички процедури',
                                            command=lambda: self.root.show_panel('complete_treatment',
                                                                                 [self.customer_data,
                                                                                  [self.treatment_ids,
                                                                                   self.treatment_zones]]))

        complete_all_button.configure(font=self.root.FONT)
        complete_all_button.grid(row=3, column=0, sticky=NSEW)

        # Delete button
        delete_all_button = ctk.CTkButton(self, text='Изтриване на всички процедури',
                                          command=lambda: self.root.delete_treatments(self.treatment_ids))
        delete_all_button.configure(font=self.root.FONT)
        delete_all_button.grid(row=3, column=1, columnspan=3, sticky=NSEW)

        # Change button
        change_all_button = ctk.CTkButton(self, text='Преместване на всички процедури',
                                          command=lambda: self.root.edit_treatments([self.treatment_ids,
                                                                                     self.treatment_zones,
                                                                                     [day_string.get(),
                                                                                      [k for k, v in
                                                                                       self.root.MONTHS.items()
                                                                                       if v == month_string.get()][0],
                                                                                      year_string.get()],
                                                                                     time_string.get(),
                                                                                     self.root.DURATIONS[
                                                                                         duration_string.get()]]))

        change_all_button.configure(font=self.root.FONT)
        change_all_button.grid(row=3, column=4, columnspan=2, sticky=NSEW)

        new_zone_label = Label(self, text='Добавяне на нова зона', bg=self.root.BG_COLOR)
        new_zone_label.grid(row=4, column=0, sticky=NSEW)

        # Add new zone
        new_zone_string = StringVar(self)
        new_zone_string.set('Избор')
        new_zone = OptionMenu(self, new_zone_string, *self.root.ZONES)
        new_zone.configure(bg=self.root.BOX_COLOR)
        new_zone['menu'].configure(bg=self.root.BOX_COLOR)
        new_zone.grid(row=4, column=1, columnspan=3, sticky=NSEW)

        new_zone_button = ctk.CTkButton(self, text='Добавяне на нова зона',
                                        command=lambda: self.root.add_new_zone(new_zone_string.get()))
        new_zone_button.configure(font=self.root.FONT)
        new_zone_button.grid(row=4, column=4, columnspan=2, sticky=NSEW)

    def init_widgets_single(self):
        """
        The second part of the widget initialization.
        For each zone in the booking are created the needed Label, OptionMenu(along with StringVar) and Button widgets.

        In order to get the correct placement of the additional OptionMenus and Button the following formulas were used:
        Menus -> 2*(i-1)+1 if i>0 else i
        Buttons -> 2*i if i>0 else i
        That guarantees that regardless of the amount of widget rows to be added, there always will be
        a row of OptionMenus followed by a row of Buttons.
        Note that since those widgets start at the 5th row:
        for Menus 5 is added to the cases when i=0 and 6 for the rest of the cases
        for Buttons 6 is added
        Hence the final formulas are:
        Menus -> 6+2*(i-1)+1 if i>0 else 5+i
        Buttons -> 6+2*i if i>0 else 6+i


        Returns
        -------
        None
        """
        # Lists to contain the widgets that the loop below will produce
        zone_labels = []

        day_strings = []
        day_menus = []

        month_strings = []
        month_menus = []

        year_strings = []
        year_menus = []

        time_strings = []
        time_menus = []

        duration_strings = []
        duration_menus = []

        buttons_move = []
        buttons_delete = []

        empty_labels = []

        # Separator

        # Iterating over all tuples in the treatments list while keeping track of index
        for i in range(0, len(self.treatment_ids)):
            empty_labels.append(Label(self, text='', bg=self.root.BG_COLOR))
            empty_labels[i].grid(row=Grid.size(self)[1], column=0)

            _, curr_rows = Grid.size(self)

            # Zone label
            zone_labels.append(
                Label(self, text=' Зона ' + str(i + 1) + ': ' + self.treatment_zones[i], bg=self.root.BG_COLOR))
            zone_labels[i].grid(row=curr_rows, column=0, sticky=NSEW)

            # Day
            day_strings.append(StringVar(self))
            day_strings[i].set(self.date[0])
            day_menus.append(OptionMenu(self, day_strings[i], *self.root.DAYS))
            day_menus[i].configure(bg=self.root.BOX_COLOR)
            day_menus[i]['menu'].configure(bg=self.root.BOX_COLOR)
            day_menus[i].grid(row=curr_rows, column=1, sticky=NSEW)

            # Month
            month_strings.append(StringVar(self))
            month_strings[i].set(self.root.MONTHS[self.date[1]])
            month_menus.append(OptionMenu(self, month_strings[i], *self.root.MONTHS.values()))
            month_menus[i].configure(bg=self.root.BOX_COLOR)
            month_menus[i]['menu'].configure(bg=self.root.BOX_COLOR)
            month_menus[i].grid(row=curr_rows, column=2, sticky=NSEW)

            # Year
            year_strings.append(StringVar(self))
            year_strings[i].set(self.date[2])
            year_menus.append(OptionMenu(self, year_strings[i], *self.root.YEARS))
            year_menus[i].configure(bg=self.root.BOX_COLOR)
            year_menus[i]['menu'].configure(bg=self.root.BOX_COLOR)
            year_menus[i].grid(row=curr_rows, column=3, sticky=NSEW)

            # Time
            time_strings.append(StringVar(self))
            time_strings[i].set(self.time)
            time_menus.append(OptionMenu(self, time_strings[i], *self.root.TIMES[1:]))
            time_menus[i].configure(bg=self.root.BOX_COLOR)
            time_menus[i]['menu'].configure(bg=self.root.BOX_COLOR)
            time_menus[i].grid(row=curr_rows, column=4, sticky=NSEW)

            # Duration
            duration_strings.append(StringVar(self))
            duration_strings[i].set(list(self.root.DURATIONS.keys())[self.duration - 1])
            duration_menus.append(OptionMenu(self, duration_strings[i], *self.root.DURATIONS.keys()))
            duration_menus[i].configure(bg=self.root.BOX_COLOR)
            duration_menus[i]['menu'].configure(bg=self.root.BOX_COLOR)
            duration_menus[i].grid(row=curr_rows, column=5, sticky=NSEW)

            # Move button
            # By using lambda c=i, when the button action is invoked the right corresponding index is used
            # otherwise, i takes the value of its last iteration and everything acts as if the last row buttons are used
            buttons_move.append(
                ctk.CTkButton(self, text='Премести зона ' + self.treatment_zones[i] + ' като нова резервация',
                              command=lambda c=i: self.root.edit_treatments([[self.treatment_ids[c]],
                                                                             [self.treatment_zones[c]],
                                                                             [day_strings[c].get(),
                                                                              [k for k, v in self.root.MONTHS.items() if
                                                                               v == month_strings[c].get()][0],
                                                                              year_strings[c].get()],
                                                                             time_strings[c].get(), self.root.DURATIONS[
                                                                                 duration_strings[c].get()]])))

            buttons_move[i].configure(font=self.root.FONT)
            buttons_move[i].grid(row=curr_rows + 1, column=1, columnspan=3, sticky=NSEW)

            # Delete button
            buttons_delete.append(ctk.CTkButton(self, text='Изтрий зона ' + self.treatment_zones[i],
                                                command=lambda z=i: self.root.delete_treatments(
                                                    [self.treatment_ids[z]])))  # ids[z], date,index_first)))
            buttons_delete[i].configure(font=self.root.FONT)
            buttons_delete[i].grid(row=curr_rows + 1, column=4, columnspan=2, sticky=NSEW)

    def destroy(self):
        self.root.reset_panel_variable('edit_multi')
        Toplevel.destroy(self)
