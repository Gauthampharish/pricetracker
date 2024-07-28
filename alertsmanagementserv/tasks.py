# import asyncio
# import json
# import logging
# import websockets
# from django.core.mail import send_mail
# from django.conf import settings
# from alertsmanagementserv.models import Alert
# from asgiref.sync import sync_to_async

# # Configure logging

# # Get the logger for monitor_alerts
# logger = logging.getLogger('monitor_alerts')

# def monitor_alerts():
#     logging.info("Starting monitor_alerts task")
#     asyncio.run(monitor_binance())
#     logging.info("Finished monitor_alerts task")

# async def monitor_binance():
#     uri = settings.BINANCE_WS_URL
#     logging.info(f"Connecting to WebSocket at {uri}")
#     async with websockets.connect(uri) as websocket:
#         await websocket.send(json.dumps({
#             "method": "SUBSCRIBE",
#             "params": ["!ticker@arr"],
#             "id": 1
#         }))
#         logging.info("Subscribed to Binance ticker stream")
#         while True:
#             response = await websocket.recv()
#             data = json.loads(response)
#             logging.info("Received data from WebSocket")
#             await check_alerts(data)

# async def check_alerts(data):
#     logging.info("Checking alerts")
#     alerts = await sync_to_async(Alert.objects.filter)(status='created')
#     alerts_count = await sync_to_async(alerts.count)()
#     logging.info(f"Found {alerts_count} alerts with status 'created'")
#     for alert in alerts:
#         for ticker in data:
#             if ticker['s'] == alert.cryptocurrency.upper() and float(ticker['c']) >= alert.target_price:
#                 logging.info(f"Alert triggered for {alert.cryptocurrency} at price {ticker['c']}")
#                 # send_alert_email(alert)
#                 alert.status = 'triggered'
#                 await sync_to_async(alert.save)()
#                 logging.info(f"Updated alert status to 'triggered' for {alert.cryptocurrency}")

# def send_alert_email(alert):
#     logging.info(f"Sending email for alert {alert.cryptocurrency}")
#     send_mail(
#         'Price Alert Triggered',
#         f'The target price for {alert.cryptocurrency} has been reached.',
#         settings.DEFAULT_FROM_EMAIL,
#         [alert.user.email],
#         fail_silently=False,
#     )
#     logging.info(f"Email sent for alert {alert.cryptocurrency}")