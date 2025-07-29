DROP DATABASE IF EXISTS vehicle_registration;
CREATE DATABASE vehicle_registration;
USE vehicle_registration;

CREATE TABLE vehicle_registration (
    license_plate VARCHAR(15)  not null PRIMARY KEY, -- 車牌號碼 (PK)
    car_color VARCHAR(20) not null,                 -- 車子顏色
    car_model VARCHAR(50) not null,                 -- 車子型號
    owner_name VARCHAR(100)  not null,               -- 車主姓名
    owner_id_number VARCHAR(20)  not null,           -- 車主身份證號
    registered_address VARCHAR(255)  not null,       -- 戶籍地址
    owner_contact_phone VARCHAR(20) not null,       -- 車主聯絡電話
    engine_capacity DECIMAL(5,2) not null,          -- 排氣量
    vehicle_type VARCHAR(20)  not null,              -- 車輛類型
    manufacture_year YEAR  not null,                 -- 製造年份
    is_deregistered BOOLEAN DEFAULT FALSE  not null, -- 是否註銷 (0: 未註銷, 1: 已註銷)
    registration_date DATE  not null,                -- 登記日期
    inspection_expiry DATE  not null                -- 是否過期檢驗
);

INSERT INTO vehicle_registration 
(license_plate, car_color, car_model, owner_name, owner_id_number, 
registered_address, owner_contact_phone, engine_capacity, vehicle_type, 
manufacture_year, is_deregistered, registration_date, inspection_expiry)
VALUES 
('NMP8330', '紅色', 'Toyota Corolla', '林大明', 'A100456789', '新北市三重區中正路123號', '0922Ray_93071556', 1.8, 'Sedan', 2020, FALSE, '2020-02-10', '2025-02-10'),
('NBF1432', '藍色', 'Honda Civic', '陳小華', 'B200654321', '台中市南區建國路45巷', '0932567890', 2.0, 'Sedan', 2018, FALSE, '2018-05-15', '2023-05-15'),
('1680ZQ', '黑色', 'BMW X5', '張小明', 'C135792468', '高雄市左營區光復路789巷', '0943782910', 3.0, 'SUV', 2019, FALSE, '2019-07-01', '2024-07-01'),
('ABC0572', '白色', 'Tesla Model 3', '王家豪', 'D246813579', '台北市大安區信義路123巷', '0953897211', 0.0, 'Electric', 2021, FALSE, '2021-03-20', '2026-03-20'),
('DMV3320', '銀色', 'Ford Focus', '劉建國', 'E164209753', '台南市中西區府前路1段', '0965Ray_93071556', 1.6, 'Hatchback', 2017, TRUE, '2017-10-18', '2023-10-18');
