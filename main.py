import logSystem
from config import nombreBD
from gestorDeDatos import GestorDeDatos
from formularios import Busqueda

from flask import Flask, render_template, request, redirect, url_for

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ee18abb43892f9b37df141a308e6864c0be4847c83d938324690500dbf0beb55837d0a1ebebd2a367cc1e014d72e9b92e8ff140e47678d60f380b9d5dfd5a000'
                            

guiaSocial = GestorDeDatos("https://datos.madrid.es/egob/catalogo/212774-0-atencion-social.json")

if not os.path.exists(nombreBD):
    guiaSocial.crearModificarDB("", True)
    guiaSocial.crearEntidadesSQL();
    logSystem.log("INFO", "Programa arrancado. Creada y actualizada base de datos.")
else:
    logSystem.log("INFO", "Programa arrancado. No es necesario crear base de datos")

@app.route("/")
def index():
    page = request.args.get('page', 1)
    lista = request.args.get('list', 20)
    entidades = guiaSocial.consultarDB("SELECT * FROM entidades")
    return render_template("index.html", entidades=entidades)

@app.route("/busqueda/", methods=["GET", "POST"])
def busqueda():
    formulario = Busqueda()
    entidades = guiaSocial.consultarDB(f"SELECT * FROM entidades")

    if formulario.validate_on_submit():
        busqueda = formulario.terminoBusqueda.data
        busquedaFormateada = "%" + "{}".format(busqueda.replace(" ","%")) + "%"
        
        entidades = guiaSocial.consultarDB(f"SELECT * FROM entidades WHERE nombre LIKE '{busquedaFormateada}'")

    return render_template("busqueda.html", entidades=entidades, formulario=formulario)

@app.route("/por-nombre/")
def por_nombre():

    entidades = guiaSocial.consultarDB("SELECT * FROM entidades ORDER BY nombre DESC")
    
    return render_template("index.html", entidades=entidades)