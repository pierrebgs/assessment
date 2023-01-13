import json
from datetime import datetime, timedelta

class Car:
    def __init__(self, id, price_per_day, price_per_km):
        self.id = id
        self.price_per_day = price_per_day
        self.price_per_km = price_per_km

    def rental_price(self, start_date, end_date, distance):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end_date - start_date).days + 1
        time_component = 0
        price_per_day = self.price_per_day
        for i in range(days):
            if i == 0:
                time_component += self.price_per_day
            elif 1 <= i < 4:
                time_component += self.price_per_day * 0.9
            elif 4 <= i < 10:
                time_component += self.price_per_day * 0.7
            else:
                time_component += self.price_per_day * 0.5
        distance_component = distance * self.price_per_km
        return int(time_component + distance_component)

# load data from input.json
with open("data/input.json") as json_file:
    data = json.load(json_file)

# create a map of car id to car object 
car_map = {}
for car_data in data["cars"]:
    car = Car(car_data["id"], car_data["price_per_day"], car_data["price_per_km"])
    car_map[car.id] = car
    
result = {}
result["rentals"] = []
for rental_data in data["rentals"]:
    car = car_map[rental_data["car_id"]]
    rental_price = car.rental_price(rental_data["start_date"], rental_data["end_date"], rental_data["distance"])
    start_date = datetime.strptime(rental_data["start_date"], '%Y-%m-%d')
    end_date = datetime.strptime(rental_data["end_date"], '%Y-%m-%d')
    days = (end_date - start_date).days + 1
    commission = 0.3 * rental_price
    insurance_fee = commission / 2
    assistance_fee = days * 100
    drivy_fee = commission - insurance_fee - assistance_fee
    result["rentals"].append({
        "id": rental_data["id"], 
        "price": rental_price,
        "commission": {
            "insurance_fee": int(insurance_fee),
            "assistance_fee": int(assistance_fee),
            "drivy_fee": int(drivy_fee)
        }
    })


# save data to output.json
with open("data/output.json", "w") as json_file:
    json.dump(result, json_file, indent = 2)


