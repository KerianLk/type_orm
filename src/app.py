from flask import Flask
from flask import jsonify
from flask import request

from database import get_10_random_customers, get_store, get_product_with_max_price, get_product_price_stats, \
    create_store, delete_store

app = Flask(__name__)


@app.route('/customers/show/', methods=['GET'])
def get_customers_info():
    data = get_10_random_customers()
    return jsonify(data)


@app.route('/stores/<store_id>', methods=['GET'])
def get_store_info(store_id):
    if not store_id.isdigit():
        return {}
    data = get_store(int(store_id))
    return data


@app.route('/prices/max', methods=['GET'])
def get_price_max():
    data = get_product_with_max_price()
    return data


@app.route('/prices/stats/<product_id>', methods=['GET'])
def get_product_stats(product_id):
    if not product_id.isdigit():
        return {}
    data = get_product_price_stats(int(product_id))
    return data


@app.route('/stores/add', methods=['POST'])
def add_store():
    region = request.form['region']
    if not region.isdigit():
        return {}
    address = request.form['address']
    data = create_store(int(region), address)
    return data


@app.route('/stores/delete/<store_id>', methods=['POST'])
def remove_store(store_id):
    try:
        if not store_id.isdigit():
            return {'status': 'not found'}
        data = delete_store(int(store_id))
        return {'status': data}
    except Exception:
        return {}
