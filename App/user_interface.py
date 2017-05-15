import psycopg2  # for connection to database
import psycopg2.extras  # for working with database
from datetime import datetime  # for getting date and time obviously
from time import gmtime, strftime
from entity_ids import *


def create_group(db_cursor, db_connection, current_user_info, group_name_):
    try:
        sql_string = "INSERT INTO Groups (group_name) VALUES (%s)"
        sql_data_tuple = (group_name_,)
        db_cursor.execute(sql_string, sql_data_tuple)
        temp = backend_get_group_id(db_cursor, group_name_)
        sql_string = "INSERT INTO User_groups (group_id, user_id, user_status) VALUES (%s, %s, %s)"
        sql_data_tuple = (temp, current_user_info[1], 1)
        db_cursor.execute(sql_string, sql_data_tuple)
        sql_string = "INSERT INTO Entitys (type, group_id) VALUES (%s, %s)"
        sql_data_tuple = (True, temp)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return


def invite_to_group(db_cursor, db_connection, current_user_info, group_name_, other_user_name):
    try:
        sql_string = "SELECT * FROM User_groups WHERE user_id = %s AND user_status = '1'"
        sql_data_tuple = (current_user_info[1],)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            return
        group_id = backend_get_group_id(db_cursor, group_name_)
        other_user_id = backend_get_user_id(db_cursor, other_user_name)
        sql_string = "INSERT INTO User_groups (group_id, user_id, user_status) VALUES (%s, %s, 2)"
        sql_data_tuple = (group_id, other_user_id)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return


def show_list_of_sessions(db_cursor, current_user_info, current_session_info, amount_of_rows=10):
    try:
        if amount_of_rows <= 0:
            return current_session_info
        amount_of_rows = int(amount_of_rows)

        sql_string = "SELECT * FROM Sessions_log WHERE entity_id = %s ORDER BY time_stamp DESC"
        sql_data_tuple = (current_user_info[2],)
        db_cursor.execute(sql_string, sql_data_tuple)
        sessions_list = db_cursor.fetchall()

        if len(sessions_list) == 0:
            return current_session_info

        amount_of_sessions = len(sessions_list)//2

        if len(sessions_list) < amount_of_rows*2:
            amount_of_rows = len(sessions_list)//2

        end = datetime.strptime(sessions_list[0][3], "%d-%m-%Y %H:%M:%S")
        start = datetime.strptime(sessions_list[1][3], "%d-%m-%Y %H:%M:%S")
        avg_sessions_length = end-start

        for i in range(amount_of_sessions):
            end = datetime.strptime(sessions_list[i*2][3], "%d-%m-%Y %H:%M:%S")
            start = datetime.strptime(sessions_list[i*2+1][3], "%d-%m-%Y %H:%M:%S")
            if i != 0:
                avg_sessions_length += end - start
            if i < amount_of_rows:
                print("┣━ %s spent from |%s| to |%s|" % (str(end - start), str(start), str(end)))

        avg_sessions_length /= amount_of_sessions

        print("┣━━━━━ You've made %s sessions, average duration is: %s" % (amount_of_sessions, avg_sessions_length))

    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return current_session_info


def start_session(db_connection, db_cursor, current_user_info, current_session_info):
    try:
        sql_string = "INSERT INTO Sessions_log (entity_id, type, time_stamp) VALUES (%s, %s, %s)"
        current_time = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        sql_data_tuple = (current_user_info[2], False, current_time)
        db_cursor.execute(sql_string, sql_data_tuple)
        print('┣━━━━━ Session started on %s' % current_time)
        db_connection.commit()
        return [current_user_info[2], False, current_time]
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return current_session_info


def stop_session(db_connection, db_cursor, current_user_info, current_session_info):
    try:
        sql_string = "INSERT INTO Sessions_log (entity_id, type, time_stamp) VALUES (%s, %s, %s)"
        current_time = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        sql_data_tuple = (current_user_info[2], True, current_time)
        db_cursor.execute(sql_string, sql_data_tuple)
        print('┣━━━━━ Session ended on %s' % current_time)
        db_connection.commit()
        return [current_user_info[2], True, current_time]
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return current_session_info


# Help
def frontend_show_help(current_user_info):
    if len(current_user_info) == 0:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  'r' or 'register' to register if you're new                   ┃")
        print("┃  'l' or 'login' to login if you're already registered          ┃")
        print("┃  'c' or 'clear' if you want to clear your screen               ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    else:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  'c' or 'clear' if you want to clear your screen               ┃")
        print("┃  'o' or 'logout' to logout from your account                   ┃")
        print("┃  'g' or 'go' to start a time management session                ┃")
        print("┃  's' or 'stop' to stop a time management session               ┃")
        print("┃  'stats' or 'stats n' to get a list of 10 or n last sessions   ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")