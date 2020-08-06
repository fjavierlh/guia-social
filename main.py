import logSystem

from apiBrowser import ApiBrowser

from flask import Flask, render_template

from flask_sqlalchemy import Pagination

app = Flask(__name__)

guiaSocial = ApiBrowser("https://datos.madrid.es/egob/catalogo/212774-0-atencion-social.json", "centros_atencion_social.json");

guiaSocial.obtenerDatos();

guiaSocial.guardarDatosEnLocal("centros_atencion_social.json", "w");

@app.route("/")
@app.route("/page/<int:page>")
def index():
    #return render_template("index.html", datos=Pagination(guiaSocial.datos, 1, 15, 30,len(guiaSocial.datos.keys())))
    return render_template("index.html", datos=guiaSocial.datos)