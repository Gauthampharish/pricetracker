import json
import websocket
import threading
from .models import Alert
# from django.db.models import Q
#from .tasks import send_price_alert_email

alerts = [
    {"cryptocurrency": "btcusdt", "target_price": 30000, "is_active": True, "user_email": "user@example.com"},
    {"cryptocurrency": "ethusdt", "target_price": 2000, "is_active": True, "user_email": "user2@example.com"}
]

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received message: {data}")

    if 'result' in data and data['result'] is None and 'id' in data:
        return

    if 's' in data and 'p' in data:
        symbol = data['s']
        price = float(data['p'])
    else:
        return

    # alerts = Alert.objects.filter(Q(cryptocurrency=symbol.lower()) & Q(status="created")).distinct()
    print(f"Alerts: {alerts}")
    for alert in alerts:
        if alert["cryptocurrency"] == symbol.lower() and alert["is_active"]:
            if (alert["target_price"] >= price and price >= alert["target_price"]) or (
                    alert["target_price"] <= price and price <= alert["target_price"]):
                print(f'The price of {symbol} has reached your target price of {alert["target_price"]}.')
                alert["is_active"] = False  # Simulate status change
            else:
                print(f'The price of {symbol} is now {price}. Target price is {alert["target_price"]}.')

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"### closed ### Status code: {close_status_code}, Message: {close_msg}")

def on_open(ws):
    alerts= Alert.objects.filter(status="created").values("cryptocurrency").distinct()

    subscription_params = [f'{alert["cryptocurrency"]}@trade' for alert in alerts]
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": subscription_params,
        "id": 1
    }))
    print(f"Sent subscription: {subscription_params}")

def start_price_tracker():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    def run_ws():
        ws.run_forever()

    ws_thread = threading.Thread(target=run_ws)
    ws_thread.start()

if __name__ == "__main__":
    start_price_tracker()