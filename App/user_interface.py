import psycopg2  # for connection to database
import psycopg2.extras  # for working with database
from datetime import datetime  # for getting date and time obviously
from time import gmtime, strftime
from entity_ids import *


def show_groups_list(db_cursor, current_user_info):
    try:
        sql_string = "SELECT Groups.group_id, user_status, group_name FROM User_groups, Groups WHERE user_id = %s AND (user_status = '1' OR user_status = '2') " \
                     "AND User_groups.group_id = Groups.group_id;"
        sql_data_tuple = (current_user_info[1],)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            print("┣━━━━━ Error: you aren't a member or invited to any of groups.")
            return
        else:
            for i in something:
                status = ''
                if i[1] == '1':
                    status = 'member'
                else:
                    status = 'invited'
                print("┣━━ Group name: '%s'. Your status: '%s'" % (i[2], status))
            return
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return


def switch_group(db_cursor, current_user_info, group_name):
    try:
        group_id = backend_get_group_id(db_cursor, group_name)
        if group_id == -1:
            print("┣━━━━━ Error: there is no such group yet.")
            return

        # check if current_user is a member
        sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND user_id = %s AND user_status = '1'"
        sql_data_tuple = (group_id, current_user_info[1],)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            print("┣━━━━━ Error: you aren't a member of that group.")
            return []
        else:
            print("┣━━━━━ Success. Group switched to '%s'" % group_name)
            return [group_name, group_id, backend_get_group_entity_id(db_cursor, group_id)]

    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return


def delete_group(db_cursor, current_user_info, group_name_):
    try:
        group_id = backend_get_group_id(db_cursor, group_name_)
        if group_id == -1:
            print("┣━━━━━ Error: there is no such group yet.")
            return
        # check if current_user is a member
        sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND user_id = %s AND user_status = '1'"
        sql_data_tuple = (group_id, current_user_info[1],)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            print("┣━━━━━ Error: you don't have permission.")
            return
        else:
            sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND (user_status = '1' OR user_status = '2')"
            sql_data_tuple = (group_id,)
            db_cursor.execute(sql_string, sql_data_tuple)
            something = db_cursor.fetchall()
            for i in something:
                sql_string = "UPDATE User_groups SET user_status = '0' WHERE group_id = %s AND user_id = %s;"
                sql_data_tuple = (group_id, i[1])
                db_cursor.execute(sql_string, sql_data_tuple)
                print("┣━━━━━ Success.")
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return


def leave_group(db_cursor, current_user_info, group_name_):
    try:
        group_id = backend_get_group_id(db_cursor, group_name_)
        if group_id == -1:
            print("┣━━━━━ Error: there is no such group yet.")
            return
        # check if current_user is a member
        sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND user_id = %s AND user_status = '1'"
        sql_data_tuple = (group_id, current_user_info[1],)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            print("┣━━━━━ Error: you aren't a member of that group.")
            return
        else:
            sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND (user_status = '1' OR user_status = '2')"
            sql_data_tuple = (group_id,)
            db_cursor.execute(sql_string, sql_data_tuple)
            something = db_cursor.fetchall()
            i = something[0]
            sql_string = "UPDATE User_groups SET user_status = '0' WHERE group_id = %s AND user_id = %s;"
            sql_data_tuple = (group_id, i[1])
            db_cursor.execute(sql_string, sql_data_tuple)
            print("┣━━━━━ Success.")
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return



def join_group(db_cursor, current_user_info, group_name_):
    try:
        # check if group exist
        temp = backend_get_group_id(db_cursor, group_name_)
        if temp == -1:
            print("┣━━━━━ Error: there is no such group yet.")
            return

        # check if current_user is invited
        sql_string = "SELECT * FROM User_groups WHERE user_id = %s AND group_id = %s"
        sql_data_tuple = (current_user_info[1], temp)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            print("┣━━━━━ Error: you are not invited to that group.")
            return
        else:
            if something[0][2] == '0':
                print("┣━━━━━ Error: you are not invited to that group.")
                return
            if something[0][2] == '1':
                print("┣━━━━━ Error: you are already a member.")
                return
            if something[0][2] == '2':
                sql_string = "UPDATE User_groups SET user_status = '1' WHERE group_id = %s AND user_id = %s;"
                sql_data_tuple = (temp, current_user_info[1])
                db_cursor.execute(sql_string, sql_data_tuple)
                print("┣━━━━━ Success.")
                return
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return


def create_group(db_cursor, current_user_info, group_name_):
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


def invite_to_group(db_cursor, current_user_info, group_name_, other_user_name):
    try:
        group_id = backend_get_group_id(db_cursor, group_name_)
        if group_id == -1:
            print("┣━━━━━ Error: there is no such group yet.")
            return

        # check if current_user is a member
        sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND user_id = %s AND user_status = '1'"
        sql_data_tuple = (group_id, current_user_info[1],)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) == 0:
            print("┣━━━━━ Error: you don't have permission.")
            return

        other_user_id = backend_get_user_id(db_cursor, other_user_name)
        if other_user_id == -1:
            print("┣━━━━━ Error: there is no such user yet.")
            return

        # check if adding yourself
        if current_user_info[0] == other_user_name:
            print("┣━━━━━ Error: you can't invite yourself.")
            return

        # check if other user is already a member or invited
        sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND user_id = %s AND (user_status = '1' OR user_status = '2')"
        sql_data_tuple = (group_id, other_user_id,)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) != 0:
            if something[0][2] == 1:
                print("┣━━━━━ Error, that user is already a member.")
            else:
                print("┣━━━━━ Error, that user is already invited.")
            return


        # check if other user is not a member (means he has user_status 0)
        sql_string = "SELECT * FROM User_groups WHERE group_id = %s AND user_id = %s AND user_status = '0'"
        sql_data_tuple = (group_id, other_user_id,)
        db_cursor.execute(sql_string, sql_data_tuple)
        something = db_cursor.fetchall()
        if len(something) != 0:
            sql_string = "UPDATE User_groups SET user_status = '2' WHERE group_id = %s AND user_id = %s;"
            sql_data_tuple = (other_user_id,)
            db_cursor.execute(sql_string, sql_data_tuple)
            print('┣━━━━━ Success.')
            return


        # well we can invite him now
        sql_string = "INSERT INTO User_groups (group_id, user_id, user_status) VALUES (%s, %s, 2)"
        sql_data_tuple = (group_id, other_user_id)
        db_cursor.execute(sql_string, sql_data_tuple)
        print('┣━━━━━ Success.')
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

