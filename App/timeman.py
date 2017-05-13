import psycopg2  # for connection to database
import psycopg2.extras  # for working with database
import os  # for clearing console screen
from tm_reglog import *  # functions for logging in and out
from tm_dbconn import *  # functions for working with database
from tm_userint import *  # functions for user interface


def main():
    # create an connection and cursor
    db_connection = db_connect()
    db_cursor = db_connection.cursor()

    current_user_info = []
    current_session_info = []

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣━━━━━ TimeManagementApp3000 ━━━━━━━━━━━━━━┫")
    print("┣━ 'help' or 'h' to get a list of commands ┫")
    print("┣━ 'quit' or 'q' to exit the app ━━━━━━━━━━┫")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    while True:
        try:
            try:
                input_line = input('┣ ➤  ')

                if input_line == 'h' or input_line == 'help':
                    frontend_show_help(current_user_info)

                elif input_line == 'r' or input_line == 'register':
                    if len(current_user_info) == 0:
                        current_user_info = frontend_user_registration(db_cursor)
                        db_connection.commit()
                    else:
                        print("┣━━━━━ Error: you are already logged in. Use 'h' or 'help'")

                elif input_line == 'l' or input_line == 'login':
                    if len(current_user_info) == 0:
                        current_user_info = frontend_user_login(db_cursor)
                    else:
                        print("┣━━━━━ Error: you are already logged in. Use 'h' or 'help'")

                elif input_line == 'q' or input_line == 'quit':
                    if len(current_session_info) != 0 and current_session_info[1] is False:
                        stop_session(db_cursor, current_user_info, current_session_info)
                    shutdown_app()

                elif input_line == 'o' or input_line == 'logout':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        print("┣━━━━━ Goodbye, %s" % (current_user_info[0],))
                        current_user_info = []

                elif input_line == 'clear' or input_line == 'c':
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif input_line == 'go' or input_line == 'g':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if len(current_session_info) == 0 or current_session_info[1] is True:
                            current_session_info = start_session(
                                db_cursor, current_user_info, current_session_info)
                            db_connection.commit()
                        else:
                            print("┣━━━━━ Error: you have an active session. Use 's' or 'stop'")

                elif input_line == 'stop' or input_line == 's':
                    if len(current_user_info) == 0:
                        print("┣━━━━━ Error: you aren't logged in. Use 'l' or 'login'")
                    else:
                        if len(current_session_info) != 0 and current_session_info[1] is False:
                            current_session_info = stop_session(
                                db_cursor, current_user_info, current_session_info)
                            db_connection.commit()
                        else:
                            print("┣━━━━━ Error: first you have to start a session. Use 'g' or 'go'")

                else:
                    print("┣━━━━━ Error: no such command, try again or use 'h' or 'help'")

            except EOFError:
                if len(current_session_info) != 0 and current_session_info[1] is False:
                    stop_session(db_cursor, current_user_info, current_session_info)
                shutdown_app()
        except KeyboardInterrupt:
            if len(current_session_info) != 0 and current_session_info[1] is False:
                stop_session(db_cursor, current_user_info, current_session_info)
            shutdown_app()


main()
