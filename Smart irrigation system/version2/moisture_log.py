import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('soil_data.db')
cursor = conn.cursor()

# Fetch all records with timestamp and status
cursor.execute("SELECT timestamp, moisture_status FROM moisture_log")
rows = cursor.fetchall()

conn.close()

# Prepare data for plotting
timestamps = []
statuses = []

for row in rows:
    # Parse timestamp
    timestamps.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
    statuses.append(1 if row[1] == 'DRY' else 0)  # DRY = 1, WET = 0

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(timestamps, statuses, marker='o', color='blue', linewidth=2, label='Moisture Level')

plt.title("Soil Moisture Log Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Moisture Status (1=Dry, 0=Wet)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Format x-axis with better date formatting
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.tight_layout()
plt.show()
