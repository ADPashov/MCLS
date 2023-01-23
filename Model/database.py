import sqlite3 as sq

import psycopg2
import psycopg2 as pg
# from configparser import ConfigParser
import os


# ALTER SEQUENCE customers_customer_id_seq RESTART WITH 2;
# ALTER SEQUENCE treatments_treatment_id_seq RESTART WITH 1;
# Filler treatments will be with customer id = 1, filler filler 00000 0 filler@filler.filler
class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.init_connection()

    def init_connection(self):
        # self.connection = pg.connect(**self.configs())
        self.connection = pg.connect(host = 'db.bit.io',
                                     database = 'pashovv/MCLS',
                                     user = 'pashovv',
                                     password = 'v2_3y7vQ_hbFBwkTcHzbssJCAmTxFTv6',
                                     port = 5432)
        self.cursor = self.connection.cursor()

    # @staticmethod
    # def configs(filename="db_config.ini", section='postgresql'):
    #     parser = ConfigParser()
    #     curr_folder = os.path.dirname(os.path.abspath(__file__))
    #     init_file = os.path.join(curr_folder, filename)
    #     parser.read(init_file)
    #
    #     if parser.has_section(section):
    #         return dict(parser.items(section))
    #     else:
    #         raise Exception

    @staticmethod
    def transform_date(date_param):
        date = date_param.copy()
        date.reverse()
        # Rework list of ints of type[d,m,y] into YYYY-MM-DD
        return '-'.join([str(x) for x in date])

    # Customer actions
    def add_customer(self, customer_data):
        try:
            query = 'INSERT INTO customers(fname, lname, phone, skin_type, mail) VALUES(%s, %s, %s, %s, %s) RETURNING *'

            self.cursor.execute(query, tuple(customer_data))
            self.connection.commit()

            return self.cursor.fetchone()
        except psycopg2.OperationalError:
            self.init_connection()
            return self.add_customer(customer_data)

    def get_customer(self, customer_id):
        try:
            query = 'SELECT * FROM customers WHERE customer_id=%s'
            self.cursor.execute(query, (customer_id,))
            return self.cursor.fetchone()
        except psycopg2.OperationalError:
            self.init_connection()
            return self.get_customer(customer_id)

    def get_customer_short(self, customer_id):
        try:
            query = 'SELECT fname, lname, phone FROM customers WHERE customer_id=%s'
            self.cursor.execute(query, (customer_id,))
            return self.cursor.fetchone()

        except psycopg2.OperationalError:
            self.init_connection()
            self.get_customer_short(customer_id)

    def find_customer(self, data):
        try:
            # Strings to be added to the query, depending on values for which columns are provided
            strings = ['customer_id = %s', 'fname = %s', 'lname = %s', 'phone = %s', 'mail = %s']

            # Base SELECT query to which will be added the needed items for the strings list
            query = 'SELECT * FROM customers WHERE '

            # Search conditions depending on for which columns are provided values
            # It will hold values from the strings list
            conditions = []

            # The values provided for the given conditions
            criteria = []

            # Keeping track of the number of conditions specified by user,
            # as 'AND' will need to be inserted if they're more than 1
            conditions_counter = 0
            for index, entry in enumerate(data):
                # If no search value is entered in the box, there should be empty string
                # Therefore, if entry in data is anything else, it should be search parameter
                if entry != '':
                    # Add the given value to the list of values
                    criteria.append(entry)
                    # Append the corresponding string(part of the query) to the list
                    conditions.append(strings[index])
                    # If this is not the first condition, inser 'AND'
                    if conditions_counter > 0:
                        conditions.append('AND')
                    conditions_counter += 1

            # Format query based on the conditions list
            for item in conditions:
                query += item

            self.cursor.execute(query, (*criteria,))
            return self.cursor.fetchall()
        except psycopg2.OperationalError:
            self.init_connection()
            return self.find_customer(data)
        except psycopg2.errors.InvalidTextRepresentation:
            return 'error'

    def edit_customer(self, customer_id, field, value):
        try:
            query = 'UPDATE customers SET ' + field + ' = %s WHERE customer_id = %s RETURNING *'
            self.cursor.execute(query, (value, customer_id))
            self.connection.commit()
            return self.cursor.fetchone()

        except psycopg2.OperationalError:
            self.init_connection()
            return self.edit_customer(customer_id, field, value)

    # Treatments actions
    def get_customer_treatments(self, customer_id):
        try:
            query = 'SELECT date, time, zone, i, hz, j, is_complete FROM treatments WHERE customer_id=%s'
            self.cursor.execute(query, (customer_id,))
            return self.cursor.fetchall()

        except psycopg2.OperationalError:
            self.init_connection()
            return self.get_customer_treatments(customer_id)

    def book_treatment(self, customer_id, date, time, duration, zones):
        try:
            # Base query to which will be added the values tuples
            base_query = 'INSERT INTO treatments(customer_id, zone, date, time, duration, is_complete) VALUES'

            # Sub-query that will contain the tuples with the values for the actual treatements
            treatments_args = ','.join(self.cursor.mogrify('(%s, %s, %s, %s, %s, %s)'
                                                           , (customer_id, zone, self.transform_date(date), time, duration,
                                                              False)).decode('UTF-8')
                                       for zone in zones)
            print('mogrified: {}'.format(treatments_args))
            self.cursor.execute(base_query + treatments_args)
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.book_treatment(customer_id, date, time, duration, zones)

    def complete_treatments(self, treatment_ids, data):
        try:
            query_single = 'UPDATE treatments SET is_complete = %s, i = %s, hz = %s, j=%s WHERE treatment_id = %s;'

            query = ''
            for index, treatment_id in enumerate(treatment_ids):
                query += self.cursor.mogrify(query_single, (True, *data[index], treatment_id)).decode('UTF-8')

            self.cursor.execute(query)
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.complete_treatments(treatment_ids, data)

    def edit_complete_treatment(self, treatment_id, field, value):
        try:
            query = 'UPDATE treatments SET ' + field + '=%s WHERE treatment_id = %s'
            self.cursor.execute(query, (value, treatment_id))
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.edit_complete_treatment(treatment_id, field, value)

    def get_complete_treatment_data(self, treatment_id):
        try:
            # Returning the treatment_id that is obviouslty known would not slow down the request return
            # However it will contribute to readability when passing argumnets from model.select_treatment()
            query = 'SELECT treatment_id, zone, i, hz, j FROM treatments WHERE treatment_id=%s'
            self.cursor.execute(query, (treatment_id,))
            return self.cursor.fetchone()

        except psycopg2.OperationalError:
            self.init_connection()
            return self.get_complete_treatment_data(treatment_id)

    def delete_treatment(self, treatment_ids):
        try:
            query = 'DELETE FROM treatments WHERE '
            args = ' OR '.join(
                [self.cursor.mogrify('treatment_id = %s', (treatment_id,)).decode('UTF-8') for treatment_id in
                 treatment_ids])
            self.cursor.execute(query + args)
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.delete_treatment(treatment_ids)

    # Notes actions
    def get_notes(self, customer_id):
        try:
            query = 'SELECT note_id, note FROM notes WHERE customer_id=%s'
            self.cursor.execute(query, (customer_id,))
            return self.cursor.fetchall()

        except psycopg2.OperationalError:
            self.init_connection()
            return self.get_notes(customer_id)

    def add_note(self, customer_id, note):
        try:
            query = 'INSERT INTO notes(customer_id, note) VALUES(%s, %s)'
            self.cursor.execute(query, (customer_id, note))
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.add_note(customer_id, note)

    def edit_note(self, note_data):
        try:
            query = self.cursor.mogrify('UPDATE notes SET note=%s WHERE note_id=%s', (note_data[1], note_data[0]))
            self.cursor.execute(query)
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.edit_note(note_data)

    def delete_note(self, note_id):
        try:
            query = 'DELETE FROM notes WHERE note_id=%s'
            self.cursor.execute(query, (note_id,))
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.delete_note(note_id)

    # Calendar actions
    def get_day(self, date):
        try:
            query = 'SELECT treatment_id, time, zone, customer_id, duration, is_complete FROM treatments WHERE date = %s'
            self.cursor.execute(query, (self.transform_date(date),))
            return self.cursor.fetchall()

        except psycopg2.OperationalError:
            self.init_connection()
            return self.get_day(date)

    # Operator actions
    def add_operator(self, date, operator):
        try:
            query = 'INSERT INTO operators(date, operator) VALUES(%s,%s)'
            self.cursor.execute(query, (self.transform_date(date), operator))
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.add_operator(date, operator)

    def update_operator(self, date, operator):
        try:
            query = 'UPDATE operators SET operator=%s WHERE date=%s'
            self.cursor.execute(query, (operator, self.transform_date(date)))
            self.connection.commit()

        except psycopg2.OperationalError:
            self.init_connection()
            self.update_operator(date, operator)

    def get_operator(self, date):
        try:
            query = 'SELECT operator from operators where date=%s'
            self.cursor.execute(query, (self.transform_date(date),))
            return self.cursor.fetchone()

        except psycopg2.OperationalError:
            self.init_connection()
            return self.get_operator(date)

    #

    #

    #

    #

    #
    #
    #
    #

    #

    #

    #
    # def is_free(self, date, time, duration):
    #     data = date + [time]
    #
    #
    #     query1 = 'SELECT * FROM complete_treatments WHERE (day = %s AND month = %s AND year = %s AND time = %s)'
    #     query2 = 'SELECT * FROM future_treatments WHERE (day = %s AND month = %s AND year = %s AND time = %s)'
    #
    #     flag = True
    #     times_index = self.times.index(data[3])
    #     for i in range(0, int(duration)):
    #         res1 = self.cursor.execute(query1, (data[0], data[1], data[2], self.times[times_index + i])).fetchall()
    #         res2 = self.cursor.execute(query2, (data[0], data[1], data[2], self.times[times_index + i])).fetchall()
    #         if res1 or res2:
    #             flag = False
    #     return flag
    #

    #

    #

    #

    # def find_customer(self, data):
    #     strings = ['id = %s', 'fname = %s', 'lname = %s', 'phone = %s', 'mail = %s']
    #
    #     query = 'SELECT * FROM clients WHERE '
    #     conditions = []
    #     criteria = []
    #     for i in range(0, 5):
    #         if data[i] != '':
    #             criteria.append(data[i])
    #             conditions.append(strings[i])
    #
    #     counter = 1
    #     if len(conditions) > 0:
    #         for i in range(0, len(conditions) - 1):
    #             conditions.insert(counter, ' AND ')
    #             counter += 2
    #
    #     for item in conditions:
    #         query += item
    #
    #     self.cursor.execute(query, (*criteria,))
    #     return self.cursor.fetchall()
    #
    # def get_customer(self, customer_id):
    #     query = 'SELECT * FROM clients WHERE id=%s'
    #     self.cursor.execute(query, (customer_id,))
    #     return self.cursor.fetchall()
    #
    # def add_customer(self, customer_data):
    #     fname, lname, phone, skintype, mail = customer_data
    #
    #     self.cursor.execute('INSERT INTO clients(fname, lname, phone, skin_type, mail) VALUES(%s, %s, %s, %s, %s)',
    #                         (fname, lname, phone, mail, skintype))
    #     self.connection.commit()
    #     id = self.cursor.lastrowid
    #
    #     return self.get_customer(id)

    # def edit_customer(self, id, field, value):
    #     query_update = 'UPDATE clients SET ' + field + ' = %s WHERE id = %s'
    #     query_return = 'SELECT * FROM clients WHERE id=%s'
    #     self.cursor.execute(query_update, (value, id))
    #     self.connection.commit()
    #     return self.cursor.execute(query_return, (id,)).fetchall()

    # def get_customer_treatments(self, clid):
    #     query1 = 'SELECT * FROM complete_treatments WHERE clientID=%s'
    #     query2 = 'SELECT * FROM future_treatments WHERE clientID=%s'
    #     result = [*self.cursor.execute(query1, (clid,)).fetchall(), 'futures are next',
    #               *self.cursor.execute(query2, (clid,)).fetchall()]
    #     return result
