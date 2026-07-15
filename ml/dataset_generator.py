import os
import random
import pandas as pd

os.makedirs("dataset", exist_ok=True)

records = []

brands = [
    "Indian Oil",
    "HP",
    "BPCL",
    "Shell",
    "Reliance"
]

weather_conditions = [
    "Clear",
    "Clouds",
    "Rain"
]

poi_levels = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

for _ in range(30000):

    hour = random.randint(0,23)

    weekday = random.randint(0,6)

    month = random.randint(1,12)

    holiday = 1 if weekday>=5 else 0

    weather = random.choice(weather_conditions)

    brand = random.choice(brands)

    poi_level = random.choice(poi_levels)

    pump_count = random.randint(4,10)

    service_time = round(random.uniform(2.2,3.0),2)

    demand = 0

    # Morning Peak

    if 7<=hour<=10:

        demand += 10

    # Evening Peak

    if 17<=hour<=21:

        demand += 15

    # Weekend

    if holiday:

        demand += 5

    # Rain

    if weather=="Rain":

        demand += 6

    # Commercial Area

    if poi_level=="HIGH":

        demand += 10

    elif poi_level=="MEDIUM":

        demand += 5

    # Brand

    if brand=="Indian Oil":

        demand += 5

    elif brand=="Shell":

        demand += 3

    demand += random.randint(-3,3)

    demand=max(demand,0)

    queue=min(demand,35)

    waiting=round(

        queue*

        service_time/

        pump_count,

        2

    )

    records.append({

        "hour":hour,

        "weekday":weekday,

        "month":month,

        "holiday":holiday,

        "weather":weather,

        "brand":brand,

        "poi_level":poi_level,

        "pump_count":pump_count,

        "service_time":service_time,

        "queue_length":queue,

        "waiting_time":waiting

    })

df=pd.DataFrame(records)

df.to_csv(

    "dataset/crowd_dataset.csv",

    index=False

)

print(df.head())

print()

print("Rows :",len(df))