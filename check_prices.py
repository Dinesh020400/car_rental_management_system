from database import mongodb

cars = list(mongodb.cars.find())
print('Sample car prices:')
for c in cars[:3]:
    print(f"ID: {c.get('id')}, Make: {c.get('make')}, price_per_day: {c.get('price_per_day')}")
