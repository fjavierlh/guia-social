#Guía Social

"Guía Social" nace con la ilusión de convertirse en un recurso habitual de las profesionales de entidades y organizaciones del Tercer Sector (Trabajadoras/es Sociales, Educadoras/es, Técnicos de Integración Social, etc.).

Actualmente la aplicación está centada en el municipio de Madrid, pero 

##Instalación:

1. Crea un entorno virtual y actívalo.
2. Instala con pip las dependencias que encontrarás el archivo "requirements.txt" (pip install -r requirements.txt)
3. Completa el archivo ".env-example" con tus API Keys y renombralo para que quede como ".env"
4. Abre el archo ``main.py`` y ejecútalo con el comando ``flask run`` (Al arrancar el servidor de flask por primera vez dale unos segundos, tiene que generar la base de datos SQLite a partir de los datos de la API)
5. ¡Listo! ¡A trastear con el proyecto! :)


##ToDo List:

1. Ampliar base de datos: Incluir información de otras apis de https://datos.madrid.es
2. Implementar crawler que extraiga datos de contacto de la web de https://madrid.es
3. Añadir funcionalidad que permita actualizar la base de datos.
4. Permitir a los usuarios/as hacer comentarios y valoraciones sobre las entidades.

