CREATE DATABASE db_biblioteca_2m;
USE db_biblioteca_2m;

-- ==============================================================
--                           TABELAS
-- ==============================================================

CREATE TABLE Autores (
    ID_autor INT AUTO_INCREMENT PRIMARY KEY,
    Nome_autor VARCHAR(255) NOT NULL,
    Nacionalidade VARCHAR(255),
    Data_nascimento DATE,
    Biografia TEXT
);

CREATE TABLE Generos (
    ID_genero INT AUTO_INCREMENT PRIMARY KEY,
    Nome_genero VARCHAR(255) NOT NULL
);

CREATE TABLE Editoras (
    ID_editora INT AUTO_INCREMENT PRIMARY KEY,
    Nome_editora VARCHAR(255) NOT NULL,
    Endereco_editora TEXT
);

CREATE TABLE Livros (
    ID_livro INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Autor_id INT,
    ISBN VARCHAR(13) NOT NULL,
    Ano_publicacao INT,
    Genero_id INT,
    Editora_id INT,
    Quantidade_disponivel INT,
    Resumo TEXT,
    FOREIGN KEY (Autor_id) REFERENCES Autores(ID_autor),
    FOREIGN KEY (Genero_id) REFERENCES Generos(ID_genero),
    FOREIGN KEY (Editora_id) REFERENCES Editoras(ID_editora)
);

CREATE TABLE Usuarios (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nome_usuario VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Numero_telefone VARCHAR(15),
    Data_inscricao DATE,
    Multa_atual DECIMAL(10, 2)
);

CREATE TABLE Emprestimos (
    ID_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    Usuario_id INT,
    Livro_id INT,
    Data_emprestimo DATE,
    Data_devolucao_prevista DATE,
    Data_devolucao_real DATE,
    Status_emprestimo ENUM('pendente', 'devolvido', 'atrasado'),
    FOREIGN KEY (Usuario_id) REFERENCES Usuarios(ID_usuario),
    FOREIGN KEY (Livro_id) REFERENCES Livros(ID_livro)
);

-- ==============================================================
--                           GATILHOS
-- ==============================================================

DELIMITER $

-- ========================= VALIDAÇÕES =========================

-- 1
CREATE TRIGGER verificar_user_name BEFORE INSERT
ON Usuarios
FOR EACH ROW
BEGIN
    IF NEW.Nome_usuario IS NULL OR LENGTH(NEW.Nome_usuario) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'O nome do usuário não pode ser nulo ou vazio';
    END IF;
END$

-- 2
CREATE TRIGGER verificar_ISBN BEFORE INSERT
ON Livros
FOR EACH ROW
BEGIN
    IF LENGTH(NEW.ISBN) != 13 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'O ISBN deve ter exatamente 13 caracteres';
    END IF;
END$

-- 3
CREATE TRIGGER verificar_data_devolucao BEFORE INSERT
ON Emprestimos
FOR EACH ROW
BEGIN
    IF NEW.Data_devolucao_prevista < NEW.Data_emprestimo THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A data de devolução prevista não pode ser anterior à data de empréstimo';
    END IF;
END$

-- 4
CREATE TRIGGER verificar_quantidade_disponivel BEFORE INSERT
ON Livros
FOR EACH ROW
BEGIN
    if NEW.Quantidade_disponivel < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A quantidade disponível de livros não pode ser negativa';
    END IF;
END$

-- 5
CREATE TRIGGER verificar_data_nascimento BEFORE INSERT
ON Autores
FOR EACH ROW
BEGIN
    IF NEW.Data_nascimento IS NOT NULL AND NEW.Data_nascimento > CURDATE() THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A data de nascimento não pode ser uma data futura';
    END IF;
END$