from validaciones import validar_opcion


def mostrar_menu():
    print("\n==============================")
    print("         MECHA-ARENA")
    print("==============================")
    print("1. Crear Mecha")
    print("2. Ver Mecha")
    print("3. Iniciar Combate")
    print("4. Salir")
    print("==============================")


def obtener_opcion():
    while True:
        opcion = input("Seleccione una opción: ").strip()

        if validar_opcion(opcion, ["1", "2", "3", "4"]):
            return opcion

        print("\nOpción no válida. Intente nuevamente.")


def main():
    while True:
        mostrar_menu()
        opcion = obtener_opcion()

        if opcion == "1":
            print("\n=== CREACIÓN DE MECHA ===")
            print("Módulo pendiente de integración.")

        elif opcion == "2":
            print("\n=== INFORMACIÓN DEL MECHA ===")
            print("Módulo pendiente de integración.")

        elif opcion == "3":
            print("\n=== INICIO DEL COMBATE ===")
            print("Módulo pendiente de integración.")

        elif opcion == "4":
            print("\nGracias por jugar MECHA-ARENA.")
            break


if __name__ == "__main__":
    main()