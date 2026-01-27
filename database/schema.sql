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

CREATE TABLE Historico (
    ID_historico INT AUTO_INCREMENT PRIMARY KEY,
    Tabela_envolvida VARCHAR(50) NOT NULL,
    Acao ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    Data_hora DATETIME NOT NULL,
    Envolvido_id INT NOT NULL,
    Dados_anteriores TEXT,
    Dados_novos TEXT
);

CREATE TABLE Historico_Livro (
    ID_delete INT AUTO_INCREMENT PRIMARY KEY,
    Acao ENUM('INSERT','DELETE') NOT NULL,
    Livro_id INT NOT NULL,
    Titulo VARCHAR(255),
    Autor_id INT,
    ISBN VARCHAR(20),
    Ano_publicacao INT,
    Genero_id INT,
    Editora_id INT,
    Quantidade_disponivel INT,
    Resumo TEXT,
    Data_hora DATETIME NOT NULL,
    Usuario_id INT NOT NULL
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

-- ========================= AUDITORIA =========================

-- 1
CREATE TRIGGER historico_usuario_insert AFTER INSERT
ON Usuarios
FOR EACH ROW
BEGIN
    INSERT INTO Historico (
        Tabela_envolvida,
        Acao,
        Data_hora,
        Envolvido_id,
        Dados_novos
    )
    VALUES (
        'Usuarios',
        'INSERT',
        NOW(),
        NEW.ID_usuario,
        CONCAT(
            'Nome: ', NEW.Nome_usuario,
            ', Email: ', NEW.Email,
            ', Telefone: ', NEW.Numero_telefone,
            ', Data inscrição: ', NEW.Data_inscricao,
            ', Multa: ', NEW.Multa_atual
        )
    );
END$

-- 2
CREATE TRIGGER historico_livro_insert
AFTER INSERT ON Livros
FOR EACH ROW
BEGIN
    INSERT INTO Historico_Livro (
        Acao,
        Livro_id,
        Titulo,
        Autor_id,
        ISBN,
        Ano_publicacao,
        Genero_id,
        Editora_id,
        Quantidade_disponivel,
        Resumo,
        Data_hora,
        Usuario_id
    )
    VALUES (
        'INSERT',
        NEW.ID_livro,
        NEW.Titulo,
        NEW.Autor_id,
        NEW.ISBN,
        NEW.Ano_publicacao,
        NEW.Genero_id,
        NEW.Editora_id,
        NEW.Quantidade_disponivel,
        NEW.Resumo,
        NOW(),
        @usuario_logado_id
    );
END$

-- 3
CREATE TRIGGER historico_livro_delete
AFTER DELETE ON Livros
FOR EACH ROW
BEGIN
    INSERT INTO Historico_Livro (
        Acao,
        Livro_id,
        Titulo,
        Autor_id,
        ISBN,
        Ano_publicacao,
        Genero_id,
        Editora_id,
        Quantidade_disponivel,
        Resumo,
        Data_hora,
        Usuario_id
    )
    VALUES (
        'DELETE',
        OLD.ID_livro,
        OLD.Titulo,
        OLD.Autor_id,
        OLD.ISBN,
        OLD.Ano_publicacao,
        OLD.Genero_id,
        OLD.Editora_id,
        OLD.Quantidade_disponivel,
        OLD.Resumo,
        NOW(),
        @usuario_logado_id 
    );
END$

-- 4
CREATE TRIGGER historico_usuario_delete AFTER DELETE
ON Usuarios
FOR EACH ROW
BEGIN
    INSERT INTO Historico (
        Tabela_envolvida,
        Acao,
        Data_hora,
        Envolvido_id,
        Dados_anteriores
    )
    VALUES (
        'Usuarios',
        'DELETE',
        NOW(),
        OLD.ID_usuario,
        CONCAT(
            'Nome: ', OLD.Nome_usuario,
            ', Email: ', OLD.Email,
            ', Telefone: ', OLD.Numero_telefone,
            ', Data inscrição: ', OLD.Data_inscricao,
            ', Multa: ', OLD.Multa_atual
        )
    );
END$

-- 5
CREATE TRIGGER historico_emprestimo_update AFTER UPDATE
ON Emprestimos
FOR EACH ROW
BEGIN
    INSERT INTO Historico (
        Tabela_envolvida,
        Acao,
        Data_hora,
        Envolvido_id,
        Dados_anteriores,
        Dados_novos
    )
    VALUES (
        'Emprestimos',
        'UPDATE',
        NOW(),
        NEW.ID_emprestimo,
        CONCAT(
            'Id do Usuário: ', OLD.Usuario_id,
            ', Id do Livro: ', OLD.Livro_id,
            ', Data do empréstimo: ', OLD.Data_emprestimo,
            ', Data de devolução prevista: ', OLD.Data_devolucao_prevista,
            ', Data que foi devolvido: ', OLD.Data_devolucao_real,
            ', Status do empréstimo: ', OLD.Status_emprestimo 
        ),
        CONCAT(
            'Id do Usuário: ', NEW.Usuario_id,
            ', Id do Livro: ', NEW.Livro_id,
            ', Data do empréstimo: ', NEW.Data_emprestimo,
            ', Data de devolução prevista: ', NEW.Data_devolucao_prevista,
            ', Data que foi devolvido: ', NEW.Data_devolucao_real,
            ', Status do empréstimo: ', NEW.Status_emprestimo 
        )
    );
END$


-- ========================= ATUALIZAÇÃO =========================

-- 1
DELIMITER $
CREATE TRIGGER retirar_estoque_insert AFTER INSERT
ON Emprestimos
FOR EACH ROW
BEGIN 
    UPDATE Livros SET Quantidade_disponivel = Quantidade_disponivel - 1 WHERE ID_livro = NEW.Livro_id;
END$

-- 2
CREATE TRIGGER adicionar_estoque_update AFTER UPDATE
ON Emprestimos
FOR EACH ROW
BEGIN 
    IF (OLD.Status_emprestimo <> 'devolvido' AND NEW.Status_emprestimo = 'devolvido') THEN
        UPDATE Livros SET Quantidade_disponivel = Quantidade_disponivel + 1 WHERE ID_livro = OLD.Livro_id;
    END IF;
END$

-- 3
CREATE TRIGGER atualizar_estoque_delete AFTER DELETE
ON Emprestimos
FOR EACH ROW
BEGIN 
    IF OLD.Status_emprestimo <> 'devolvido' THEN
        UPDATE Livros SET Quantidade_disponivel = Quantidade_disponivel + 1 WHERE ID_livro = OLD.Livro_id;
    END IF;
END$

-- 4
CREATE TRIGGER retirar_estoque_update AFTER UPDATE 
ON Emprestimos 
FOR EACH ROW
BEGIN
    IF OLD.Status_emprestimo = 'devolvido' AND NEW.Status_emprestimo <> 'devolvido' THEN
        UPDATE Livros SET Quantidade_disponivel = Quantidade_disponivel - 1 WHERE ID_livro = NEW.Livro_id;
    END IF;
END$

-- 5

CREATE FUNCTION atualizar_status (data_prazo DATE, data_entrega DATE) 
RETURNS VARCHAR(10)
BEGIN
    DECLARE res varchar(10);
    IF (data_entrega IS NOT NULL) THEN
        SET res = 'devolvido';
    ELSEIF (CURDATE() > data_prazo) THEN
        SET res = 'atrasado';
    ELSE 
        SET res = 'pendente';
    END IF; 

    RETURN res;
END $

CREATE TRIGGER atualizar_status_emprestimo BEFORE UPDATE
ON Emprestimos
FOR EACH ROW
BEGIN
    SET NEW.Status_emprestimo = atualizar_status(NEW.Data_devolucao_prevista, NEW.Data_devolucao_real);
END$


-- ========================= INSERIR VALORES =========================

-- 1
CREATE TRIGGER auto_data_inscricao BEFORE INSERT
ON Usuarios
FOR EACH ROW
BEGIN
    SET NEW.Data_inscricao = CURDATE();
END$

-- 2
CREATE TRIGGER auto_data_emprestimo BEFORE INSERT 
ON Emprestimos
FOR EACH ROW
BEGIN
    SET NEW.Data_emprestimo = CURDATE();
END$

-- 3
CREATE TRIGGER auto_data_devolucao_prevista BEFORE INSERT 
ON Emprestimos
FOR EACH ROW
BEGIN
    SET NEW.Data_devolucao_prevista = DATE_ADD(CURDATE(), INTERVAL 30 DAY);
END$

-- 4
CREATE TRIGGER auto_status_emprestimo BEFORE INSERT 
ON Emprestimos
FOR EACH ROW
BEGIN
    SET NEW.Status_emprestimo = 'pendente';

END$

-- 5
CREATE TRIGGER auto_data_devolucao_real BEFORE UPDATE 
ON Emprestimos
FOR EACH ROW
BEGIN
    IF NEW.Status_emprestimo = 'devolvido' AND OLD.Status_emprestimo <> 'devolvido' THEN
        SET NEW.Data_devolucao_real = CURDATE();
    END IF;
END$

DELIMITER ;