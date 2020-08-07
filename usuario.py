from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class  Usuario(UserMixin):
    def __init__(self, nombre, correoElectronico, password):
        self.nombre = nombre
        self.correoElectronico = correoElectronico
        self.password = generate_password_hash(password)

        self.favoritos = []

    def __repr__(self):
        return f"{self.correoElectronico}"

    def establecer_password(self, password):
        self.password = generate_password_hash(password)

    def comprobar_password(self, password):
        return check_password_hash(self.password, password)

