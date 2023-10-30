CREATE DATABASE BDTrivia; 

CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    redes VARCHAR(255),
    puntaje INT,
    tiempo_respondido TIME
);

CREATE TABLE Preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL
);

CREATE TABLE RespuestasUsuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    pregunta_id INT,
    respuesta_usuario TEXT,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
    FOREIGN KEY (pregunta_id) REFERENCES Preguntas(id)
);