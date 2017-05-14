import psycopg2  # for connection to database
import psycopg2.extras  # for working with database
from datetime import datetime  # for getting date and time obviously


def show_list_of_sessions(db_cursor, current_user_info, current_session_info):
    try:
        this_user_entity_id = current_user_info[2]
        sql_string = "SELECT * FROM Sessions_log ORDER BY time_stamp ASC"
        db_cursor.execute(sql_string)
        abcd = db_cursor.fetchall()
        for i in abcd:
            print(i)
    except psycopg2.Error as e:
        print("┣━━━━━ Error: some unexpected error.", e)
        return current_session_info


def start_session(db_connection, db_cursor, current_user_info, current_session_info):
    try:
        sql_string = "INSERT INTO Sessions_log (entity_id, type, time_stamp) VALUES (%s, %s, %s)"
        current_time = datetime.today()
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
        current_time = datetime.today()
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
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┣━━━━━━━ First you have to login into your account ━━━━━━━━━┫")
        print("┣━ 'r' or 'register' to register if you're new ━━━━━━━━━━━━━┫")
        print("┣━ 'l' or 'login' to login if you're already registered ━━━━┫")
        print("┣━ 'c' or 'clear' if you want to clear your screen ━━━━━━━━━┫")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    else:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┣━━━━━━━━━━━ List of commands available for you ━━━━━━━━━━━━┫")
        print("┣━ 'c' or 'clear' if you want to clear your screen ━━━━━━━━━┫")
        print("┣━ 'o' or 'logout' to logout from your account ━━━━━━━━━━━━━┫")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")