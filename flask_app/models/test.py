import random
number = random.randint(1,10)
lists = [1,3,5,7,9] 

while number in lists:
    print(number)
    number = random.randint(1,10)

print(number)