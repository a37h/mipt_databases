import psycopg2
import psycopg2.extras


def db_connect():
    connection_string = 'dbname=mipt_db_project user=mipt_db_project_user ' \
                        'password=ggHkfIJ9aAFxzjmrkIMfWrvC03wZkgpK host=localhost'
    try:
        return psycopg2.connect(connection_string)
        print("Connection is successful! You can now proceed to work!")
    except psycopg2.Error as e:
        print("Can't connect to database. Error:", e)


def main():
    # create an connection and cursor
    db_connection = db_connect()
    db_cursor = db_connection.cursor()

    while True:
        try:
            print('>')
            input_line = input()
            print(input_line)
        except:
            print('ayy lmao')
            exit(2)


def user_login(db_cursor, name, password):
    try:
        sql_string = "SELECT * FROM Users WHERE user_name = %s AND user_password = %S"
        sql_data_tuple = (name, password)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("Error loggining. Error:", e)
    result = db_cursor.fetchall()
    if len(result) == 1:
        print('Success. Welcome, %s' % name)
    else:
        print('Ooh. Something went wrong here')


def register_new_user(db_cursor, name, email, password, email_subscrition):
    try:
        sql_string = "INSERT INTO Users (user_name, user_email, user_password, " \
                     "email_sub_agreement) values ('%s', '%s', '%s', '%s');"
        sql_data_tuple = (name, email, password, email_subscrition)
        db_cursor.execute(sql_string, sql_data_tuple)
    except psycopg2.Error as e:
        print("Error registering user. Error:", e)


def show_a_list_of_users(db_cursor, name):
    try:
        print("Retrieving list of all users...")
        db_cursor.execute("SELECT * FROM Users;")
        user_list = db_cursor.fetchall()
    except psycopg2.Error as e:
        print("Error fetching users. Error: ", e)
    if name == 'Superuser':
        for i in user_list:
            print(i)
    else:
        for i in user_list:
            print(i[1])

main()
