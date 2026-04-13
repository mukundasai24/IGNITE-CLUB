import http.server
import socketserver
import sqlite3
import json
import urllib.parse
import os

PORT = 8000
DB_NAME = 'students.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            department TEXT NOT NULL,
            domain TEXT NOT NULL,
            email TEXT NOT NULL,
            events TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

class StudentHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO students (name, roll_number, department, domain, email, events)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('name', ''),
                    data.get('rollNumber', ''),
                    data.get('department', ''),
                    data.get('domain', ''),
                    data.get('email', ''),
                    data.get('events', '')
                ))
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

    def do_GET(self):
        if self.path == '/admin' or self.path == '/admin/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Fetch all records
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('SELECT id, name, roll_number, department, domain, email, events, created_at FROM students ORDER BY id DESC')
            records = c.fetchall()
            conn.close()
            
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Admin Dashboard - Registered Students</title>
                <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
                <style>
                    body {{ 
                        font-family: 'Plus Jakarta Sans', sans-serif; 
                        background-color: #f8fafc; 
                        color: #0f172a; 
                        margin: 0; 
                        padding: 3rem;
                    }}
                    h1 {{ color: #3b82f6; margin-bottom: 2rem; }}
                    table {{ 
                        width: 100%; 
                        border-collapse: collapse; 
                        background: white; 
                        border-radius: 12px; 
                        overflow: hidden; 
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }}
                    th, td {{ padding: 1.25rem 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                    th {{ background-color: #f1f5f9; font-weight: 600; color: #475569; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; }}
                    tr:last-child td {{ border-bottom: none; }}
                    tr:hover td {{ background-color: #f8fafc; }}
                    .empty {{ text-align: center; color: #64748b; padding: 3rem; font-style: italic; }}
                    .header-container {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }}
                    .btn-back {{ background: #0f172a; color: white; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 0.9rem; }}
                </style>
            </head>
            <body>
                <div class="header-container">
                    <h1>Student Registration Database</h1>
                    <a href="/" class="btn-back">Back to Portal</a>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Roll No</th>
                            <th>Dept</th>
                            <th>Domain</th>
                            <th>Email</th>
                            <th>Events/Workshops</th>
                            <th>Registered At</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            if not records:
                html += '<tr><td colspan="8" class="empty">No students have registered yet.</td></tr>'
            else:
                for r in records:
                    html += f"<tr><td>{r[0]}</td><td><strong>{r[1]}</strong></td><td>{r[2]}</td><td><span style='background:#e0e7ff;color:#4338ca;padding:0.2rem 0.6rem;border-radius:100px;font-size:0.8rem;white-space:nowrap;'>{r[3].upper()}</span></td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td><span style='color:#64748b;font-size:0.9rem;'>{r[7]}</span></td></tr>"
                    
            html += """
                    </tbody>
                </table>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            # Handle normal file serving requests (index.html, styles.css, etc.)
            if self.path == '/':
                self.path = '/index.html'
            return super().do_GET()

if __name__ == '__main__':
    # Ensure working directory is correctly resolved
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    init_db()
    with socketserver.TCPServer(("", PORT), StudentHandler) as httpd:
        print(f"Backend SQL server gracefully booted up and running at http://localhost:{PORT}")
        httpd.serve_forever()
