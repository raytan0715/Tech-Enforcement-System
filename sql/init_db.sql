SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS traffic_enforcement;
CREATE DATABASE traffic_enforcement;
USE traffic_enforcement;

CREATE TABLE violation_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    speed_limit INT NOT NULL,
    current_speed INT NOT NULL,
    cam_id VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL,
    image LONGBLOB NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,    -- 經度
    latitude DECIMAL(9, 6) NOT NULL,     -- 緯度
    recognition BOOLEAN DEFAULT FALSE,
    error_code INT,
    ticket BOOLEAN DEFAULT FALSE
);

INSERT INTO violation_records (license_plate, location, speed_limit, current_speed, cam_id, date_time, image, longitude, latitude, recognition, error_code, ticket) VALUES
('AXT-8798', '台北市大安區忠孝東路10號', 60, 95, 'ID021', '2024-09-12 08:15:00', RANDOM_BYTES(1024), 121.54423492883545,25.041452781384134, TRUE, 0, TRUE),
('4919-LR', '台北市中山區林森北路8號', 50, 85, 'ID022', '2024-11-16 17:40:00', RANDOM_BYTES(1024), 121.52370915767095, 25.0465864, TRUE, 0, TRUE), 
('9276-MG', '台北市松山區光復南路12號', 55, 100, 'ID023', '2024-10-30 09:25:00', RANDOM_BYTES(1024), 121.5574823306837, 25.04349090000001, TRUE, 0, TRUE),
('7953-66', '台北市北投區中央北路三段17-1號', 60, 110, 'ID024', '2024-12-02 13:55:00', RANDOM_BYTES(1024),121.48599403381529, 25.13796340625815, TRUE, 0, TRUE),
('AFF-0666', '台北市士林區中正路15號', 50, 70, 'ID025', '2024-09-24 14:40:00', RANDOM_BYTES(1024), 121.53079772883545, 25.096063012100785, TRUE, 0, TRUE),
('BGR-5851', '台北市大安區四維路10號', 55, 95, 'ID026', '2024-11-10 10:35:00', RANDOM_BYTES(1024), 121.54802570370418, 25.03699893099302, TRUE, 0, TRUE),
('AKT-5088', '台北市大同區塔城街5號', 60, 85, 'ID027', '2024-10-14 07:20:00', RANDOM_BYTES(1024), 121.51069077116453,25.04984301967978, TRUE, 0, TRUE),
('AXD-0102', '台北市中山區建國北路29-3號', 50, 80, 'ID028', '2024-12-08 16:25:00', RANDOM_BYTES(1024), 121.53726901349361, 25.05451160000001, TRUE, 0, TRUE),
('AAA-6385', '台北市松山區南京東路四段10號', 55, 95, 'ID029', '2024-09-29 11:15:00', RANDOM_BYTES(1024), 121.55209342883545,25.05132737825296, TRUE, 0, TRUE),
('1051-K7', '台北市信義區基隆路5號', 60, 90, 'ID030', '2024-11-04 12:30:00', RANDOM_BYTES(1024), 121.5693816, 25.048922100000006, TRUE, 0, TRUE),
('AXT-8798', '台北市南港區7號', 50, 75, 'ID031', '2024-10-22 18:50:00', RANDOM_BYTES(1024), 121.59198453488582, 25.05396802116418, TRUE, 0, TRUE),
('4919-LR', '台北市大安區羅斯福路8號', 60, 100, 'ID032', '2024-09-21 09:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('9276-MG', '台北市中山區民生東路12號', 50, 85, 'ID033', '2024-12-13 17:45:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('7953-66', '台北市文山區木柵路4號', 55, 90, 'ID034', '2024-10-07 08:00:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('AFF-0666', '台北市士林區天母路16號', 60, 95, 'ID035', '2024-11-18 19:05:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('BGR-5851', '台北市中正區台北車站前1號', 50, 75, 'ID036', '2024-09-05 06:40:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('AKT-5088', '台北市南港區南港路1號', 55, 80, 'ID037', '2024-12-12 11:15:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('AXD-0102', '台北市中山區敦化北路6號', 60, 90, 'ID038', '2024-09-19 08:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('AAA-6385', '台北市信義區信義路2號', 50, 85, 'ID039', '2024-11-14 15:50:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('1051-K7', '台北市北投區石牌路5號', 60, 95, 'ID040', '2024-12-17 10:10:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('AXT-1234', '台北市大安區忠孝東路10號', 60, 90, 'ID001', '2024-09-10 07:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('BGR-5678', '台北市中山區林森北路8號', 50, 70, 'ID002', '2024-11-12 16:45:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('CDE-7890', '台北市松山區光復南路12號', 55, 90, 'ID003', '2024-10-01 09:20:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('DEF-8901', '台北市北投區中央北路9號', 60, 100, 'ID004', '2024-12-05 13:15:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('EFG-9012', '台北市士林區中正路15號', 50, 75, 'ID005', '2024-09-20 14:50:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('FGH-0123', '台北市中正區建國路10號', 55, 80, 'ID006', '2024-11-08 10:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('GHI-1234', '台北市大同區塔城街5號', 60, 90, 'ID007', '2024-10-14 07:10:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('HIJ-2345', '台北市中山區建國北路3號', 50, 85, 'ID008', '2024-12-08 15:25:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('IJK-3456', '台北市松山區南京東路10號', 50, 80, 'ID009', '2024-09-28 10:40:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('JKL-4567', '台北市信義區基隆路5號', 60, 90, 'ID010', '2024-11-03 12:15:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('KLM-5678', '台北市南港區中和路7號', 50, 80, 'ID011', '2024-10-22 18:00:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('LMN-6789', '台北市大安區羅斯福路8號', 60, 100, 'ID012', '2024-09-19 09:00:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('MNO-7890', '台北市中山區民生東路12號', 50, 80, 'ID013', '2024-12-13 17:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('NOP-8901', '台北市文山區木柵路4號', 55, 80, 'ID014', '2024-10-06 08:10:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('OPQ-9012', '台北市士林區天母路16號', 60, 90, 'ID015', '2024-11-17 19:20:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('PQR-0123', '台北市中正區台北車站前1號', 50, 70, 'ID016', '2024-09-04 06:50:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('QRS-1234', '台北市南港區南港路1號', 55, 80, 'ID017', '2024-12-11 11:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('RST-2345', '台北市中山區敦化北路6號', 60, 90, 'ID018', '2024-09-18 08:10:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('STU-3456', '台北市信義區信義路2號', 50, 90, 'ID019', '2024-11-13 15:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('TUV-4567', '台北市北投區石牌路5號', 60, 90, 'ID020', '2024-12-16 10:20:00', RANDOM_BYTES(1024), 121.940000, 25.345, TRUE, 0, TRUE),
('UVW-5678', '台北市大安區忠孝東路10號', 60, 90, 'ID021', '2024-09-12 08:15:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('VWX-6789', '台北市中山區林森北路8號', 50, 80, 'ID022', '2024-11-16 17:40:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('WXY-7890', '台北市松山區光復南路12號', 55, 100, 'ID023', '2024-10-30 09:25:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('XYZ-8901', '台北市北投區中央北路9號', 60, 100, 'ID024', '2024-12-02 13:55:00', RANDOM_BYTES(1024),121.940, 25.345, TRUE, 0, TRUE),
('YZA-9012', '台北市士林區中正路15號', 50, 70, 'ID025', '2024-09-24 14:40:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('ZAB-0123', '台北市中正區建國路10號', 55, 100, 'ID026', '2024-11-10 10:35:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('ABC-1234', '台北市大同區塔城街5號', 60, 90, 'ID027', '2024-10-14 07:20:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('BCD-2345', '台北市中山區建國北路3號', 50, 90, 'ID028', '2024-12-08 16:25:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('CDE-3456', '台北市松山區南京東路10號', 55, 90, 'ID029', '2024-09-29 11:15:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE),
('DEF-4567', '台北市信義區基隆路5號', 60, 80, 'ID030', '2024-11-04 12:30:00', RANDOM_BYTES(1024), 121.940, 25.345, TRUE, 0, TRUE);
DELIMITER $$

-- 0 ai辨識沒問題 1沒車籍 2已註銷 3多車牌 4人工無法辨識

CREATE TRIGGER check_error_code
BEFORE INSERT ON violation_records
FOR EACH ROW
BEGIN
    -- 如果 error_code 不為 0，將 recognition 設為 False
    IF NEW.error_code != 0 THEN
        SET NEW.recognition = FALSE;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER set_ticket_false
BEFORE INSERT ON violation_records
FOR EACH ROW
BEGIN
    SET NEW.ticket = FALSE;
END$$

DELIMITER ;

DROP DATABASE IF EXISTS vehicle_registration;
CREATE DATABASE vehicle_registration;
USE vehicle_registration;

CREATE TABLE vehicle_registration (
    license_plate VARCHAR(15) NOT NULL PRIMARY KEY, -- 車牌號碼 (PK)
    car_color VARCHAR(20) NOT NULL,                 -- 車子顏色
    car_model VARCHAR(50) NOT NULL,                 -- 車子型號
    owner_name VARCHAR(100) NOT NULL,               -- 車主姓名
    owner_id_number VARCHAR(20) NOT NULL,           -- 車主身份證號
    registered_address VARCHAR(255) NOT NULL,       -- 戶籍地址
    owner_contact_phone VARCHAR(20) NOT NULL,       -- 車主聯絡電話
    engine_capacity INT NOT NULL,                   -- 排氣量
    vehicle_type VARCHAR(20) NOT NULL,              -- 車輛類型
    manufacture_year YEAR NOT NULL,                 -- 製造年份
    is_deregistered BOOLEAN DEFAULT FALSE NOT NULL, -- 是否註銷 (0: 未註銷, 1: 已註銷)
    registration_date DATE NOT NULL,                -- 登記日期
    inspection_expiry DATE NOT NULL,                 -- 是否過期檢驗
    birth_date DATE NOT NULL               			-- 出生日期
);

INSERT INTO vehicle_registration 
(license_plate, car_color, car_model, owner_name, owner_id_number, 
registered_address, owner_contact_phone, engine_capacity, vehicle_type, 
manufacture_year, is_deregistered, registration_date, inspection_expiry, birth_date)
VALUES 
('AKT-5088', '紅色', 'Toyota RAV4', '陳威宏', 'Q123456789', '台北市信義區松山路100號', '0935123456', 2.0, '小客車', 2018, FALSE, '2018-09-15', '2023-09-15', '1990-05-01'),
('AXD-0102', '黑色', 'Honda Accord', '林曉芸', 'B234567891', '新北市新莊區建國路200號', '0967456789', 2.4, '小客車', 2019, FALSE, '2019-06-10', '2024-06-10', '1985-03-15'),
('AAA-6385', '銀色', 'Ford Focus', '劉建國', 'E164209753', '台南市中西區府前路1段', '0965123456', 1.6, '小客車', 2017, TRUE, '2017-10-18', '2023-10-18', '1978-11-22'),
('1051-K7', '白色', 'Tesla Model 3', '王家豪', 'D246813579', '台北市大安區信義路123巷', '0953897211', 0.0, '小客車', 2021, FALSE, '2021-03-20', '2026-03-20', '1995-02-28'),
('AXT-8798', '藍色', 'Mazda CX-3', '張冠宇', 'C556677889', '桃園市八德區中山路89巷', '0923994455', 2.0, '小客車', 2020, FALSE, '2020-07-01', '2025-07-01', '1992-06-18'),
('4919-LR', '灰色', 'Volkswagen Golf', '蔡明志', 'D445566778', '高雄市鼓山區美術館路100號', '0912888777', 1.8, '小客車', 2019, FALSE, '2019-11-05', '2024-11-05', '1986-04-20'),
('9276-MG', '白色', 'BMW 5 Series', '黃天成', 'E667788990', '台中市西屯區民生路789號', '0977994455', 2.5, '小客車', 2021, TRUE, '2021-03-15', '2026-03-15', '1991-07-05'),
('7953-66', '黃色', 'Nissan X-Trail', '李依涵', 'F778899112', '嘉義市東區民族路300號', '0912333445', 2.3, '小客車', 2022, FALSE, '2022-05-18', '2027-05-18', '1989-12-10'),
('AFF-0666', '黑色', 'BMW X3', '劉阿豪', 'A123456789', '桃園市八德區永福路8號', '0918123456', 2.0, '小客車', 2020, FALSE, '2020-08-15', '2025-08-15', '2000-01-01'),
('BGR-5851', '白色', 'Toyota Camry', '劉土豪', 'A987654321', '桃園市缺德路87號', '0937888999', 2.5, '小客車', 2021, FALSE, '2021-09-10', '2026-09-10', '2000-02-02');


DROP DATABASE IF EXISTS traffic_fines;
CREATE DATABASE traffic_fines;
USE traffic_fines;

CREATE TABLE fines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,                 -- 交通佐理員員工ID
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 時間
    ip_address VARCHAR(45) NOT NULL,           -- 處理機IP位址
    license_plate VARCHAR(20),        -- 辨識車牌號碼
    is_recognized ENUM('yes', 'no') NOT NULL,  -- 是否辨識成功
    image LONGBLOB NOT NULL,               -- 圖片路徑
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 紀錄時間
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(50) NOT NULL UNIQUE,   -- 帳號
    password VARCHAR(255) NOT NULL,         -- 密碼
    ip_address VARCHAR(45)                  -- 員工登入時的 IP 位址
);

INSERT INTO users (username, password, ip_address) VALUES 
('user1', '1234', '192.168.1.10'),
('test2', '2345', '192.168.1.20'); 

CREATE TABLE openfine_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    ip VARCHAR(45) NOT NULL  -- 用來存儲 IP 地址，長度為 45 字符以支援 IPv6
);

INSERT INTO openfine_users (username, password, ip) VALUES ('user2', '2345', '192.168.1.2');

ALTER TABLE fines
ADD CONSTRAINT fk_employee
FOREIGN KEY (employee_id) REFERENCES users(id);

USE traffic_fines;

CREATE OR REPLACE VIEW ticket_view AS
SELECT 
    vr.id AS violation_id,                   -- 違規紀錄 ID
    vr.license_plate AS license_plate,      -- 車牌號碼
    vr.location AS violation_location,      -- 違規地點
    vr.date_time AS violation_time,         -- 違規時間
    vr.speed_limit AS speed_limit,          -- 限速 (公里/小時)
    vr.current_speed AS actual_speed,       -- 實際速度 (公里/小時)
    (CASE 
        WHEN (vr.current_speed - vr.speed_limit) <= 20 THEN 3000
        WHEN (vr.current_speed - vr.speed_limit) <= 40 THEN 6000
        ELSE 12000
    END) AS fine_amount,                    -- 罰款金額 (新台幣)
    DATE_ADD(vr.date_time, INTERVAL 11 DAY) AS payment_due_date,  -- 繳納期限 (11天後)
    CONCAT(vr.cam_id,'型號：TS-200，校準日期：2024-12-01') AS speed_camera_info, -- 測速設備資訊
    '台北市警察局中山分局' AS issuing_agency,        -- 開單單位
    '道路交通管理處罰條例第42條' AS legal_basis,     -- 法律依據
    vr.image AS vehicle_image,              -- 照片 (車輛照片)
    vr.cam_id AS camera_id,                 -- 攝影機 ID
    vr.error_code,
    vr.ticket,
    -- 車輛資訊
    vreg.owner_name AS owner_name,          -- 車主姓名
    vreg.owner_id_number AS owner_id_number, -- 車主身份證號
    vreg.registered_address AS registered_address, -- 車主住址
    vreg.owner_contact_phone AS contact_phone, -- 車主聯絡電話
    vreg.vehicle_type AS vehicle_type       -- 車輛類型       
FROM 
    traffic_enforcement.violation_records vr
LEFT JOIN 
    vehicle_registration.vehicle_registration vreg
ON 
    vr.license_plate = vreg.license_plate
WHERE 
    vr.error_code IN (0, 1, 2);

-- 建立罰單列印日誌表，並關聯 violation_records 的 id
CREATE TABLE fines_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,    -- 日誌 ID (主鍵)
    ticket_id INT NOT NULL,                   -- 對應罰單 ID
    printed_by INT NOT NULL,                  -- 列印員工 ID
    print_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 列印時間
    ip_address VARCHAR(45) NOT NULL,          -- 處理機 IP 位址
    printed_image MEDIUMBLOB NOT NULL,        -- 列印的車輛照片
    FOREIGN KEY (ticket_id) REFERENCES traffic_enforcement.violation_records(id) -- 關聯到 violation_records 表
);

SET FOREIGN_KEY_CHECKS = 1;