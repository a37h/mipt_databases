import psycopg2  # for connection to database
import psycopg2.extras  # for working with database


# create a connection to a database
def db_connect():
    connection_string = 'dbname=mipt_db_project user=mipt_db_project_user ' \
                        'password=qwe host=localhost'
    try:
        return psycopg2.connect(connection_string)
    except psycopg2.Error as e:
        print("Can not connect to database.")
        exit(0)
