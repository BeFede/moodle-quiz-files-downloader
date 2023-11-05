# Descargador de Archivos de Moodle

Este script en Python te permite descargar archivos de las pruebas en la plataforma Moodle de la Universidad Tecnológica Nacional (UTN) - Facultad Regional Córdoba. Automatiza el proceso de inicio de sesión, navegación hasta una prueba específica y descarga de archivos desde todos los intentos.

## Características

- Iniciar sesión en Moodle con tus credenciales.
- Seleccionar una prueba específica mediante su ID.
- Crear automáticamente un directorio para guardar los archivos descargados.
- Descargar archivos desde todos los intentos dentro de la prueba seleccionada.

## Requisitos

Antes de comenzar, asegúrate de cumplir con los siguientes requisitos:

- Tener Python 3.x instalado en tu máquina local.
- Asegúrate de que las bibliotecas de Python necesarias (requests, bs4) estén instaladas. Puedes instalarlas mediante pip:
  ```shell
  pip install -r requirements.txt