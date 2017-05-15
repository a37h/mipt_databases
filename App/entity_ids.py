

# Used in registration and login
def backend_get_user_id(db_cursor, name):
    sql_string = "SELECT user_id FROM Users WHERE user_name = %s"
    sql_data_tuple = (name,)
    db_cursor.execute(sql_string, sql_data_tuple)
    new_user_id_list = db_cursor.fetchall()
    if len(new_user_id_list) == 0:
        return -1
    else:
        return new_user_id_list[0]


# Used in registration and login
def backend_get_user_entity_id(db_cursor, user_id):
    sql_string = "SELECT entity_id FROM Entitys WHERE user_id = %s"
    sql_data_tuple = (user_id,)
    db_cursor.execute(sql_string, sql_data_tuple)
    new_user_id_list = db_cursor.fetchall()
    return new_user_id_list[0]


def backend_get_group_id(db_cursor, group_name):
    sql_string = "SELECT group_id FROM Groups WHERE group_name = %s"
    sql_data_tuple = (group_name,)
    db_cursor.execute(sql_string, sql_data_tuple)
    qq = db_cursor.fetchall()
    if len(qq) == 0:
        return -1
    else:
        return qq[0]

def backend_get_group_entity_id(db_cursor, group_id):
    sql_string = "SELECT entity_id FROM Entitys WHERE group_id = %s"
    sql_data_tuple = (group_id,)
    db_cursor.execute(sql_string, sql_data_tuple)
    group_entity_id = db_cursor.fetchall()
    return group_entity_id[0]


def backend_get_last_group_session_status(db_cursor, group_entity_id):
    sql_string = "SELECT type FROM Sessions_log WHERE entity_id = %s ORDER BY time_stamp DESC LIMIT 1"
    sql_data_tuple = (group_entity_id,)
    db_cursor.execute(sql_string, sql_data_tuple)
    group_session = db_cursor.fetchall()
    try:
        return group_session[0][0]
    except IndexError:
        return True
