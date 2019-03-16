#program Little Internet Shop

users = [
  'Anna',
  'Bob',
  'Veronika',
  'Matthew',
  'Lucas',
  'Vladimir',
  'Michael',
  'Helena',
]

goods = [
  ['Apples', 70],
  ['Bananas', 30],
  ['Sugar', 45],
  ['Tea', 50],
  ['Coffee', 95],
]

name = input('what is your name: ')

print('Hello, ' + name)

something = input('What do you want to buy: ')

count = input('How many: ')

print('You want to buy ' + str(count) + ' ' + something)

total = 1

print('It will cost you ' + str(total) + ' rouble(s)')
