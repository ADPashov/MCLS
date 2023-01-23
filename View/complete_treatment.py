from tkinter import Toplevel, NSEW, Label, Entry, Grid
import customtkinter as ctk


class CompleteTreatment(Toplevel):
    """
    This panel provides the user interface needed for completing a zone treatment.
    Regardless of whether the booking is for a single zone or a couple of zones, always this panel shows up
    and completes a single zone.
    A treatment is completed when it is performed in reality and the details i, hz and j settings are added.

    Attributes
    ----------
    root: tkinter.Tk
        The object that owns and controls this panel and to whom requests are sent

    customer_data: list
        The name of the customer


    treatment_data: List
        The id and the zone of the given treatment.

    Methods
    -------
    init_widgets()
        Initializes the needed widgets for the panel

    make_resizable()
        Allows for the widgets in the panel to keep their positions and proportions with screen resizing

    """

    def __init__(self, root, customer_data, treatment_data):
        # [[100, 102], [' Предмишници ', ' Цели крака ']]
        # [[103], [' Врат ']]
        """
        Constructs the CompleteTreatment object and initializes the widgets

        Parameters
        ----------
        root
            See class description
        ustomer_data
            See class description
        treatment_data
            See class description
        """
        Toplevel.__init__(self, root)

        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        self.customer_data = customer_data
        self.treatment_data = treatment_data

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

        # # Header label
        # main_label = Label(self,
        #                    text='Завършване на процедура: ' + self.treatment_data[1] + ' на ' + self.customer_data, bg=self.root.BG_COLOR)
        # main_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # Header label
        main_label = Label(self,
                           text='Завършване на процедура на ' + self.customer_data, bg=self.root.BG_COLOR)
        main_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        zone_labels = []

        i_labels = []
        i_boxes = []

        hz_labels = []
        hz_boxes = []

        j_labels = []
        j_boxes = []

        for i in range(len(self.treatment_data[0])):
            zone_labels.append(Label(self, text='Зона: ' + self.treatment_data[1][i], bg=self.root.BG_COLOR))
            zone_labels[i].grid(row=Grid.size(self)[1], column=0, columnspan=2, sticky=NSEW)

            # Impulse widgets
            i_labels.append(Label(self, text='Импулси:', bg=self.root.BG_COLOR))
            i_labels[i].grid(row=Grid.size(self)[1], column=0, sticky=NSEW)

            i_boxes.append(Entry(self, width=10, bg=self.root.BOX_COLOR))
            i_boxes[i].grid(row=Grid.size(self)[1] - 1, column=1, sticky=NSEW)

            # Frequency widgets
            hz_labels.append(Label(self, text='Честота(Hz):', bg=self.root.BG_COLOR))
            hz_labels[i].grid(row=Grid.size(self)[1], column=0, sticky=NSEW)

            hz_boxes.append(Entry(self, width=10, bg=self.root.BOX_COLOR))
            hz_boxes[i].grid(row=Grid.size(self)[1] - 1, column=1, sticky=NSEW)

            # Energy widgets
            j_labels.append(Label(self, text='Джаули(J):', bg=self.root.BG_COLOR))
            j_labels[i].grid(row=Grid.size(self)[1], column=0, sticky=NSEW)

            j_boxes.append(Entry(self, width=10, bg=self.root.BOX_COLOR))
            j_boxes[i].grid(row=Grid.size(self)[1] - 1, column=1, sticky=NSEW)

        complete_button = ctk.CTkButton(self, text='Завърши Процедурата', command=lambda: button_action())
        complete_button.configure(font=self.root.FONT)
        complete_button.grid(row=Grid.size(self)[1], column=0, columnspan=2, sticky=NSEW)

        def button_action():

            data = []
            for i in range(len(self.treatment_data[0])):
                data.append([i_boxes[i].get(), hz_boxes[i].get(), j_boxes[i].get()])
                # data.append([i_boxes[i].get(), hz_boxes[i].get(), j_boxes[i].get()])
            self.root.complete_treatments(self.treatment_data[0], data, self.treatment_data[1])

        # Bind the complete button functionality also to the Enter key
        self.root.bind('<Return>', button_action)

    def destroy(self):
        self.root.reset_panel_variable('complete_treatment')
        Toplevel.destroy(self)
