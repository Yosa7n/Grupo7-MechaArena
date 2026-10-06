import random
import tkinter as tk
from tkinter import messagebox, ttk

from combate import SistemaCombate
from mecha import Mecha


class InterfazMechaArena:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mecha-Arena | Mazmorra")
        self.ventana.geometry("980x850")
        self.ventana.minsize(880, 790)
        self.ventana.configure(bg="#102d24")

        estilo = ttk.Style()
        estilo.configure("TFrame", background="#102d24")
        estilo.configure("TLabel", background="#102d24", foreground="#e4f5df")
        estilo.configure("TLabelframe", background="#102d24", foreground="#a7e887")
        estilo.configure("TLabelframe.Label", background="#102d24", foreground="#a7e887")

        self.sistema = SistemaCombate()
        self.jugador = None
        self.enemigo = None
        self.victorias = 0
        self.refacciones = []
        self.campos = {}
        self.etiquetas_estado = {}
        self.botones_combate = []
        self.boton_iniciar = None

        self._crear_componentes()
        self._actualizar_estado()

    def _crear_componentes(self):
        marco = ttk.Frame(self.ventana, padding=14)
        marco.pack(fill="both", expand=True)

        ttk.Label(
            marco,
            text="MAZMORRA MECHA-ARENA",
            font=("Segoe UI", 19, "bold"),
            foreground="#b5f27c"
        ).pack(anchor="w")
        self.etiqueta_piso = ttk.Label(marco, text="Piso 1 | Victorias: 0")
        self.etiqueta_piso.pack(anchor="w", pady=(2, 0))

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

        ttk.Label(datos, text="Patas iniciales:").grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=2
        )
        ttk.Label(datos, text="1 (crece al vencer rivales, máximo 8)").grid(
            row=3,
            column=1,
            sticky="w",
            pady=2
        )
        datos.columnconfigure(1, weight=1)
        ttk.Button(
            datos,
            text="Crear / guardar mi único robot",
            command=self._guardar_mecha
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        self.arena = tk.Canvas(
            marco,
            height=320,
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

        inventario = ttk.LabelFrame(marco, text="Refacciones guardadas", padding=6)
        inventario.pack(fill="x", pady=(2, 6))
        self.lista_refacciones = tk.Listbox(
            inventario,
            height=3,
            bg="#0b211a",
            fg="#dbf4d1",
            selectbackground="#528c43",
            relief="flat",
            highlightthickness=0
        )
        self.lista_refacciones.pack(side="left", fill="x", expand=True)
        self.boton_usar_refaccion = ttk.Button(
            inventario,
            text="Usar refacción",
            command=self._usar_refaccion
        )
        self.boton_usar_refaccion.pack(side="right", padx=(8, 0), fill="y")

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
        if texto == "Iniciar combate":
            self.boton_iniciar = boton
        else:
            boton.state(["disabled"])
            self.botones_combate.append(boton)

    def _guardar_mecha(self):
        valores = {
            nombre: self.campos[nombre].get().strip()
            for nombre in ("Nombre", "Modelo", "Color")
        }
        if not all(valores.values()):
            messagebox.showwarning(
                "Datos incompletos",
                "Completa nombre, modelo y color del Mecha."
            )
            return

        if self.jugador is None:
            self.jugador = Mecha(
                valores["Nombre"],
                valores["Modelo"],
                valores["Color"],
                1
            )
        else:
            self.jugador.nombre = valores["Nombre"]
            self.jugador.modelo = valores["Modelo"]
            self.jugador.color = valores["Color"]

        self._escribir_registro(f"Robot {self.jugador.nombre} guardado.")
        self._actualizar_estado()

    def _iniciar_combate(self):
        if self.jugador is None:
            messagebox.showinfo("Mecha requerido", "Primero crea tu robot.")
            return
        if self.enemigo is not None:
            return
        if self.jugador.vida <= 0:
            messagebox.showinfo(
                "Mazmorra terminada",
                "Tu robot ya no tiene vida. La mazmorra terminó."
            )
            return

        # La vida permanece entre pisos; la energía se recarga al entrar.
        self.jugador.energia = 100
        self.jugador.defendiendo = False
        self.enemigo = self._generar_rival()
        self._escribir_registro(
            f"Piso {self.victorias + 1}: {self.jugador.nombre} vs {self.enemigo.nombre}."
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
            1
        )
        dificultad = self.victorias
        rival.vida_maxima = 100 + dificultad * 10
        rival.vida = rival.vida_maxima
        rival.ataque = random.randint(15, 22) + min(dificultad, 8)
        rival.defensa = random.randint(6, 12) + min(dificultad // 2, 5)
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
                self._escribir_registro("Tu robot se prepara para defender.")
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
        if self.sistema.esta_destruido(self.enemigo):
            self._escribir_registro(f"Venciste a {self.enemigo.nombre}.")
            self.victorias += 1
            if self.jugador.patas < 8:
                self.jugador.patas += 1
                self._escribir_registro(
                    f"Tu robot creció y ahora tiene {self.jugador.patas} patas."
                )
            else:
                self._escribir_registro("Tu robot ya alcanzó el máximo de 8 patas.")

            porcentaje = random.choice((25, 50, 100))
            self.refacciones.append(porcentaje)
            self._escribir_registro(
                f"Encontraste una refacción de vida del {porcentaje}%."
            )
            self.enemigo = None
            self._habilitar_acciones(False)
            self._actualizar_estado()
            return True

        if self.sistema.esta_destruido(self.jugador):
            self._escribir_registro("Tu robot fue destruido. La mazmorra terminó.")
            self.enemigo = None
            self._habilitar_acciones(False)
            self._actualizar_estado()
            return True

        return False

    def _retirarse(self):
        if self.enemigo is None:
            return
        self._escribir_registro("Te retiraste del combate. Conservas la vida restante.")
        self.enemigo = None
        self._habilitar_acciones(False)
        self._actualizar_estado()

    def _habilitar_acciones(self, habilitadas):
        estado = ["!disabled"] if habilitadas else ["disabled"]
        for boton in self.botones_combate:
            boton.state(estado)
        if self.boton_iniciar is not None:
            self.boton_iniciar.state(["disabled"] if habilitadas else ["!disabled"])
        self._actualizar_refacciones()

    def _usar_refaccion(self):
        if self.jugador is None or self.enemigo is not None:
            return
        seleccion = self.lista_refacciones.curselection()
        if not seleccion:
            messagebox.showinfo("Inventario", "Selecciona una refacción guardada.")
            return

        porcentaje = self.refacciones.pop(seleccion[0])
        vida_maxima = self.jugador.vida_maxima
        vida_anterior = self.jugador.vida
        cantidad = int(vida_maxima * porcentaje / 100)
        self.jugador.vida = min(vida_maxima, vida_anterior + cantidad)
        recuperada = self.jugador.vida - vida_anterior
        self._escribir_registro(
            f"Usaste una refacción del {porcentaje}% y recuperaste {recuperada} de vida."
        )
        self._actualizar_estado()

    def _actualizar_refacciones(self):
        self.lista_refacciones.delete(0, "end")
        for numero, porcentaje in enumerate(self.refacciones, start=1):
            self.lista_refacciones.insert(
                "end",
                f"{numero}. Refacción de vida {porcentaje}%"
            )

        puede_usar = (
            bool(self.refacciones)
            and self.jugador is not None
            and self.jugador.vida < self.jugador.vida_maxima
            and self.enemigo is None
        )
        self.boton_usar_refaccion.state(
            ["!disabled"] if puede_usar else ["disabled"]
        )

    def _actualizar_estado(self):
        if self.jugador is None:
            self.etiquetas_estado["Jugador"].configure(text="Jugador: Sin crear")
        else:
            self.etiquetas_estado["Jugador"].configure(
                text=f"Jugador: {self.sistema.mostrar_estado(self.jugador)} | "
                f"Patas: {self.jugador.patas}"
            )

        if self.enemigo is None:
            texto = "Rival: Sin combate"
        else:
            texto = f"Rival: {self.sistema.mostrar_estado(self.enemigo)}"
        self.etiquetas_estado["Rival"].configure(text=texto)
        self.etiqueta_piso.configure(
            text=f"Piso {self.victorias + 1} | Victorias: {self.victorias}"
        )
        if self.jugador is not None and self.jugador.vida <= 0:
            self.boton_iniciar.state(["disabled"])
        self._actualizar_refacciones()
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
        alto = max(lienzo.winfo_height(), 320)
        centro = ancho / 2
        suelo = alto - 50

        lienzo.create_rectangle(0, suelo, ancho, alto, fill="#17472f", outline="")
        lienzo.create_line(0, suelo, ancho, suelo, fill="#8bcf70", width=2)
        lienzo.create_text(
            centro,
            24,
            text=f"PISO {self.victorias + 1}  |  ARENA",
            fill="#d4f4a5",
            font=("Segoe UI", 12, "bold")
        )

        if self.jugador is None:
            lienzo.create_text(
                centro,
                alto / 2,
                text="Crea tu robot para entrar a la mazmorra",
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

        self._dibujar_robot(lienzo, x_jugador, suelo, self.jugador, False)
        if self.enemigo is not None:
            self._dibujar_robot(lienzo, x_rival, suelo, self.enemigo, True)
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
                alto - 112,
                text="SIGUIENTE RIVAL",
                fill="#bce8a6",
                font=("Segoe UI", 10, "bold")
            )

    def _dibujar_robot(self, lienzo, x, suelo, mecha, mira_izquierda):
        color = self._color_robot(mecha.color)
        oscuro = "#283b36"
        direccion = -1 if mira_izquierda else 1
        cuerpo_y = suelo - 105
        patas = max(1, min(8, mecha.patas))
        nombre_patas = "pata" if patas == 1 else "patas"

        lienzo.create_text(
            x,
            52,
            text=f"{mecha.nombre} | {patas} {nombre_patas}",
            fill="#f0f7de",
            font=("Segoe UI", 10, "bold")
        )
        self._dibujar_barra_vida(lienzo, x, 67, mecha)

        parejas = patas // 2
        espacios = [
            -30 + indice * 60 / max(1, parejas - 1)
            for indice in range(parejas)
        ]
        for indice, desplazamiento in enumerate(espacios):
            cadera_x = x + desplazamiento
            for lado in (-1, 1):
                rodilla_x = cadera_x + lado * (26 + indice * 3)
                rodilla_y = cuerpo_y + 72
                pie_x = cadera_x + lado * (43 + indice * 4)
                puntos = (cadera_x, cuerpo_y + 48, rodilla_x, rodilla_y, pie_x, suelo - 5)
                lienzo.create_line(*puntos, fill=oscuro, width=10, capstyle=tk.ROUND)
                lienzo.create_line(*puntos, fill=color, width=5, capstyle=tk.ROUND)
                lienzo.create_oval(
                    rodilla_x - 5,
                    rodilla_y - 5,
                    rodilla_x + 5,
                    rodilla_y + 5,
                    fill="#d8e2d3",
                    outline=oscuro,
                    width=2
                )

        if patas % 2:
            cadera_x = x + direccion * 10
            rodilla_x = cadera_x + direccion * 16
            rodilla_y = cuerpo_y + 72
            pie_x = cadera_x + direccion * 25
            puntos = (cadera_x, cuerpo_y + 48, rodilla_x, rodilla_y, pie_x, suelo - 5)
            lienzo.create_line(*puntos, fill=oscuro, width=10, capstyle=tk.ROUND)
            lienzo.create_line(*puntos, fill=color, width=5, capstyle=tk.ROUND)

        lienzo.create_rectangle(
            x - 48,
            cuerpo_y + 24,
            x + 48,
            cuerpo_y + 66,
            fill=color,
            outline="#e1f1d4",
            width=2
        )
        lienzo.create_rectangle(
            x - 34,
            cuerpo_y + 32,
            x + 34,
            cuerpo_y + 43,
            fill="#29433a",
            outline="#91c978"
        )
        lienzo.create_oval(
            x - 22,
            cuerpo_y + 2,
            x + 22,
            cuerpo_y + 34,
            fill=oscuro,
            outline="#e1f1d4",
            width=2
        )
        ojo_x = x + 11 * direccion
        lienzo.create_rectangle(
            ojo_x - 9,
            cuerpo_y + 13,
            ojo_x + 9,
            cuerpo_y + 22,
            fill="#f5e86c",
            outline=""
        )
        lienzo.create_oval(
            x - 7,
            cuerpo_y + 49,
            x + 7,
            cuerpo_y + 61,
            fill="#b5f27c",
            outline=""
        )

    def _dibujar_barra_vida(self, lienzo, x, y, mecha):
        ancho = 118
        vida_maxima = max(1, mecha.vida_maxima)
        vida = max(0, min(vida_maxima, mecha.vida))
        lienzo.create_rectangle(
            x - ancho / 2,
            y,
            x + ancho / 2,
            y + 9,
            fill="#25372f",
            outline=""
        )
        lienzo.create_rectangle(
            x - ancho / 2,
            y,
            x - ancho / 2 + ancho * vida / vida_maxima,
            y + 9,
            fill="#9de36b" if vida / vida_maxima > 0.3 else "#e35b4f",
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
