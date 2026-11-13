"""
Sistema de gestión de clientes, servicios y reservas.

Proyecto desarrollado para la Fase 4 del curso Programación.
"""

import logging
from abc import ABC, abstractmethod


# Configuración del archivo donde se guardarán los eventos
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# Excepciones básicas del sistema
class ErrorSoftwareFJ(Exception):
    """Representa un error controlado dentro del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un cliente no son válidos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un servicio no son válidos."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando hay un problema al realizar una reserva."""


# Clase abstracta que representa las entidades del sistema
class Entidad(ABC):

    def __init__(self, identificacion):
        self._identificacion = identificacion

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def mostrar_informacion(self):
        """Método que deben implementar las clases derivadas."""
        pass


# Clase Cliente: hereda de Entidad
class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):

        # Validar identificación
        if not isinstance(identificacion, str) or not identificacion.isdigit():
            raise ClienteInvalidoError(
                "La identificación debe contener solamente números."
            )

        # Validar nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError(
                "El nombre del cliente es obligatorio."
            )

        # Validar correo electrónico
        if not isinstance(correo, str) or "@" not in correo or "." not in correo.split("@")[-1]:
            raise ClienteInvalidoError(
                "El correo electrónico no es válido."
            )

        # Validar teléfono
        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) != 10:
            raise ClienteInvalidoError(
                "El teléfono debe tener exactamente 10 dígitos."
            )

        super().__init__(identificacion)

        # Encapsular los datos personales del cliente
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono

        logging.info(
            f"Cliente registrado correctamente: {self.__nombre}"
        )

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        """Muestra la información del cliente."""

        print("\nDATOS DEL CLIENTE")
        print(f"Identificación: {self.identificacion}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")
        print(f"Teléfono: {self.telefono}")


def main():
    print("=" * 50)
    print("SISTEMA DE GESTIÓN - SOFTWARE FJ")
    print("=" * 50)

    logging.info("El programa inició correctamente.")

    # Cliente utilizado para comprobar el funcionamiento de la clase
    cliente_prueba = Cliente(
        "1108456723",
        "Carlos Ramírez",
        "carlos@gmail.com",
        "3104567890"
    )

    cliente_prueba.mostrar_informacion()


if __name__ == "__main__":
    main()

# Proyecto colaborativo Fase 4 - Software FJ