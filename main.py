from machine import UART, Pin
import time
import urequests
import ujson
import network

# Firebase Configuration
FIREBASE_URL = "https://siotch-default-rtdb.europe-west1.firebasedatabase.app/"  # Replace with your Firebase URL
DB_PATH = "/pm25_data.json"  # Path to store data in Firebase

# Wi-Fi Configuration
WIFI_SSID = "12 Brompton Lodge"
WIFI_PASSWORD = "01052001"

# Sensor Configuration
uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(13))  # UART1: TX (17), RX (13)
sensor_pin = Pin(13, Pin.IN)

def connect_to_wifi():
    """Connect to Wi-Fi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi:", wlan.ifconfig())

def read_pm25():
    """Read PM2.5 data from ZPH02 sensor via UART."""
    if uart.any():
        data = uart.read(9)  # Read 9-byte frame
        if data[0] == 0xFF and data[1] == 0x18:  # Validate frame start
            pm25 = (data[2] << 8) | data[3]  # Combine bytes for PM2.5
            return pm25
    return None

def upload_to_firebase(pm25):
    """Upload PM2.5 reading to Firebase Realtime Database."""
    try:
        timestamp = time.time()  # Get current timestamp
        data = {
            "timestamp": timestamp,
            "pm25": pm25
        }
        url = FIREBASE_URL + DB_PATH
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(url, headers=headers, data=ujson.dumps(data))
        print("Data uploaded:", response.status_code)
        response.close()
    except Exception as e:
        print("Error uploading data:", e)

def main():
    """Main program loop."""
    connect_to_wifi()
    print("Starting PM2.5 monitoring...")
    
    while True:
        pm25 = read_pm25()
        if pm25 is not None:
            print(f"PM2.5: {pm25} µg/m³")
            upload_to_firebase(pm25)
        else:
            print("Sensor read failed or no data available.")
        time.sleep(30)  # Recommended interval: 30 seconds

if __name__ == "__main__":
    main()
