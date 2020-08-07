import pytz

from dotenv import load_dotenv
from pathlib import Path

import os

#dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#Ajuste de huso horario del log
husoHorario = pytz.timezone('Europe/Madrid')

#Configuración del esquema y nombre de la base de datos
nombreBD = "basededatos.db"
esquemaDB = "basededatos_esquema.sql"