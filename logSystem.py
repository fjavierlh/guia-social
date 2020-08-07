import settings
import logging
from datetime import datetime

import pytz

def log(opcion, mensaje):
    '''
    opcion: "DEBUG", "INFO", "WARNING", guarda el log en archivos separados.
    mensaje: String que se grabará en el log acompañado de la fecha y hora.
    '''
    opcion = opcion.upper();

    fechaCreacion = datetime.now(settings.husoHorario).strftime("%D %H:%M:%S")
    mensaje = f"{fechaCreacion} - {mensaje}";

    logging.basicConfig(filename='info.log',level=logging.DEBUG);

    if opcion == "DEBUG":
        logging.debug(mensaje);

    elif opcion == "INFO":
        logging.info(mensaje);

    elif opcion == "WARNING":
        logging.warning(mensaje);