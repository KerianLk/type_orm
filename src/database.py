from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker

from orm import Customer, Store, Price, Sale

engine = create_engine("postgresql+psycopg2://wahrksle:postgres@localhost:5433/wahrksle")
Session = sessionmaker(bind=engine)
session = Session()


def get_10_random_customers():
    customers = session.query(Customer).order_by(func.random()).limit(10).all()
    return [
        {
            'customer_id': customer.customer_id,
            'name': customer.name,
            'surname': customer.surname,
            'birth_date': customer.surname
        }
        for customer in customers
    ]


def get_store(store_id: int):
    if not isinstance(store_id, int):
        return {}
    store = session.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        return {}
    return {
        'store_id': store.store_id,
        'address': store.address,
        'region': store.region
    }


def get_product_with_max_price():
    sub_query = session.query(func.max(Price.price))
    data = session.query(Price).filter(
        Price.price.in_(sub_query)
    ).order_by(desc(Price.end_date)).limit(1).first()
    return {
        'price_id': data.price_id,
        'product_id': data.product_id,
        'price': data.price,
        'start_date': data.start_date,
        'end_date': data.end_date,
    }


def get_product_price_stats(product_id):
    if not isinstance(product_id, int):
        return {}
    cnt = session.query(Sale).filter(Sale.product_id == product_id).count()
    stores_count = session.query(Sale.store_id).filter(Sale.product_id == product_id).group_by(Sale.store_id).count()
    max_price = session.query(func.max(Price.price)).filter(Price.product_id == product_id).first()[0]
    min_price = session.query(func.min(Price.price)).filter(Price.product_id == product_id).first()[0]
    avg_price = session.query(func.avg(Price.price)).filter(Price.product_id == product_id).first()[0]
    return {
        'count': cnt,
        'stores_count': stores_count,
        'max_price': max_price,
        'min_price': min_price,
        'avg_price': avg_price
    }


def create_store(region, address):
    store = Store(region=region, address=address)
    session.add(store)
    session.commit()
    return {'store_id': store.store_id}


def delete_store(store_id):
    if not isinstance(store_id, int):
        return 'not found'
    obj = session.query(Store).filter(Store.store_id == store_id).first()
    if not obj:
        return 'not found'
    session.delete(obj)
    session.commit()
    return 'ok'


if __name__ == '__main__':
    delete_store(64549)
