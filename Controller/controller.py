import datetime
import sqlite3

import smsapi.exception
from smsapi.client import SmsApiBgClient
from transliterate import translit

from Model.model import Model, NotFreeException, NoUserException, NoZoneException
from View.view import View
from thread_with_return import ThreadWithReturn


class Controller:
    def __init__(self):
        self.model = Model(self)
        self.notify_var = None
        self.view = View(self)
        self.sms_client = SmsApiBgClient(
            access_token="28jcabwPJ0yUN4An1Xm91vIXFtkRwdWikNMcHzaj"
        )

        today = self.model.current_date
        sms_date = datetime.date(today[2], today[1], today[0]) + datetime.timedelta(
            days=2
        )
        self.view.display_daily_schedule(
            data=self.model.format_daily_scehdule(
                [sms_date.day, sms_date.month, sms_date.year]
            )
        )
        self.send_reminder_sms([sms_date.day, sms_date.month, sms_date.year])
        self.view.display_daily_schedule(data=self.model.format_daily_scehdule(today))

    # SMS sending
    def send_reminder_sms(self, date):
        data = self.model.format_daily_sms(date)
        result = []
        message_single = "Здравейте, {}! Напомняме Ви, че имате резервация за зона {} на {} от {}. Mon Cheri Laser Studio"
        message_multi = "Здравейте, {}! Напомняме Ви, че имате резервация за зони {} на {} от {}. Mon Cheri Laser Studio"
        for entry in data:
            date_str = ".".join([str(x) for x in date])
            zones = ", ".join(entry[3])
            if len(entry[3]) == 1:
                message = message_single.format(entry[1], zones, date_str, entry[2])
            else:
                message = message_multi.format(entry[1], zones, date_str, entry[2])

            result.append([entry[0], translit(message, "bg", reversed=True)])
            # result.append([entry[0], message])
        flag = True
        no_num = ""
        if not self.model.is_daily_sms_sent(date):
            for item in result:
                if item[0] != "":
                    try:
                        print("Nomer: {}, Text: {}".format(*item))
                        self.sms_client.sms.send(to=item[0], message=item[1], test="1")
                    except smsapi.exception.SendException as e:
                        flag = False
                        print(e)
                else:
                    no_num += ",\nно в деня има клиенти с липсващи номера"

        if flag:
            self.model.set_daily_sms(date)
            self.view.show_error(
                "СМС-ите за {} са изпратени успешно{}".format(
                    self.model.date_to_string(date), no_num
                )
            )
        else:
            self.view.show_error("Грешка при изпращане на СМС")

    # Get constants section
    def get_main_zones(self):
        return self.model.ZONES

    def get_main_times(self):
        return self.model.TIMES

    def get_main_packages(self):
        return self.model.PACKAGES

    def get_main_durations(self):
        return self.model.DURATIONS

    def get_main_operators(self):
        return self.model.OPERATORS

    def get_main_days(self):
        return self.model.DAYS

    def get_main_months(self):
        return self.model.MONTHS

    def get_main_years(self):
        return self.model.YEARS

    # Date and time gettes section
    def get_date_string(self):
        return self.model.date_to_string()

    def get_current_date(self):
        return self.model.get_current_date()

    def get_current_time(self):
        return self.model.current_time

    # Customer getters section
    def find_customer(self, criteria):
        thread = ThreadWithReturn(
            target=self.model.find_customer, args=[criteria], notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        if thread.result == "error":
            self.view.show_error("Въведена невалидна стойност в полето за търсене")
        return thread.result

    def get_customer(self, index):
        thread = ThreadWithReturn(
            target=self.model.get_customer,
            kwargs={"index": index},
            notify_var=self.notify_var,
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        return thread.result

    def get_customer_short(self, customer_id):
        thread = ThreadWithReturn(
            target=self.model.get_customer_short,
            args=[customer_id],
            notify_var=self.notify_var,
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        return thread.result

    def get_current_customer_name(self):
        return self.model.current_customer[1] + " " + self.model.current_customer[2]

    def get_current_customer_data(self):
        return self.model.current_customer

    def get_customer_notes(self):
        thread = ThreadWithReturn(
            target=self.model.get_notes, notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        return thread.result

    def get_customer_note(self, index):
        thread = ThreadWithReturn(
            target=self.model.get_customer_note,
            args=[index],
            notify_var=self.notify_var,
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        return thread.result

    def get_customer_treatments(self):
        thread = ThreadWithReturn(
            target=self.model.format_customer_treatments, notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        return thread.result

    # Other getters
    def get_daily_schedule(self, date):
        thread = ThreadWithReturn(
            target=self.model.format_daily_scehdule,
            args=[date],
            notify_var=self.notify_var,
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        return thread.result

    # Actions section

    # Customer actions
    def add_customer(self, customer_data):
        try:
            data = self.model.validate_customer_data(customer_data)
            thread = ThreadWithReturn(
                target=self.model.add_customer, args=[data], notify_var=self.notify_var
            )
            thread.start()
            self.view.wait_variable(self.notify_var)
            self.view.display_customer(data=thread.result)
            return True
        except ValueError as e:
            match e.__str__():
                case "fname":
                    self.view.show_error("Невалидно първо име")
                case "lname":
                    self.view.show_error("Невалидна фамилия")
                    return False
                case "phone":
                    self.view.show_error("Невалиден телефон")
                    return False
                case "skintype":
                    self.view.show_error("Невалиден тип кожа")
                    return False
                case "mail":
                    self.view.show_error("Невалиден мейл")
                    return False
        except sqlite3.IntegrityError:
            self.view.show_error("Вече съществува клиент с този телефонен номер")
            return False

    def edit_customer(self, field, value):
        try:
            customer_data = self.model.edit_customer(
                [field, self.model.validate_customer_data(value, field)]
            )
            self.view.display_customer(data=customer_data)
        except ValueError as e:
            match e.__str__():
                case "fname":
                    self.view.show_error("Невалидно първо име")
                case "lname":
                    self.view.show_error("Невалидна фамилия")
                case "phone":
                    self.view.show_error("Невалиден телефон")
                case "skintype":
                    self.view.show_error("Невалиден тип кожа")
                case "mail":
                    self.view.show_error("Невалиден мейл")
        except sqlite3.IntegrityError:
            self.view.show_error("Вече съществува клиент с този телефонен номер")

    # Treatment actions
    def book_treatment(self, duration, zones):
        try:
            self.model.is_free(duration)
            self.model.validate_zones(zones)

            t1 = ThreadWithReturn(
                target=self.model.book_treatment,
                args=[duration, zones],
                notify_var=self.notify_var,
            )
            t1.start()
            self.view.wait_variable(self.notify_var)
            new_daily_schedule = self.get_daily_schedule(self.model.current_date)
            self.view.display_daily_schedule(data=new_daily_schedule)
            self.view.display_customer_treatments()
            return True
        except NotFreeException as e:
            self.view.show_error(e.__str__())
            return False

        except NoZoneException as e:
            self.view.show_error(e.__str__())
            return False

    def add_new_zone(self, zone):
        try:
            self.model.validate_zones([zone])
            thread = ThreadWithReturn(
                target=self.model.add_new_zone, args=[zone], notify_var=self.notify_var
            )
            thread.start()
            self.view.wait_variable(self.notify_var)

            new_daily_schedule = self.get_daily_schedule(self.model.current_date)
            self.view.display_daily_schedule(data=new_daily_schedule)
            self.view.display_customer_treatments()
            self.re_select_treatment()
            self.view.destroy_edit_panel()
        except NoZoneException as e:
            self.view.show_error(e.__str__())
            self.view.lift_edit_panel()

    def select_treatment(self, index):
        result = self.model.select_treatment(index)
        self.view.show_panel(*result)

    def display_treatment_user(self, index):
        try:
            customer_id = self.model.get_daily_customer_id(index)

            t1 = ThreadWithReturn(
                target=self.model.get_customer,
                kwargs={"id": customer_id},
                notify_var=self.notify_var,
            )
            t1.start()
            self.view.wait_variable(self.notify_var)
            self.view.show_panel("main")
            self.view.display_customer(data=t1.result)
            return True
        except NoUserException as e:
            self.view.show_error(e.__str__())

    def complete_treatments(self, treatment_id, data):
        try:
            self.model.validate_complete_data(data)
            thread = ThreadWithReturn(
                target=self.model.complete_treatments,
                args=[treatment_id, data],
                notify_var=self.notify_var,
            )
            thread.start()
            self.view.wait_variable(self.notify_var)

            new_daily_schedule = self.get_daily_schedule(self.model.current_date)
            self.view.display_daily_schedule(data=new_daily_schedule)
            self.view.display_customer_treatments()
            self.re_select_treatment()
            return True
        except ValueError:
            self.view.show_error(
                "Невалидни данни в поне едно от полетата.\nДанните трябва да съдържат само числа."
            )
            return False

    def edit_complete_treatment(self, params):
        try:
            self.model.validate_complete_data([[params[1]]])
            thread = ThreadWithReturn(
                target=self.model.edit_complete_treatment,
                args=[params],
                notify_var=self.notify_var,
            )
            thread.start()
            self.view.wait_variable(self.notify_var)

            new_daily_schedule = self.get_daily_schedule(self.model.current_date)
            self.view.display_daily_schedule(data=new_daily_schedule)
            self.view.display_customer_treatments()
            self.re_select_treatment()
            return True
        except ValueError:
            self.view.show_error(
                "Невалидни данни в поне едно от полетата.\nДанните трябва да съдържат само числа."
            )
            return False

    def edit_treatments(self, params):
        try:
            self.model.is_free(date=params[2], time=params[3], duration=params[4])

            thread = ThreadWithReturn(
                target=self.model.edit_treatments,
                args=[params],
                notify_var=self.notify_var,
            )
            thread.start()
            self.view.wait_variable(self.notify_var)

            # Not a one-liner for readability
            # Also don't think new method for a one liner will contribute to readability
            new_daily_schedule = self.get_daily_schedule(self.model.current_date)
            self.view.display_daily_schedule(data=new_daily_schedule)
            self.view.display_customer_treatments()
            self.view.destroy_edit_panel()
            self.re_select_treatment(ids=params[0], flag=params[-1])
        except NotFreeException as e:
            self.view.show_error(e.__str__())
            self.view.lift_edit_panel()

    def delete_treatments(self, params):
        thread = ThreadWithReturn(
            target=self.model.delete_treatments,
            args=[params],
            notify_var=self.notify_var,
        )
        thread.start()
        self.view.wait_variable(self.notify_var)

        new_daily_schedule = self.get_daily_schedule(self.model.current_date)
        self.view.display_daily_schedule(data=new_daily_schedule)
        self.view.display_customer_treatments()
        self.re_select_treatment(ids=params)

    def re_select_treatment(self, ids=[], table="future", flag=True):
        if len(ids) <= 1 and flag and table == "future":
            thread = ThreadWithReturn(
                target=self.model.select_treatment,
                args=[self.model.current_selected_index],
                notify_var=self.notify_var,
            )
            thread.start()
            self.view.wait_variable(self.notify_var)

    def suggest_next_date(self, zones):
        string = self.model.suggest_next_date(zones)
        self.view.show_error(string)

    # Notes actions
    def show_add_note(self):
        try:
            self.view.show_panel("add_note", self.get_current_customer_name())
        except NoUserException as e:
            self.view.show_error(e.__str__())

    def add_note(self, note):
        thread = ThreadWithReturn(
            target=self.model.add_note, args=[note], notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        self.update_notes()

    def edit_note(self, note_data):
        thread = ThreadWithReturn(
            target=self.model.edit_note, args=[note_data], notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)

        self.update_notes()

    def delete_note(self, note_id):
        thread = ThreadWithReturn(
            target=self.model.delete_note, args=[note_id], notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)
        self.update_notes()

    def update_notes(self):
        self.view.flush_screen("notes")
        new_notes = self.get_customer_notes()
        self.view.display_customer_notes(new_notes)

    def set_operator(self, operator):
        thread = ThreadWithReturn(
            target=self.model.set_operator, args=[operator], notify_var=self.notify_var
        )
        thread.start()
        self.view.wait_variable(self.notify_var)

        new_daily_schedule = self.get_daily_schedule(self.model.current_date)
        self.view.display_daily_schedule(data=new_daily_schedule)
