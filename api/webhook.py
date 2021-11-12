import requests
import json
import time

SOW_WEBHOOK_URL = 'https://forex-notification.azurewebsites.net/sharkoutofwater'
MA_POST_WEBHOOK_URL= 'https://forex-notification.azurewebsites.net/masave'
MA_CHECK_WEBHOOK_URL='https://forex-notification.azurewebsites.net/macheck'

sellmsg = {"text": "XAUUSD Bullish SOW ended"}
buymsg = {"text": "XAUUSD Bearish SOW ended"}

above200ma = {"text": "XXAUUSD, Greater Than Moving Average (200, close, 0)"}
below200ma = {"text": "XAUUSD, Less Than Moving Average (200, close, 0)"}

r = requests.post(MA_POST_WEBHOOK_URL, data=json.dumps(above200ma), headers={'Content-Type': 'application/json'})

r = requests.post(SOW_WEBHOOK_URL, data=json.dumps(buymsg), headers={'Content-Type': 'application/json'})
