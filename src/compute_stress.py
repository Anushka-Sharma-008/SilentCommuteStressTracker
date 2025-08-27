import pandas as pd
import numpy as np

df = pd.read_csv("data\clean_commutes.csv")
df['date'] = pd.to_datetime(df['date'])

# Delay normalization
# cap delays at 60 min so outliers don't explode the score
delay_cap = 60.0
df['delay_capped'] = df['delay_minutes'].clip(0, delay_cap)
# normalize 0..1
df['delay_norm'] = df['delay_capped'] / delay_cap

# PM2.5 -> aqi_norm (simple mapping)
# Map pm25 to a 0..1 scale:
# 0-12 µg/m3 -> 0..0.2 (good)
# 12-35 -> 0.2..0.5 (moderate)
# 35-55 -> 0.5..0.8 (unhealthy for sensitive)
# 55+ -> 0.8..1.0 (unhealthy+)
def pm25_to_norm(x):
    if x <= 12:
        return (x/12)*0.2
    if x <= 35.4:
        return 0.2 + (x-12)/(35.4-12)*(0.3)
    if x <= 55.4:
        return 0.5 + (x-35.4)/(55.4-35.4)*(0.3)
    # above 55.4
    return 0.8 + min((x-55.4)/100, 0.2)  # cap at +0.2

df['aqi_norm'] = df['pm25'].apply(pm25_to_norm).clip(0,1)

# Noise normalization
# Typical urban values: 30 dB (quiet) to 100 dB (very loud). We'll map 30..100 -> 0..1
noise_min, noise_max = 30.0, 100.0
df['noise_norm'] = ((df['noise_db'] - noise_min) / (noise_max - noise_min)).clip(0,1)

# Crowding normalization
# crowding factor is already 1.0..2.0; map 1.0 -> 0, 2.0 -> 1.0
df['crowd_norm'] = (df['crowding'] - 1.0) / (2.0 - 1.0)
df['crowd_norm'] = df['crowd_norm'].clip(0,1)

# Geometric mean (multiplicative feel)
df['stress_geo'] = (df['delay_norm'] * df['aqi_norm'] * df['noise_norm'] * df['crowd_norm']).pow(1/4)
df['stress_pct'] = (df['stress_geo'] * 100).round(1)

# Save
df.to_csv("data/with_stress.csv", index=False)
print("Saved data/with_stress.csv — sample:")
print(df[['date','city','route','delay_minutes','pm25','noise_db','crowding','stress_pct']].head())