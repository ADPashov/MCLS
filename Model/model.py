import datetime as dt
import time
from itertools import groupby
from operator import itemgetter
from string import Template
from threading import Thread

from database import Database
import re
import csv


class NoUserException(Exception):
    def __init__(self, message='Не е избран потребител'):
        super().__init__(message)


class NotFreeException(Exception):
    def __init__(self, message='Избраните ден, час и продължителност не са свободни'):
        super().__init__(message)


class NoZoneException(Exception):
    def __init__(self, message='Поне една от зоните е невалидна'):
        super().__init__(message)


class Model:
    DAYS = [*range(1, 32)]
    MONTHS = {1: 'Януари', 2: 'Февруари', 3: 'Март', 4: 'Април', 5: 'Май', 6: 'Юни', 7: 'Юли', 8: 'Август',
              9: 'Септември', 10: 'Октомври', 11: 'Ноември', 12: 'Декември'}
    YEARS = [*range(2022, 2030)]

    def __init__(self, controller):
        self.db = Database()

        self.current_customer = []
        self.current_notes = []
        self.current_selected_index = None
        self.current_operator = None

        self.ZONES, self.TIMES, self.PACKAGES, self.DURATIONS, self.OPERATORS, self.NEXT_DAYS = self.read_csvs()

        self.find_customer_results = None

        self.current_date = [dt.datetime.now().day,
                             dt.datetime.now().month,
                             dt.datetime.now().year]

        self.daily_ids = []
        self.daily_treatments_ids = []
        self.daily_durations = []
        self.daily_uniques = []
        self.daily_schedule = None
        self.fillers = {}
        self.reset_calendar_lists()
        self.current_time = None

    @staticmethod
    def read_csvs():
        zones = []
        times = []
        packages = {}
        durations = {}
        operators = []
        next_days = {}

        with open('zones.csv', encoding='utf8') as csvfile:
            z = csv.reader(csvfile, delimiter=',')
            for row in z:
                zones.append(*row)

        with open('times.csv', encoding='utf8') as csvfile:
            z = csv.reader(csvfile, delimiter=',')
            for row in z:
                times.append(*row)

        with open('packages.csv', encoding='utf8') as csvfile:
            z = csv.reader(csvfile, delimiter=',')
            for row in z:
                packages[row[0]] = row[1:]

        with open('durations.csv', encoding='utf8') as csvfile:
            z = csv.reader(csvfile, delimiter=',')
            for row in z:
                durations[row[0]] = int(row[1])

        with open('operators.csv', encoding='utf8') as csvfile:
            z = csv.reader(csvfile, delimiter=',')
            for row in z:
                operators.append(*row)

        with open('next_date.csv', encoding='utf8') as csvfile:
            z = csv.reader(csvfile, delimiter=',')
            for row in z:
                next_days[row[0]] = row[1:]

        return zones, times, packages, durations, operators, next_days

    def date_to_string(self, val=None):
        date = self.current_date if val is None else val

        res = str(date[0])
        match res:
            case 1 | 21 | 31:
                res += '-ви '
            case 2 | 22:
                res += '-ри'
            case 3 | 4 | 23 | 24:
                res += '-ти '
            case 7 | 8 | 27 | 28:
                res += '-ми '
            case _:
                res += '-и '

        res += self.MONTHS[int(date[1])]
        res += ' ' + str(date[2]) + 'г.'
        return res

    def get_current_date(self):
        return self.current_date

    def find_customer(self, criteria):
        self.find_customer_results = self.db.find_customer(criteria)
        return self.find_customer_results

    def add_customer(self, customer_data):
        self.current_customer = self.db.add_customer(customer_data)
        return self.current_customer

    def get_customer(self, index=None, id=None):
        if index is not None:
            self.current_customer = [str(x) for x in self.find_customer_results[index]]
        elif id is not None:
            self.current_customer = self.db.get_customer(id)
        else:
            self.current_customer = self.db.get_customer(self.current_customer[0])
        return self.current_customer

    def book_treatment(self, duration, zones):
        self.db.book_treatment(self.current_customer[0], self.current_date, self.current_time, duration, zones)

    def validate_zones(self, zones):
        for zone in zones:
            if zone not in self.ZONES:
                raise NoZoneException

    def is_free(self, duration, time=None, date=None):
        if date is None:
            date = self.current_date
        if time is None:
            time = self.current_time

        free_times = self.TIMES.copy()

        for treatment in self.db.get_day(date):
            time_index = self.TIMES.index(treatment[1])
            treatment_duration = treatment[4]
            # Avoid showing being occupied by itself
            if self.current_time != treatment[1]:
                for i in range(treatment_duration):
                    free_times[time_index + i] = None

        flag = False
        requested_time_index = self.TIMES.index(time)
        for i in range(duration):
            if free_times[requested_time_index + i] is None:
                flag = True
        if flag:
            raise NotFreeException

    def add_new_zone(self, zone):
        self.db.book_treatment(self.current_customer[0], self.current_date, self.current_time,
                               self.daily_durations[self.current_selected_index], [zone])

    def complete_treatments(self, treatment_id, data):
        self.db.complete_treatments(treatment_id, data)

    def validate_complete_data(self, data):
        for item in data:
            [int(x) for x in item]

    def suggest_next_date(self, zones):
        if len(zones) == 1:
            string = 'Препоръчанa датa за следващo посещениe: \n'
        else:
            string = 'Препоръчани дати за следващи посещения: \n'

        for zone in zones:
            for key in self.NEXT_DAYS.keys():
                bool = zone == self.NEXT_DAYS[key][1]
                if zone in self.NEXT_DAYS[key]:
                    next_date = dt.date(day=self.current_date[0], month=self.current_date[1],
                                        year=self.current_date[2]) + dt.timedelta(days=int(key))

                    string += 'Зона {} - {} \n'.format(zone, self.date_to_string(
                        [next_date.day, next_date.month, next_date.year]))
        return string

    def get_notes(self):
        self.current_notes = self.db.get_notes(self.current_customer[0])
        return self.current_notes

    def add_note(self, note):
        self.db.add_note(self.current_customer[0], note)
        return self.get_notes()

    def format_customer_treatments(self):

        treatments = [list(treatment) for treatment in sorted(self.get_customer_treatments(), key=lambda x: x[2])]
        res = []
        for item in treatments:
            entry = Template('$d.$m.$y | $time | $zone').substitute(d=item[0].day,
                                                                    m=item[0].month,
                                                                    y=item[0].year,
                                                                    time=item[1],
                                                                    zone=item[2])
            if item.pop():
                i, hz, j = item[3:6]
                entry += Template(' | I = $i | Hz = $hz | J = $j').substitute(i=i, hz=hz, j=j)
            res.append(entry)
        return res

    def get_customer_treatments(self):
        return self.db.get_customer_treatments(self.current_customer[0])

    def get_day(self, date):
        return self.db.get_day(date)

    def get_customer_short(self, customer_id):
        return self.db.get_customer_short(customer_id)

    def get_complete_treatment_data(self, treatment_id):
        return self.db.get_complete_treatment_data(treatment_id)

    def validate_customer_data(self, customer_data, field=None):
        match field:
            case 'fname':
                return self.validate_customer_name(customer_data, 'fname')
            case 'lname':
                return self.validate_customer_name(customer_data, 'lname')
            case 'phone':
                return self.validate_customer_phone(customer_data)
            case 'skin_type':
                return self.validate_customer_skintype(customer_data)
            case 'mail':
                return self.validate_customer_mail(customer_data)
            case None:
                fname, lname, phone, skintype, mail = customer_data
                return [self.validate_customer_name(fname, 'fname'),
                        self.validate_customer_name(lname, 'lname'),
                        self.validate_customer_phone(phone),
                        self.validate_customer_skintype(skintype),
                        self.validate_customer_mail(mail)]

    @staticmethod
    def validate_customer_name(name, indicator):
        pattern = r'^[А-Я][а-я]*$'
        # Supporting complex names
        for x in name.split('-'):
            if not re.fullmatch(pattern, x):
                raise ValueError(indicator)
        return name

    @staticmethod
    def validate_customer_phone(phone):
        # phone_pattern_int = r'^\+[1-9]{1}[0-9]{3,14}$'
        pattern_bg = r'^\+359[0-9]{9}$'
        if phone != '':
            if phone[0] == '0':
                phone = '+359' + phone[1:]

        # TODO - remove after past data is entered and all customers have phones
        if phone != '':
            if not re.fullmatch(pattern_bg, phone):
                raise ValueError('phone')
        return phone

    @staticmethod
    def validate_customer_skintype(skintype):
        pattern = r'^[1-4]$'
        if skintype == '':
            skintype = None
        else:
            if not re.fullmatch(pattern, skintype):
                raise ValueError('skintype')
        return skintype

    @staticmethod
    def validate_customer_mail(mail):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if mail != '':
            if not re.fullmatch(pattern, mail):
                raise ValueError('mail')
        return mail

    def format_daily_scehdule(self, date):
        # TODO - chech if this line needs to be uncommented or or the reset calendar lists in the flush calendar method
        # self.flushScreen('calendar')
        result = self.TIMES.copy()
        times = self.TIMES.copy()
        self.reset_calendar_lists()
        self.current_date = date

        self.current_operator = self.get_operator()
        result[0] += self.current_operator[0] if self.current_operator else ''
        # data 1 - past, data 2 - future, fillers - [time, id]
        complete = []
        future = []
        for item in self.get_day(self.current_date):
            if item[-1]:
                complete.append(item[:-1])
            else:
                future.append(item[:-1])

        # complete, future, fillers = self.get_day(self.current_date)
        complete = [x + ('complete',) for x in complete]
        future = [x + ('future',) for x in future]
        # {'13:30': 39, '16:30': 59, '17:00': 60, '17:30': 61}
        # self.fillers = dict(fillers)

        # Sort the results by their start time
        # Results takes form of [[time1, [[zone1, clID, trID, dur, indicator], [zone2, clID, trID, dur, indicator],...]],
        #                        time2, [[zone1, clID, trID, dur, indicator], [zone2, clID, trID, dur, idnicator],...]],
        #                         ........]]]
        temp2 = [list(res) for res in complete + future]
        temp2.sort(key=itemgetter(1))
        res = [[k, [[a, b, x, c, d] for x, y, a, b, c, d in z]] for k, z in groupby(temp2, key=itemgetter(1))]
        # [['11:00', [['Шия', 1, 83, 1, 'future']]], ['14:30', [['Рамене', 1, 6, 1, 'complete']]],
        # ['16:00', [['Цели ръце', 5, 57, 4, 'future'], ['Цели крака', 5, 58, 4, 'future']]]]

        # a list of the numbers as long as the list of times
        # the slots with zones form one booking have the same number
        # different bookings have different values of that number
        counter_uniq = 0
        for x in res:

            # x is [time1, [[zone1, clID, trID, dur, idnicator], [zone2, clID, trID, dur, idnicator],...]]
            time = x[0]
            id = x[1][0][1]
            duration = x[1][0][3]
            indicator = x[1][0][4]  # future or complete

            fname, lname, phone = self.get_customer_short(id)
            pos = result.index(time)
            counter = 0

            for y in x[1]:
                treatment_id = y[2]

                zone = y[0]
                if counter == 0:
                    self.daily_treatments_ids[pos] = (treatment_id, indicator)

                    self.daily_ids[pos] = id
                    self.daily_durations[pos] = duration
                    self.daily_uniques[pos] = counter_uniq
                    string = '' + time + ' | ' + zone + ' | ' + fname + '  ' + lname + ' | ' + phone
                    result[pos] = string
                    counter += 1
                else:
                    self.daily_treatments_ids.insert(pos + 1, (treatment_id, indicator))

                    self.daily_ids.insert(pos + 1, id)
                    self.daily_durations.insert(pos + 1, duration)
                    self.daily_uniques.insert(pos + 1, counter_uniq)
                    string = '_' * (len(time) - 1) + '| ' + zone + ' | ' + ' ' * len(fname) + ' '
                    times.insert(pos + 1, time)
                    result.insert(pos + 1, string)
                    counter += 1

            for i in range(duration - 1):
                result.pop(pos + counter)
            counter_uniq += 1
        self.daily_schedule = result
        return result, times

    def reset_calendar_lists(self):
        length = len(self.TIMES)
        self.daily_ids = [None] * length
        self.daily_treatments_ids = [None] * length
        self.daily_durations = [None] * length
        self.daily_uniques = [None] * length

    def select_treatment(self, real_index):
        entry = self.daily_schedule[real_index]
        index_first = self.daily_uniques.index(self.daily_uniques[real_index])
        self.current_selected_index = index_first
        if entry[0] == '_':
            self.current_time = self.daily_schedule[index_first][0:5]
        else:
            self.current_time = entry[0:5]

        # Book
        if len(entry) == 5:
            return 'book_treatment', [self.get_current_customer_name()]
            # if self.current_customer:
            # else:
            #     raise NoUserException

        if entry[:8] == 'Оператор':
            return 'operator', None

        _, zone, name, _ = self.daily_schedule[index_first].split('|')

        # Edit single
        # TODO - edit if shit works with current_selected_index
        if self.daily_treatments_ids[index_first][1] == 'future' and self.is_single(index_first):
            treatment_data = [self.daily_treatments_ids[index_first][0], zone[1:-1], self.daily_durations[index_first]]

            return 'edit_treatment', [name, treatment_data]


        # Edit multi
        elif self.daily_treatments_ids[index_first][1] == 'future' and not self.is_single(index_first):
            treatment_ids = []
            treatment_zones = []
            for i in range(0, len(self.daily_uniques)):
                if self.daily_uniques[i] == self.daily_uniques[index_first]:
                    treatment_id = self.daily_treatments_ids[i][0]
                    treatment_zone = self.daily_schedule[i].split('|')[1][1:-1]
                    treatment_ids.append(treatment_id)
                    treatment_zones.append(treatment_zone)

            # TODO - see if index_first needs passing or can be omitted
            return 'edit_multi', [name, treatment_ids, treatment_zones,
                                  self.daily_durations[index_first]]

        # Edit complete
        else:
            # Fixing issue where when editing compplete treatment from a multi booking changes the attribute for the first treatment
            self.current_selected_index = real_index
            # TODO - make it more readable
            treatment_data = list(
                self.get_complete_treatment_data(self.daily_treatments_ids[real_index][0]))
            return 'edit_complete', [name, treatment_data]

    def get_daily_customer_id(self, index):
        if self.current_customer or self.daily_ids[index]:
            return self.daily_ids[index]
        else:
            raise NoUserException

    def is_single(self, index):
        return False if self.daily_uniques.count(self.daily_uniques[index]) > 1 else True

    def are_fillers(self, index):
        num_fillers = self.daily_durations[index] - 1
        if num_fillers >= 1:
            filler_times = []
            for i in range(0, num_fillers):
                curr_index_time = self.TIMES.index(self.current_time)
                curr_filler_counter = self.TIMES[curr_index_time + i + 1]
                filler_times.append(curr_filler_counter)

            return [self.fillers[key] for key in filler_times]
        else:
            return []

    def edit_note(self, note_data):
        self.db.edit_note(note_data)

    def delete_note(self, note_id):
        self.db.delete_note(note_id)

    def get_customer_note(self, index):
        return self.current_notes[index]

    def get_current_customer_name(self):
        if self.current_customer:
            return self.current_customer[1] + ' ' + self.current_customer[2]
        else:
            raise NoUserException

    def edit_complete_treatment(self, params):
        self.db.edit_complete_treatment(self.daily_treatments_ids[self.current_selected_index][0], *params)

    def edit_customer(self, params):
        self.db.edit_customer(self.current_customer[0], *params)
        return self.get_customer()

    def delete_treatments(self, treatment_ids):
        self.db.delete_treatment(treatment_ids)

    # TODO - rearrange them in edit panels so we can pass params[0] and params[1:]
    def edit_treatments(self, params):
        treatment_ids_list, zones, date, time, duration = params
        self.delete_treatments(treatment_ids_list)
        self.db.book_treatment(self.daily_ids[self.current_selected_index], date, time, duration, zones)

    def set_operator(self, operator):
        if self.current_operator:
            self.db.update_operator(self.current_date, operator)
        else:
            self.db.add_operator(self.current_date, operator)

    def get_operator(self):
        return self.db.get_operator(self.current_date)
