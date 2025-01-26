# Proyecto Urban Grocers 
**Autor:** Alonso Hernández González
**Fecha:** Enero 2025  
**Cohorte:** 20  
**Sprint:** 7  

## Descripción del Proyecto
Este proyecto realiza diferentes pruebas a una API para verificar su correcto funcionamiento, utilizando herramientas y librerías específicas para garantizar la calidad del software.

## Librerías Utilizadas
- **pytest**: Framework para realizar pruebas automatizadas.
- **requests**: Librería para realizar solicitudes HTTP.

Para acceder a la documentación de la API, visita la siguiente URL:  
`<URL del servidor lanzado>/docs/`

---

## Estructura del Proyecto
El proyecto se organiza en los siguientes archivos principales:

1. **`configuration.py`**  
   Contiene las URLs configuradas para realizar consultas a la API.

2. **`data.py`**  
   Almacena los cuerpos de las solicitudes (body) en formato JSON. Ademas de variables con diferentes tipos de caracteres y patrones para evaluar el parametro name de los kits.

3. **`sender_stand_request.py`**  
   Implementa las funciones para realizar solicitudes HTTP a la aplicación.

4. **`create_kit_name_kit_test.py`**  
   Contiene las pruebas (`assert`) y casos de test para validar el comportamiento de la API.

---

## Cómo Ejecutar las Pruebas
1. Asegúrate de tener instaladas las dependencias necesarias:
   ```bash
   pip install pytest requests
