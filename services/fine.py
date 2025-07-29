from pathlib import Path
from flask import Flask, make_response, send_file, render_template, request, jsonify
from fpdf import FPDF
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.database import VEHICLE_DATABASE_URL, TRAFFIC_FINE_DATABASE_URL
import os
from datetime import datetime, timedelta
from PIL import Image
import base64
from config.database import db
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# 設定 PDF 儲存的路徑
def generate_pdf_file_path(id):
    output_dir = "C:/tmp"

    # 若目錄不存在，創建目錄
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 設定 PDF 檔案儲存路徑
    file_path = f"{output_dir}/ticket_{id}.pdf"
    print(f"Generated PDF path: {file_path}")
    return file_path

# 連接車輛註冊資料庫
def get_vehicle_registration_session():
    engine = create_engine(VEHICLE_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

# 連接 traffic_fines 資料庫
def get_traffic_fines_session():
    engine1 = create_engine(TRAFFIC_FINE_DATABASE_URL)
    Session1 = sessionmaker(bind=engine1)
    return Session1()

# 查詢車主資料
def get_owner_data_from_vehicle_db(license_plate):
    session = get_vehicle_registration_session()
    result = session.execute(
        text("SELECT owner_name, owner_id_number, registered_address, owner_contact_phone, is_deregistered FROM vehicle_registration WHERE license_plate = :license_plate"),
        {'license_plate': license_plate}
    ).fetchone()
    session.close()
    return result if result else None

# 查詢違規資料
# 查詢所有罰單資料（來自 ticket_view）
def get_violation_data_from_ticket_view(violation_id):
    try:
        # 查詢 ticket_view 資料表中的所有欄位
        result = db.session.execute(
            text("""
                SELECT *
                FROM traffic_fines.ticket_view
                WHERE violation_id = :violation_id
            """),
            {'violation_id': violation_id}
        ).fetchone()

        if result:
            return {
                'violation_id': result[0],  # 違規ID
                'license_plate': result[1],  # 車牌
                'violation_location': result[2],  # 違規位置
                'violation_time': result[3],  # 違規時間
                'speed_limit': result[4],  # 限速
                'current_speed': result[5],  # 實際車速
                'fine_amount': result[6],  # 罰款金額
                'payment_due_date': result[7],  # 繳款期限
                'speed_camera_info': result[8],  # 測速照相機資訊
                'issuing_agency': result[9],  # 發單機關
                'legal_basis': result[10],  # 法條依據
                'vehicle_image': result[11],  # 車輛圖片
                'camera_id': result[12],  # 攝影機ID
                'owner_name': result[15],  # 車主姓名
                'owner_id_number': result[16],  # 車主ID
                'registered_address': result[17],  # 車主地址
                'contact_phone': result[18],  # 車主聯絡電話
                'vehicle_type': result[19],  # 車輛種類
            }
        else:
            print(f"違規資料未找到，violation_id={violation_id}")
            return None
    except Exception as e:
        print(f"查詢違規紀錄時發生錯誤: {e}")
        return None


def convert_violation_to_pdf(violation_data, pdf_path):
    owner_data = get_owner_data_from_vehicle_db(violation_data['license_plate'])
    if owner_data is None:
        raise ValueError(f"找不到車牌 {violation_data['license_plate']} 的車主資料")
    if owner_data[4] == 1:
        raise ValueError(f"車牌 {violation_data['license_plate']} 的車輛已註銷")

    owner_name, owner_id_number, registered_address, owner_contact_phone, _ = owner_data

    pdf = FPDF(orientation='L')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = 'C:/Windows/Fonts/kaiu.ttf' if os.name == 'nt' else 'path/to/your/font.ttf'
    pdf.add_font('Microsoft JhengHei', '', font_path, uni=True)
    pdf.set_font('Microsoft JhengHei', '', 12)

    # 頁面設定
    margin = 10
    page_width = pdf.w - 3 * margin
    line_height = 15
    current_y = margin

    # 標題
    pdf.cell(0, 10, "台北市政府警察局舉發違反道路交通管理事件單", ln=True, align='C')
    current_y = pdf.get_y() + 5
    # 插入印章
    fixed_image_path = "static/uploads/popoink.jpg"
    if os.path.exists(fixed_image_path):
        pdf.image(fixed_image_path, x=pdf.w-margin-60, y=current_y, w=40)

    # 基本資訊區塊
    # 第一行：罰單編號和車牌
    pdf.rect(margin, current_y, page_width/2, line_height)
    pdf.text(margin + 2, current_y + 7, f"罰單編號: {str(violation_data['violation_id']).zfill(6)}")
    
    pdf.rect(margin + page_width/2, current_y, page_width/2, line_height)
    pdf.text(margin + page_width/2 + 2, current_y + 7, f"車牌號碼: {violation_data['license_plate']}")
    
    current_y += line_height

    # 第二行：違規地點
    pdf.rect(margin, current_y, page_width, line_height)
    pdf.text(margin + 2, current_y + 7, f"違規地點: {violation_data['violation_location']}")
    current_y += line_height

    # 第三行：違規時間
    pdf.rect(margin, current_y, page_width, line_height)
    pdf.text(margin + 2, current_y + 7, f"違規時間: {violation_data['violation_time']}")
    current_y += line_height

    # 第四行：違規事實
    pdf.rect(margin, current_y, page_width, line_height*2)
    violation_fact = f"違規事實: 限速 {violation_data['speed_limit']} 公里，經測時速 {violation_data['current_speed']} 公里，超速逾 {max(violation_data['current_speed'] - violation_data['speed_limit'], 0)} 公里"
    pdf.text(margin + 2, current_y + 7, violation_fact)
    current_y += line_height * 2

    # 第五行：罰款金額和繳款期限
    pdf.rect(margin, current_y, page_width/2, line_height)
    pdf.text(margin + 2, current_y + 7, f"罰款金額: NT${violation_data['fine_amount']}")
    
    pdf.rect(margin + page_width/2, current_y, page_width/2, line_height)
    pdf.text(margin + page_width/2 + 2, current_y + 7, f"繳款期限: {violation_data['payment_due_date']}")
    current_y += line_height

    # 第六行：測速照相機資訊
    pdf.rect(margin, current_y, page_width, line_height)
    pdf.text(margin + 2, current_y + 7, f"測速照相機: {violation_data['speed_camera_info']}")
    current_y += line_height

    # 第七行：發單機關和法條依據
    pdf.rect(margin, current_y, page_width/2, line_height)
    pdf.text(margin + 2, current_y + 7, f"發單機關: {violation_data['issuing_agency']}")
    
    pdf.rect(margin + page_width/2, current_y, page_width/2, line_height)
    pdf.text(margin + page_width/2 + 2, current_y + 7, f"法條依據: {violation_data['legal_basis']}")
    current_y += line_height

    # 車主資訊區塊
    # 第八行：車主姓名和身分證號
    pdf.rect(margin, current_y, page_width/2, line_height)
    pdf.text(margin + 2, current_y + 7, f"車主姓名: {owner_name}")
    
    pdf.rect(margin + page_width/2, current_y, page_width/2, line_height)
    pdf.text(margin + page_width/2 + 2, current_y + 7, f"身分證字號: {owner_id_number}")
    current_y += line_height

    # 第九行：戶籍地址
    pdf.rect(margin, current_y, page_width, line_height)
    pdf.text(margin + 2, current_y + 7, f"戶籍地址: {registered_address}")
    current_y += line_height

    # 第十行：聯絡電話和車種
    pdf.rect(margin, current_y, page_width/2, line_height)
    pdf.text(margin + 2, current_y + 7, f"聯絡電話: {owner_contact_phone}")
    
    pdf.rect(margin + page_width/2, current_y, page_width/2, line_height)
    pdf.text(margin + page_width/2 + 2, current_y + 7, f"車種: {violation_data['vehicle_type']}")
    current_y += line_height + 10

    # 插入違規圖片
    image_data = violation_data.get('vehicle_image')
    if image_data:
        try:
            image_file_path = f"C:/tmp/ticket_image_{violation_data['violation_id']}.png"
            with open(image_file_path, 'wb') as img_file:
                img_file.write(image_data)
            with Image.open(image_file_path) as img:
                img = img.convert("RGB")
                img.save(image_file_path, "PNG")
            
            # 調整圖片位置和大小
            pdf.image(image_file_path, x=210, y=60, w=55, h=45)  # x: 10, y: current_y, w: 80, h: 60
        except Exception as e:
            logging.error(f"圖片處理錯誤: {e}")
        finally:
            if os.path.exists(image_file_path):
                os.remove(image_file_path)



    pdf.output(pdf_path)


# 假設你已經有 `get_traffic_fines_session()` 函數來連接資料庫
def log_print_ticket(ticket_id, printed_by, ip_address, vehicle_image):
    try:
        session = get_traffic_fines_session()  # 資料庫會話

        # 將車輛圖片轉換為二進位資料
        vehicle_image_blob = base64.b64decode(vehicle_image) if vehicle_image else None

        # 插入列印日誌
        session.execute(
        text("""
                INSERT INTO fines_log (ticket_id, printed_by, ip_address, printed_image)
                VALUES (:ticket_id, :printed_by, :ip_address, :printed_image)
            """),
            {
                "ticket_id": ticket_id,
                "printed_by": printed_by,  # 假設是列印員工ID，這裡可以放入假的ID
                "ip_address": ip_address,  # 使用者的IP地址，這裡可以是假的IP
                "printed_image": vehicle_image_blob,  # 這是列印車輛的圖片的二進位資料
            }
        )

        session.commit()
        print("列印日誌已成功儲存")
    except Exception as e:
        session.rollback()
        logging.error(f"儲存列印日誌時發生錯誤: {e}")
    finally:
        session.close()



# 範例：在列印完罰單後呼叫 log_print_ticket 記錄
@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
def generate_and_record_ticket(id):
    # 查詢違規資料（從 ticket_view 中抓取）
    violation_data = get_violation_data_from_ticket_view(id)
    if not violation_data:
        return "找不到該違規紀錄", 404

    # 模擬列印員工的 ID 和處理機 IP 位址
    printed_by = 1  # 假設是列印員工ID，您可以從使用者系統獲得
    ip_address = '192.168.23.1'  # 使用 request 來取得 IP 位址
    
    # 假設圖片已經是 base64 編碼的字串
    vehicle_image = base64.b64encode(violation_data['vehicle_image']).decode('utf-8') if violation_data['vehicle_image'] else None
    
    # 呼叫 log_print_ticket 函數來儲存列印日誌
    log_print_ticket(id, printed_by, ip_address, vehicle_image)

    # 生成 PDF 並返回
    pdf_path = generate_pdf_file_path(id)
    convert_violation_to_pdf(violation_data, pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
