CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO usuarios (nombre, email, password)
VALUES
    ('Mabel', 'mabel@gmail.com', '1234'),
    ('Laura', 'laura@gmail.com', '1234'),
    ('Sofia', 'sofia@gmail.com', '1234');