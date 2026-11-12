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


# Clase para guardar la información de los clientes
class Cliente:

    def __init__(self, identificacion, nombre, correo, telefono):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        logging.info(
            f"Se creó el cliente {self.nombre} "
            f"con identificación {self.identificacion}."
        )

    def mostrar_informacion(self):
        """Muestra los datos principales del cliente."""
        print("\nDatos del cliente")
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
