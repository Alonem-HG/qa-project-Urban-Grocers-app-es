import data
import sender_stand_request


############################## POSITIVE ASSERT ########################################################################
""" 
Logica:
Envíar una solicitud para crear un nuevo usuario o usuaria y obtener el token de autenticación (authToken). 
Envíar una solicitud para crear un kit personal para este usuario o usuaria junto con el encabezado Authorization. 
"""


def positive_assert(kit_body):
    """
    :param kit_body:
    :return: True, False
    """
    # El cuerpo de la solicitud actualizada se guarda en la variable kit_body
    kit_body = sender_stand_request.get_kit_body(kit_body)

    # Realiza la solicitud para crear un nuevo kit de producto
    kit_response = sender_stand_request.post_new_client_kit(kit_body)

    # Comprueba si el código de estado es 201 (creación exitosa)
    assert kit_response.status_code == 201, f"Error: Código de estado {kit_response.status_code}"

    # Comprobaciones de user y authToken.
    assert "user" in kit_response.json(), "Error: 'user' no encontrado en la respuesta."
    assert "authToken" in kit_response.json()["user"], "Error: 'authToken' no encontrado en la respuesta del usuario."
    assert kit_response.json()["user"]["authToken"] != "", "Error: 'authToken' vacío."

    # Comprobar que el resultado de la solicitud se guarda correctamente en la tabla de kits
    kits_table_response = sender_stand_request.get_kits_table()

    # Crear cadena con el kit que se creó recientemente
    str_kit = kit_body["name"]

    # Verificar si el kit está en la tabla de kits y es único
    assert kits_table_response.text.count(str_kit) == 1, f"Error: El kit {str_kit} no se encuentra o hay duplicados."


# Prueba 1. El número permitido de caracteres (1)
def test_create_kit_with_1_character_name_get_success_response():
    """
    Código de respuesta: 201
    :return: Passed or Failed
    """
    positive_assert(data.one_character_name)


# Prueba 2. El número permitido de caracteres (511)
def test_create_kit_with_511_character_name_get_success_response():
    """
    Código de respuesta: 201
    :return: Passed or Failed
    """
    positive_assert(data.kit_body_511)


# Prueba 5. Se permiten caracteres especiales
def test_create_kit_with_special_characters_name_get_success_response():
    """
    Código de respuesta: 201
    :return: Passed or Failed
    """
    positive_assert(data.special_characters)


# Prueba 6. Se permiten espacios
def test_create_kit_with_spaces_in_name_get_success_response():
    """
    Código de respuesta: 201
    :return: Passed or Failed
    """
    positive_assert(data.with_spaces)


# Prueba 7. Se permiten números
def test_create_kit_with_numbers_in_name_get_success_response():
    """
    Código de respuesta: 201
    :return: Passed or Failed
    """
    positive_assert(data.with_numbers)


# #################################### NEGATIVE ASSERT #################################################################

def negative_assert_code_400(kit_body):
    """
    Realiza una solicitud para crear un kit y comprueba que la respuesta tenga un código de estado 400.
    """
    # El cuerpo de la solicitud actualizada se guarda en la variable kit_body
    kit_body = sender_stand_request.get_kit_body(kit_body)

    # El resultado se guarda en la variable response
    response = sender_stand_request.post_new_client_kit(kit_body)

    # Comprueba si el código de estado es 400
    assert response.status_code == 400, f"Error: Se esperaba el código de estado 400, pero se obtuvo {response.status_code}"

    # Comprueba que el atributo 'code' en el cuerpo de respuesta es 400
    assert response.json().get("code") == 400, f"Error: El atributo 'code' no es 400, es {response.json().get('code')}"

    # Comprueba el atributo 'message' en el cuerpo de respuesta
    assert response.json().get("message") == "No se enviaron todos los parámetros requeridos", (
        f"Error: El mensaje de error no coincide. Se recibió: {response.json().get('message')}"
    )



# prueba 3. el número de caracteres es menor que la cantidad permitida (0)
def test_create_kit_with_empty_name_get_error_response():
    """
    Código de respuesta: 400
    :return: Passed or Failed
    """
    negative_assert_code_400(data.empty_name)


# prueba 4. el número de caracteres es mayor que la cantidad permitida (512)
def test_create_kit_with_512_character_name_get_error_response():
    """
    Código de respuesta: 400
    :return: Passed or Failed
    """
    #long_name = "a" * 512
    negative_assert_code_400(data.kit_body_512)


# Prueba 8: El parámetro "name" no se pasa en la solicitud
def test_create_kit_without_name_parameter_get_error_response():
    """
    Código de respuesta: 400
    :return: Passed or Failed
    """
    negative_assert_code_400(data.no_name)  # Cuerpo vacío, no se pasa el parámetro "name"


# Prueba 9: Se pasa un tipo de parámetro diferente (número)
def test_create_kit_with_number_as_name_get_error_response():
    """
    Código de respuesta: 400
    :return: Passed or Failed
    """
    negative_assert_code_400(data.numbers)  # El nombre se pasa como número en lugar de cadena
