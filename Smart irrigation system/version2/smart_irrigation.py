import lgpio
import time
import sqlite3

# GPIO Pin Assignments
SOIL_MOISTURE_PIN = 27  # Soil Sensor Digital Output (D0)
RELAY_PIN = 25  # Relay (to control pump)

import requests

api_key = '0b11caa46ef26158931c68d5661f552e'

user_input = "banashankari"

weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}"
)

data = weather_data.json()

if data['cod'] == '404':
    print("No City Found")
else:
    weather = data['weather'][0]['main']
    temp = round(data['main']['temp'])

    print(f"The weather in {user_input} is: {weather}")
    print(f"The temperature in {user_input} is: {temp}ºF")

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Configure GPIO pins
lgpio.gpio_claim_input(h, SOIL_MOISTURE_PIN, lgpio.SET_PULL_DOWN)  # Soil Sensor
lgpio.gpio_claim_output(h, RELAY_PIN)  # Relay Control

# Connect to SQLite Database
conn = sqlite3.connect("soil_data.db")
cursor = conn.cursor()

def log_data(moisture_status):
    """Store data in SQLite database."""
    cursor.execute("INSERT INTO moisture_log (moisture_status) VALUES (?)", (moisture_status,))
    conn.commit()

def turn_pump_on():
    lgpio.gpio_write(h, RELAY_PIN, 1)  # Reset previous state
    time.sleep(0.5)  # Small delay to ensure reset
    lgpio.gpio_write(h, RELAY_PIN, 0)  # Activate relay, pump ON
    print("💧 Soil is DRY... Pump ON - Watering Soil")
    log_data("DRY")

def turn_pump_off():
    lgpio.gpio_write(h, RELAY_PIN, 0)  # Reset previous state
    time.sleep(0.5)  # Small delay to ensure reset
    lgpio.gpio_write(h, RELAY_PIN, 1)  # Deactivate relay, pump OFF
    print("✅ Soil is WET... Pump OFF - Soil is Moist")
    log_data("WET")


def read_soil_moisture():
    pin_value = lgpio.gpio_read(h, SOIL_MOISTURE_PIN)
    print(f"Sensor Reading: {pin_value}") 

    if pin_value == 0:  # Soil is Wet
        turn_pump_off()
    else:  # Soil is Dry
        if weather.lower() in ["rain", "drizzle","clouds", "thunderstorm"]:
            print("It is raining outside! or about to rain")
            turn_pump_off()
        else:
            turn_pump_on()


try:
    while True:
        read_soil_moisture()
        time.sleep(5)  # Check moisture every 5 seconds
except KeyboardInterrupt:
    print("\n🚨 Program terminated")
    turn_pump_off()  # Turn off pump before exiting
    lgpio.gpiochip_close(h)  # Cleanup GPIO
    conn.close()  # Close database connection