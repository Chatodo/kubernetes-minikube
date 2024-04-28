CREATE DATABASE dbflask;
USE dbflask;

CREATE TABLE utilisateurs (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL
	is_admin BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE produits (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(255) NOT NULL,
	prix DECIMAL(10, 2) NOT NULL,
	stock INT NOT NULL DEFAULT 0
);
INSERT INTO produits (nom, prix, stock) VALUES ('Livre', 19.99, 10);
INSERT INTO produits (nom, prix, stock) VALUES ('Ordinateur', 999.99, 2);
INSERT INTO produits (nom, prix, stock) VALUES ('Xbox Series X', 500, 0);