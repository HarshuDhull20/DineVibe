from http.server import BaseHTTPRequestHandler
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        email = data.get('email', '')
        new_password = data.get('new_password', '')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Password validation rules
        errors = []
        
        if len(new_password) < 8:
            errors.append("Minimum 8 characters required")
        if not re.search(r'[A-Z]', new_password):
            errors.append("At least one uppercase letter required")
        if not re.search(r'[a-z]', new_password):
            errors.append("At least one lowercase letter required")
        if not re.search(r'[0-9]', new_password):
            errors.append("At least one number required")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            errors.append("At least one special character required (!@#$%^&*)")
        
        if errors:
            response = {
                "status": "ERROR",
                "message": "Password does not meet requirements",
                "errors": errors
            }
        else:
            response = {
                "status": "SUCCESS",
                "access_token": "demo_token_after_password_set",
                "user": {
                    "name": email.split('@')[0].title(),
                    "email": email,
                    "role": "admin"
                },
                "message": "Password set successfully"
            }
        
        self.wfile.write(json.dumps(response).encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
