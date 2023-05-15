from models import (Base, session, Product, engine)
import csv
from datetime import datetime
import time


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


def menu():
    print('\n***** PRODUCT INVENTORY *****')
    while True:
        print('''\rPlease select from the following options:
        \r1. View Product Details (enter 'v')
        \r2. Add New Product (enter 'a')
        \r3. Backup Database (enter 'b')
        \r4. Quit (enter 'q')''')
        choice = input('\nWhat would you like to do?  ').lower()
        if choice in ['v', 'a', 'b', 'q']:
            return choice
        else:
            print('''
            \nSorry, please enter a valid option:
            \rExample:
            \rv''')


def view_product():
    print("Available Product IDs:")
    products = session.query(Product).all()
    product_ids = []
    for product in products:
        product_ids.append(product.product_id)
    id_str = ', '.join(str(item) for item in product_ids)
    print(id_str)
    while True:
        id_selection = input('Please enter a product ID:  ')
        product_selection = session.query(Product).filter_by(
            product_id=id_selection).first()
        if product_selection:
            print(product_selection)
            break
        else:
            print('Invalid product ID. Please try again.')


def add_product():
    print("\nTo add a new product please enter the product details below:")
    product_name = input('\nProduct Name (ex: Basil):  ')
    quantity_error = True
    while quantity_error:
        product_quantity = input('Product Quantity (ex: 31):  ')
        try:
            product_quantity = int(product_quantity)
        except ValueError:
            ('Sorry, please enter a valid quantity (integer)')
        else:
            quantity_error = False
    price_error = True
    while price_error:
        product_price = input('Product Price (ex: $4.95):  ')
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False
    date_updated = datetime.today()
    new_product = Product(
        product_name=product_name,
        product_quantity=product_quantity,
        product_price=product_price,
        date_updated=date_updated)
    print(new_product)
    # session.add(new_product)
    # session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            view_product()
            input('Press enter to continue')
        elif choice == 'a':
            add_product()
        elif choice == 'q':
            return


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
