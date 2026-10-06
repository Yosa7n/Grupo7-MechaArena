import random
import tkinter as tk
from tkinter import messagebox, ttk

from combate import SistemaCombate
from mecha import Mecha


class InterfazMechaArena:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mecha-Arena")
        self.ventana.geometry("920x760")
        self.ventana.minsize(820, 700)
        self.ventana.configure(bg="#102d24")

        estilo = ttk.Style()
        estilo.configure("TFrame", background="#102d24")
        estilo.configure("TLabel", background="#102d24", foreground="#e4f5df")
        estilo.configure("TLabelframe", background="#102d24", foreground="#a7e887")
        estilo.configure("TLabelframe.Label", background="#102d24", foreground="#a7e887")

        self.sistema = SistemaCombate()
        self.jugador = None
        self.enemigo = None
        self.campos = {}
        self.patas_jugador = tk.StringVar(value="4")
        self.etiquetas_estado = {}
        self.botones_combate = []

        self._crear_componentes()
        self._actualizar_estado()

    def _crear_componentes(self):
        marco = ttk.Frame(self.ventana, padding=14)
        marco.pack(fill="both", expand=True)

        ttk.Label(
            marco,
            text="MECHA-ARENA",
            font=("Segoe UI", 19, "bold"),
            foreground="#b5f27c"
        ).pack(anchor="w")

        datos = ttk.LabelFrame(marco, text="Tu robot", padding=8)
        datos.pack(fill="x", pady=(8, 8))

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

        ttk.Label(datos, text="Patas:").grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=2
        )
        ttk.Combobox(
            datos,
            textvariable=self.patas_jugador,
            values=("4", "6", "8"),
            state="readonly",
            width=8
        ).grid(row=3, column=1, sticky="w", pady=2)

        datos.columnconfigure(1, weight=1)
        ttk.Button(
            datos,
            text="Crear / guardar mi único robot",
            command=self._guardar_mecha
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        self.arena = tk.Canvas(
            marco,
            height=285,
            bg="#1b593b",
            highlightthickness=1,
            highlightbackground="#81c76b"
        )
        self.arena.pack(fill="x", pady=(0, 8))

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
        self.registro = tk.Text(
            registro,
            height=5,
            state="disabled",
            wrap="word",
            bg="#0b211a",
            fg="#dbf4d1",
            insertbackground="#dbf4d1",
            relief="flat"
        )
        self.registro.pack(fill="both", expand=True)
        self._dibujar_arena()

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

        patas = int(self.patas_jugador.get())
        if self.jugador is None:
            self.jugador = Mecha(nombre, modelo, color, patas)
        else:
            self.jugador.nombre = nombre
            self.jugador.modelo = modelo
            self.jugador.color = color
            self.jugador.patas = patas

        self._escribir_registro(f"Mecha {nombre} guardado.")
        self._actualizar_estado()

    def _iniciar_combate(self):
        if self.jugador is None:
            messagebox.showinfo("Mecha requerido", "Primero crea tu Mecha.")
            return

        self.jugador.vida = 100
        self.jugador.energia = 100
        self.jugador.defendiendo = False
        self.enemigo = self._generar_rival()
        self._escribir_registro(
            f"Comienza el combate: {self.jugador.nombre} vs {self.enemigo.nombre}."
        )
        self._habilitar_acciones(True)
        self._actualizar_estado()

    def _generar_rival(self):
        nombres = ("Voltaris", "Chatarra X", "Centinela", "Rayo Negro", "Ironclaw")
        modelos = ("RX-4", "MK-8", "VTX-2", "A-16", "KR-9")
        colores = ("#e35b4f", "#e7bd45", "#5aa8dd", "#d66bc2", "#e8e7dc")
        rival = Mecha(
            random.choice(nombres),
            random.choice(modelos),
            random.choice(colores),
            random.choice((4, 6, 8))
        )
        rival.ataque = random.randint(15, 22)
        rival.defensa = random.randint(6, 12)
        return rival

    def _accion(self, accion):
        if self.jugador is None or self.enemigo is None:
            return

        atacantes = []
        try:
            if accion == "ataque":
                dano = self.sistema.atacar(self.jugador, self.enemigo)
                self._escribir_registro(f"Tu ataque causa {dano} de daño.")
                atacantes.append("jugador")
            elif accion == "defensa":
                self.sistema.defender(self.jugador)
                self._escribir_registro("Tu Mecha se prepara para defender.")
            else:
                dano = self.sistema.ataque_especial(self.jugador, self.enemigo)
                self._escribir_registro(f"El ataque especial causa {dano} de daño.")
                atacantes.append("jugador")
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
            self._escribir_registro(f"{self.enemigo.nombre} adopta una posición defensiva.")
        else:
            self._escribir_registro(f"{self.enemigo.nombre} causa {dano} de daño.")
            atacantes.append("rival")

        self._comprobar_fin()
        self._actualizar_estado()
        if self.enemigo is not None:
            self._reproducir_animacion(atacantes)

    def _reproducir_animacion(self, atacantes, indice=0):
        if indice >= len(atacantes):
            self._dibujar_arena()
            return

        self._dibujar_arena(atacantes[indice])
        self.ventana.after(
            180,
            lambda: self._reproducir_animacion(atacantes, indice + 1)
        )

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
        self._dibujar_arena()

    def _color_robot(self, color):
        colores = {
            "rojo": "#e35b4f",
            "azul": "#5aa8dd",
            "verde": "#b5f27c",
            "amarillo": "#e7bd45",
            "negro": "#303943",
            "blanco": "#e8e7dc",
            "naranja": "#ed8b42",
            "morado": "#b279d4",
            "rosa": "#d66bc2"
        }
        color = colores.get(color.strip().lower(), color.strip())
        try:
            self.ventana.winfo_rgb(color)
            return color
        except tk.TclError:
            return "#d8e2d3"

    def _dibujar_arena(self, atacante=None):
        lienzo = self.arena
        lienzo.delete("all")
        ancho = max(lienzo.winfo_width(), 820)
        alto = max(lienzo.winfo_height(), 285)
        centro = ancho / 2

        lienzo.create_rectangle(0, alto - 52, ancho, alto, fill="#17472f", outline="")
        lienzo.create_line(0, alto - 51, ancho, alto - 51, fill="#8bcf70", width=2)
        lienzo.create_line(centro, 22, centro, alto - 52, fill="#3b8050", dash=(5, 7))
        lienzo.create_text(
            centro,
            25,
            text="ARENA MECHA",
            fill="#d4f4a5",
            font=("Segoe UI", 12, "bold")
        )

        if self.jugador is None:
            lienzo.create_text(
                centro,
                alto / 2,
                text="Crea tu robot para entrar a la arena",
                fill="#e4f5df",
                font=("Segoe UI", 15, "bold")
            )
            return

        x_jugador = centro * 0.52
        x_rival = centro * 1.48
        if atacante == "jugador":
            x_jugador += 20
        elif atacante == "rival":
            x_rival -= 20

        self._dibujar_robot(lienzo, x_jugador, alto - 55, self.jugador, False)
        if self.enemigo is not None:
            self._dibujar_robot(lienzo, x_rival, alto - 55, self.enemigo, True)
            if atacante is not None:
                lienzo.create_text(
                    centro,
                    alto * 0.54,
                    text="IMPACTO",
                    fill="#f5e86c",
                    font=("Segoe UI", 13, "bold")
                )
        else:
            lienzo.create_text(
                x_rival,
                alto - 118,
                text="RIVAL ALEATORIO",
                fill="#bce8a6",
                font=("Segoe UI", 10, "bold")
            )

    def _dibujar_robot(self, lienzo, x, suelo, mecha, mira_izquierda):
        color = self._color_robot(mecha.color)
        oscuro = "#283b36"
        direccion = -1 if mira_izquierda else 1
        cuerpo_y = suelo - 112
        nombre = getattr(mecha, "nombre", "Mecha")
        patas = getattr(mecha, "patas", 4)

        lienzo.create_text(
            x,
            suelo - 255,
            text=f"{nombre}  |  {patas} patas",
            fill="#f0f7de",
            font=("Segoe UI", 10, "bold")
        )
        self._dibujar_barra_vida(lienzo, x, suelo - 235, mecha)

        # Las patas se reparten simétricamente y siempre en número par.
        if patas == 4:
            posiciones = (-28, -9, 9, 28)
        elif patas == 6:
            posiciones = (-42, -25, -8, 8, 25, 42)
        else:
            posiciones = (-52, -37, -22, -7, 7, 22, 37, 52)

        for desplazamiento in posiciones:
            cadera_x = x + desplazamiento
            rodilla_x = cadera_x + direccion * (8 if desplazamiento * direccion < 0 else -8)
            rodilla_y = suelo - 35
            pie_x = cadera_x + direccion * 5
            lienzo.create_line(
                cadera_x,
                suelo - 76,
                rodilla_x,
                rodilla_y,
                pie_x,
                suelo - 7,
                fill=oscuro,
                width=9,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND
            )
            lienzo.create_line(
                cadera_x,
                suelo - 76,
                rodilla_x,
                rodilla_y,
                pie_x,
                suelo - 7,
                fill=color,
                width=4,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND
            )
            lienzo.create_oval(
                rodilla_x - 5,
                rodilla_y - 5,
                rodilla_x + 5,
                rodilla_y + 5,
                fill="#d8e2d3",
                outline=oscuro,
                width=2
            )
            lienzo.create_line(
                pie_x - 8,
                suelo - 5,
                pie_x + 8,
                suelo - 5,
                fill="#d8e2d3",
                width=5,
                capstyle=tk.ROUND
            )

        lienzo.create_line(
            x - 41,
            cuerpo_y + 32,
            x - 66 * direccion,
            cuerpo_y + 51,
            x - 72 * direccion,
            cuerpo_y + 75,
            fill=oscuro,
            width=13,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND
        )
        lienzo.create_line(
            x + 41,
            cuerpo_y + 32,
            x + 66 * direccion,
            cuerpo_y + 51,
            x + 72 * direccion,
            cuerpo_y + 75,
            fill=oscuro,
            width=13,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND
        )
        lienzo.create_rectangle(
            x - 44,
            cuerpo_y,
            x + 44,
            cuerpo_y + 67,
            fill=color,
            outline="#e1f1d4",
            width=2
        )
        lienzo.create_rectangle(
            x - 32,
            cuerpo_y + 12,
            x + 32,
            cuerpo_y + 27,
            fill="#29433a",
            outline="#91c978"
        )
        lienzo.create_oval(
            x - 27,
            cuerpo_y - 37,
            x + 27,
            cuerpo_y + 1,
            fill=oscuro,
            outline="#e1f1d4",
            width=2
        )
        ojo_x = x + 11 * direccion
        lienzo.create_rectangle(
            ojo_x - 9,
            cuerpo_y - 24,
            ojo_x + 9,
            cuerpo_y - 14,
            fill="#f5e86c",
            outline=""
        )
        lienzo.create_oval(
            x - 8,
            cuerpo_y + 35,
            x + 8,
            cuerpo_y + 51,
            fill="#b5f27c",
            outline=""
        )

    def _dibujar_barra_vida(self, lienzo, x, y, mecha):
        ancho = 118
        vida = max(0, min(100, getattr(mecha, "vida", 100)))
        lienzo.create_rectangle(x - ancho / 2, y, x + ancho / 2, y + 9, fill="#25372f", outline="")
        lienzo.create_rectangle(
            x - ancho / 2,
            y,
            x - ancho / 2 + ancho * vida / 100,
            y + 9,
            fill="#9de36b" if vida > 30 else "#e35b4f",
            outline=""
        )

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