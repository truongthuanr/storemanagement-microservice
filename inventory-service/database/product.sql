-- Tạo cơ sở dữ liệu (nếu chưa có)
CREATE DATABASE IF NOT EXISTS inventory_db;

-- Sử dụng cơ sở dữ liệu đã tạo
USE inventory_db;

-- Tạo bảng products
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Kiểm tra bảng đã được tạo
SHOW TABLES;
