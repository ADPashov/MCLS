import datetime
from tkinter import Frame, Label, NSEW, Entry, Listbox, END

import customtkinter as ctk
import tkcalendar as tkcalendar


class MainPanel(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)

        self.root = root
        self.configure(bg=self.root.BG_COLOR)

        # Initialize widgets responsible for searching for a customer
        self.find_widgets = {}
        self.init_find()

        # Initialize widgets responsible for displaying a customer after searching
        self.customer_widgets = {}
        self.init_customer()

        # Initialize widgets responsible for displaying the calendar

        self.calendar_widgets = {}
        self.init_calendar()

        # self.root.make_resizable(self)
        self.root.make_resizable(self, wide_rows=[7, 9])
        self.double_click_flag = False

    def init_find(self):
        """
        Initializes the widgets responsible for finding a customer.
        Includes the Label and Entry widgets for the search criteria fields, as well a search button
        and a results box.

        Returns
        -------
        None

        """

        # Section header label
        self.find_widgets["find_label"] = Label(
            self, text="Търсене на клиент", bg=self.root.BG_COLOR
        )
        self.find_widgets["find_label"].grid(row=0, column=1, sticky=NSEW)

        # ID widgets
        self.find_widgets["id_label"] = Label(
            self, text="Кл. номер", bg=self.root.BG_COLOR
        )
        self.find_widgets["id_label"].grid(row=1, column=0, sticky=NSEW)

        self.find_widgets["id_box"] = Entry(self, bg=self.root.BOX_COLOR)
        self.find_widgets["id_box"].grid(row=1, column=1, sticky=NSEW)

        # First name widgets
        self.find_widgets["fname_label"] = Label(
            self, text="Име", bg=self.root.BG_COLOR
        )
        self.find_widgets["fname_label"].grid(row=2, column=0, sticky=NSEW)

        self.find_widgets["fname_box"] = Entry(self, bg=self.root.BOX_COLOR)
        self.find_widgets["fname_box"].grid(row=2, column=1, sticky=NSEW)

        # Last name widgets
        self.find_widgets["lname_label"] = Label(
            self, text="Фамилия", bg=self.root.BG_COLOR
        )
        self.find_widgets["lname_label"].grid(row=3, column=0, sticky=NSEW)

        self.find_widgets["lname_box"] = Entry(self, bg=self.root.BOX_COLOR)
        self.find_widgets["lname_box"].grid(row=3, column=1, sticky=NSEW)

        # Phone number widgets
        self.find_widgets["phone_label"] = Label(
            self, text="Телефон", bg=self.root.BG_COLOR
        )
        self.find_widgets["phone_label"].grid(row=4, column=0, sticky=NSEW)

        self.find_widgets["phone_box"] = Entry(self, bg=self.root.BOX_COLOR)
        self.find_widgets["phone_box"].grid(row=4, column=1, sticky=NSEW)

        # Mail widgets
        self.find_widgets["mail_label"] = Label(
            self, text="Имейл", bg=self.root.BG_COLOR
        )
        self.find_widgets["mail_label"].grid(row=5, column=0, sticky=NSEW)

        self.find_widgets["mail_box"] = Entry(self, bg=self.root.BOX_COLOR)
        self.find_widgets["mail_box"].grid(row=5, column=1, sticky=NSEW)

        # Find button
        self.find_widgets["find_button"] = ctk.CTkButton(
            self,
            text="Намиране на клиент",
            command=lambda: self.find_customer(None),
            fg_color=self.root.BUTTONS_FG,
            text_color=self.root.BUTTONS_TEXT,
            hover_color=self.root.BUTTONS_HOVER,
        )
        self.find_widgets["find_button"].configure(font=self.root.BUTTON_FONT)
        self.find_widgets["find_button"].grid(
            row=6, column=0, columnspan=2, sticky=NSEW
        )

        # Bind the same search functionality also to the Enter key
        self.root.bind("<Return>", self.find_customer)

        # Results box
        self.find_widgets["results_box"] = Listbox(
            self,
            bg=self.root.BOX_COLOR,
            width=35,
            highlightbackground=self.root.BG_COLOR,
        )
        self.find_widgets["results_box"].grid(
            row=7, column=0, rowspan=3, columnspan=2, sticky=NSEW
        )

        # self.find_widgets['xscroll'] = Scrollbar(self, orient=HORIZONTAL)
        # self.find_widgets['results_box'].config(xscrollcommand=self.find_widgets['xscroll'].set)
        # self.find_widgets['xscroll'].config(command=self.find_widgets['results_box'].xview)
        # self.find_widgets['xscroll'].grid(row=10, column=0, columnspan=2, sticky=NSEW)

        # Bind method to a Listbox click
        self.find_widgets["results_box"].bind("<<ListboxSelect>>", self.select_customer)

        # Not part of the actual find functionalities, but is placed in the same section of the main panel
        self.find_widgets["add_button"] = ctk.CTkButton(
            self,
            text="Добавяне на клиент",
            command=lambda: self.root.show_panel("add_customer"),
            fg_color=self.root.BUTTONS_FG,
            text_color=self.root.BUTTONS_TEXT,
            hover_color=self.root.BUTTONS_HOVER,
        )
        self.find_widgets["add_button"].configure(font=self.root.BUTTON_FONT)
        self.find_widgets["add_button"].grid(
            row=10, column=0, columnspan=2, sticky=NSEW
        )

    def find_customer(self, event):
        self.root.find_customer(self.get_search_criteria())

    def select_customer(self, event):
        # Stops random errors resulting from clicks outside active indices to pop up
        try:
            index = self.find_widgets["results_box"].curselection()[0]
            self.root.display_customer(index)

        except IndexError as e:
            pass

    def get_search_criteria(self):
        """
        Gets the contents of all text boxes in the search section and puts them in a list

        Returns
        -------
        List of the values currently in the search criteria fields
        """
        return [
            self.find_widgets["id_box"].get(),
            self.find_widgets["fname_box"].get().capitalize(),
            self.find_widgets["lname_box"].get().capitalize(),
            self.find_widgets["phone_box"].get(),
            self.find_widgets["mail_box"].get(),
        ]

    def insert_result(self, pos, text):
        self.find_widgets["results_box"].insert(pos, text)

    def init_customer(self):
        """
        Initializes the widgets needed for showing and interacting with customer data.
        Includes: labels, showing the customer data
                  notes text box
                  customer treatments text box
                  buttons for adding notes and editing customer

        Returns
        -------
        None
        """

        # Section Header Label
        self.customer_widgets["text_customer"] = Label(
            self, text="Клиент", bg=self.root.BG_COLOR
        )
        self.customer_widgets["text_customer"].grid(
            row=0, column=2, columnspan=2, sticky=NSEW
        )

        # ID labels
        self.customer_widgets["id_label"] = Label(
            self, text="Клиентски номер", bg=self.root.BG_COLOR
        )
        self.customer_widgets["id_label"].grid(row=1, column=2, sticky=NSEW)

        self.customer_widgets["id_result"] = Label(self, text="", bg=self.root.BG_COLOR)
        self.customer_widgets["id_result"].grid(row=1, column=3, sticky=NSEW)

        # Name labels
        self.customer_widgets["name_label"] = Label(
            self, text="Име", bg=self.root.BG_COLOR
        )
        self.customer_widgets["name_label"].grid(row=2, column=2, sticky=NSEW)

        self.customer_widgets["name_result"] = Label(
            self, text="", bg=self.root.BG_COLOR
        )
        self.customer_widgets["name_result"].grid(row=2, column=3, sticky=NSEW)

        # Skin type labels
        self.customer_widgets["skintype_label"] = Label(
            self, text="Фототип Кожа", bg=self.root.BG_COLOR
        )
        self.customer_widgets["skintype_label"].grid(row=3, column=2, sticky=NSEW)

        self.customer_widgets["skintype_result"] = Label(
            self, text="", bg=self.root.BG_COLOR
        )
        self.customer_widgets["skintype_result"].grid(row=3, column=3, sticky=NSEW)

        # Phone number labels
        self.customer_widgets["phone_label"] = Label(
            self, text="Телефон", bg=self.root.BG_COLOR
        )
        self.customer_widgets["phone_label"].grid(row=4, column=2, sticky=NSEW)

        self.customer_widgets["phone_result"] = Label(
            self, text="", bg=self.root.BG_COLOR
        )
        self.customer_widgets["phone_result"].grid(row=4, column=3, sticky=NSEW)

        # Mail labels
        self.customer_widgets["mail_label"] = Label(
            self, text="Имейл", bg=self.root.BG_COLOR
        )
        self.customer_widgets["mail_label"].grid(row=5, column=2, sticky=NSEW)

        self.customer_widgets["mail_result"] = Label(
            self, text="", bg=self.root.BG_COLOR
        )
        self.customer_widgets["mail_result"].grid(row=5, column=3, sticky=NSEW)

        # Notes label and text box
        self.customer_widgets["notes_label"] = Label(
            self, text="Бележки на клиента", bg=self.root.BG_COLOR
        )
        self.customer_widgets["notes_label"].grid(
            row=6, column=2, columnspan=2, sticky=NSEW
        )

        self.customer_widgets["notes_box"] = Listbox(
            self,
            bg=self.root.BOX_COLOR,
            width=50,
            height=1,
            highlightbackground=self.root.BG_COLOR,
        )
        self.customer_widgets["notes_box"].grid(
            row=7, column=2, columnspan=2, sticky=NSEW
        )
        self.customer_widgets["notes_box"].bind("<<ListboxSelect>>", self.select_note)

        # Treatments label and text box
        self.customer_widgets["text_treatments"] = Label(
            self, text="Процедури на клиента", bg=self.root.BG_COLOR
        )
        self.customer_widgets["text_treatments"].grid(
            row=8, column=2, columnspan=2, sticky=NSEW
        )

        self.customer_widgets["treatments_box"] = Listbox(
            self,
            bg=self.root.BOX_COLOR,
            width=50,
            highlightbackground=self.root.BG_COLOR,
        )
        self.customer_widgets["treatments_box"].grid(
            row=9, column=2, columnspan=2, sticky=NSEW
        )
        self.customer_widgets["treatments_box"].bind(
            "<<ListboxSelect>>", self.select_customer_treatment
        )

        # self.customer_widgets['xscroll'] = Scrollbar(self, orient=HORIZONTAL, bd=10)
        # self.customer_widgets['treatments_box'].config(xscrollcommand=self.customer_widgets['xscroll'].set)
        # self.customer_widgets['xscroll'].config(command=self.customer_widgets['treatments_box'].xview)
        # self.customer_widgets['xscroll'].grid(row=10, column=2, columnspan=2, sticky = NSEW)

        # Edit customer button
        self.customer_widgets["edit_button"] = ctk.CTkButton(
            self,
            text="Промяна на клиент",
            command=lambda: self.root.show_panel("edit_customer"),
            fg_color=self.root.BUTTONS_FG,
            text_color=self.root.BUTTONS_TEXT,
            hover_color=self.root.BUTTONS_HOVER,
        )
        self.customer_widgets["edit_button"].configure(font=self.root.BUTTON_FONT)
        self.customer_widgets["edit_button"].grid(row=10, column=2, sticky=NSEW)

        # Add note to customer button
        self.customer_widgets["add_note"] = ctk.CTkButton(
            self,
            text="Добавяне на бележка",
            command=lambda: self.root.show_add_note(),
            fg_color=self.root.BUTTONS_FG,
            text_color=self.root.BUTTONS_TEXT,
            hover_color=self.root.BUTTONS_HOVER,
        )
        self.customer_widgets["add_note"].configure(font=self.root.BUTTON_FONT)
        self.customer_widgets["add_note"].grid(row=10, column=3, sticky=NSEW)

    def select_note(self, event):
        index = self.customer_widgets["notes_box"].curselection()[0]
        self.root.select_note(index)
        # self.show_edit_note([self.current_notes_ids[index], note])

    def update_customer_labels(self, customer_data):
        # Decompose customer data
        id, fname, lname, phone, skintype, mail = customer_data
        # Set label values to customer daata
        self.customer_widgets["id_result"].configure(text=str(id))
        self.customer_widgets["name_result"].configure(text=fname + " " + lname)
        self.customer_widgets["skintype_result"].configure(text=skintype)
        self.customer_widgets["phone_result"].configure(text=phone)
        self.customer_widgets["mail_result"].configure(text=mail)

    def insert_note(self, pos, text):
        self.customer_widgets["notes_box"].insert(pos, text)

    def resize_notes_box(self, height):
        self.customer_widgets["notes_box"].configure(height=height)

    def insert_customer_treatment(self, pos, text):
        self.customer_widgets["treatments_box"].insert(pos, text)

    def init_calendar(self):
        date = [
            datetime.datetime.now().day,
            datetime.datetime.now().month,
            datetime.datetime.now().year,
        ]
        # Remove if no issues occur
        self.calendar_widgets[
            "treatment_times"
        ] = self.root.get_treatment_times().copy()
        # Calendar label
        self.calendar_widgets["text"] = Label(
            self, text="Календар", bg=self.root.BG_COLOR
        )
        self.calendar_widgets["text"].grid(row=0, column=4, sticky=NSEW)
        # Actual calendar
        self.calendar_widgets["calendar"] = tkcalendar.Calendar(
            self,
            selectmode="day",
            year=date[2],
            month=date[1],
            day=date[0],
            width=45,
            borderwidth=1,
            font=self.root.FONT,
            showweeknumbers=False,
        )
        self.calendar_widgets["calendar"].grid(row=1, column=4, rowspan=6, sticky=NSEW)
        self.calendar_widgets["calendar"].bind(
            "<<CalendarSelected>>", self.request_daily_schedule
        )
        self.calendar_widgets["calendar"].configure(background=self.root.BOX_COLOR)
        self.calendar_widgets["calendar"].configure(
            headersbackground=self.root.BOX_COLOR
        )
        self.calendar_widgets["calendar"].configure(
            normalbackground=self.root.CALENDAR_NORMALBG
        )
        self.calendar_widgets["calendar"].configure(
            weekendbackground=self.root.CALENDAR_WEEKENDSBG
        )
        self.calendar_widgets["calendar"].configure(
            othermonthbackground=self.root.CALENDAR_OTHERMONTHBG
        )
        self.calendar_widgets["calendar"].configure(
            othermonthwebackground=self.root.CALENDAR_OTHERMONTWEHBG
        )
        self.calendar_widgets["calendar"].configure(
            bordercolor=self.root.CALENDAR_BORDERS
        )
        self.calendar_widgets["calendar"].configure(
            selectbackground=self.root.CALENDAR_SELECTBG
        )
        # Daily scehdule box
        self.calendar_widgets["box"] = Listbox(
            self,
            bg=self.root.BOX_COLOR,
            width=45,
            highlightbackground=self.root.BG_COLOR,
        )
        self.calendar_widgets["box"].grid(column=4, row=7, rowspan=3, sticky=NSEW)
        self.calendar_widgets["box"].bind(
            "<<ListboxSelect>>", self.display_treatment_user
        )
        self.calendar_widgets["box"].bind("<Double-1>", self.select_treatment)

        # self.calendar_widgets['xscroll'] = Scrollbar(self, orient=HORIZONTAL, bd=10)
        # self.calendar_widgets['box'].config(xscrollcommand=self.calendar_widgets['xscroll'].set)
        # self.calendar_widgets['xscroll'].config(command=self.calendar_widgets['box'].xview)
        # self.calendar_widgets['xscroll'].grid(row=10, column=4, sticky=NSEW)

        # Show today button
        self.calendar_widgets["show_today_button"] = ctk.CTkButton(
            self,
            text="Покажи днес",
            command=lambda x=date: self.show_today(x),
            fg_color=self.root.BUTTONS_FG,
            text_color=self.root.BUTTONS_TEXT,
            hover_color=self.root.BUTTONS_HOVER,
        )
        self.calendar_widgets["show_today_button"].configure(font=self.root.BUTTON_FONT)
        self.calendar_widgets["show_today_button"].grid(row=10, column=4, sticky=NSEW)

    # TODO - check for redundancy as this is replaced with self.results[index]
    # def get_calendar_box(self, index):
    #     return self.calendar_widgets['box'].get(index)

    def display_treatment_user(self, event):
        self.root.after(300, self.calendar_click_action)

    def select_treatment(self, event):
        self.double_click_flag = True

    def calendar_click_action(self):
        if self.double_click_flag:
            try:
                index = self.calendar_widgets["box"].curselection()[0]
                self.root.select_treatment(index)
            except IndexError:
                pass
            finally:
                self.double_click_flag = False
        else:
            self.root.display_treatment_user(
                self.calendar_widgets["box"].curselection()[0]
            )

    def select_customer_treatment(self, event):
        index = self.customer_widgets["treatments_box"].curselection()[0]
        data = self.customer_widgets["treatments_box"].get(index)
        d, m, y = data.split("|")[0].split(".")
        self.root.display_daily_schedule(date=[int(d), int(m), int(y) + 2000])

    def show_today(self, today):
        self.root.display_daily_schedule(today)
        self.calendar_widgets["calendar"].selection_set(
            datetime.date(today[2], today[1], today[0])
        )

    def request_daily_schedule(self, event):
        m, d, y = self.calendar_widgets["calendar"].get_date().split("/")
        self.root.display_daily_schedule(date=[int(d), int(m), int(y) + 2000])

    def update_calendar(self, result, times):
        for i in range(0, len(result)):
            self.calendar_widgets["box"].insert(i, result[i])
        self.calendar_widgets["treatment_times"] = times

    def flush_find(self):
        self.find_widgets["results_box"].delete(
            0, self.find_widgets["results_box"].size()
        )

    def flush_select_customer(self):
        self.find_widgets["results_box"].delete(
            0, self.find_widgets["results_box"].size()
        )
        self.find_widgets["id_box"].delete(0, END)
        self.find_widgets["fname_box"].delete(0, END)
        self.find_widgets["lname_box"].delete(0, END)
        self.find_widgets["phone_box"].delete(0, END)
        self.find_widgets["mail_box"].delete(0, END)
        self.customer_widgets["notes_box"].delete(
            0, self.customer_widgets["notes_box"].size()
        )
        self.flush_customer_treatments()

    def flush_customer_treatments(self):
        self.customer_widgets["treatments_box"].delete(
            0, self.customer_widgets["treatments_box"].size()
        )

    def flush_calendar(self):
        self.calendar_widgets[
            "treatment_times"
        ] = self.root.get_treatment_times().copy()
        self.calendar_widgets["box"].delete(0, self.calendar_widgets["box"].size())
        # for i in range(0, len(self.calendar_widgets['treatment_times'])):
        #     self.calendar_widgets['box'].insert(i, self.calendar_widgets['treatment_times'][i])
        # TODO - if this one need uncommenting move it to view method
        # self.root.reset_calendar_lists()

    def flush_notes(self):
        self.customer_widgets["notes_box"].delete(
            0, self.customer_widgets["notes_box"].size()
        )
