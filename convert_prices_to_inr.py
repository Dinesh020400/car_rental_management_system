from database import mongodb

# Convert all existing car prices from USD to INR
USD_TO_INR_RATE = 83.0

cars = list(mongodb.cars.find())
print(f"Converting {len(cars)} cars from USD to INR pricing...")

for car in cars:
    old_price = car.get('price_per_day', 0)
    new_price = round(old_price * USD_TO_INR_RATE, 2)
    
    mongodb.cars.update_one(
        {'_id': car['_id']},
        {'$set': {'price_per_day': new_price}}
    )
    print(f"Car ID {car.get('id')}: ${old_price} -> ₹{new_price}")

print("\nConversion complete! All prices are now in INR.")
