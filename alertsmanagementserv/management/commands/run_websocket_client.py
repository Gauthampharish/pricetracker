import asyncio
import websockets
import json
from django.core.management.base import BaseCommand
from alertsmanagementserv.models import Alert
from asgiref.sync import sync_to_async
import logging
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

logger = logging.getLogger(__name__)
@shared_task
def send_email_task(user_email, symbol):
    
    send_mail(
        'Price Alert Triggered',
        f'The target price for {symbol} has been reached.',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )

class Command(BaseCommand):
    help = 'Runs the Binance WebSocket client for price alerts for 1 minute'

    @sync_to_async
    def get_alerts(self, symbol):
        return list(Alert.objects.filter(cryptocurrency=symbol, status='created'))
    @sync_to_async
    def get_symbols(self):
        return list(Alert.objects.values_list('cryptocurrency', flat=True).distinct())
    @sync_to_async
    def update_alert(self, alert, status):
        alert.status = status
        alert.save()

    @sync_to_async
    def get_user_email(self, alert):
        return alert.user.email
    
    @sync_to_async
    def get_target_price(self, alert):
        return alert.target_price
    

    
        
    async def log_alert(self, symbol, price, alert):

        user_email= await self.get_user_email(alert)
        target_price= await self.get_target_price(alert)
        self.stdout.write(self.style.SUCCESS(
            f"ALERT TRIGGERED: {symbol} at {price}. "
            f"User: {user_email}, Target: {target_price}"
        ))
        send_email_task.delay(user_email, symbol)

    

    async def process_ticker(self, ticker,symbols):
        symbol = ticker['s']
        if symbol not in symbols:
            return
        price = round(float(ticker['c']))
        
        alerts = await self.get_alerts(symbol)
        
        
        for alert in alerts:
            if alert.target_price<=price:
                # Log alert in a different color
                await self.log_alert(symbol, price, alert)
                self.stdout.write(self.style.SUCCESS(
                    f"ALERT TRIGGERED: {symbol} at {price}. "
        ))
                
                await self.update_alert(alert, 'triggered')
          
    async def binance_websocket(self):
        uri = "wss://stream.binance.com:9443/ws/!ticker@arr"
        symbols= await self.get_symbols()
        async with websockets.connect(uri) as websocket:
            self.stdout.write(self.style.SUCCESS("Connected to Binance WebSocket"))
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                   
                   
                    filtered_data = [ticker for ticker in data if ticker['s'] in symbols]
                    for ticker in filtered_data:
                        
                        await self.process_ticker(ticker,symbols)
                except asyncio.TimeoutError:
                    # This allows us to check the time condition more frequently
                    continue
                except websockets.exceptions.ConnectionClosed:
                    self.stdout.write(self.style.WARNING("WebSocket connection closed."))
                    await asyncio.sleep(5) 
            
        

    def handle(self, *args, **options):
       
        asyncio.run(self.binance_websocket())