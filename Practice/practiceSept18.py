# ==================== Activity 1 ====================

print("Grab toothbrush")
print("Open the tube of toothpaste and squeeze toothpaste onto the toothbrush's brush")
print("Gently move the toothbrush back ahnd forth on all your teeth")
print("After a few minutes, rinse your mouth with water to clean off extra toothpaste.")

# ==================== Activity 2 ====================

color = input("What is your favorite color? ")
if color:
    print(f"Wow, I like {color} too!")

# ==================== Activity 3 ====================

num = int(input('Select a number: '))

if num > 0:
    print("Positive number")
elif num == 0:
    print("Zero")
else:
    print("Negative number")

# ==================== Activity 4 ====================

for i in range(3):
    print("Nicholas")

# ==================== Activity 5 ====================

number = int(input('Select a number: '))

if number % 2 == 1:
    print('Odd')
else:
    print("Even")

# ==================== Activity 6 ====================

x = int(input('Select a number: '))

for i in range(10):
    print(x * (i+1))

# ==================== Activity 7 ====================

age = int(input("What is your age? "))

if 0 <= age < 13:
    print("Child ticket: $8")
elif 13 <= age <= 59:
    print( "Adult ticket: $12")
elif age >= 60:
    print("Senior ticket: $6")
else:
    print("Please enter a valid age.")