import logSystem
from config import nombreBD
from usuario import Usuario
from gestorDeDatos import GestorDeDatos
from formularios import Busqueda, LoginApp, FormularioRegistro

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user
from werkzeug.urls import url_parse


import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ee18abb43892f9b37df141a308e6864c0be4847c83d938324690500dbf0beb55837d0a1ebebd2a367cc1e014d72e9b92e8ff140e47678d60f380b9d5dfd5a000'
login_manager = LoginManager(app)                  

guiaSocial = GestorDeDatos("https://datos.madrid.es/egob/catalogo/212774-0-atencion-social.json")

if not os.path.exists(nombreBD):
    print("Creando Base de datos.")
    guiaSocial.crearModificarDB("", True)
    guiaSocial.crearEntidadesSQL();
    print("Base de datos creada con éxito")
    logSystem.log("INFO", "Programa arrancado. Creada y actualizada base de datos.")
else:
    logSystem.log("INFO", "Programa arrancado. No es necesario crear base de datos")

@login_manager.user_loader
def cargar_usuario(id):
    usuario = guiaSocial.consultarDB(f"SELECT * FROM usuarios WHERE ID = '{ id }'")
    if usuario:
        return usuario
    else:
        return None

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


@app.route("/registro/", methods=["GET", "POST"])
def registro():
    template = "registro.html"

    formularioRegistro = FormularioRegistro()
    if formularioRegistro.validate_on_submit():
        nombre = formularioRegistro.nombre.data
        correoElectronico = formularioRegistro.correoElectronico.data
        password = formularioRegistro.password.data

        nuevoUsuario = Usuario(nombre, correoElectronico, password)
        
        guiaSocial.crearModificarDB(f'''INSERT INTO usuarios
        VALUES(NULL, "{nuevoUsuario.nombre}", "{nuevoUsuario.correoElectronico}","{nuevoUsuario.password}","{nuevoUsuario.favoritos}");''')

        template = "registro_completado.html"

    return render_template(f"{ template }", formularioRegistro = formularioRegistro, formulario = Busqueda())

@app.route("/acceso/", methods=["GET", "POST"])
def acceso():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    formularioLogin = LoginApp()

    if formularioLogin.validate_on_submit():
        usuario = guiaSocial.getUsuario(formularioLogin.correoElectronico.data)
        print(usuario)
        if  usuario is not None and usuario.comprobar_password(formularioLogin.password.data):
            login_user(usuario, recuerdame=formularioLogin.recuerdame.data)
            siguiente_pagina = request.args.get('next')
            
            if not siguiente_pagina or url_parse(siguiente_pagina).netloc != '':
                siguiente_pagina = url_for('index')
            return redirect(siguiente_pagina)

    return render_template('login.html', formularioLogin=formularioLogin, formulario = Busqueda())
