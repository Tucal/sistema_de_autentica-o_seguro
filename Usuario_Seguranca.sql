CREATE DATABASE users_db;

USE users_db;

CREATE TABLE users (
   id INT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(255) UNIQUE NOT NULL,
   password_hash VARCHAR(255) NOT NULL
);

 SELECT * 
  FROM users
 WHERE 1=1; 
 