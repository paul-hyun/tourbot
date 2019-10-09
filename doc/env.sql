---
--- MYSQL
---

-- DB 생성
CREATE DATABASE tourbot;

-- 계정생성
CREATE USER 'tourbot'@'localhost' IDENTIFIED BY 'tourbot123!';
CREATE USER 'tourbot'@'%' IDENTIFIED BY 'tourbot123!';

-- 권한
GRANT ALL PRIVILEGES ON tourbot.* TO 'tourbot'@'localhost';
SHOW GRANTS FOR 'tourbot'@'localhost';
GRANT ALL PRIVILEGES ON tourbot.* TO 'tourbot'@'%';
SHOW GRANTS FOR 'tourbot'@'%';

-- 권한 적용
FLUSH PRIVILEGES;


---
--- POSTGRESQL
---
-- 계정
CREATE USER tourbot WITH ENCRYPTED PASSWORD 'tourbot';
-- 권한
CREATE DATABASE tourbot OWNER tourbot ENCODING 'utf-8';

