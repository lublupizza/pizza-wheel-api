import json
import requests
import os
from http.server import BaseHTTPRequestHandler
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8318266784:AAEMm9ODwttqCr3gbATJrjfU7Vkz0eBrcls"
ADMIN_ID = 450860374

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/api/result':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
                
                phone = data.get('phone', 'N/A')
                prize = data.get('prize', 'N/A')
                value = data.get('value', 'N/A')
                timestamp = data.get('timestamp', datetime.now().isoformat())
                
                # Формируем сообщение
                message = f"""📊 <b>НОВЫЙ РЕЗУЛЬТАТ РУЛЕТКИ</b>

📱 Номер: <code>{phone}</code>
🎁 Приз: <b>{prize}</b>
💰 Значение: <b>{value}</b>
⏰ Время: <code>{timestamp}</code>"""
                
                # Отправляем в Telegram
                try:
                    response = requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": ADMIN_ID,
                            "text": message,
                            "parse_mode": "HTML"
                        },
                        timeout=10
                    )
                    print(f"Telegram response: {response.status_code}")
                except Exception as e:
                    print(f"Telegram error: {e}")
                
                self.wfile.write(json.dumps({"success": True, "message": "Data received"}).encode())
                
            except Exception as e:
                print(f"Error: {e}")
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
        else:
            self.wfile.write(json.dumps({"success": False, "error": "Not found"}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
