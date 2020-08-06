from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Busqueda(FlaskForm):
    terminoBusqueda = StringField('Busqueda', validators=[DataRequired(), Length(min=3, max=128)])
    enviar = SubmitField("Enviar")