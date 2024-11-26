from machine import UART, Pin, I2C
import time
import urequests
import ujson
from ahtx0 import AHT20
import network

# Firebase Configuration
FIREBASE_URL = "https://siotch-default-rtdb.europe-west1.firebasedatabase.app/"  # Replace with your Firebase URL
DB_PATH = "/air_quality.json"
FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" # Add API key on the end
EMAIL = "callum.hargrove21@imperial.ac.uk"  # Replace with your Firebase email
PASSWORD = ""  # Replace with your Firebase password
id_token = None  # Firebase authentication token

# Wi-Fi Configuration
WIFI_SSID = "Bethwall Guest"
WIFI_PASSWORD = "climbing"

# Unique Arch Identifier
ARCH_ID = "Arch "  # Change to "Arch B", "Arch C", "Arch D" for other devices

# ZPH02 Sensor Configuration
uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(13))  # TX (17), RX (13)

# AHT20 Sensor Configuration
i2c = I2C(0, scl=Pin(23), sda=Pin(22))  # D33 (SCL), D22 (SDA)

# Initialise AHT20 Sensor
try:
    aht20 = AHT20(i2c)
    print("AHT20 sensor initialised successfully.")
except OSError as e:
    print("Error initialising AHT20:", e)
    aht20 = None

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi:", wlan.ifconfig())

def authenticate():
    global id_token
    try:
        payload = {"email": EMAIL, "password": PASSWORD, "returnSecureToken": True}
        response = urequests.post(FIREBASE_AUTH_URL, json=payload)
        data = response.json()
        id_token = data.get("idToken")
        print("Successfully authenticated!")
    except Exception as e:
        print("Authentication failed:", e)

def read_zph02():
    if uart.any():
        data = uart.read(9)
        if data and data[0] == 0xFF and data[1] == 0x18:
            pm25 = (data[2] << 8) | data[3]
            pm10 = (data[4] << 8) | data[5]
            return pm25, pm10
    return None, None

def read_aht20():
    try:
        if aht20:
            temperature = aht20.temperature
            humidity = aht20.relative_humidity
            return round(temperature, 2), round(humidity, 2)
        else:
            print("AHT20 sensor not initialised.")
            return None, None
    except Exception as e:
        print("Error reading AHT20:", e)
        return None, None

def upload_to_firebase(data):
    try:
        if not id_token:
            print("No authentication token available!")
            return

        url = f"{FIREBASE_URL}{DB_PATH}?auth={id_token}"
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(url, headers=headers, data=ujson.dumps(data))
        print(f"Data uploaded: {response.status_code}")
        response.close()
    except Exception as e:
        print("Error uploading data:", e)

def main():
    connect_to_wifi()
    authenticate()
    print("Starting air quality monitoring...")

    while True:
        pm25, pm10 = read_zph02()
        temperature, humidity = read_aht20()

        if pm25 is not None and pm10 is not None:
            print(f"{ARCH_ID} - PM2.5: {pm25} µg/m³, PM10: {pm10} µg/m³")
        if temperature is not None and humidity is not None:
            print(f"{ARCH_ID} - Temperature: {temperature} °C, Humidity: {humidity} %")

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {
            "arch": ARCH_ID,
            "timestamp": timestamp,
            "pm25": pm25,
            "pm10": pm10,
            "temperature": temperature,
            "humidity": humidity
        }

        upload_to_firebase(data)
        time.sleep(30)

if __name__ == "__main__":
    main()
