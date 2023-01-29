import datetime
from tkinter import Tk, Frame, NSEW, Grid, messagebox, StringVar

from add_customer import AddCustomer
from add_note import AddNote
from book_treatment import BookTreatment
from choose_operator import ChooseOperator
from complete_treatment import CompleteTreatment
from edit_completed_treatment import EditCompletedTreatment
from edit_customer import EditCustomer
from edit_multi import EditMulti
from edit_note import EditNote
from edit_treatment import EditTreatment
from loading_panel import LoadingPanel
from main_panel import MainPanel


class View(Tk):
    """
    The main class of the view package.

    This class is responsible for controlling the GUI of the app.
    It receives data and commands from the Controller package, operates the panels accordingly
    and sends back requests/commands back to the controller.

    ...
    Attributes
    ----------
    BG_COLOR : str
        the backgroound color of the application in a Hex format

    BOX_COLOR : str
        the color of all ListBox, OptionMenu and Entry widgets in a Hex format
    Font : (str, int)
        tuple containing the font and font size of all widgets and panels
    main_frame : tkinter.Frame
        the main panel of the app

    Methods
    -------



    """

    BG_COLOR = "#FE019A"
    BOX_COLOR = "#FF69B4"

    FONT = ("Monotype Corsiva", 18)
    BUTTON_FONT = ("Monotype Corsiva", 25)

    CALENDAR_NORMALBG = "#D30E92"
    CALENDAR_WEEKENDSBG = "#DB76BC"
    CALENDAR_OTHERMONTHBG = "#FFC0EE"
    CALENDAR_OTHERMONTWEHBG = "#ffd2f3"
    CALENDAR_BORDERS = "#7A3E8D"
    CALENDAR_SELECTBG = "#D4A1FE"

    BUTTONS_FG = "#dcb5ff"
    BUTTONS_TEXT = "#FE019A"
    BUTTONS_HOVER = "#b643cd"

    def __init__(self, controller):
        Tk.__init__(self)
        self.controller = controller

        # Panels
        self.main_frame = None
        self.panel_add_customer = None
        self.panel_add_note = None
        self.panel_book_treatment = None
        self.panel_complete_treatment = None
        self.panel_edit_complete_treatment = None
        self.panel_edit_customer = None
        self.panel_edit_multi = None
        self.panel_edit_note = None
        self.panel_edit_treatment = None
        self.panel_choose_operator = None
        self.loading_panel = None
        # self.show_panel('loading')

        self.DURATIONS = self.controller.get_main_durations()
        self.TIMES = self.controller.get_main_times()
        self.ZONES = self.controller.get_main_zones()
        self.PACKAGES = self.controller.get_main_packages()
        self.DAYS = self.controller.get_main_days()
        self.MONTHS = self.controller.get_main_months()
        self.YEARS = self.controller.get_main_years()

        root = Frame(self)
        self.configure(bg=self.BG_COLOR)
        root.option_add("*Font", self.FONT)
        self.controller.notify_var = StringVar()

        self.show_main_panel()

        self.iconbitmap(True, "mc_logo.ico")
        self.title("Mon Cheri Laser Studio")

        # Allows resizability
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    # Constant getters section
    def get_treatment_times(self):
        return self.controller.get_main_times()

    def get_packages(self):
        return self.controller.get_main_packages()

    def get_operators(self):
        return self.controller.get_main_operators()

    def get_current_date(self):
        return self.controller.get_current_date()

    def get_current_time(self):
        return self.controller.get_current_time()

    def get_date_string(self):
        return self.controller.get_date_string()

    # Utility methods section
    @staticmethod
    def show_error(error):
        messagebox.showinfo("Mon Cheri Laser Studio", error)

    @staticmethod
    def make_resizable(panel, wide_cols=[], wide_rows=[]):
        columns, rows = Grid.grid_size(panel)
        for i in range(columns):
            if i in wide_cols:
                panel.columnconfigure(i, weight=3)
            else:
                panel.columnconfigure(i, weight=1)

        for i in range(rows):
            if i in wide_rows:
                panel.rowconfigure(i, weight=3)
            else:
                panel.rowconfigure(i, weight=1)

    def flush_screen(self, screen):
        match screen:
            case "find":
                self.main_frame.flush_find()
            case "select_customer":
                self.main_frame.flush_select_customer()
            case "customer_treatments":
                self.main_frame.flush_customer_treatments()
            case "calendar":
                self.main_frame.flush_calendar()
            case "notes":
                self.main_frame.flush_notes()

    def reset_panel_variable(self, panel):
        match panel:
            case "add_customer":
                self.panel_add_customer = None
            case "add_note":
                self.panel_add_note = None
            case "book_treatment":
                self.panel_book_treatment = None
            case "complete_treatment":
                self.panel_complete_treatment = None
            case "edit_complete_treatment":
                self.panel_edit_complete_treatment = None
            case "edit_customer":
                self.panel_edit_customer = None
            case "edit_multi":
                self.panel_edit_multi = None
            case "edit_note":
                self.panel_edit_note = None
            case "edit_treatment":
                self.panel_edit_treatment = None
            case "operator":
                self.panel_choose_operator = None

    def destroy_edit_panel(self):
        for panel in [
            self.panel_edit_treatment,
            self.panel_edit_multi,
            self.panel_edit_complete_treatment,
        ]:
            if panel:
                panel.destroy()

    # Display panel section
    def show_main_panel(self):
        self.main_frame = MainPanel(self)
        self.main_frame.grid(row=0, column=0, sticky=NSEW)
        self.show_panel("main")

    def display_daily_schedule(self, date=None, data=None):
        self.show_panel("loading")
        if date is not None:
            result, times = self.controller.get_daily_schedule(date)
            self.main_frame.calendar_widgets["calendar"].selection_set(
                datetime.date(date[2], date[1], date[0])
            )
        if data is not None:
            result, times = data
        self.flush_screen("calendar")
        self.main_frame.update_calendar(result, times)
        self.show_panel("main")

    # Controller needs to invoke a function from this class in order for the exceptin to be caught
    # Otherwise, model needs to be imported here, breaking MVC
    def show_add_note(self):
        self.controller.show_add_note()

    def show_panel(self, panel, params=None):
        match panel:
            case "add_customer":
                if self.panel_add_customer:
                    self.panel_add_customer.lift()
                else:
                    self.panel_add_customer = AddCustomer(self)
            case "add_note":
                if self.panel_add_note:
                    self.panel_add_note.lift()
                else:
                    self.panel_add_note = AddNote(self, params)
            case "book_treatment":
                if self.panel_book_treatment:
                    self.panel_book_treatment.lift()
                else:
                    self.panel_book_treatment = BookTreatment(self, *params)
            case "complete_treatment":
                if self.panel_complete_treatment:
                    self.panel_complete_treatment.lift()
                else:
                    self.panel_complete_treatment = CompleteTreatment(self, *params)
            case "edit_complete":
                if self.panel_edit_complete_treatment:
                    self.panel_edit_complete_treatment.lift()
                else:
                    self.panel_edit_complete_treatment = EditCompletedTreatment(
                        self, *params
                    )
            case "edit_customer":
                if self.panel_edit_customer:
                    self.panel_edit_customer.lift()
                else:
                    customer_data = self.controller.get_current_customer_data()
                    if customer_data:
                        self.panel_edit_customer = EditCustomer(self, customer_data)
                    else:
                        self.show_error("Не е избран клиент")
            case "edit_multi":
                if self.panel_edit_multi:
                    self.panel_edit_multi.lift()
                else:
                    self.panel_edit_multi = EditMulti(self, *params)
            case "edit_note":
                if self.panel_edit_note:
                    self.panel_edit_note.lift()
                else:
                    self.panel_edit_note = EditNote(self, *params)
            case "edit_treatment":
                if self.panel_edit_treatment:
                    self.panel_edit_treatment.lift()
                else:
                    self.panel_edit_treatment = EditTreatment(self, *params)
            case "operator":
                if self.panel_choose_operator:
                    self.panel_choose_operator.lift()
                else:
                    self.panel_choose_operator = ChooseOperator(self)
            case "loading":
                self.loading_panel = LoadingPanel(self)
                self.loading_panel.tkraise()
            case "main":
                self.loading_panel = None
                self.main_frame.tkraise()

    # Allowing for the right panel to be lifted in case controller.edit_treatment catches exception
    def lift_edit_panel(self):
        if self.panel_edit_treatment:
            self.show_panel("edit_treatment")
        else:
            self.show_panel("edit_multi")

    # Actions section

    # Customer actions
    def add_customer(self, customer_data):
        self.show_panel("loading")
        if self.controller.add_customer(customer_data):
            self.panel_add_customer.destroy()
        else:
            self.show_panel("add_customer")
        self.show_panel("main")

    def find_customer(self, criteria):
        self.show_panel("loading")
        self.flush_screen("find")
        results = self.controller.find_customer(criteria)
        self.update_results(results)
        self.show_panel("main")

    def edit_customer(self, field, value):
        self.show_panel("loading")
        self.controller.edit_customer(field, value)
        self.show_panel("edit_customer")
        self.show_panel("main")

    # Customer displaying methods
    def update_results(self, results):
        if len(results) == 1:
            self.display_customer(index=0)
        else:
            for i in range(0, len(results)):
                self.main_frame.insert_result(i, results[i][:-2])

    def display_customer(self, index=None, data=None):
        self.show_panel("loading")
        if data is not None:
            customer_data = data
        if index is not None:
            customer_data = self.controller.get_customer(index)
        self.flush_screen("select_customer")
        self.main_frame.update_customer_labels(customer_data)
        self.display_customer_notes()
        self.display_customer_treatments()
        self.show_panel("main")

    def display_customer_notes(self, notes=None):
        # When updating notes after inserting a note, the mnotes are passed as argument
        # If no notes are passed, ask controller for them
        if not notes:
            notes = self.controller.get_customer_notes()
        # Display notes
        num_notes = len(notes)
        self.main_frame.resize_notes_box(num_notes + 1)
        for i in range(0, num_notes):
            self.main_frame.insert_note(i, notes[i][1])

    def display_customer_treatments(self):
        self.flush_screen("customer_treatments")
        data = self.controller.get_customer_treatments()
        if data:
            for i in range(0, len(data)):
                self.main_frame.insert_customer_treatment(i, data[i])

    def display_treatment_user(self, index):
        return self.controller.display_treatment_user(index)

    # Treatment Actions
    def book_treatment(self, duration, zones):
        self.show_panel("loading")
        self.lift()
        flag = self.controller.book_treatment(duration, zones)
        if flag:
            self.panel_book_treatment.destroy()
        else:
            self.show_panel("book_treatment")
        self.show_panel("main")

    # TODO - rename to add zone to treatment or something
    def add_new_zone(self, zone):
        self.show_panel("loading")
        self.controller.add_new_zone(zone)
        self.show_panel("main")

    def complete_treatments(self, treatment_id, data, zones):
        self.show_panel("loading")
        if self.controller.complete_treatments(treatment_id, data):
            self.panel_complete_treatment.destroy()
            self.destroy_edit_panel()
            self.suggest_next_date(zones)
        else:
            self.show_panel("complete_treatment")

        self.show_panel("main")

    def select_treatment(self, real_index):
        # To avoid situations where excepetion is thrown in display treatment user
        # and execution continues with select treatment
        res = self.display_treatment_user(real_index) if real_index > 0 else False
        # self.show_panel('loading')
        if res or real_index == 0:
            self.controller.select_treatment(real_index)
        # self.show_panel('main')

    def delete_treatments(self, params):
        self.show_panel("loading")
        self.controller.delete_treatments(params)
        self.destroy_edit_panel()
        self.show_panel("main")

    def edit_treatments(self, params):
        self.show_panel("loading")
        self.controller.edit_treatments(params)
        self.show_panel("main")

    def suggest_next_date(self, zones):
        self.show_panel("loading")
        self.controller.suggest_next_date(zones)
        self.show_panel("main")

    def edit_complete_treatment(self, params):
        self.show_panel("loading")
        if self.controller.edit_complete_treatment(params):
            self.panel_edit_complete_treatment.destroy()
        else:
            self.show_panel("edit_complete")
        self.show_panel("main")

    # Note actions

    def select_note(self, index):
        self.show_panel("loading")
        note = self.controller.get_customer_note(index)
        name = self.controller.get_current_customer_name()
        self.show_panel("edit_note", [name, note])
        self.show_panel("main")

    def add_note(self, note):
        self.show_panel("loading")
        self.controller.add_note(note)
        self.panel_add_note.destroy()
        self.show_panel("main")

    def edit_note(self, note_data):
        self.show_panel("loading")
        self.controller.edit_note(note_data)
        self.panel_edit_note.destroy()
        self.show_panel("main")

    def delete_note(self, note_id):
        self.show_panel("loading")
        self.controller.delete_note(note_id)
        self.panel_edit_note.destroy()
        self.show_panel("main")

    # Operator actions
    def set_operator(self, operator):
        self.show_panel("loading")
        self.controller.set_operator(operator)
        self.panel_choose_operator.destroy()
        self.show_panel("main")
