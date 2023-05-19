from sqlalchemy import (create_engine, Column, Integer, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column('Name', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Date Updated', DateTime)

    def __repr__(self):
        return f'\nProduct: {self.product_name}\nID#: {self.product_id}\nQuantity: {self.product_quantity}\nPrice: ${float(self.product_price/100)}\nDate Updated: {self.date_updated.strftime("%m/%d/%Y")}'
