CREATE TABLE IF NOT EXISTS usuarios(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correoElectronico TEXT NOT NULL,
    password TEXT NOT NULL,
    favoritos TEXT
);

CREATE TABLE IF NOT EXISTS entidades(
    identificador TEXT NOT NULL,
    nombre TEXT,
    descripcion TEXT,
    servicios TEXT,
    coordenadas TEXT,
    urlInfo TEXT,
    distrito TEXT,
    barrio TEXT,
    horario TEXT,
    calleNumero TEXT,
    codigoPostal TEXT,
    municipio TEXT
);