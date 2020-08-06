import urllib.request, json
import os

import logSystem

class ApiBrowser(object):
    def __init__(self, url, rutaFichero):
        self.url = url;
        self.rutaFichero = rutaFichero;
        if not os.path.exists(self.rutaFichero):
            self.datos = self.obtenerDatos();
    
    def obtenerDatos(self):
        try:
            with urllib.request.urlopen(self.url) as urlJSON:
                self.datos = json.loads(urlJSON.read().decode())
            salida = "Datos descargados con éxito."
            logSystem.log("INFO", "Copia local del archivo JSON realizada con éxito.");              

        except ValueError:
            salida = "Ha ocurrido un error. Revisa el archivo \"info.log\" para más información."
            logSystem.log("WARNING", f"Error al descargar el recurso '{url}'.")

        return self.datos

    def guardarDatosEnLocal(self, rutaFichero, modo):
        try:
            with open(self.rutaFichero, "w") as ficheroJSON:
                json.dump(self.datos, ficheroJSON, indent=4);
                salida = "Datos guardados con éxito."
                logSystem.log("INFO", "Copia local del archivo JSON realizada con éxito.");

        except ValueError:
            salida = "Ha ocurrido un error. Revisa el archivo \"info.log\" para más información."
            logSystem.log("WARNING", "Error al crear la copia local del archivo JSON.");

        return salida;     

    def mostrarTodo(self):
        with open(self.rutaFichero, "r") as ficheroJSON:
            contenido = json.load(ficheroJSON);

        salida = ""
        for entidad in self.datos["@graph"]: 
            try:
                nombre = "{}".format()
                descripcion = "{}".format(entidad["organization"]["organization-desc"])
                servicios = "{}".format()
                masInformacion = "{}".format(entidad["relation"])

                distrito = entidad["address"]["district"]["@id"].rsplit("/", 1)[-1]
                #salida += "Distrito: {}".format(distrito[-1])

                barrio = entidad["address"]["area"]["@id"].rsplit("/", 1)[-1]
                #salida += " - Barrio: {}\n".format(barrio[-1])

                calleNumero += "{}".format(entidad["address"]["street-address"])
                codigoPostal += "{}".format(entidad["address"]["postal-code"])
                municipio += "{}".format(entidad["address"]["locality"])

            except KeyError:
                logSystem.log("INFO",f"{KeyError}");
                continue;
        salida = f"{nombre} {descripcion} {servicios} {distrito} {barrio} {calleNumero} {codigoPostal} {municipio}"

        return salida;