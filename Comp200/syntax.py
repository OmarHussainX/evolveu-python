"""
Comp200 - Basic Syntax

Gaining familiarity with python
"""


# Declare integer variable and print it
x = 42
print(f'number \'x\': {x}')


# Declare string variable and print it
x = 'The answer to the life, universe, and everything'
print(f'string \'x\': {x}')


# Declare boolean variable and print it
bool = True
print(f'boolean \'bool\': {bool}')


# Declare list variable and print it
myLaptop = ['ThinkPad', 'T580']
print(f'list \'myLaptop\': {myLaptop}')


# Declare dictionary and print it
learner = {
    'name':      'Omar',
    'education': 'Bsc',
    'JSlevel':    4
}
print('\n--------------------------------------------------')
print(f'dictionary \'learner\': {learner}')
print(f'dictionary \'learner\' keys: {learner.keys()}')
print(f'dictionary \'learner\' values: {learner.values()}')
print(f'dictionary \'learner\' items: {learner.items()}')


# Declare 'None' (undefined) variable and print it
undef = None
print('\n--------------------------------------------------')
print(f'undefined variable \'undef\': {undef}')


# basic if/else construct...
name = 'Omar'
if (name == 'Omar'):
    print('Assalaamolaikum, Omar!')
else:
    print('Who are you!?')

print('Assalaamolaikum, Omar!') if (name == 'Omar') else print('Who are you!?')


# function takes two parameters: num1 & num2, returns their sum
def adder(num1, num2):
    """returns sum of two numbers"""
    return num1 + num2

print('\n--------------------------------------------------')
print(f'result of calling adder(2,3): {adder(2, 3)}')


# Working with lists
# list 'myLaptop' was declared earlier
print('\n--------------------------------------------------')
print(f'\'myLaptop\' before updates: {myLaptop}')

# list - add to front: insert
myLaptop.insert(0, 'Lenovo')
print(f'\'myLaptop\' after add to front (insert): {myLaptop}')

# list - add to end: append
myLaptop.append("8GB")
print(f'\'myLaptop\' after add to end (append): {myLaptop}')

# list - update value
myLaptop[-1] = '16GB'
print(f'\'myLaptop\' after changing value: {myLaptop}')


# Working with loops
# for/in loop
print('\n--------------------------------------------------')
print('printing list contents via for/in loop:')
for item in myLaptop:
    print(item)

# dictionary 'learner' was declared earlier
print('\n--------------------------------------------------')
print('printing dictionary contents via for/in loop:')
for key, value in learner.items():
    print(f'key: {key}, value: {value}')


# while loop
print('\n--------------------------------------------------')
print('printing list contents via while loop: ')
i = 0
while i < len(myLaptop):
    print(myLaptop[i])
    i += 1


# do/while equivalent
# http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks
print('\n--------------------------------------------------')
print('printing list contents via while..True..break loop \
(no do/while in python): ')
i = 0
while True:
    print(myLaptop[i])
    i += 1
    if (i == len(myLaptop)):
        break
