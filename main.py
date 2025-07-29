import base64
from datetime import datetime
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, session, jsonify, send_file
from flask_session import Session
from api.endpoints import violations
from config.database import db  # 引入資料庫設定
from decouple import config
import os
from sqlalchemy import text
from api.routes import init_routes
from model.database import ViolationRecord
from services.fine import convert_violation_to_pdf, generate_pdf_file_path, get_violation_data_from_ticket_view

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # 用來加密 session 的密鑰

# 設定 Session 配置
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系統存儲 Session
app.config['SECRET_KEY'] = 'your_secret_key'  # 替換為安全密鑰
Session(app)

# 設定主要資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='mysql+pymysql://root:Ray_930715@localhost/traffic_enforcement')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 防止警告

# 設定多個資料庫 URL
app.config['SQLALCHEMY_BINDS'] = {
    'vehicle_registry': config('VEHICLE_DATABASE_URL', default='mysql+pymysql://root:Ray_930715@localhost/vehicle_registry'),
    'traffic_fines': config('TRAFFIC_FINE_DATABASE_URL', default='mysql+pymysql://root:Ray_930715@localhost/traffic_fines') 
}

# 初始化資料庫
db.init_app(app)

# 定义 User 模型并绑定到 'traffic_fines' 数据库
class User(db.Model):
    __bind_key__ = 'traffic_fines'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 設置 id 為主鍵
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class OpenFineUser(db.Model):
    __bind_key__ = 'traffic_fines'
    __tablename__ = 'openfine_users'
    id = db.Column(db.Integer, primary_key=True)  # 設置 id 為主鍵
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

init_routes(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 使用 ORM 查询，SQLAlchemy 自动使用绑定的数据库
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['user_type'] = 'user'
            return redirect(url_for("manual_page"))
        else:
            # 當帳號密碼錯誤時，傳遞錯誤訊息到前端
            return render_template('login.html', error_message="帳號或密碼錯誤，請再試一次。")

    return render_template('login.html')


@app.route('/openfine_login', methods=['GET', 'POST'])
def openfine_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 使用 ORM 查询，SQLAlchemy 自动使用绑定的数据库
        user = OpenFineUser.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['user_type'] = 'openfine_user'
            return redirect(url_for("openfine_page"))
        else:
            # 當帳號密碼錯誤時，傳遞錯誤訊息到前端
            return render_template('openfine_login.html', error_message="帳號或密碼錯誤，請再試一次。")

    return render_template('openfine_login.html')


# 登出功能
@app.route('/logout', methods=['POST'])
def logout():
    user_type = session.get('user_type')
    session.pop('user_id', None)
    session.pop('user_type', None)
    if user_type == 'openfine_user':
        return redirect(url_for('openfine_login'))  # 登出後返回 openfine 登入頁面
    else:
        return redirect(url_for('login'))  # 登出後返回登入頁面

# 設定根路由來返回 index.html
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

# 受保護的 manual 路由
@app.route('/manual')
def manual_page():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))
    # 從資料庫查詢所有的違規紀錄
    violations = db.session.execute(
        text('SELECT * FROM traffic_enforcement.violation_records')
    ).fetchall()

    # 將資料傳遞給 manual.html 模板
    return render_template('manual.html', violations=violations)

# openfine 路由
@app.route('/openfine')
def openfine_page():
    if 'user_id' not in session or session.get('user_type') != 'openfine_user':
        return redirect(url_for('openfine_login'))
    # 從資料庫查詢所有的違規紀錄
    violations = db.session.execute(
        text('SELECT * FROM traffic_enforcement.violation_records')
    ).fetchall()

    # 渲染 openfine.html 模板，並傳遞違規資料
    return render_template('openfine.html', violations=violations)

# 設定根路由來返回 index.html
@app.route('/search')
def search_page():
    return render_template('search.html', violations=violations)

def get_violation_data(id):
    result = db.session.execute(
        text('SELECT * FROM traffic_enforcement.violation_records WHERE id = :id'),
        {'id': id}
    ).fetchone()
    
    if result:
        return {
            'id': result['id'],
            'license_plate': result['license_plate'],
            'violation_type': result['violation_type'],
            'violation_date': result['violation_date'],
            'fine_amount': result['fine_amount']
        }
    return None

