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
