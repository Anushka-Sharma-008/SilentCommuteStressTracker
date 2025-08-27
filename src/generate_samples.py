import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

cities = ["CityA", "CityB", "CityC"]
routes = {"CityA": ["A1","A2"], "CityB": ["B1","B2"], "CityC": ["C1","C2"]}

start = datetime.today() - timedelta(days=90)
dates = [start + timedelta(days=i) for i in range(90)]

rows = []
for d in dates:
    for city in cities:
        for r in routes[city]:
            # Simulated values (realistic ranges)
            delay_minutes = max(0, np.random.normal(loc=8 if city=="CityA" else 12, scale=6))
            pm25 = max(1, np.random.normal(loc=40 if city=="CityB" else 20, scale=15))  # µg/m3
            noise_db = max(30, np.random.normal(loc=60, scale=8))
            # crowding factor: 1.0 normal, 1.5 peak, 2.0 extreme
            hour = np.random.choice([7,8,9,12,17,18])  # just simulate peak times
            crowding = 1.5 if hour in (7,8,17,18) else 1.0
            rows.append({
                "date": d.strftime("%Y-%m-%d"),
                "city": city,
                "route": r,
                "delay_minutes": round(delay_minutes,1),
                "pm25": round(pm25,1),
                "noise_db": round(noise_db,1),
                "crowding": crowding
            })

df = pd.DataFrame(rows)
df.to_csv("data/sample_commutes.csv", index=False)
print("Wrote data/sample_commutes.csv with", len(df), "rows")