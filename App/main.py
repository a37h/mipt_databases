import psycopg2
import psycopg2.extras


def db_connect():
    connection_string = 'dbname=mipt_db_project user=mipt_db_project_user ' \
                        'password=ggHkfIJ9aAFxzjmrkIMfWrvC03wZkgpK host=localhost'
    try:
        print("Connecting...")
        return psycopg2.connect(connection_string)
    except:
        print("Can't connect to database. Error:")


def main():
    db_connection = db_connect()
    db_cursor = db_connection.cursor()
    try:
        # db_cursor.execute("INSERT INTO Users (user_name, user_email, user_password, email_sub_agreement) "
        #                  "values ('teqwqwesaqwedfeqwt1', 'tesqaqweqwsdfweq2', 'tes3aqwedsqwef213', True);")
        db_cursor.execute("SELECT * FROM Users")
        results = db_cursor.fetchall()
        for i in results:
            print(i)
            db_cursor.execute("DELETE FROM Users WHERE user_id = %s" % i[0])
        db_connection.commit()
    except psycopg2.Error as e:
        print("Error", e)


main()
