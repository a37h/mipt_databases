

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