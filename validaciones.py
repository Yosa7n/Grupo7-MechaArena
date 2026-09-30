def validar_nombre(nombre):
    """
    Valida que el nombre del mecha no esté vacío
    y tenga al menos 3 caracteres.
    """
    if not isinstance(nombre, str):
        return False

    nombre = nombre.strip()

    if len(nombre) < 3:
        return False

    return True


def validar_numero_positivo(valor):
    """
    Valida que un valor sea numérico y mayor que cero.
    """
    try:
        numero = int(valor)

        if numero <= 0:
            return False

        return True

    except (ValueError, TypeError):
        return False


def validar_estadistica(valor, minimo=1, maximo=100):
    """
    Valida estadísticas del mecha como ataque,
    defensa, velocidad o energía.
    """
    try:
        numero = int(valor)

        if numero < minimo or numero > maximo:
            return False

        return True

    except (ValueError, TypeError):
        return False


def validar_opcion(opcion, opciones_validas):
    """
    Comprueba que una opción pertenezca
    a una lista de opciones permitidas.
    """
    return str(opcion) in [str(op) for op in opciones_validas]


def solicitar_entero(mensaje, minimo=1, maximo=100):
    """
    Solicita un número hasta que el usuario
    ingrese un valor válido.
    """
    while True:

        valor = input(mensaje)

        try:
            numero = int(valor)

            if minimo <= numero <= maximo:
                return numero

            print(
                f"Error: ingrese un valor entre "
                f"{minimo} y {maximo}."
            )

        except ValueError:
            print("Error: debe ingresar un número entero.")


def solicitar_nombre(mensaje="Ingrese el nombre del Mecha: "):
    """
    Solicita un nombre válido para el mecha.
    """
    while True:

        nombre = input(mensaje).strip()

        if validar_nombre(nombre):
            return nombre

        print(
            "Error: el nombre debe tener "
            "al menos 3 caracteres."
        )