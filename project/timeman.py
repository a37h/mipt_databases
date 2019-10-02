import psycopg2  # for connection to database
import psycopg2.extras  # for working with database
import os  # for clearing console screen
from regis_login import *  # functions for logging in and out
from database_conn import *  # functions for working with database
from user_interface import *  # functions for user interface
import re
from help import *  # help functions

def main():
    # create an connection and cursor
    db_connection = db_connect()
    db_cursor = db_connection.cursor()

    current_user_info = []  # user_name, user_id, user_entity_id
    current_session_info = []  # user_entity_id, Boolean, time
    current_active_group = []  # group_name, group_id, group_entity_id

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
    regular7 = re.compile('switch group [a-zA-Z0-9]*')
    regular8 = re.compile('group stats [0-9]+')


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
                splitedline7 = regular7.findall(input_line)
                splitedline8 = regular8.findall(input_line)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if input_line == 'h' or input_line == 'help':
                    frontend_show_help(current_user_info)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'help groups':
                    frontend_show_help_groups(current_user_info)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'current group':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if len(current_active_group) != 0:
                            print("┣━━━━━ Right now you're working in '%s' group" % current_active_group[0])
                        else:
                            print("┣━━━━━ You aren't in any of groups right now. Use 'switch group <group name>'")
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
                        current_active_group = []
                        current_session_info = []
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
                elif input_line == 'group go' or input_line == 'gg':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if len(current_active_group) != 0:
                            temp = backend_get_last_group_session_status(db_cursor, current_active_group[2])
                            if temp is True:
                                group_start_session(db_cursor, current_active_group)
                                db_connection.commit()
                            else:
                                print("┣━━━━━ Error: group has an active session. Use 'gs' or 'group stop'")
                        else:
                            print("┣━━━━━ Error: first you should select an active group")
                            print("              use 'switch group <group_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'group stop' or input_line == 'gs':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        temp = backend_get_last_group_session_status(db_cursor, current_active_group[2])
                        if temp is False:
                            group_stop_session(db_cursor, current_active_group)
                            db_connection.commit()
                        else:
                            print("┣━━━━━ Error: group have to start a session first. Use 'gg' or 'group go'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'stats' or (len(splitedline) != 0 and len(input_line.split()) == 2):
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if input_line == 'stats':
                            print("┣━━━━━ Showing last 10 results by default (use h for more info):")
                            show_list_of_sessions(db_cursor, current_user_info, current_session_info)
                        else:
                            try:
                                regular = re.compile('[0-9]+')
                                wtf = regular.findall(input_line)
                                print("┣━━━━━ Showing last %s results:" % wtf[0])
                                show_list_of_sessions(db_cursor, current_user_info, current_session_info, int(wtf[0]))
                            except ValueError or IndexError:
                                print("┣━━━━━ Error: use 'stats <n>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'group stats' or (len(splitedline8) != 0 and len(input_line.split()) == 3):
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if input_line == 'group stats':
                            print("┣━━━━━ Showing last 10 results by default (use h for more info):")
                            show_group_list_of_sessions(db_cursor, current_active_group)
                        else:
                            try:
                                regular = re.compile('[0-9]+')
                                wtf = regular.findall(input_line)
                                print("┣━━━━━ Showing last %s results:" % wtf[0])
                                show_group_list_of_sessions(db_cursor, current_active_group, int(wtf[0]))
                            except ValueError or IndexError:
                                print("┣━━━━━ Error: use 'stats <n>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline2) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        try:
                            regular = re.compile('[a-zA-Z0-9]+')
                            wtf = regular.findall(input_line)
                            create_group(db_cursor, current_user_info, wtf[2])
                            db_connection.commit()
                        except ValueError:
                            print("┣━━━━━ Error: use 'create group <group_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline3) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        try:
                            regular = re.compile('[a-zA-Z0-9]+')
                            wtf = regular.findall(input_line)
                            invite_to_group(db_cursor, current_user_info, wtf[2], wtf[4])
                            db_connection.commit()
                        except ValueError:
                            print("┣━━━━━ Error: use 'invite to <group_name> user <user_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline4) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        try:
                            regular = re.compile('[a-zA-Z0-9]+')
                            wtf = regular.findall(input_line)
                            join_group(db_cursor, current_user_info, wtf[2])
                            db_connection.commit()
                        except ValueError:
                            print("┣━━━━━ Error: use 'join group <group_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline5) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        try:
                            regular = re.compile('[a-zA-Z0-9]+')
                            wtf = regular.findall(input_line)
                            delete_group(db_cursor, current_user_info, wtf[2])
                            db_connection.commit()
                        except ValueError:
                            print("┣━━━━━ Error: use 'delete group <group_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline6) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        try:
                            regular = re.compile('[a-zA-Z0-9]+')
                            wtf = regular.findall(input_line)
                            leave_group(db_cursor, current_user_info, wtf[2])
                            db_connection.commit()
                        except ValueError:
                            print("┣━━━━━ Error: use 'leave group <group_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif len(splitedline7) != 0:
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        try:
                            regular = re.compile('[a-zA-Z0-9]+')
                            wtf = regular.findall(input_line)
                            current_active_group = switch_group(db_cursor, current_user_info, wtf[2])
                        except ValueError:
                            print("┣━━━━━ Error: use 'leave group <group_name>'")
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                elif input_line == 'groups list':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        show_groups_list(db_cursor, current_user_info)
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


main()
