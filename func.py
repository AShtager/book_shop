import sqlalchemy as sq
import models as m
from sqlalchemy.orm import sessionmaker
import json
import os
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
TYPE_DB = os.getenv("TYPE_DB")

DSN = f"{TYPE_DB}://{LOGIN}:{PASSWORD}@{HOST}/{DB_NAME}"
engine = sq.create_engine(url=DSN) # echo=True 

Session = sessionmaker(bind=engine)
session = Session()


def record_bd(file):
    with open(file) as f:
        data = json.load(f)

    for row in data:
        table = {
            "publisher": m.Publisher,
            "book": m.Book,
            "shop": m.Shop,
            "stock": m.Stock,
            "sale": m.Sale 
        }
        table_class = table[row.get("model")]
        session.add(table_class(id=row.get("pk"), **row.get("fields")))

    session.commit()

def enquiry_db(query_user):
    if query_user.isnumeric():
        res = session.query(m.Book.title, m.Shop.name, m.Sale.price, m.Sale.date_sale)\
            .join(m.Publisher, m.Publisher.id == m.Book.id_publisher)\
            .join(m.Stock, m.Stock.id_book == m.Book.id)\
            .join(m.Shop, m.Shop.id == m.Stock.id_shop)\
            .join(m.Sale, m.Sale.id_stock == m.Stock.id)\
            .filter(m.Publisher.id == query_user).all()
    else:
        res = session.query(m.Book.title, m.Shop.name, m.Sale.price, m.Sale.date_sale)\
            .join(m.Publisher, m.Publisher.id == m.Book.id_publisher)\
            .join(m.Stock, m.Stock.id_book == m.Book.id)\
            .join(m.Shop, m.Shop.id == m.Stock.id_shop)\
            .join(m.Sale, m.Sale.id_stock == m.Stock.id)\
            .filter(m.Publisher.name == query_user).all()
    
    for title, name, price, date_sale in res:
        print(f"{title} | {name} | {price} | {date_sale}")
    

session.close()
