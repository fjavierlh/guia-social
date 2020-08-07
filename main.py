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

@app.route("/", methods=["GET", "POST"])
@app.route("/resultado/", methods=["GET", "POST"])
def index():
    page = request.args.get('page', 1)
    lista = request.args.get('list', 20)

    formulario = Busqueda()
    entidades = guiaSocial.consultarDB(f"SELECT * FROM entidades")
    busqueda = ""
    template = "index.html"

    if formulario.validate_on_submit():
        busqueda = formulario.terminoBusqueda.data
        busquedaFormateada = "%" + "{}".format(busqueda.replace(" ","%")) + "%"
        
        entidades = guiaSocial.consultarDB(f"""SELECT * FROM entidades
        WHERE nombre LIKE '{busquedaFormateada}' OR descripcion LIKE '{busquedaFormateada}' OR servicios LIKE '{busquedaFormateada}'
        OR distrito LIKE '{busquedaFormateada}' OR barrio LIKE '{busquedaFormateada}' OR horario LIKE '{busquedaFormateada}'
        OR calleNumero LIKE '{busquedaFormateada}' OR codigoPostal LIKE '{busquedaFormateada}' OR municipio LIKE '{busquedaFormateada}'""")
        
        template = "resultado.html"

    return render_template(f"{template}", entidades=entidades, formulario=formulario, busqueda=busqueda)


@app.route("/entidad/<nombre>/", methods=["GET", "POST"])
def mostrarDetalle(nombre):
    entidad = guiaSocial.consultarDB(f"SELECT * FROM entidades WHERE nombre = '{nombre}'")

    coordenadas = eval(entidad[0][4])
    
    return render_template("detalle.html", entidad=entidad, nombre=nombre, coordenadas=coordenadas, formulario = Busqueda())