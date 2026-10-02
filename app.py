import random
import datetime
from flask import Flask, render_template, request, jsonify
import pywhatkit as kit
import mysql.connector

app = Flask(__name__)

# Configure your SQL Database connection details here
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Tabran@007',
    'database': 'college_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    phone = data.get('phone') # Format must include country code, e.g., +91...
    password = data.get('password') # In production, ensure you hash this with bcrypt!

    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
        if cursor.fetchone():
            return jsonify({'success': False, 'error': 'Phone number already registered.'}), 400

        # Insert user data and temporary OTP
        query = "INSERT INTO users (name, phone, password, otp, is_verified) VALUES (%s, %s, %s, %s, FALSE)"
        cursor.execute(query, (name, phone, password, otp))
        conn.commit()
        cursor.close()
        conn.close()

        # Trigger WhatsApp message delivery via pywhatkit
        # Note: Time calculations configure the browser to fire text in roughly 15-20 seconds
        now = datetime.datetime.now()
        send_hour = now.hour
        send_min = now.minute + 1
        if send_min >= 60:
            send_min = 0
            send_hour = (send_hour + 1) % 24

        message = f"Hello {name}, your college project verification OTP is: *{otp}*. Valid for 5 minutes."
        
        # This will open your local browser window to dispatch the message through your logged-in WhatsApp Web
        kit.sendwhatmsg(phone, message, send_hour, send_min, wait_time=15, tab_close=True)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone = data.get('phone')
    user_otp = data.get('otp')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT otp, is_verified FROM users WHERE phone = %s", (phone,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'User not found.'}), 404

    if user['otp'] == user_otp:
        # Mark user as verified and clear OTP
        cursor.execute("UPDATE users SET is_verified = TRUE, otp = NULL WHERE phone = %s", (phone,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    else:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Invalid OTP. Please try again.'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)