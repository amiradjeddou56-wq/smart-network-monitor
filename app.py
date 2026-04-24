from flask import Flask, render_template, request, redirect
import sqlite3
import subprocess

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ip TEXT,
            port TEXT,
            type TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def ping(ip):
    try:
        subprocess.check_output(["ping", "-n", "1", ip])
        return "Actif"
    except:
        return "Inactif"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    import sqlite3
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    devices = c.execute("SELECT * FROM devices").fetchall()

    routers = sum(1 for d in devices if d[4] == "Routeur")
    switches = sum(1 for d in devices if d[4] == "Switch")

    conn.close()

    return render_template("dashboard.html",
                           devices=devices,
                           routers=routers,
                           switches=switches)

    return render_template("dashboard.html",
                           devices=devices,
                           routers=routers,
                           switches=switches)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        port = request.form['port']
        type_ = request.form['type']

        status = ping(ip)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO devices (name, ip, port, type, status) VALUES (?, ?, ?, ?, ?)",
                  (name, ip, port, type_, status))
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template("add_device.html")

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

if __name__ == "__main__":
    print("Server starting...")
    app.run(debug=True)
