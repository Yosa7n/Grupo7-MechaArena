import random


class SistemaCombate:
    """
    Sistema de combate por turnos para Mecha-Arena.

    Este módulo se encarga de:
    - Ataques normales
    - Defensa
    - Ataques especiales
    - Cálculo de daño
    - Control básico de energía
    """

    def calcular_dano(self, atacante, defensor):
        """
        Calcula el daño de un ataque normal.
        """

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

        variacion = random.randint(-3, 5)

        dano = ataque + variacion - defensa

        return max(1, dano)

    def atacar(self, atacante, defensor):
        """
        Ejecuta un ataque normal.
        """

        dano = self.calcular_dano(
            atacante,
            defensor
        )

        vida = self._obtener_vida(defensor)

        nueva_vida = max(
            0,
            vida - dano
        )

        self._establecer_vida(
            defensor,
            nueva_vida
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

        return True

    def ataque_especial(
        self,
        atacante,
        defensor
    ):
        """
        Ataque especial que consume energía.
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

        return dano

    def esta_destruido(self, mecha):
        """
        Comprueba si el mecha perdió toda su vida.
        """

        return self._obtener_vida(
            mecha
        ) <= 0

    def _obtener_vida(self, mecha):
        """
        Permite trabajar con vida_actual o vida.
        """

        return self._obtener_atributo(
            mecha,
            ["vida_actual", "vida"],
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

    def _obtener_energia(self, mecha):
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