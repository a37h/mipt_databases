import psycopg2
import psycopg2.extras


def db_connect():
    connection_string = 'dbname=mipt_db_project user=mipt_db_project_user ' \
                        'password=ggHkfIJ9aAFxzjmrkIMfWrvC03wZkgpK host=localhost'
    try:
        print("Connecting...")
        return psycopg2.connect(connection_string)
    except psycopg2.Error as e:
        print("Can't connect to database. Error:", e)


def main():
    db_connection = db_connect()
    db_cursor = db_connection.cursor()

    register(db_cursor, 'abb', 'bbb', 'cbb', 'True')
    db_connection.commit()
    get_all_users(db_cursor)
    db_connection.commit()


def register(db_cursor, name, email, password, email_subscrition):
    try:
        db_cursor.execute("INSERT INTO Users (user_name, user_email, user_password, email_sub_agreement) "
                          "values ('%s', '%s', '%s', '%s');" % (name, email, password, email_subscrition))
    except psycopg2.Error as e:
        print("Error registering user. Error:", e)


def get_all_users(db_cursor):
    try:
        db_cursor.execute("SELECT * FROM Users;")
        user_list = db_cursor.fetchall()
        for i in user_list:
            print(i)
    except psycopg2.Error as e:
        print("Error fetching users. Error: ", e)


main()
