from tkinter import Toplevel, Label, NSEW, Entry, Grid
import customtkinter as ctk


class EditCompletedTreatment(Toplevel):
    """
    This panel provides the user interface needed for editing existing complete(a past treatment that already has
    the additional parameters i,hz and j set) treatment. Allows the user to enter new value for every i, hz and j
    or delete the treatment and sends request to the root.

    Attributes
    ----------
    root: tkinter.Tk
        The object that owns and controls this panel and to whom requests are sent

    customer_data: list
        The names of the user for whom the booking is

    date: List
        The date for which the treatment is currently booked: [day, month, year]

    treatment_data: List
        The specific details of the treatment. [treatment ID, zone, i, hz, j]
        Impulses(j), frequency(hz) and energy(j) are parameters which are specific to each treatment/customer/zone.
        They're added to the treatment after completing the treatment. Hence, treatments that have such data are already
        done and "completed" by the user.
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
        treatment_data
            See class description
        """
        Toplevel.__init__(self, root)
        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.customer_data = customer_data
        self.treatment_data = treatment_data
        print('customer: {} \n treatment: {}'. format(customer_data, treatment_data))

        self.init_widgets()
        self.root.make_resizable(self, wide_rows=[2, 3])

    def init_widgets(self):
        """
        Initializes the needed Label,Entry and Button widgets.
        Adds the corresponding functionality to the buttons for sending requests to root.

        Returns
        -------
        None

        """
        # Header label
        main_label = Label(self, text="Промяна на завършена процедура", bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, columnspan=4, sticky=NSEW)

        # Info labels for customer, zone and date
        date_label = Label(self, text='Дата: ' + self.root.get_date_string(), bg=self.root.BG_COLOR)
        date_label.grid(row=1, column=0, columnspan=4, sticky=NSEW)

        customer_label = Label(self, text='Клиент: ' + self.customer_data, bg=self.root.BG_COLOR)
        customer_label.grid(row=2, column=0, sticky=NSEW)

        zone_label = Label(self, text='Зона: ' + self.treatment_data[1], bg=self.root.BG_COLOR)
        zone_label.grid(row=3, column=0, sticky=NSEW)

        # Impulse widgets
        i_label = Label(self, text='Импулси: ' + str(self.treatment_data[2]), bg=self.root.BG_COLOR)
        i_label.grid(row=2, column=1, sticky=NSEW)

        i_box = Entry(self, bg=self.root.BOX_COLOR, width=20)
        i_box.grid(row=3, column=1, sticky=NSEW)

        i_button = ctk.CTkButton(self, text='Промени импулси',
                                 command=lambda: self.root.edit_complete_treatment(['i', i_box.get()]))

        i_button.configure(font=self.root.FONT)
        i_button.grid(row=4, column=1, sticky=NSEW)

        # Frequency widgets
        hz_label = Label(self, text='Честота: ' + str(self.treatment_data[3]), bg=self.root.BG_COLOR)
        hz_label.grid(row=2, column=2, sticky=NSEW)

        hz_box = Entry(self, bg=self.root.BOX_COLOR, width=20)
        hz_box.grid(row=3, column=2, sticky=NSEW)

        hz_button = ctk.CTkButton(self, text='Промени честота',
                                  command=lambda: self.root.edit_complete_treatment(['hz', hz_box.get()]))
        hz_button.configure(font=self.root.FONT)
        hz_button.grid(row=4, column=2, sticky=NSEW)

        # Energy widgets
        j_label = Label(self, text='Джаули: ' + str(self.treatment_data[4]), bg=self.root.BG_COLOR)
        j_label.grid(row=2, column=3, sticky=NSEW)

        j_box = Entry(self, bg=self.root.BOX_COLOR, width=20)
        j_box.grid(row=3, column=3, sticky=NSEW)

        j_button = ctk.CTkButton(self, text='Промени джаули',
                                 command=lambda: self.root.edit_complete_treatment(['j', j_box.get()]))
        j_button.configure(font=self.root.FONT)
        j_button.grid(row=4, column=3, sticky=NSEW)

        # Delete treatment button
        delete_button = ctk.CTkButton(self, text='Изтрий процедура',
                                      command=lambda: self.root.delete_treatments([self.treatment_data[0]]))
        delete_button.configure(font=self.root.FONT)
        delete_button.grid(row=4, column=0, sticky=NSEW)


    def destroy(self):
        self.root.reset_panel_variable('edit_complete_treatment')
        Toplevel.destroy(self)
