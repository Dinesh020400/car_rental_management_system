from database import mongodb

# Check current prices
cars = list(mongodb.cars.find())
print("Current car prices:")
for car in cars:
    print(f"Car ID {car.get('id')}: price_per_day = {car.get('price_per_day')}")
