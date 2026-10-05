import tkinter as tk
from tkinter import messagebox, ttk

from combate import SistemaCombate
from mecha import Mecha


class InterfazMechaArena:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mecha-Arena")
        self.ventana.geometry("560x500")
        self.ventana.resizable(False, False)

        self.sistema = SistemaCombate()
        self.jugador = None
        self.enemigo = None
        self.campos = {}
        self.etiquetas_estado = {}
        self.botones_combate = []

        self._crear_componentes()
        self._actualizar_estado()

    def _crear_componentes(self):
        marco = ttk.Frame(self.ventana, padding=12)
        marco.pack(fill="both", expand=True)

        ttk.Label(
            marco,
            text="MECHA-ARENA",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        datos = ttk.LabelFrame(marco, text="Mi Mecha", padding=8)
        datos.pack(fill="x", pady=(8, 6))

        for fila, nombre in enumerate(("Nombre", "Modelo", "Color")):
            ttk.Label(datos, text=f"{nombre}:").grid(
                row=fila,
                column=0,
                sticky="w",
                padx=(0, 8),
                pady=2
            )
            campo = ttk.Entry(datos, width=32)
            campo.grid(row=fila, column=1, sticky="ew", pady=2)
            self.campos[nombre] = campo

        datos.columnconfigure(1, weight=1)
        ttk.Button(
            datos,
            text="Crear / guardar Mecha",
            command=self._guardar_mecha
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        estado = ttk.LabelFrame(marco, text="Estado", padding=8)
        estado.pack(fill="x", pady=6)
        for fila, nombre in enumerate(("Jugador", "Rival")):
            etiqueta = ttk.Label(estado, text=f"{nombre}: Sin combate")
            etiqueta.grid(row=fila, column=0, sticky="w", pady=2)
            self.etiquetas_estado[nombre] = etiqueta

        acciones = ttk.Frame(marco)
        acciones.pack(fill="x", pady=6)
        self._agregar_boton(acciones, "Iniciar combate", self._iniciar_combate)
        self._agregar_boton(acciones, "Atacar", lambda: self._accion("ataque"))
        self._agregar_boton(acciones, "Defender", lambda: self._accion("defensa"))
        self._agregar_boton(acciones, "Especial", lambda: self._accion("especial"))
        self._agregar_boton(acciones, "Retirarse", self._retirarse)

        registro = ttk.LabelFrame(marco, text="Combate", padding=6)
        registro.pack(fill="both", expand=True, pady=(4, 0))
        self.registro = tk.Text(registro, height=8, state="disabled", wrap="word")
        self.registro.pack(fill="both", expand=True)

    def _agregar_boton(self, marco, texto, comando):
        boton = ttk.Button(marco, text=texto, command=comando)
        boton.pack(side="left", expand=True, fill="x", padx=2)
        if texto != "Iniciar combate":
            boton.state(["disabled"])
            self.botones_combate.append(boton)

    def _guardar_mecha(self):
        nombre, modelo, color = (
            self.campos[campo].get().strip()
            for campo in ("Nombre", "Modelo", "Color")
        )
        if not nombre or not modelo or not color:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa nombre, modelo y color del Mecha."
            )
            return

        if self.jugador is None:
            self.jugador = Mecha(nombre, modelo, color)
        else:
            self.jugador.nombre = nombre
            self.jugador.modelo = modelo
            self.jugador.color = color

        self._escribir_registro(f"Mecha {nombre} guardado.")
        self._actualizar_estado()

    def _iniciar_combate(self):
        if self.jugador is None:
            messagebox.showinfo("Mecha requerido", "Primero crea tu Mecha.")
            return

        self.jugador.vida = 100
        self.jugador.energia = 100
        self.jugador.defendiendo = False
        self.enemigo = Mecha("Titan CPU", "TX-900", "Rojo")
        self.enemigo.ataque = 18
        self.enemigo.defensa = 8
        self._escribir_registro(f"Comienza el combate: {self.jugador.nombre} vs Titan CPU.")
        self._habilitar_acciones(True)
        self._actualizar_estado()

    def _accion(self, accion):
        if self.jugador is None or self.enemigo is None:
            return

        try:
            if accion == "ataque":
                dano = self.sistema.atacar(self.jugador, self.enemigo)
                self._escribir_registro(f"Tu ataque causa {dano} de daño.")
            elif accion == "defensa":
                self.sistema.defender(self.jugador)
                self._escribir_registro("Tu Mecha se prepara para defender.")
            else:
                dano = self.sistema.ataque_especial(self.jugador, self.enemigo)
                self._escribir_registro(f"El ataque especial causa {dano} de daño.")
        except ValueError as error:
            messagebox.showwarning("Energía insuficiente", str(error))
            return

        if self._comprobar_fin():
            return

        accion_enemigo, dano = self.sistema.turno_enemigo(
            self.enemigo,
            self.jugador
        )
        if accion_enemigo == "defensa":
            self._escribir_registro("Titan CPU adopta una posición defensiva.")
        else:
            self._escribir_registro(f"Titan CPU causa {dano} de daño.")

        self._comprobar_fin()
        self._actualizar_estado()

    def _comprobar_fin(self):
        ganador = self.sistema.obtener_ganador(self.jugador, self.enemigo)
        if ganador is None:
            self._actualizar_estado()
            return False

        self._escribir_registro(f"Fin del combate. Ganador: {ganador.nombre}.")
        self.enemigo = None
        self._habilitar_acciones(False)
        self._actualizar_estado()
        return True

    def _retirarse(self):
        if self.enemigo is None:
            return
        self._escribir_registro("Te retiraste del combate.")
        self.enemigo = None
        self._habilitar_acciones(False)
        self._actualizar_estado()

    def _habilitar_acciones(self, habilitadas):
        estado = ["!disabled"] if habilitadas else ["disabled"]
        for boton in self.botones_combate:
            boton.state(estado)

    def _actualizar_estado(self):
        if self.jugador is None:
            self.etiquetas_estado["Jugador"].configure(text="Jugador: Sin crear")
        else:
            self.etiquetas_estado["Jugador"].configure(
                text=f"Jugador: {self.sistema.mostrar_estado(self.jugador)}"
            )

        if self.enemigo is None:
            texto = "Rival: Sin combate"
        else:
            texto = f"Rival: {self.sistema.mostrar_estado(self.enemigo)}"
        self.etiquetas_estado["Rival"].configure(text=texto)

    def _escribir_registro(self, mensaje):
        self.registro.configure(state="normal")
        self.registro.insert("end", mensaje + "\n")
        self.registro.see("end")
        self.registro.configure(state="disabled")


def iniciar_interfaz():
    ventana = tk.Tk()
    InterfazMechaArena(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()