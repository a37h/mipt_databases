import psycopg2
import psycopg2.extras
import os
import getpass
import time


def db_connect():
    connection_string = 'dbname=mipt_db_project user=mipt_db_project_user ' \
                        'password=ggHkfIJ9aAFxzjmrkIMfWrvC03wZkgpK host=localhost'
    try:
        return psycopg2.connect(connection_string)
    except psycopg2.Error as e:
        print("Can not connect to database. Error:", e)
        exit(0)


def main():
    # create an connection and cursor
    db_connection = db_connect()
    db_cursor = db_connection.cursor()

    current_user_info = []

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣━━━━━ TimeManagementApp3000 ━━━━━━━━━━━━━━┫")
    print("┣━ 'help' or 'h' to get a list of commands ┫")
    print("┣━ 'quit' or 'q' to exit the app ━━━━━━━━━━┫")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    while True:
        try:
            input_line = input('┣ ➤  ')

            if input_line == 'h' or input_line == 'help':
                frontend_show_help(current_user_info)

            elif input_line == 'r' or input_line == 'register':
                if len(current_user_info) == 0:
                    current_user_info = frontend_user_registration(db_cursor)
                    db_connection.commit()
                else:
                    print("┣━━━━━ Error: you are already logged in. Use 'h' or 'help'")

            elif input_line == 'l' or input_line == 'login':
                if len(current_user_info) == 0:
                    current_user_info = frontend_user_login(db_cursor)
                else:
                    print("┣━━━━━ Error: you are already logged in. Use 'h' or 'help'")

            elif input_line == 'q' or input_line == 'quit':
                shutdown_app()

            elif input_line == 'o' or input_line == 'logout':
                if len(current_user_info) == 0:
                    print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                else:
                    print("┣━━━━━ Goodbye, %s" % (current_user_info[0],))
                    current_user_info = []

            elif input_line == 'clear' or input_line == 'c':
                os.system('cls' if os.name == 'nt' else 'clear')

            elif input_line == 'start' or input_line == 's':
                if len(current_user_info) == 0:
                    print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                else:
                    start_session(db_cursor, current_user_info)
                    db_connection.commit()

            else:
                print("┣━━━━━ Error: no such command, try again or use 'h' or 'help'")

        except EOFError:
            shutdown_app()


def start_session(db_cursor, current_user_info):
    try:
        sql_string = "INSERT INTO Sessions_log (entity_id, type, time_stamp) VALUES (%s, %s, %s)"
        current_time = time.time()
        sql_data_tuple = (current_user_info[2], False, current_time)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("Error error error", e)


# Shutdown app safely
def shutdown_app():
    print()
    print('┗━━━━━━━━━━ Peace out ━━━ ◠ ◡ ◠  ━━━━━━━━━━━━━━━')
    print()
    exit(0)


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


# Login (first part)
def frontend_user_login(db_cursor):
    try:
        try:
            name =     input('┣━━━━━ Login: ')
            password = getpass.getpass('┣━━━━━ Password: ')
            return backend_user_login(db_cursor, name, password)
        except KeyboardInterrupt:
            print()
            return []
    except EOFError:
        shutdown_app()


# Login (second part)
def backend_user_login(db_cursor, name, password):
    try:
        sql_string = "SELECT * FROM Users WHERE user_name = %s AND user_password = %s"
        sql_data_tuple = (name, password)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("┣━━━━v Error loggining. Error:", e)
    result = db_cursor.fetchall()
    if len(result) == 1:
        print('┣━━━━━ Success. Welcome, %s' % name)
        new_user_id = backend_get_user_id(db_cursor, name)

        user_entity_id = backend_get_user_entity_id(db_cursor, new_user_id)
        return [name, new_user_id, user_entity_id]
    else:
        print('┣━━━━━ Error: such user doesn\'t exist or password is wrong')
        return ''


# Registration (first part)
def frontend_user_registration(db_cursor):
    try:
        try:
            name = input('┣━━━━━ Please enter your login: ')
            email = input('┣━━━━━ Please enter your email: ')
            password = getpass.getpass('┣━━━━━ Please enter your password: ')
            email_subscription = str(input('┣━━━━━ Email subscription? (y\\n): '))
            if email_subscription == 'y':
                email_subscription = True
            else:
                email_subscription = False
            return backend_register_new_user(db_cursor, name, email, password, email_subscription)
        except KeyboardInterrupt:
            print()
            return []
    except EOFError:
        shutdown_app()


# Registration (second part)
def backend_register_new_user(db_cursor, name, email, password, email_subscrition):
    try:
        sql_string = "INSERT INTO Users (user_name, user_email, user_password, " \
                     "email_sub_agreement) VALUES (%s, %s, %s, %s);"
        sql_data_tuple = (name, email, password, email_subscrition)
        db_cursor.execute(sql_string, sql_data_tuple)

        new_user_id = backend_get_user_id(db_cursor, name)

        sql_string = "INSERT INTO Entitys (type, user_id) VALUES (%s, %s)"
        sql_data_tuple = (False, new_user_id)
        db_cursor.execute(sql_string, sql_data_tuple)

        user_entity_id = backend_get_user_entity_id(db_cursor, new_user_id)

        print("┣━━━━━ Success. You are now logged in,", name)
        return [name, new_user_id, user_entity_id]
    except psycopg2.Error as e:
        print("┣━━━━━ Error registering user. Error:", e)
        return []


# Used in registration and login
def backend_get_user_id(db_cursor, name):
    sql_string = "SELECT user_id FROM Users WHERE user_name = %s"
    sql_data_tuple = (name,)
    db_cursor.execute(sql_string, sql_data_tuple)
    new_user_id_list = db_cursor.fetchall()
    return new_user_id_list[0]

def backend_get_user_entity_id(db_cursor, user_id):
    sql_string = "SELECT entity_id FROM Entitys WHERE user_id = %s"
    sql_data_tuple = (user_id,)
    db_cursor.execute(sql_string, sql_data_tuple)
    new_user_id_list = db_cursor.fetchall()
    return new_user_id_list[0]



main()
