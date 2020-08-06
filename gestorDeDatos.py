import json
import sqlite3
import urllib.request
import os

from config import nombreBD, esquemaDB

from entidad import Entidad

import logSystem

class GestorDeDatos():
    def __init__(self, url):
        self.url = url;
        self.datos = self.obtenerDatos();
    
    def obtenerDatos(self):
        try:
            with urllib.request.urlopen(self.url) as urlJSON:
                self.datos = json.loads(urlJSON.read().decode())
                logSystem.log("INFO", "Datos de la API descargados con éxito.");
                  
        except ValueError:
            #BUSCAR FORMA DE HACER EXCEPCIONES MEDIANTE CODIGO DE ESTADO
            logSystem.log("WARNING", f"Error al descargar el recurso '{url}'.")

        return self.datos  

       
    def crearModificarDB(self, consulta="", crear=False):
        '''
        Permite consultar o crear la base de datos del proyecto.

        Parámetros:
        consulta (default:""): Consulta SQL a realizar;
        crear (default: False): Con valor "True" permite crear una base de datos a partir del archivo "basededatos_esquema.sql"
        '''
        conexion = sqlite3.connect(nombreBD);
        cursor = conexion.cursor()

        if crear:
            with sqlite3.connect(nombreBD) as conexion:
                with open(esquemaDB, "rt") as ficheroSQL:
                    esquemaScript = ficheroSQL.read()
                    conexion.executescript(esquemaScript);
                    
        else:
            print(consulta)
            cursor.execute(consulta)
            conexion.commit()
            conexion.close()

    def consultarDB(self, consulta):
        conexion = sqlite3.connect(nombreBD)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        salida = cursor.fetchall();
        conexion.close()
        return salida;

    def crearEntidadesSQL(self): 
        for entidad in self.datos["@graph"]:
            try:
                identificador = entidad["id"]
                nombre = entidad["title"].replace("í", "i")
                descripcion = entidad["organization"]["organization-desc"]
                servicios = entidad["organization"]["services"]
                coordenadas = entidad["location"]
                urlInfo = entidad["relation"]
                distrito = entidad["address"]["district"]["@id"].rsplit("/", 1)[-1]
                barrio = entidad["address"]["area"]["@id"].rsplit("/", 1)[-1]
                horario = entidad["organization"]["schedule"]
                calleNumero = entidad["address"]["street-address"]
                codigoPostal = entidad["address"]["postal-code"]
                municipio = entidad["address"]["locality"]  

                nuevaEntidad = Entidad(identificador, nombre, descripcion, servicios, coordenadas, urlInfo, distrito, barrio, horario, calleNumero, codigoPostal, municipio)
                self.crearModificarDB(f'INSERT INTO "entidades" VALUES({identificador}, "{nombre}", "{descripcion}", "{servicios}", "{coordenadas}", "{urlInfo}", "{distrito}", "{barrio}", "{horario}", "{calleNumero}", "{codigoPostal}", "{municipio}");')
            
            except KeyError:
                logSystem.log("INFO",f"{KeyError}");
                continue;
        return logSystem.log("INFO","Entidades creadas con éxito")