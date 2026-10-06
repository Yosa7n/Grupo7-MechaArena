class Mecha:
    def __init__(self, nombre, modelo, color, patas=4):
        if patas not in (4, 6, 8):
            raise ValueError("Un Mecha debe tener entre 1 y 8 patas.")

        self.nombre = nombre
        self.modelo = modelo
        self.color = color
        self.patas = patas

        self.vida = 100
        self.vida_maxima = 100
        self.energia = 100
        self.ataque = 20
        self.defensa = 10

    def mostrar_estado(self):
        print("\n===== DATOS DEL MECHA =====")
        print(f"Nombre: {self.nombre}")
        print(f"Modelo: {self.modelo}")
        print(f"Color: {self.color}")
        print(f"Vida: {self.vida}/{self.vida_maxima}")
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
                nuevo_nombre = input("Nuevo nombre: ").strip()

                if nuevo_nombre:
                    self.nombre = nuevo_nombre
                    print("Nombre actualizado correctamente.")
                else:
                    print("El nombre no puede estar vacio.")

            elif opcion == "2":
                nuevo_modelo = input("Nuevo modelo: ").strip()

                if nuevo_modelo:
                    self.modelo = nuevo_modelo
                    print("Modelo actualizado correctamente.")
                else:
                    print("El modelo no puede estar vacio.")
           
            elif opcion == "3":
                nuevo_color = input("Nuevo color: ").strip()

                if nuevo_color:
                    self.color = nuevo_color
                    print("Color actualizado correctamente.")
                else:
                    print("El color no puede estar vacio.")

            elif opcion == "4":
                self.mostrar_estado()

            elif opcion == "5":
                print("Personalizacion finalizada.")
                break

            else:
                print("Opcion invalida.")

    def esta_activo(self):
        return self.vida > 0

def crear_mecha():
    print("\n================================")
    print("       CREACION DEL MECHA")
    print("================================")

    while True:
        nombre = input("Ingrese el nombre del Mecha: ").strip()

        if nombre:
            break

        print("El nombre no puede estar vacio.")

    while True:
        modelo = input("Ingrese el modelo del Mecha: ").strip()

        if modelo:
            break

        print("El modelo no puede estar vacio.")

    while True:
        color = input("Ingrese el color del Mecha: ").strip()

        if color:
            break

        print("El color no puede estar vacio.")

    nuevo_mecha = Mecha(nombre, modelo, color)

    print("\nMecha creado correctamente.")

    return nuevo_mecha

if __name__ == "__main__":
    mecha = crear_mecha()

    print("\n===== MECHA CREADO =====")
    mecha.mostrar_estado()

    mecha.personalizar()

    print("\n===== CONFIGURACION FINAL =====")
    mecha.mostrar_estado()