# deposit = float(input("Please deposit the money into the machine: "))

# if deposit < 2:
#     print("Please continue to deposit")
# elif deposit == 2:
#     print("Here is your snack!")
# elif deposit > 2:
#     print("Here is your snack and change!")
# else:
#     print("Please entera valid amount")
    
snack_choice = int(input("Please input the snack you want(1-10): "))
snack_price = None
snack = None

if snack_choice == 1:
    snack = "chocolate bar"
    snack_price = 2
elif snack_choice == 2:
    snack = "M&Ms"
    snack_price = 2.50
elif snack_choice == 3:
    snack = "chips"
    snack_price = 2
elif snack_choice == 4:
    snack = "mini pretzels"
    snack_price = 2.50
elif snack_choice == 5:
    snack = "crackers"
    snack_price = 2.50
elif snack_choice == 6:
    snack = "gummies"
    snack_price = 3
elif snack_choice == 7:
    snack = "sour strips"
    snack_price = 4.5
elif snack_choice == 8:
    snack = "choco-mints"
    snack_price = 5
elif snack_choice == 9:
    snack = "granola bar"
    snack_price = 1
elif snack_choice == 10:
    snack = "Skittles"
    snack_price = 2.50
else:
    print("Please enter a valid amount.")
    
deposit = float(input("Please deposit the money into the machine: "))


if deposit < snack_price:
    print("Please continue to deposit")
elif deposit == snack_price:
    print(f"Here is your {snack}!")
elif deposit > snack_price:
    print(f"Here is your {snack} and change of ${deposit-snack_price}!")
elif deposit > 20:
    print("We only accept up to $20")
else:
    print("Please enter a valid amount of cash")
    
    