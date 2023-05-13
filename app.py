from models import (Base, session, Product, engine)
import csv
import datetime
import time


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(
                Product.name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = row[2]
                date_updated = clean_date(row[3])
                new_product = Product(
                    product_name=product_name, product_price=product_price,
                    product_quantity=product_quantity, date_updated=date_updated)
                session.add(new_product)
                session.commit()


def clean_price(price):
    pass


def clean_date(date):
    pass


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # add_csv()
