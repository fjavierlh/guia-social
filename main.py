import urllib.request, json
import os

with urllib.request.urlopen("https://datos.madrid.es/egob/catalogo/212774-0-atencion-social.json") as url:
    data = json.loads(url.read().decode())

if not os.path.exists("centros_atencion_social.json"):
    print("Cargando datos, esto puede tardar un poco.")

    with open("centros_atencion_social.json", "w") as ficheroJSON:
        json.dump(data, ficheroJSON, indent=4);

    print("Datos descargados con éxito :)")

input("Pulsa 'Enter' para continuar");

with open("centros_atencion_social.json", "r") as ficheroJSON:
    contenido = json.load(ficheroJSON);
    

def mostrarTodo():
    salida = ""
    for entidad in contenido["@graph"]: 
        try:
            salida += "Nombre: {}\n".format(entidad["title"])
            salida += "Descripción: {}\n".format(entidad["organization"]["organization-desc"])
            salida += "Servicios: {}\n".format(entidad["organization"]["services"])
            salida += "Más información: {}\n".format(entidad["relation"])

            distrito = entidad["address"]["district"]["@id"].rsplit("/", 1)
            salida += "Distrito: {}".format(distrito[-1])

            barrio = entidad["address"]["area"]["@id"].rsplit("/", 1)
            salida += " - Barrio: {}\n".format(barrio[-1])

            salida += "Dirección: "
            salida += "{}\n".format(entidad["address"]["street-address"])
            salida += "{}\n".format(entidad["address"]["postal-code"])
            salida += "{}\n".format(entidad["address"]["locality"])
            salida += "\n"

        except KeyError:
            continue;

    return salida;

print(mostrarTodo());