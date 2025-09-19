PIN = 4918
input = int(input("Enter your PIN: "))
balance = 10
# balance = 0
withdrawl = None

if PIN == input:
    print("ACCESS ALLOWED")
    # Normally, after a withdrawl is transacted, the if statement/while loop will run again.
    if balance > 0:
        while balance > 0:
            print("Withdrawl Access Granted")
            withdrawl = True
            break
    else:
        print("Withdrawl Permission Denied")
        withdrawl = False
else:
    print("PIN is INCORRECT")