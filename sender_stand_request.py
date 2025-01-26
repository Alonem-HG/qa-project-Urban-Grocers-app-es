import configuration
import data
import requests

############################### USER ###############################################

# Función para cambiar el valor del parámetro firstName en el cuerpo de la solicitud
def get_user_body(first_name):
    # Copiar el diccionario con el cuerpo de la solicitud desde el archivo de datos
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)


def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

################################ KITS #############################################

def get_kit_body(name):
    # Copiar el diccionario con el cuerpo de la solicitud desde el archivo de datos
    current_body = data.kit_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["name"] = name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

def get_new_user_token(user_body):
    """
    Envía una solicitud para crear un nuevo usuario o usuaria y devuelve el token de autenticación.
    """
    user_response = requests.post(
        configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # URL para crear el nuevo usuario
        json=user_body,  # Cuerpo de la solicitud con la información del usuario
        headers=data.headers  # Encabezados de la solicitud
    )

    # Comprueba si la solicitud fue exitosa (código 201) y devuelve el token de autenticación
    if user_response.status_code == 201:
        return user_response.json().get("authToken")
    else:
        raise Exception("Error al crear el usuario. Código de estado:", user_response.status_code)


def post_new_client_kit(kit_body):
    # Realiza una solicitud POST para crear un nuevo user.
    create_user = post_new_user(data.user_body)
    # Obtener el token del user
    auth_token = create_user.json()['authToken']
    # Agregar auth_token a headers
    headers = data.headers.copy()
    headers["Authorization"] = f"Bearer {auth_token}"

    # Crear un kit con el user de arriba
    return requests.post(
        configuration.URL_SERVICE + configuration.KITS_PATH,  # Concatenación de URL base y ruta.
        json=kit_body,  # Datos a enviar en la solicitud.
        headers=headers
    )


def get_kits_table():
    return requests.get(configuration.URL_SERVICE + configuration.KITS_TABLE_PATH)
