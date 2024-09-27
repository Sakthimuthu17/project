from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from flask_session import Session
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

ADMIN_CREDENTIALS = {
    'Admin': 'admin',
    'Sakthi': '12345'
}

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      mail TEXT NOT NULL,
                      date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mail = request.form['mail']
    date_str = request.form['date']
    appointment_date = datetime.strptime(date_str, '%Y-%m-%d')
    current_date = datetime.now()

    if appointment_date < current_date:
        flash("Error: The appointment date cannot be in the past.")
        return redirect(url_for('index'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(name, mail, date) VALUES (?, ?, ?)', (name, mail, date_str))
    conn.commit()
    conn.close()

    flash(f"Appointment confirmed for {name} on {date_str}. A confirmation email will be sent to {mail}.")
    return redirect(url_for('index'))  # Redirect to index after submitting

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['logged_in'] = True
            flash('Successfully logged in!')
            return redirect(url_for('result'))  # Redirect to result after successful login
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))  # Redirect back to login on failure

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Successfully logged out. Please log in again.')
    return redirect(url_for('login'))  # Redirect to login page after logout

# Result route
@app.route('/result')
def result():
    if 'logged_in' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('result.html',data=data)  # Create a result.html template
conn=sqlite3.connect('database.db')
cursor=conn.cursor()
cursor.execute('SELECT * FROM users')
data=cursor.fetchall()
conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
