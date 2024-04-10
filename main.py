import models as m
import func as f
from pprint import pprint


user_query = input("Введите имя или идентификатор издателя: ")

m.create_table(f.engine)
f.record_bd("book_json.json")
f.enquiry_db(user_query)
