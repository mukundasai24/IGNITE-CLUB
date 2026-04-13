from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

# Import modularized components
from config import Config
from apiIntegration import APIIntegration

app = Flask(__name__, static_folder=Config.STATIC_FOLDER)

def init_db():
    conn = sqlite3.connect(Config.DB_NAME)
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

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        # 1. Save to SQLite Database
        conn = sqlite3.connect(Config.DB_NAME)
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
        
        # 2. Trigger External API (FormSubmit)
        # This replaces the need for the frontend to call FormSubmit directly!
        APIIntegration.send_to_formsubmit(data)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin')
def admin():
    # Fetch all records
    conn = sqlite3.connect(Config.DB_NAME)
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
    return html

# Static file serving
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    # Ensure working directory is correctly resolved
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    init_db()
    print(f"Flask Backend configured and running gracefully on port {Config.PORT}")
    app.run(port=Config.PORT, debug=True)
