from mecha import Mecha
from combate import SistemaCombate
from validaciones import validar_opcion, solicitar_nombre


def mostrar_menu():
    print("\n================================")
    print("       BIENVENIDO A MECHA-ARENA")
    print("================================")
    print("1. Crear Mecha")
    print("2. Ver Mecha")
    print("3. Iniciar Combate")
    print("4. Salir")
    print("================================")


def obtener_opcion():
    while True:
        opcion = input("Seleccione una opción: ").strip()

        if validar_opcion(opcion, ["1", "2", "3", "4"]):
            return opcion

        print("\nOpción no válida. Intente nuevamente.")


def crear_mecha_jugador():
    print("\n================================")
    print("       CREACION DEL MECHA")
    print("================================")

    nombre = solicitar_nombre("Ingrese el nombre del Mecha: ")

    modelo = input("Ingrese el modelo del Mecha: ").strip()
    while not modelo:
        print("Error: el modelo no puede estar vacío.")
        modelo = input("Ingrese el modelo del Mecha: ").strip()

    color = input("Ingrese el color del Mecha: ").strip()
    while not color:
        print("Error: el color no puede estar vacío.")
        color = input("Ingrese el color del Mecha: ").strip()

    mecha = Mecha(nombre, modelo, color)

    print("\nMecha creado correctamente.")

    return mecha


def mostrar_mecha(mecha):
    if mecha is None:
        print("\nPrimero debe crear un Mecha.")
        return

    mecha.mostrar_estado()


def crear_enemigo():
    enemigo = Mecha(
        "Titan CPU",
        "TX-900",
        "Rojo"
    )

    enemigo.vida = 100
    enemigo.energia = 100
    enemigo.ataque = 18
    enemigo.defensa = 8

    return enemigo


def mostrar_menu_combate():
    print("\n------------------------------")
    print("       TURNO DEL JUGADOR")
    print("------------------------------")
    print("1. Ataque normal")
    print("2. Defender")
    print("3. Ataque especial")
    print("4. Retirarse")
    print("------------------------------")


def iniciar_combate(jugador):
    if jugador is None:
        print("\nPrimero debe crear un Mecha.")
        return

    sistema = SistemaCombate()
    enemigo = crear_enemigo()

    # Reiniciar al jugador para un nuevo combate.
    jugador.vida = 100
    jugador.energia = 100

    print("\n================================")
    print("       INICIO DEL COMBATE")
    print("================================")
    print(f"{jugador.nombre} VS {enemigo.nombre}")

    while True:
        print("\nESTADO ACTUAL")
        print(sistema.mostrar_estado(jugador))
        print(sistema.mostrar_estado(enemigo))

        mostrar_menu_combate()

        opcion = input("Seleccione una acción: ").strip()

        if not validar_opcion(
            opcion,
            ["1", "2", "3", "4"]
        ):
            print("\nOpción de combate no válida.")
            continue

        if opcion == "1":
            dano = sistema.atacar(
                jugador,
                enemigo
            )

            print(
                f"\n{jugador.nombre} realizó "
                f"{dano} puntos de daño."
            )

        elif opcion == "2":
            sistema.defender(jugador)

            print(
                f"\n{jugador.nombre} "
                "adoptó una posición defensiva."
            )

        elif opcion == "3":
            try:
                dano = sistema.ataque_especial(
                    jugador,
                    enemigo
                )

                print(
                    f"\n{jugador.nombre} utilizó "
                    f"un ataque especial e hizo {dano} "
                    "puntos de daño."
                )

            except ValueError as error:
                print(f"\n{error}")
                continue

        elif opcion == "4":
            print("\nHas abandonado el combate.")
            return

        if sistema.esta_destruido(enemigo):
            print("\n================================")
            print(f"GANADOR: {jugador.nombre}")
            print("================================")
            return

        print("\nTurno del enemigo...")

        accion, dano = sistema.turno_enemigo(
            enemigo,
            jugador
        )

        if accion == "ataque":
            print(
                f"{enemigo.nombre} realizó un "
                f"ataque normal causando {dano} "
                "puntos de daño."
            )

        elif accion == "especial":
            print(
                f"{enemigo.nombre} utilizó un "
                f"ataque especial causando {dano} "
                "puntos de daño."
            )

        elif accion == "defensa":
            print(
                f"{enemigo.nombre} adoptó "
                "una posición defensiva."
            )

        if sistema.esta_destruido(jugador):
            print("\n================================")
            print(f"GANADOR: {enemigo.nombre}")
            print("================================")
            return


def main():
    mecha_jugador = None

    while True:
        mostrar_menu()

        opcion = obtener_opcion()

        if opcion == "1":
            mecha_jugador = crear_mecha_jugador()

        elif opcion == "2":
            mostrar_mecha(mecha_jugador)

        elif opcion == "3":
            iniciar_combate(mecha_jugador)

        elif opcion == "4":
            print("\nGracias por jugar MECHA-ARENA.")
            print("Hasta la próxima.")
            break


if __name__ == "__main__":
    main()