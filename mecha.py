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

    def esta_activo(self):
        return self.vida > 0
def crear_mecha():
    print("\n================================")
    print("       CREACION DEL MECHA")
    print("================================")

    nombre = input("Ingrese el nombre del Mecha: ")
    modelo = input("Ingrese el modelo del Mecha: ")
    color = input("Ingrese el color del Mecha: ")

    nuevo_mecha = Mecha(nombre, modelo, color)

    print("\nMecha creado correctamente.")

    return nuevo_mecha