def mostrar_menu():
    print("\n==============================")
    print("         MECHA-ARENA")
    print("==============================")
    print("1. Crear Mecha")
    print("2. Ver Mecha")
    print("3. Iniciar Combate")
    print("4. Salir")
    print("==============================")


def main():
    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nCreación de Mecha")
            print("Módulo pendiente de integración.")

        elif opcion == "2":
            print("\nInformación del Mecha")
            print("Módulo pendiente de integración.")

        elif opcion == "3":
            print("\nInicio del Combate")
            print("Módulo pendiente de integración.")

        elif opcion == "4":
            print("\nGracias por jugar MECHA-ARENA.")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()