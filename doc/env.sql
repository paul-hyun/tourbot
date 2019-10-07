-- DB 생성
CREATE DATABASE tourbot;

-- 계정생성
CREATE USER 'tourbot'@'localhost' IDENTIFIED BY 'tourbot123!';

-- 권한
GRANT ALL PRIVILEGES ON tourbot.* TO 'tourbot'@'localhost';
SHOW GRANTS FOR 'tourbot'@'localhost';

-- 권한 적용
FLUSH PRIVILEGES;

