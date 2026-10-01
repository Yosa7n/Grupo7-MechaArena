class Mecha:
    def __init__(self, nombre, modelo, color):
        self.nombre = nombre
        self.modelo = modelo
        self.color = color

        self.vida = 100
        self.energia = 100
        self.ataque = 20
        self.defensa = 10

    def mostrar_estado(self):
        print("\n===== DATOS DEL MECHA =====")
        print(f"Nombre: {self.nombre}")
        print(f"Modelo: {self.modelo}")
        print(f"Color: {self.color}")
        print(f"Vida: {self.vida}")
        print(f"Energía: {self.energia}")
        print(f"Ataque: {self.ataque}")
        print(f"Defensa: {self.defensa}")

    def personalizar(self):
        while True:
            print("\n===== PERSONALIZAR MECHA =====")
            print("1. Cambiar nombre")
            print("2. Cambiar modelo")
            print("3. Cambiar color")
            print("4. Ver configuracion")
            print("5. Terminar personalizacion")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                self.nombre = input("Nuevo nombre: ")
                print("Nombre actualizado correctamente.")

            elif opcion == "2":
                self.modelo = input("Nuevo modelo: ")
                print("Modelo actualizado correctamente.")

            elif opcion == "3":
                self.color = input("Nuevo color: ")
                print("Color actualizado correctamente.")

            elif opcion == "4":
                self.mostrar_estado()

            elif opcion == "5":
                print("Personalizacion finalizada.")
                break

            else:
                print("Opcion invalida.")

    def esta_activo(self):
        return self.vida > 0