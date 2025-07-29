from flask import Flask, render_template, request, redirect, url_for, session
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL 資料庫連接設置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ray_930715',
    'database': 'traffic_fines'
}

# 儲存資料到資料庫
def save_to_database(image_file, license_plate, is_recognized, employee_id, ip_address):
    image_path = os.path.join('static', 'uploads', image_file.filename)
    image_file.save(image_path)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fines (employee_id, event_time, ip_address, license_plate, is_recognized, image)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (employee_id, datetime.now(), ip_address, license_plate, is_recognized, image_path))
    conn.commit()
    cursor.close()
    conn.close()

# 用戶驗證
def authenticate_user(username, password):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    if user:
        ip_address = request.remote_addr
        cursor.execute("UPDATE users SET ip_address = %s WHERE id = %s", (ip_address, user['id']))
        conn.commit()
    
    cursor.close()
    conn.close()
    return user

# 登入頁面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="無效的帳號或密碼")
    return render_template('login.html')

# 登出
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 主頁
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        image = request.files.get('image')
        is_recognized = request.form.get('is_recognized')
        ip_address = request.remote_addr

        # 驗證是否成功辨識
        if is_recognized == 'yes':
            license_plate_letter = request.form.get('license_plate_letter')
            license_plate_number = request.form.get('license_plate_number')

            if not license_plate_letter or not license_plate_number:
                return render_template('index.html', error="請輸入完整的車牌號碼")

            license_plate = f"{license_plate_letter}-{license_plate_number}"
        else:
            license_plate = None  # 無法辨識時不需要車牌

        # 儲存到資料庫
        save_to_database(image, license_plate, 'yes' if is_recognized == 'yes' else 'no',
                         session['user_id'], ip_address)

        return render_template('index.html', success="資料已儲存！")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
