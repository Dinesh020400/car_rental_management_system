from database import mongodb

USD_TO_INR_RATE = 83.0

# These look like they were already converted, so divide by 83 to get originals
cars = list(mongodb.cars.find())
print("Restoring to original USD prices, then converting to proper INR...")

for car in cars:
    current = car.get('price_per_day', 0)
    # Get back to original (assuming current is already multiplied)
    original_usd = current / USD_TO_INR_RATE
    # Now convert properly to INR
    proper_inr = round(original_usd * USD_TO_INR_RATE, 2)
    
    print(f"Car ID {car.get('id')}: Current={current}, Original USD={original_usd:.2f}, Proper INR={proper_inr}")
    
    # Set to proper INR price
    mongodb.cars.update_one(
        {'_id': car['_id']},
        {'$set': {'price_per_day': proper_inr}}
    )

print("\nDone!")
