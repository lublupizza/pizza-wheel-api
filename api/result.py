import json
import requests
from http.server import BaseHTTPRequestHandler
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8318266784:AAEMm9ODwttqCr3gbATJrjfU7Vkz0eBrcls"
ADMIN_ID = 450860374

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/result':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body)
                
                phone = data.get('phone', 'N/A')
                prize = data.get('prize', 'N/A')
                value = data.get('value', 'N/A')
                
                message = f"""📊 НОВЫЙ РЕЗУЛЬТАТ РУЛЕТКИ

📱 Номер: {phone}
🎁 Приз: {prize}
💰 Значение: {value}
⏰ Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"""
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_ID,
                        "text": message,
                        "parse_mode": "HTML"
                    }
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.end_headers()
