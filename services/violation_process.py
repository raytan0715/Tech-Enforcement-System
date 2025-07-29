import datetime
from model.database import ViolationRecord
from config.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

def check_license_plate_in_database(license_plate):
    """
    檢查車牌在資料庫中的狀態：
    - 如果偵測到多個車牌，直接返回 0。
    - 如果是單車牌，進行資料庫查詢，並返回相應結果。
    """
    if isinstance(license_plate, list):
        if len(license_plate) > 1:
            return 3  # 多車牌，直接返回 3
        elif len(license_plate) == 1:
            license_plate = license_plate[0]  # 提取唯一的車牌進行檢查
        else:
            return 1  # 空的清單，返回 1 表示不存在

    if isinstance(license_plate, str):  # 單車牌檢測
        try:
            query = text("SELECT license_plate, is_deregistered FROM vehicle_registration.vehicle_registration WHERE license_plate = :license_plate")
            result = db.session.execute(query, {'license_plate': license_plate}).fetchone()

            if result:
                is_deregistered = result[1]  # 第二列數據 (是否已註銷)
                if is_deregistered == 'TRUE' or is_deregistered == 1:
                    return 2  # 車牌已註銷
                else:
                    return 0  # 車牌存在且未註銷
            else:
                return 1  # 車牌不存在
        except SQLAlchemyError as e:
            print(f"資料庫查詢出錯: {e}")
            db.session.rollback() 
            return 1


def process_violation(license_plate, location, speed_limit, current_speed, cam_id, date_time, image_path, longitude, latitude):
    speed_limit = int(speed_limit) if isinstance(speed_limit, str) else speed_limit
    current_speed = int(current_speed) if isinstance(current_speed, str) else current_speed

    if isinstance(date_time, str):
        date_time = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M')

    result_code = check_license_plate_in_database(license_plate)

    try:
        with open(image_path, 'rb') as image_file:
            image_binary = image_file.read()

         # 僅保存第一個車牌
        if isinstance(license_plate, list) and license_plate:
            license_plate = license_plate[0]
        else:
            license_plate = license_plate

        violation = ViolationRecord(
            license_plate=license_plate,
            location=location,
            speed_limit=speed_limit,
            current_speed=current_speed,
            cam_id=cam_id,
            date_time=date_time,
            image=image_binary,
            error_code=result_code,
            longitude=longitude,
            latitude=latitude
        )

        db.session.add(violation)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"資料庫寫入錯誤: {e}")
        db.session.rollback()
