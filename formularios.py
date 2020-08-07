from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class Busqueda(FlaskForm):
    terminoBusqueda = StringField("Busqueda", validators=[DataRequired(), Length(min=3, max=128)])
    buscar = SubmitField("Buscar")

class LoginApp(FlaskForm):
    correoElectronico = StringField("Correo Electrónico", validators=[DataRequired()])
    password = StringField("Contraseña", validators=[DataRequired()])
    recuerdame = BooleanField("Recuérdame")
    entrar = SubmitField("Entrar")


class FormularioRegistro(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    correoElectronico = StringField("Correo Electrónico", validators=[DataRequired()])
    password = StringField("Contraseña", validators=[DataRequired()])
    registrarme = SubmitField("Registrarme")
