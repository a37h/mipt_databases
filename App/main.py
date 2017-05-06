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

    register(db_cursor, 'Anatoly', 'Anatoly@mail.ru', '123', 'True')


def register(db_cursor, name, email, password, email_subscrition):
    try:
        db_cursor.execute("INSERT INTO Users (user_name, user_email, user_password, email_sub_agreement) "
                          "values ('%s', '%s', '%s', '%s');" % "Anatoly" "Anatoly@mail.ru" "123" "True")
    except psycopg2.Error as e:
        print("Error registering user. Error:", e)

main()