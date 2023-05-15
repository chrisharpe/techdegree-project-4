from models import (Base, session, Product, engine)
import csv
from datetime import datetime
import time


def add_csv():
    products = []
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)
        for row in data:
            product = {}
            for i, value in enumerate(row):
                product[header[i]] = value
            products.append(product)
    for product in products:
        price_str = product['product_price']
        product['product_price'] = clean_price(price_str)
    for product in products:
        product['product_quantity'] = int(product['product_quantity'])
    for product in products:
        date_str = product['date_updated']
        product['date_updated'] = clean_date(date_str)
    for product in products:
        existing_product = session.query(Product).filter_by(
            product_name=product['product_name']).first()
        if existing_product == None:
            new_product = Product(
                product_name=product['product_name'],
                product_price=product['product_price'],
                product_quantity=product['product_quantity'],
                date_updated=product['date_updated'])
            session.add(new_product)
            session.commit()


def clean_price(price_str):
    try:
        clean_price = price_str.replace('$', '')
        clean_price = int(float(clean_price) * 100)
    except ValueError:
        print('''
        \nSorry, there was an error accepting the price value. \rPlease enter the price of the item in the following format: $5.95''')
    else:
        return clean_price


def clean_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        print('''
        \nSorry, there was an error accepting the date value.
        \rPlease enter the Product Date Updated in the following format:  01/01/2020 (MM/DD/YYYY)''')
    else:
        return date_obj


def app():
    pass


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    # app()
