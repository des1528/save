DROP DATABASE IF EXISTS lab_db;
CREATE DATABASE lab_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lab_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL
);

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(20),
    norm VARCHAR(50)
);

CREATE TABLE studies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    test_id INT NOT NULL,
    user_id INT NOT NULL,
    study_date DATE NOT NULL,
    result VARCHAR(50) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (test_id) REFERENCES tests(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (login, password, full_name) VALUES
    ('admin', 'admin', 'Иванов И.И.'),
    ('lab1', '1234', 'Петрова А.С.');

INSERT INTO patients (full_name, birth_date, phone) VALUES
    ('Сидоров П.П.', '1985-03-12', '+79001234567'),
    ('Кузнецова М.А.', '1992-07-25', '+79007654321'),
    ('Орлов Д.В.', '1978-11-30', '+79005556677');

INSERT INTO tests (name, unit, norm) VALUES
    ('Гемоглобин', 'г/л', '120-160'),
    ('Глюкоза', 'ммоль/л', '3.3-5.5'),
    ('Холестерин', 'ммоль/л', '3.0-6.0');

INSERT INTO studies (patient_id, test_id, user_id, study_date, result) VALUES
    (1, 1, 1, '2026-04-01', '140'),
    (2, 2, 1, '2026-04-05', '4.8'),
    (3, 3, 2, '2026-04-10', '5.2');
