set_password = "BCTS2025"
is_entered = False

while is_entered == False:
    user_input_password = input("Please enter your password: ")
    if set_password == user_input_password:
        is_entered = True
        print("Welcome")
    else:
        print("Try again. Python may be case sensitive.")