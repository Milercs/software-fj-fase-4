"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Proyecto correspondiente a la Fase 4 del curso Programación 213023.
El sistema administra clientes, servicios y reservas para Software FJ,
aplicando programación orientada a objetos y manejo de excepciones.
"""

from abc import ABC, abstractmethod
import logging


# ---------------------------------------------------------------
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ---------------------------------------------------------------

# Nombre del archivo donde se almacenarán los eventos y errores.
NOMBRE_ARCHIVO_LOG = "software_fj.log"

# Configuración general del sistema de registro.
logging.basicConfig(
    filename=NOMBRE_ARCHIVO_LOG,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

# Logger principal utilizado por las clases y funciones del sistema.
logger = logging.getLogger("software_fj")


def registrar_evento(mensaje):
    """
    Registra un evento informativo en el archivo de logs.

    Args:
        mensaje (str): Descripción del evento que se desea registrar.
    """
    logger.info(mensaje)


def registrar_advertencia(mensaje):
    """
    Registra una advertencia que no detiene la ejecución del sistema.

    Args:
        mensaje (str): Descripción de la advertencia presentada.
    """
    logger.warning(mensaje)


def registrar_error(mensaje, incluir_rastreo=False):
    """
    Registra un error ocurrido durante la ejecución del sistema.

    Args:
        mensaje (str): Descripción del error presentado.
        incluir_rastreo (bool): Indica si debe guardarse el rastreo
        completo de una excepción activa.
    """
    if incluir_rastreo:
        logger.exception(mensaje)
    else:
        logger.error(mensaje)


def main():
    """Inicia la ejecución del sistema."""
    registrar_evento("Inicio de la aplicación Software FJ.")

    try:
        print("=" * 60)
        print("SOFTWARE FJ")
        print("Sistema de gestión de clientes, servicios y reservas")
        print("=" * 60)
        print("Inicialización realizada correctamente.")
        print(f"Los eventos se registran en: {NOMBRE_ARCHIVO_LOG}")

    except Exception as error:
        registrar_error(
            f"Error inesperado durante la inicialización: {error}",
            incluir_rastreo=True
        )

        print("Ocurrió un error durante la inicialización del sistema.")

    else:
        registrar_evento(
            "La aplicación se inicializó correctamente."
        )

    finally:
        registrar_evento(
            "Finalizó el proceso inicial de la aplicación."
        )


if __name__ == "__main__":
    main()
