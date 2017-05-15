import psycopg2  # for connection to database
import psycopg2.extras  # for working with database
import os  # for clearing console screen
from regis_login import *  # functions for logging in and out
from database_conn import *  # functions for working with database
from user_interface import *  # functions for user interface
import re


def main():
    # create an connection and cursor
    db_connection = db_connect()
    db_cursor = db_connection.cursor()

    current_user_info = []  # user_name, user_id, user_entity_id
    current_session_info = []  # user_entity_id, Boolean, time

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣━━━━━ TimeManagementApp3000                                     ┃")
    print("┃ 'help' or 'h' to get a list of commands                        ┃")
    print("┃ 'quit' or 'q' to exit the app                                  ┃")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    regular1 = re.compile('stats [0-9]*')
    regular2 = re.compile('create group [a-zA-Z0-9]*')
    regular3 = re.compile('invite to [a-zA-Z0-9]* user [a-zA-Z0-9]*')
    regular4 = re.compile('join group [a-zA-Z0-9]*')
    regular5 = re.compile('delete group [a-zA-Z0-9]*')
    regular6 = re.compile('leave group [a-zA-Z0-9]*')

    while True:
        try:
            try:
                input_line = input('┣ ➤  ')
                splitedline = regular1.findall(input_line)
                splitedline2 = regular2.findall(input_line)
                splitedline3 = regular3.findall(input_line)
                splitedline4 = regular4.findall(input_line)
                splitedline5 = regular5.findall(input_line)
                splitedline6 = regular6.findall(input_line)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if input_line == 'h' or input_line == 'help':
                    frontend_show_help(current_user_info)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'help groups':
                    frontend_show_help_groups(current_user_info)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'r' or input_line == 'register':
                    if len(current_user_info) == 0:
                        current_user_info = frontend_user_registration(db_cursor)
                        db_connection.commit()
                    else:
                        print("┣━━━━━ Error: you are already logged in. Use 'h' or 'help'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'l' or input_line == 'login':
                    if len(current_user_info) == 0:
                        current_user_info = frontend_user_login(db_cursor)
                    else:
                        print("┣━━━━━ Error: you are already logged in. Use 'h' or 'help'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'q' or input_line == 'quit':
                    if len(current_session_info) != 0 and current_session_info[1] is False:
                        stop_session(db_cursor, current_user_info, current_session_info)
                    print('┗━━━━━━━━━━ Peace out ━━━ ◠ ◡ ◠  ━━━━━━━━━━━━━━━')
                    print()
                    exit(0)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'o' or input_line == 'logout':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        print("┣━━━━━ Goodbye, %s" % (current_user_info[0],))
                        current_user_info = []
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'clear' or input_line == 'c':
                    os.system('cls' if os.name == 'nt' else 'clear')
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'go' or input_line == 'g':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if len(current_session_info) == 0 or current_session_info[1] is True:
                            current_session_info = start_session(db_connection,
                                db_cursor, current_user_info, current_session_info)
                        else:
                            print("┣━━━━━ Error: you have an active session. Use 's' or 'stop'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'stop' or input_line == 's':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if len(current_session_info) != 0 and current_session_info[1] is False:
                            current_session_info = stop_session(db_connection,
                                db_cursor, current_user_info, current_session_info)
                        else:
                            print("┣━━━━━ Error: first you have to start a session. Use 'g' or 'go'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'stats' or len(splitedline) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if input_line == 'stats':
                            print("┣━━━━━ Showing last 10 results by default (use h for more info):")
                            show_list_of_sessions(db_cursor, current_user_info, current_session_info)
                        else:
                            regular = re.compile('[0-9]*')
                            wtf = regular.findall(input_line)
                            print("┣━━━━━ Showing last %s results:" % wtf[6])
                            show_list_of_sessions(db_cursor, current_user_info, current_session_info, int(wtf[6]))
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline2) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        regular = re.compile('[a-zA-Z0-9]*')
                        wtf = regular.findall(input_line)
                        print("┣━━━━━ ...creating group called '%s':" % wtf[4])
                        create_group(db_cursor, current_user_info, wtf[4])
                        db_connection.commit()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline3) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        regular = re.compile('[a-zA-Z0-9]*')
                        wtf = regular.findall(input_line)
                        print("┣━━━━━ ... inviting user '%s' to group '%s':" % (wtf[4], wtf[8]))
                        invite_to_group(db_cursor, current_user_info, wtf[4], wtf[8])
                        db_connection.commit()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline4) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        regular = re.compile('[a-zA-Z0-9]*')
                        wtf = regular.findall(input_line)
                        print("┣━━━━━ ... trying to join group '%s':" % wtf[4])
                        join_group(db_cursor, current_user_info, wtf[4])
                        db_connection.commit()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline5) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        regular = re.compile('[a-zA-Z0-9]*')
                        wtf = regular.findall(input_line)
                        print("┣━━━━━ ... trying to delete group '%s':" % wtf[4])
                        delete_group(db_cursor, current_user_info, wtf[4])
                        db_connection.commit()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline6) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        regular = re.compile('[a-zA-Z0-9]*')
                        wtf = regular.findall(input_line)
                        print("┣━━━━━ ... trying to leave group '%s':" % wtf[4])
                        leave_group(db_cursor, current_user_info, wtf[4])
                        db_connection.commit()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                else:
                    print("┣━━━━━ Error: no such command, try again or use 'h' or 'help'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            except EOFError:
                if len(current_session_info) != 0 and current_session_info[1] is False:
                    stop_session(db_connection, db_cursor, current_user_info, current_session_info)
                shutdown_app()
                print(1)
        except KeyboardInterrupt:
            if len(current_session_info) != 0 and current_session_info[1] is False:
                stop_session(db_connection, db_cursor, current_user_info, current_session_info)
            shutdown_app()
            print(2)


main()
