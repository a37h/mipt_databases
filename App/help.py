

# Help
def frontend_show_help(current_user_info):
    if len(current_user_info) == 0:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  'r' or 'register' to register if you're new                   ┃")
        print("┃  'l' or 'login' to login if you're already registered          ┃")
        print("┃  'c' or 'clear' if you want to clear your screen               ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    else:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  'c' or 'clear' if you want to clear your screen               ┃")
        print("┃  'o' or 'logout' to logout from your account                   ┃")
        print("┃  'g' or 'go' to start a time management session                ┃")
        print("┃  's' or 'stop' to stop a time management session               ┃")
        print("┃  'stats' or 'stats <n>' to get a list of 10 or n last sessions ┃")
        print("┃  'help groups' to get a list of commands for using groups      ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

# Help
def frontend_show_help_groups(current_user_info):
    if len(current_user_info) == 0:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  'r' or 'register' to register if you're new                   ┃")
        print("┃  'l' or 'login' to login if you're already registered          ┃")
        print("┃  'c' or 'clear' if you want to clear your screen               ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    else:
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  'create group <group name>' to create a group                 ┃")
        print("┃  'invite to <group name> user <user name> to invite a user     ┃")
        print("┃  'join group <group name>' to join a group                     ┃")
        print("┃  'switch group <group name>' to switch an active group         ┃")
        print("┃  'groups list' to get a list of groups you belong to           ┃")
        print("┃  'leave group <group name>' to leave a group                   ┃")
        print("┃  'delete group <group name>' to delete a group                 ┃")
        print("┃  'current group' to see group you're working with right now    ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")