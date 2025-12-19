from database import mongodb

# Revert - divide by 83 to get back to original
USD_TO_INR_RATE = 83.0

cars = list(mongodb.cars.find())
print(f"Reverting {len(cars)} cars back to original prices...")

for car in cars:
    current_price = car.get('price_per_day', 0)
    original_price = round(current_price / USD_TO_INR_RATE, 2)
    
    mongodb.cars.update_one(
        {'_id': car['_id']},
        {'$set': {'price_per_day': original_price}}
    )
    print(f"Car ID {car.get('id')}: ₹{current_price} -> ${original_price}")

print("\nRevert complete!")
