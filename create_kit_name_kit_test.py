import data
import sender_stand_request


############################## POSITIVE ASSERT ########################################################################
""" 
Envía una solicitud para crear un nuevo usuario o usuaria y recuerda el token de autenticación (authToken). 
Envía una solicitud para crear un kit personal para este usuario o usuaria. Asegúrate de pasar también el encabezado Authorization. 
"""

def positive_assert(kit_body):
    # Realiza una solicitud para obtener el token de autenticación
    auth_token = sender_stand_request.get_new_user_token(data.user_body)  # Obtén el token de autenticación usando los datos del usuario

    # Realiza la solicitud para crear un nuevo kit de producto
    kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)

    # Comprueba si el código de estado es 201 (creación exitosa)
    assert kit_response.status_code == 201, f"Error: Código de estado {kit_response.status_code}"

    # Comprueba que el campo 'authToken' esté presente en la respuesta y no esté vacío
    assert "authToken" in kit_response.json(), "Error: 'authToken' no encontrado en la respuesta."
    assert kit_response.json()["authToken"] != "", "Error: 'authToken' vacío."

    # Comprobar que el resultado de la solicitud se guarda correctamente en la tabla de kits
    kits_table_response = sender_stand_request.get_kits_table()

    # Crear una cadena con los datos esperados del kit, incluyendo el token
    str_kit = kit_body["name"] + ",,," + kit_body.json()["authToken"]

    # Verifica si el kit existe en la tabla de kits y es único
    assert kits_table_response.text.count(str_kit) == 1, "Error: El kit no se encuentra o hay duplicados."


# Prueba 1. El número permitido de caracteres (1)
def test_create_kit_with_1_character_name_get_success_response():
    """
    Código de respuesta: 201 El campo "name" del cuerpo de la respuesta coincide con el campo "name" del cuerpo de la solicitud
    :return:
    """
    positive_assert("a")


# Prueba 2. El número permitido de caracteres (511)
def test_create_kit_with_511_character_name_get_success_response():
    """
    Código de respuesta: 201 El campo "name" en el cuerpo de la respuesta coincide con el campo "name" en el cuerpo de la solicitud
    :return:
    """
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


# Prueba 5. Se permiten caracteres especiales
def test_create_kit_with_special_characters_name_get_success_response():
    """
    Código de respuesta: 201 El campo "name" del cuerpo de la respuesta coincide con el campo "name" del cuerpo de la solicitud
    :return:
    """
    positive_assert("№%@,")


# Prueba 6. Se permiten espacios
def test_create_kit_with_spaces_in_name_get_success_response():
    """
    Código de respuesta: 201 El campo "name" del cuerpo de la respuesta coincide con el campo "name" del cuerpo de la solicitud
    :return:
    """
    positive_assert(" A Aaa ")


# Prueba 7. Se permiten números
def test_create_kit_with_numbers_in_name_get_success_response():
    """
    Código de respuesta: 201 El campo "name" del cuerpo de la respuesta coincide con el campo "name" del cuerpo de la solicitud
    :return:
    """
    positive_assert("123")


# #################################### NEGATIVE #######################################################################


def negative_assert_code_400(kit_body):
    """
    Realiza una solicitud para crear un kit y comprueba que la respuesta tenga un código de estado 400.
    """
    # El resultado se guarda en la variable response
    response = sender_stand_request.post_new_client_kit(kit_body, sender_stand_request.get_new_user_token(data.user_body))

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
    negative_assert_code_400("")


# prueba 4. el número de caracteres es mayor que la cantidad permitida (512)
def test_create_kit_with_512_character_name_get_error_response():
    #long_name = "a" * 512
    negative_assert_code_400("abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd")


# Prueba 8: El parámetro "name" no se pasa en la solicitud
def test_create_kit_without_name_parameter_get_error_response():
    negative_assert_code_400({})  # Cuerpo vacío, no se pasa el parámetro "name"


# Prueba 9: Se pasa un tipo de parámetro diferente (número)
def test_create_kit_with_number_as_name_get_error_response():
    negative_assert_code_400({"name": 123})  # El nombre se pasa como número en lugar de cadena
