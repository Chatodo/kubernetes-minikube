CREATE DATABASE dbflask;
USE dbflask;

CREATE TABLE utilisateurs (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL
);
INSERT INTO utilisateurs (email, password) VALUES ('ivan', '$2b$12$pgBJ1KbKNouK40KGkOLKN.RLR6gdS5jvpuRsO.v1ePvahnJQPzETS');

CREATE TABLE produits (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(255) NOT NULL,
	prix DECIMAL(10, 2) NOT NULL
);
INSERT INTO produits (nom, prix) VALUES ('Livre', 19.99);
INSERT INTO produits (nom, prix) VALUES ('Ordinateur', 999.99);