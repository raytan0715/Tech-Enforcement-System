from datetime import datetime
from flask import Blueprint, jsonify, request, send_file, session
from sqlalchemy import text
from sqlalchemy import or_, and_
from model.database import ViolationRecord  # 引入違規記錄資料模型
from config.database import db
from pathlib import Path
from io import BytesIO
import base64
# 在 Flask 路由中加入這個API來取得列印紀錄
from flask import jsonify
from services.violation_process import check_license_plate_in_database

manual_bp = Blueprint('manual', __name__)

# 查詢人工辨識資料
@manual_bp.route('/manual', methods=['GET'])
def get_manual_violations():
    violations = ViolationRecord.query.filter(ViolationRecord.recognition.isnot(None)).all()

    # 構建結果
    violation_list = []
    for violation in violations:
        # 如果圖片是 BLOB 格式，則將其轉換為 base64 字串
        image = None
        if violation.image:
            img_data = violation.image  # BLOB 格式圖片
            img_base64 = base64.b64encode(img_data).decode('utf-8')  # 編碼為 base64
            image = f"data:image/jpeg;base64,{img_base64}"  # 假設圖片是 JPEG 格式


        violation_list.append({
            'id': violation.id,
            'license_plate': violation.license_plate,
            'location': violation.location,
            'speed_limit': violation.speed_limit,
            'current_speed': violation.current_speed,
            'date_time': violation.date_time.strftime('%Y-%m-%d %H:%M'),
            'error_code': violation.error_code,
            'recognition': violation.recognition,
            'image': image,  # 這裡返回 base64 編碼的圖片數據
        })

    # 回傳資料給前端
    return jsonify(violation_list)  # 返回 JSON 格式的数据

# 更新車牌號碼
@manual_bp.route('/manual/update/<int:id>', methods=['POST'])
def update_license_plate(id):
    data = request.get_json()  # 取得 POST 請求的 JSON 資料
    new_license_plate = data.get('license_plate')
    new_error_code = data.get('error_code')

    # 查找違規記錄
    violation = ViolationRecord.query.get(id)
    if violation:
        if new_license_plate:
            # 如果提供了新的車牌號，則更新車牌號
            print(f"更新車牌: {violation.license_plate} -> {new_license_plate}")
            violation.license_plate = new_license_plate
        # 更新錯誤代碼
        violation.error_code = new_error_code
        violation.recognition = True
        db.session.commit()  # 提交更改

        # 假設用戶 ID 來自於 session
        employee_id = session.get('user_id')  # 交通佐理員的 ID
        print(employee_id)
        ip_address = request.remote_addr  # 獲取處理請求的 IP 地址
        image = violation.image  # 假設圖片已經保存在違規記錄中
        is_recognized = 'yes' if violation.recognition else 'no'  # 辨識結果

        sql = """
            INSERT INTO traffic_fines.fines
            (employee_id, ip_address, license_plate, is_recognized, image, timestamp)
            VALUES
            (:employee_id, :ip_address, :license_plate, :is_recognized, :image, :timestamp)
        """

        try:
            # 执行数据库操作并提交
            db.session.execute(
                text(sql).execution_options(bind='traffic_fines'), 
                {
                    'employee_id': employee_id,
                    'ip_address': ip_address,
                    'license_plate': new_license_plate if new_license_plate else violation.license_plate,
                    'is_recognized': is_recognized,
                    'image': image,
                    'timestamp': datetime.now()
                }
            )
            db.session.commit()  # 提交事务
            return jsonify({'success': True}), 200
        except Exception as e:
            # 回滚事务
            db.session.rollback()  
            print(f"Error inserting into database: {e}")  # 打印详细错误信息
            return jsonify({'success': False, 'message': f"Error inserting into database: {str(e)}"}), 500
    else:
        return jsonify({'success': False, 'message': 'Violation not found'}), 404


# 新增返回圖片的路由
@manual_bp.route('/manual/image/<int:id>', methods=['GET'])
def get_violation_image(id):
    # 根據 id 查找違規記錄
    violation = ViolationRecord.query.get(id)
    if violation and violation.image:
        # 從 BLOB 資料庫中讀取圖片 BLOB
        img_data = violation.image

        # 使用 BytesIO 來處理二進制資料
        img_io = BytesIO(img_data)
        return send_file(img_io, mimetype='image/jpeg')  # 假設圖片是 JPEG 格式
    else:
        return jsonify({'success': False, 'message': 'Image not found'}), 404


@manual_bp.route('/fines', methods=['GET'])
def get_all_fines():
    # 查询 traffic_fines.fines 表的所有记录
    sql = """
        SELECT id, employee_id, ip_address, license_plate, timestamp
        FROM traffic_fines.fines
    """
    try:
        # 执行查询语句
        results = db.session.execute(text(sql).execution_options(bind='traffic_fines')).fetchall()

        # 构建返回数据
        fines_list = []
        for row in results:
            fines_list.append({
                'id': row[0],  # 使用索引访问元组
                'employee_id': row[1],
                'ip_address': row[2],
                'license_plate': row[3],
                'timestamp': row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None
            })
        return jsonify(fines_list), 200
    except Exception as e:
        # 捕获并返回错误信息
        print(f"Error querying fines table: {e}")
        return jsonify({'success': False, 'message': f"Error querying fines table: {str(e)}"}), 500


@manual_bp.route('/tk', methods=['GET'])
def get_ticket_able():
    query = text("""
        SELECT *
        FROM traffic_fines.ticket_view
    """)

    # 執行查詢並獲取所有資料
    results = db.session.execute(query).fetchall()

    fine_list = []
    for row in results:
        result_code = check_license_plate_in_database(row.license_plate)

        # 查找並更新對應的 violation_record
        violation_record = ViolationRecord.query.filter_by(id=row.violation_id).first()

        if violation_record:  # 確保有找到對應的記錄
            violation_record.error_code = result_code
            db.session.commit()  # 提交更改到資料庫

        # 組裝資料並加入到返回列表
        image = None
        if row.vehicle_image:
            img_data = row.vehicle_image
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            image = f"data:image/jpeg;base64,{img_base64}"

        fine_list.append({
            'violation_id': row.violation_id,
            'license_plate': row.license_plate,
            'violation_location': row.violation_location,
            'violation_time': row.violation_time.strftime('%Y-%m-%d %H:%M'),
            'speed_limit': row.speed_limit,
            'actual_speed': row.actual_speed,
            'fine_amount': row.fine_amount,
            'payment_due_date': row.payment_due_date.strftime('%Y-%m-%d'),
            'speed_camera_info': row.speed_camera_info,
            'issuing_agency': row.issuing_agency,
            'legal_basis': row.legal_basis,
            'vehicle_image': image,
            'camera_id': row.camera_id,
            'owner_name': row.owner_name,
            'owner_id_number': row.owner_id_number,
            'registered_address': row.registered_address,
            'contact_phone': row.contact_phone,
            'vehicle_type': row.vehicle_type,
            'ticket': row.ticket,
            'error_code': result_code  # 返回錯誤代碼
        })

    return jsonify(fine_list)

@manual_bp.route('/update_report', methods=['POST'])
def update_violation():
    data = request.get_json()

    violation_id = data.get('violation_id')
    ticket = data.get('ticket')

    # 假設你有一個違規紀錄模型 Violation
    violation = ViolationRecord.query.filter_by(id=violation_id).first()
    if violation:
        violation.ticket = ticket
        db.session.commit()
        return jsonify({"message": "Violation updated successfully"}), 200
    else:
        return jsonify({"error": "Violation not found"}), 404