@app.route("/ticket/<int:id>")
def generate_ticket(id):
    # 確認 get_violation_data_from_ticket_view 函數返回了數據
    violation_data = get_violation_data_from_ticket_view(id)
    print(violation_data)
    if not violation_data:
        print(f"違規資料未找到: {id}")
        return jsonify({"error": "違規資料未找到"}), 404
    
    try:
        # 嘗試生成 PDF
        pdf_path = generate_pdf_file_path(id)
        print(f"生成 PDF 路徑: {pdf_path}")  # 輸出檔案路徑調試
        convert_violation_to_pdf(violation_data, pdf_path)
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"error": f"內部伺服器錯誤: {str(e)}"}), 500

    if not os.path.exists(pdf_path):
        print(f"PDF 文件生成失敗: {pdf_path}")
        return jsonify({"error": f"PDF 文件生成失敗: {pdf_path}"}), 500

    try:
        violation = ViolationRecord.query.filter_by(id=id).first()
        if violation:
            violation.ticket = True
            db.session.commit()  # 提交更改
    except Exception as e:
        db.session.rollback()
        print(f"更新 ticket 狀態失敗: {str(e)}")
        return jsonify({"error": f"更新 ticket 狀態失敗: {str(e)}"}), 500

    try:
        # 插入資料到 fines_log 表中
        printed_by = session.get('user_id', 0)  # 假設 session 中存儲了用戶 ID
        ip_address = request.remote_addr
        printed_image = violation_data.get('vehicle_image', b'')

        db.session.execute(
            text('''
                INSERT INTO traffic_fines.fines_log (ticket_id, printed_by, print_time, ip_address, printed_image)
                VALUES (:ticket_id, :printed_by, :print_time, :ip_address, :printed_image)
            '''),
            {
                'ticket_id': id,
                'printed_by': printed_by,
                'print_time': datetime.utcnow(),
                'ip_address': ip_address,
                'printed_image': printed_image
            }
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"插入 fines_log 失敗: {str(e)}")
        return jsonify({"error": f"插入 fines_log 失敗: {str(e)}"}), 500

    # 使用 send_file 觸發下載
    return send_file(pdf_path, as_attachment=True, download_name=f"ticket_{id}.pdf")

@app.route('/api/fines_log', methods=['GET'])
def get_fines_log():
    query = text("""
    SELECT fl.log_id, fl.ticket_id, fl.printed_by, fl.print_time, fl.ip_address, fl.printed_image
    FROM traffic_fines.fines_log fl
    JOIN traffic_enforcement.violation_records vr ON fl.ticket_id = vr.id
    ORDER BY fl.print_time DESC;
    """)
    result = db.session.execute(query).fetchall()
    
    if result:
        logs = []
        for row in result:
            log_entry = {
                'log_id': row[0],
                'ticket_id': row[1],
                'printed_by': row[2],
                'print_time': row[3],
                'ip_address': row[4],
                'printed_image': base64.b64encode(row[5]).decode('utf-8') if row[5] else None  # 將二進位圖像轉為 Base64 字符串
            }
            logs.append(log_entry)
        
        return jsonify(logs)  # 返回所有紀錄作為 JSON
    else:
        print(f"開單紀錄未找到")
        return jsonify([])  # 如果沒有紀錄，返回空列表

from sqlalchemy import text

@app.route('/api/query_violations', methods=['POST'])
def query_violations():
    try:
        # 從 POST 請求中獲取資料
        data = request.get_json()
        id_card = data.get('idCard')  # 身分證字號
        birthdate = data.get('birthdate')  # 出生年月日

        # 查詢 vehicle_registration 資料表，根據身分證字號與出生日期取得車牌
        vehicle_query = text("""
            SELECT license_plate 
            FROM vehicle_registration.vehicle_registration 
            WHERE owner_id_number = :id_card AND birth_date = :birthdate
        """)
        vehicle_result = db.session.execute(vehicle_query, {'id_card': id_card, 'birthdate': birthdate}).fetchone()

        if not vehicle_result:
            return jsonify({"success": False, "message": "查無車主資料"}), 400

        license_plate = vehicle_result[0]  # 取得車牌號碼

        # 根據車牌查詢違規紀錄，只選取 ticket = 1 的紀錄
        violations_query = text("""
            SELECT id, license_plate, location, speed_limit, current_speed, date_time
            FROM traffic_enforcement.violation_records
            WHERE license_plate = :license_plate AND ticket = 1
        """)
        result = db.session.execute(violations_query, {'license_plate': license_plate})
        violations = result.fetchall()

        if not violations:
            return jsonify({"success": False, "message": "查無違規紀錄"}), 400

        # 格式化查詢結果
        violation_data = [
            {
                'ticket_id': violation[0],
                'license_plate': violation[1],
                'violation_location': violation[2],
                'speed_limit': violation[3],
                'actual_speed': violation[4],
                'violation_time': violation[5]
            }
            for violation in violations
        ]

        # 回傳查詢結果
        return jsonify({"success": True, "violations": violation_data})

    except Exception as e:
        print("查詢錯誤:", e)  # 在控制台打印具體錯誤，便於調試
        return jsonify({"success": False, "message": "查詢發生錯誤", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

