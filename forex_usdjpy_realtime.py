import websocket
import json

# Fungsi untuk menangani pesan yang diterima dari WebSocket
def on_message(ws, message):
    try:
        data = json.loads(message)

        # Periksa apakah event adalah "price"
        if data.get("event") == "price":
            # Menangkap data harga dan simbol
            symbol = data.get("symbol", "Unknown")
            price = data.get("price", "N/A")
            
            # Cek apakah bid dan ask tersedia dalam pesan
            bid = data.get("bid", None)
            ask = data.get("ask", None)
            
            # Jika bid dan ask tidak tersedia, hitung berdasarkan spread simulasi
            if bid is None or ask is None:
                spread = 0.02  # Spread simulasi
                bid = round(price - (spread / 2), 3)
                ask = round(price + (spread / 2), 3)

            # Menampilkan data dalam format yang diinginkan
            print(f"{symbol} | Bid = {bid} | Ask = {ask}")
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
    print("Sending Subscribe Message:", json.dumps(subscribe_message))
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
