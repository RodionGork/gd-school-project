import flask

import shop


messages = {
    'spy': ('You need to be registered to use our shop, sorry', 'bg-danger text-white'),
    'ordered': ('Your order was sent, thanks!', 'bg-success text-white'),
    'bye': ('Good bye, thanks!', 'bg-info text-white'),
}

app = flask.Flask(__name__, static_url_path='/s')


@app.route('/')
def main_page():
    name = flask.session.get('username')
    basket, total = shop.get_basket_and_total(name)
    data = {
        'goods': shop.get_goods(),
        'basket': basket,
        'total': total,
    }
    msg = flask.request.args.get('msg')
    if msg is not None:
        data['msg'] = messages[msg]
    return flask.render_template('index.html', data=data)


@app.route('/login', methods=['POST'])
def login():
    name = flask.request.form['name']
    if shop.is_registered_user(name):
        flask.session['username'] = name
        return flask.redirect(flask.url_for('main_page'))
    else:
        return flask.redirect(flask.url_for('main_page', msg='spy'))


@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('main_page', msg='bye'))


@app.route('/add-item', methods=['POST'])
def add_item():
    form = flask.request.form
    shop.add_item(form['user'], form['item'], form['qty'])
    return flask.redirect(flask.url_for('main_page'))


@app.route('/order')
def order():
    shop.order_ready(flask.session['username'])
    return flask.redirect(flask.url_for('main_page', msg='ordered'))


@app.route('/manager')
def manager():
    with open('orders.txt') as f:
        s = f.read()
    return flask.render_template('manager.html', data=s)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'dummy-key'
    app.run(host='0.0.0.0', port=5000, debug=True)
