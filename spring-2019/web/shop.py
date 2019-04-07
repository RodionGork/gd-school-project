import json
import datetime


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


def is_registered_user(name):
    return name in users


def get_goods():
    return goods


def get_basket_and_total(name):
    if name is None:
        return ({}, 0)
    basket = get_basket(name)
    total = calc_total(basket)
    return (basket, total)


def get_basket(name):
    return load_state().get(name, {})


def update_basket(name, basket):
    state = load_state()
    if basket is not None:
        state[name] = basket
    else:
        state.pop(name, None)
    save_state(state)


def add_item(user, item, qty):
    try:
        qty = int(qty)
    except:
        return (item, 0, 0)
    basket = get_basket(user)
    if not item in basket:
        price = find_price(item)
        basket[item] = [qty, price]
    else:
        price = basket[item][1]
        basket[item][0] += qty
    if basket[item][0] == 0:
        del basket[item]
    update_basket(user, basket)
    return (item, qty, price)


def calc_total(basket):
    return sum([v[0] * v[1] for k,v in basket.items()])


def find_price(item):
    for g in goods:
        if g[0] == item:
            return g[1]
    return 0


def order_ready(name):
    basket = get_basket(name)
    total = calc_total(basket)
    content = ', '.join([k + ' ' + str(v[0]) for k, v in basket.items()])
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    s = "%s (%s) total=%s, items: %s" % (name, dt, total, content)
    with open('orders.txt', 'a') as f:
        f.write(s + "\r\n")
    update_basket(name, None)
    

def load_state():
    try:
        with open('state.json') as f:
            return json.loads(f.read())
    except:
        return {}


def save_state(s):
    with open('state.json', 'w') as f:
        f.write(json.dumps(s))


def main():
    cont = True
    while cont:
        line = input('\nshop> ')
        cont = console_execute_command(line)


def console_execute_command(line):
    ur = line.split(' ', 4)
    command = ur[0]
    user = ur[1] if len(ur) > 1 else None
    if command == 'login':
        console_login(user)
    elif command == 'add' and user is not None:
        item = ur[2] if len(ur) > 2 else ''
        qty = ur[3] if len(ur) > 3 else '0'
        console_add(user, item, qty)
    elif command == 'order' and user is not None:
        console_order(user)
    elif command == 'goods':
        console_goods()
    elif command == 'basket' and user is not None:
        console_basket(user)
    elif command == 'exit':
        return False
    else:
        console_help()
    return True


def console_login(username):
    if is_registered_user(username):
        print('Hello, ' + username)
    else:
        print('You are not registered!\nYou can browse, but will not be able to order!')


def console_add(username, item, qty):
    res = add_item(username, item, qty)
    print('Added %s, amount=%s, cost=%s' % (res[0], res[1], res[2] * res[1]))


def console_order(username):
    if not is_registered_user(username):
        print('Sorry, we do not ship to unregistered users :(')
        return
    order_ready(username)
    print('Your order is shipped, your basked is empty again. Thanks!')


def console_basket(user):
    basket, total = get_basket_and_total(user)
    print('Your basket:')
    for item in basket:
        qty = basket[item][0]
        price = basket[item][1]
        print('  %s, amount=%s, price=%s' % (item, qty, price))
    print('------\n  total: %s$' % total)


def console_goods():
    print('Our goods:')
    for item, price in get_goods():
        print('  %s at %s$' % (item, price))

def console_help():
    print(
        'Command list:\n' +
        '  login <username>\n' +
        '  add <username> <item> <amount>\n' +
        '  order <username>\n' +
        '  basket <username>\n' +
        '  goods\n' +
        '  exit')


if __name__ == '__main__':
    main()
