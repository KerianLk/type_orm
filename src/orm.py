from sqlalchemy import (
    Column, Integer, String,
    Date,
    ForeignKey, UniqueConstraint, )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    brand = Column(String)

    __tablename__ = 'products'


class Store(Base):
    store_id = Column(Integer, primary_key=True)
    address = Column(String)
    region = Column(Integer)

    __tablename__ = 'stores'


class Customer(Base):
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    birth_date = Column(Date)

    __tablename__ = 'customers'


class Price(Base):
    price_id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.product_id'))
    price = Column(Integer)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    product = relationship('Product', backref='price')

    __tablename__ = 'prices'
    __table_args__ = (
        UniqueConstraint(
            'product_id', 'start_date', 'end_date',
            name='product_start_end'
        ),
    )


class Sale(Base):
    sale_id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.product_id'))
    store_id = Column(ForeignKey('stores.store_id'))
    customer_id = Column(ForeignKey('customers.customer_id'))
    sale_date = Column(Date, nullable=False)

    product = relationship('Product', backref='sale')
    store = relationship('Store', backref='sale')
    customer = relationship('Customer', backref='sale')

    __tablename__ = 'sales'
