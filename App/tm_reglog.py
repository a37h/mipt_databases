import getpass  # for getting password safe


# Login (first part)
def frontend_user_login(db_cursor):
    try:
        try:
            name = input('┣━━━━━ Login: ')
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


# Used in registration and login
def backend_get_user_entity_id(db_cursor, user_id):
    sql_string = "SELECT entity_id FROM Entitys WHERE user_id = %s"
    sql_data_tuple = (user_id,)
    db_cursor.execute(sql_string, sql_data_tuple)
    new_user_id_list = db_cursor.fetchall()
    return new_user_id_list[0]


# Shutdown app safely
def shutdown_app():
    print()
    print('┗━━━━━━━━━━ Peace out ━━━ ◠ ◡ ◠  ━━━━━━━━━━━━━━━')
    print()
    exit(0)