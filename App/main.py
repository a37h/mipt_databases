import psycopg2
import psycopg2.extras


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

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣━━━━━ TimeManagementApp3000 ━━━━━━━━━━━━━━┫")
    print("┣━ 'help' or 'h' to get a list of commands ┫")
    print("┣━ 'quit' or 'q' to exit the app ━━━━━━━━━━┫")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    while True:
        try:
            input_line = input('➤ ')
            parser = {'r': frontend_user_registration,
                      'register': frontend_user_registration,
                      'l': frontend_user_login,
                      'login': frontend_user_login,
                      'h': frontend_help,
                      'help': frontend_help}
        except EOFError:
            print()
            exit(0)
        try:
            activate = parser[input_line]
            activate(db_cursor)
        except KeyError:
            print("┣━━━━┫ Error: no such command, try again or use 'h' or 'help'")


def frontend_help(*args):
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣━ If you're new then register by typing 'r' or 'register' ━┫")
    print("┣━ To login with your name and password type 'l' or 'login' ┫")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


def frontend_user_login(db_cursor):
    name =     input('┣━━━━┫ Login: ')
    password = input('┣━━━━┫ Password: ')
    backend_user_login(db_cursor, name, password)


def frontend_user_registration(db_cursor):
    name = input('┣━━━━┫ Please enter your login: ')
    email = input('┣━━━━┫ Please enter your email: ')
    password = input('┣━━━━┫ Please enter your password: ')
    email_subscription = str(input('┣━━━━┫ Email subscription? (y\\n): '))
    if email_subscription == 'y':
        email_subscription = True
    else:
        email_subscription = False
    backend_register_new_user(db_cursor, name, email, password, email_subscription)


def backend_user_login(db_cursor, name, password):
    try:
        sql_string = "SELECT * FROM Users WHERE user_name = %s AND user_password = %s"
        sql_data_tuple = (name, password)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("┣━━━━┫ Error loggining. Error:", e)
    result = db_cursor.fetchall()
    if len(result) == 1:
        print('┣━━━━┫ Success. Welcome, %s' % name)
    else:
        print('┣━━━━┫ Error: such user doesn\'t exist or password is wrong')


def backend_register_new_user(db_cursor, name, email, password, email_subscrition):
    try:
        sql_string = "INSERT INTO Users (user_name, user_email, user_password, " \
                     "email_sub_agreement) VALUES (%s, %s, %s, %s);"
        sql_data_tuple = (name, email, password, email_subscrition)
        db_cursor.execute(sql_string, sql_data_tuple)

        sql_string = "SELECT user_id FROM Users WHERE user_name = %s"
        sql_data_tuple = (name,)
        db_cursor.execute(sql_string, sql_data_tuple)

        new_user_id_list = db_cursor.fetchall()
        new_user_id = new_user_id_list[0]

        sql_string = "INSERT INTO Entitys (type, user_id) VALUES (%s, %s)"
        sql_data_tuple = (False, new_user_id)
        db_cursor.execute(sql_string, sql_data_tuple)

        print("┣━━━━┫ Success. Now you can login with your login and password")
    except psycopg2.Error as e:
        print("┣━━━━┫ Error registering user. Error:", e)


def frontend_show_a_list_of_users(db_cursor, name):
    try:
        print("┣━━━━┫ Retrieving list of all users...")
        db_cursor.execute("SELECT * FROM Users;")
        user_list = db_cursor.fetchall()
    except psycopg2.Error as e:
        print("┣━━━━┫ Error fetching users. Error: ", e)
    if name == 'Superuser':
        for i in user_list:
            print(i)
    else:
        for i in user_list:
            print(i[1])


def frontend_show_a_list_of_entitys(db_cursor, name):
    try:
        print("┣━━━━┫ Retrieving list of all entitys...")
        db_cursor.execute("SELECT * FROM Entitys;")
        entitys_list = db_cursor.fetchall()
        for i in entitys_list:
            print(i)
    except psycopg2.Error as e:
        print("┣━━━━┫ Error fetching entitys. Error: ", e)


main()
