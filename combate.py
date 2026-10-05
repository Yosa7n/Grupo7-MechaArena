import random


class SistemaCombate:
    """
    Sistema de combate por turnos para Mecha-Arena.

    Funciones principales:
    - Ataque normal
    - Defensa
    - Ataque especial
    - Control de energía
    - Golpes críticos
    - Turno automático táctico del enemigo
    - Verificación de victoria y derrota
    """

    def calcular_dano(self, atacante, defensor):
        ataque = self._obtener_atributo(
            atacante,
            ["ataque"],
            10
        )

        defensa = self._obtener_atributo(
            defensor,
            ["defensa"],
            0
        )

        # Si el defensor activó defensa,
        # obtiene protección adicional.
        if getattr(defensor, "defendiendo", False):
            defensa += 10

        # Variación aleatoria del daño.
        variacion = random.randint(-3, 5)

        dano = ataque + variacion - defensa
        dano = max(1, dano)

        # 15 % de probabilidad de golpe crítico.
        es_critico = random.randint(1, 100) <= 15

        if es_critico:
            dano = int(dano * 1.5)

        return dano

    def atacar(self, atacante, defensor):
        """
        Ejecuta un ataque normal.
        """

        dano = self.calcular_dano(
            atacante,
            defensor
        )

        vida = self._obtener_vida(
            defensor
        )

        nueva_vida = max(
            0,
            vida - dano
        )

        self._establecer_vida(
            defensor,
            nueva_vida
        )

        # La defensa dura solamente un ataque.
        if hasattr(defensor, "defendiendo"):
            defensor.defendiendo = False

        # Recupera un poco de energía
        # después de atacar.
        self.recuperar_energia(
            atacante,
            5
        )

        return dano

    def defender(self, mecha):
        """
        Activa el modo defensa.
        """

        setattr(
            mecha,
            "defendiendo",
            True
        )

        self.recuperar_energia(
            mecha,
            8
        )

        return True

    def ataque_especial(
        self,
        atacante,
        defensor
    ):
        """
        Ataque más poderoso que consume energía.
        """

        costo_energia = 25

        energia = self._obtener_energia(
            atacante
        )

        if energia < costo_energia:
            raise ValueError(
                "Energía insuficiente "
                "para usar el ataque especial."
            )

        self._establecer_energia(
            atacante,
            energia - costo_energia
        )

        ataque = self._obtener_atributo(
            atacante,
            ["ataque"],
            10
        )

        defensa = self._obtener_atributo(
            defensor,
            ["defensa"],
            0
        )

        if getattr(
            defensor,
            "defendiendo",
            False
        ):
            defensa += 10

        dano = int(
            ataque * 1.5
        ) - defensa

        dano = max(
            1,
            dano
        )

        vida = self._obtener_vida(
            defensor
        )

        self._establecer_vida(
            defensor,
            max(
                0,
                vida - dano
            )
        )

        if hasattr(
            defensor,
            "defendiendo"
        ):
            defensor.defendiendo = False

        return dano

    def recuperar_energia(
        self,
        mecha,
        cantidad
    ):
        """
        Recupera energía sin superar el máximo.
        """

        energia_actual = (
            self._obtener_energia(
                mecha
            )
        )

        energia_maxima = (
            self._obtener_atributo(
                mecha,
                [
                    "energia_maxima",
                    "energia"
                ],
                100
            )
        )

        nueva_energia = min(
            energia_maxima,
            energia_actual + cantidad
        )

        self._establecer_energia(
            mecha,
            nueva_energia
        )

    def turno_enemigo(
        self,
        enemigo,
        jugador
    ):
        """
        Decide automáticamente la acción
        del mecha enemigo.

        La CPU ahora toma decisiones más tácticas:
        - Si tiene poca vida, aumenta su probabilidad de defenderse.
        - Si tiene energía suficiente, puede usar ataque especial.
        - En otros casos puede defenderse o atacar normalmente.
        """

        energia = self._obtener_energia(
            enemigo
        )

        vida = self._obtener_vida(
            enemigo
        )

        decision = random.randint(
            1,
            100
        )

        # Si la CPU tiene poca vida,
        # aumenta la posibilidad de defenderse.
        if (
            vida <= 30
            and decision <= 45
        ):
            self.defender(
                enemigo
            )

            return (
                "defensa",
                0
            )

        # Si tiene suficiente energía,
        # puede utilizar un ataque especial.
        if (
            energia >= 25
            and decision <= 35
        ):
            dano = self.ataque_especial(
                enemigo,
                jugador
            )

            return (
                "especial",
                dano
            )

        # Defensa normal.
        if decision <= 50:
            self.defender(
                enemigo
            )

            return (
                "defensa",
                0
            )

        # Ataque normal.
        dano = self.atacar(
            enemigo,
            jugador
        )

        return (
            "ataque",
            dano
        )

    def esta_destruido(
        self,
        mecha
    ):
        """
        Comprueba si el mecha perdió
        toda su vida.
        """

        return (
            self._obtener_vida(
                mecha
            )
            <= 0
        )

    def obtener_ganador(
        self,
        mecha_1,
        mecha_2
    ):
        """
        Devuelve el ganador cuando
        uno de los mechas queda sin vida.
        """

        if self.esta_destruido(
            mecha_1
        ):
            return mecha_2

        if self.esta_destruido(
            mecha_2
        ):
            return mecha_1

        return None

    def mostrar_estado(
        self,
        mecha
    ):
        """
        Devuelve el estado actual
        del mecha durante el combate.
        """

        nombre = self._obtener_atributo(
            mecha,
            ["nombre"],
            "MECHA"
        )

        vida = self._obtener_vida(
            mecha
        )

        energia = self._obtener_energia(
            mecha
        )

        return (
            f"{nombre} | "
            f"Vida: {vida} | "
            f"Energía: {energia}"
        )

    def _obtener_vida(
        self,
        mecha
    ):
        """
        Permite trabajar con
        vida_actual o vida.
        """

        return self._obtener_atributo(
            mecha,
            [
                "vida_actual",
                "vida"
            ],
            100
        )

    def _establecer_vida(
        self,
        mecha,
        valor
    ):
        if hasattr(
            mecha,
            "vida_actual"
        ):
            mecha.vida_actual = valor

        elif hasattr(
            mecha,
            "vida"
        ):
            mecha.vida = valor

        else:
            mecha.vida_actual = valor

    def _obtener_energia(
        self,
        mecha
    ):
        return self._obtener_atributo(
            mecha,
            [
                "energia_actual",
                "energia"
            ],
            100
        )

    def _establecer_energia(
        self,
        mecha,
        valor
    ):
        if hasattr(
            mecha,
            "energia_actual"
        ):
            mecha.energia_actual = valor

        elif hasattr(
            mecha,
            "energia"
        ):
            mecha.energia = valor

        else:
            mecha.energia_actual = valor

    @staticmethod
    def _obtener_atributo(
        objeto,
        nombres,
        defecto
    ):
        for nombre in nombres:

            if hasattr(
                objeto,
                nombre
            ):
                return getattr(
                    objeto,
                    nombre
                )

        return defecto