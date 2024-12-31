import websocket
import json

# Fungsi untuk menangani pesan yang diterima dari WebSocket
def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get("event") == "price":
            # Menangkap data simbol, harga, dan timestamp
            symbol = data.get("symbol", "Unknown")
            price = data.get("price", "Unknown")
            timestamp = data.get("timestamp", "Unknown")
            # Menampilkan pembaruan harga real-time
            print(f"Real-time update - {symbol}: {price} at {timestamp}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Fungsi untuk menangani error
def on_error(ws, error):
    print(f"WebSocket Error: {error}")

# Fungsi untuk menangani koneksi yang ditutup
def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed. Status Code: {close_status_code}, Message: {close_msg}")

# Fungsi untuk menangani koneksi yang dibuka
def on_open(ws):
    # Pesan subscribe
    subscribe_message = {
        "action": "subscribe",
        "params": {
            "symbols": "USD/JPY"  # Simbol sebagai string
        }
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to USD/JPY real-time updates.")

# URL WebSocket dengan API Key untuk autentikasi
websocket_url = "wss://ws.twelvedata.com/v1/quotes/price?apikey=d732f0b5f8a94b7bb365a90a70eb2d57"

# Membuka koneksi WebSocket
ws = websocket.WebSocketApp(
    websocket_url,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
ws.on_open = on_open

# Jalankan WebSocket
print("Connecting to WebSocket for real-time data...")
ws.run_forever()
