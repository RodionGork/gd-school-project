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

def find_price(item):
  for title, price in goods:
    if title == item:
      return price
  return 0

def choose_goods():
  total = 0
  while True:
    something = input('What do you want to buy (just hit enter for exit): ')
    if something == '':
      break
    price = find_price(something)
    if price > 0:
      count = input('How many: ')
      print('You want to buy %s for %s apice' % (something, price))
      count = int(count)
      print('  For %s piece it will be %s$' % (count, price * count))
      total += price * count
      print('Your current total: %s$' % total)


name = input('what is your name: ')
if name in users:
  print('Hello, ' + name)
  choose_goods()
  print('Good bye, come again!')
else:
  print('Go home, Troll!')

