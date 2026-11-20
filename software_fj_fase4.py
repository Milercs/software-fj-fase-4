"""
Sistema de gestión de clientes, servicios y reservas.

Proyecto desarrollado para la Fase 4 del curso Programación.
"""

import logging
from abc import ABC, abstractmethod


# Configuración del archivo donde se guardan los eventos y errores
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# Excepciones utilizadas en el programa
class ErrorSoftwareFJ(Exception):
    """Error general del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un cliente son incorrectos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un servicio son incorrectos."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando hay un problema con una reserva."""


class DuracionInvalidaError(ReservaInvalidaError):
    """Se usa cuando la duración ingresada no es válida."""


# Clase general para las entidades del sistema
class Entidad(ABC):

    def __init__(self, identificacion):
        self._identificacion = identificacion

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass


# Clase que representa un cliente
class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):

        if not isinstance(identificacion, str) or not identificacion.isdigit():
            raise ClienteInvalidoError(
                "La identificación debe contener solamente números."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError(
                "El nombre del cliente es obligatorio."
            )

        if (
            not isinstance(correo, str)
            or "@" not in correo
            or "." not in correo.split("@")[-1]
        ):
            raise ClienteInvalidoError(
                "El correo electrónico no es válido."
            )

        if (
            not isinstance(telefono, str)
            or not telefono.isdigit()
            or len(telefono) != 10
        ):
            raise ClienteInvalidoError(
                "El teléfono debe tener exactamente 10 dígitos."
            )

        super().__init__(identificacion)

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono

        logging.info(
            "Cliente registrado correctamente: %s",
            self.__nombre
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
        print("\nDATOS DEL CLIENTE")
        print(f"Identificación: {self.identificacion}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")
        print(f"Teléfono: {self.telefono}")


# Clase general para los servicios
class Servicio(ABC):

    def __init__(self, nombre, descripcion):

        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ServicioInvalidoError(
                "La descripción del servicio es obligatoria."
            )

        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()

    @property
    def nombre(self):
        return self._nombre

    @property
    def descripcion(self):
        return self._descripcion

    @abstractmethod
    def calcular_costo(self, duracion, impuestos=0, descuento=0):
        pass

    @abstractmethod
    def mostrar_descripcion(self):
        pass


# Servicio para reservar espacios
class ReservaEspacio(Servicio):

    def __init__(self, nombre, descripcion, tarifa_por_hora):

        if (
            not isinstance(tarifa_por_hora, (int, float))
            or tarifa_por_hora <= 0
        ):
            raise ServicioInvalidoError(
                "La tarifa por hora debe ser mayor que cero."
            )

        super().__init__(nombre, descripcion)
        self._tarifa_por_hora = tarifa_por_hora

    def calcular_costo(self, duracion, impuestos=0, descuento=0):

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ServicioInvalidoError(
                "La duración debe ser mayor que cero."
            )

        if impuestos < 0 or descuento < 0:
            raise ServicioInvalidoError(
                "Los impuestos y descuentos no pueden ser negativos."
            )

        subtotal = self._tarifa_por_hora * duracion
        total = subtotal + (subtotal * impuestos / 100)
        total = total - (subtotal * descuento / 100)

        return total

    def mostrar_descripcion(self):
        print("\nSERVICIO DE RESERVA DE ESPACIO")
        print(f"Nombre: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Tarifa por hora: ${self._tarifa_por_hora:,.0f}")


# Servicio para alquilar equipos
class AlquilerEquipo(Servicio):

    def __init__(self, nombre, descripcion, tarifa_por_dia):

        if (
            not isinstance(tarifa_por_dia, (int, float))
            or tarifa_por_dia <= 0
        ):
            raise ServicioInvalidoError(
                "La tarifa diaria debe ser mayor que cero."
            )

        super().__init__(nombre, descripcion)
        self._tarifa_por_dia = tarifa_por_dia

    def calcular_costo(self, duracion, impuestos=0, descuento=0):

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ServicioInvalidoError(
                "La duración debe ser mayor que cero."
            )

        if impuestos < 0 or descuento < 0:
            raise ServicioInvalidoError(
                "Los impuestos y descuentos no pueden ser negativos."
            )

        subtotal = self._tarifa_por_dia * duracion
        total = subtotal + (subtotal * impuestos / 100)
        total = total - (subtotal * descuento / 100)

        return total

    def mostrar_descripcion(self):
        print("\nSERVICIO DE ALQUILER DE EQUIPOS")
        print(f"Nombre: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Tarifa por día: ${self._tarifa_por_dia:,.0f}")


# Servicio de consultoría especializada
class ConsultoriaEspecializada(Servicio):

    def __init__(self, nombre, descripcion, tarifa_por_hora):

        if (
            not isinstance(tarifa_por_hora, (int, float))
            or tarifa_por_hora <= 0
        ):
            raise ServicioInvalidoError(
                "La tarifa por hora debe ser mayor que cero."
            )

        super().__init__(nombre, descripcion)
        self._tarifa_por_hora = tarifa_por_hora

    def calcular_costo(self, duracion, impuestos=0, descuento=0):

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ServicioInvalidoError(
                "La duración de la consultoría debe ser positiva."
            )

        if impuestos < 0 or descuento < 0:
            raise ServicioInvalidoError(
                "Los impuestos y descuentos no pueden ser negativos."
            )

        subtotal = self._tarifa_por_hora * duracion
        total = subtotal + (subtotal * impuestos / 100)
        total = total - (subtotal * descuento / 100)

        return total

    def mostrar_descripcion(self):
        print("\nSERVICIO DE CONSULTORÍA ESPECIALIZADA")
        print(f"Nombre: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Tarifa por hora: ${self._tarifa_por_hora:,.0f}")


# Clase que representa una reserva
class Reserva:

    def __init__(self, id_reserva, cliente, servicio, duracion):

        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ReservaInvalidaError(
                "El código de la reserva es obligatorio."
            )

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Debe seleccionar un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Debe seleccionar un servicio válido."
            )

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError(
                "La duración debe ser positiva."
            )

        self.__id_reserva = id_reserva.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__costo_total = servicio.calcular_costo(duracion)
        self.__estado = "Pendiente"

        logging.info(
            "Reserva %s registrada correctamente.",
            self.__id_reserva
        )

    @property
    def estado(self):
        return self.__estado

    def confirmar_reserva(self):
        """Confirma una reserva pendiente."""

        if self.__estado == "Cancelada":
            raise ReservaInvalidaError(
                "No se puede confirmar una reserva cancelada."
            )

        if self.__estado == "Confirmada":
            raise ReservaInvalidaError(
                "La reserva ya se encuentra confirmada."
            )

        if self.__estado == "Procesada":
            raise ReservaInvalidaError(
                "No se puede confirmar una reserva procesada."
            )

        self.__estado = "Confirmada"

        logging.info(
            "La reserva %s fue confirmada.",
            self.__id_reserva
        )

        print(f"La reserva {self.__id_reserva} fue confirmada.")

    def procesar_reserva(self):
        """Procesa una reserva que ya fue confirmada."""

        if self.__estado != "Confirmada":
            raise ReservaInvalidaError(
                "Solo se puede procesar una reserva confirmada."
            )

        self.__estado = "Procesada"

        logging.info(
            "La reserva %s fue procesada.",
            self.__id_reserva
        )

        print(f"La reserva {self.__id_reserva} fue procesada.")

    def cancelar_reserva(self):
        """Cancela una reserva que todavía no está procesada."""

        if self.__estado == "Cancelada":
            raise ReservaInvalidaError(
                "La reserva ya se encuentra cancelada."
            )

        if self.__estado == "Procesada":
            raise ReservaInvalidaError(
                "No se puede cancelar una reserva procesada."
            )

        self.__estado = "Cancelada"

        logging.info(
            "La reserva %s fue cancelada.",
            self.__id_reserva
        )

        print(f"La reserva {self.__id_reserva} fue cancelada.")

    def mostrar_informacion(self):
        print("\nINFORMACIÓN DE LA RESERVA")
        print(f"Código: {self.__id_reserva}")
        print(f"Cliente: {self.__cliente.nombre}")
        print(f"Servicio: {self.__servicio.nombre}")
        print(f"Duración: {self.__duracion}")
        print(f"Costo total: ${self.__costo_total:,.0f}")
        print(f"Estado: {self.__estado}")


# Esta función convierte la duración y conserva el error original
def convertir_duracion(valor):
    """Convierte la duración ingresada en un número."""

    try:
        duracion = float(valor)

    except (ValueError, TypeError) as error_original:
        raise DuracionInvalidaError(
            "La duración debe ser un número."
        ) from error_original

    if duracion <= 0:
        raise DuracionInvalidaError(
            "La duración debe ser mayor que cero."
        )

    return duracion


def main():

    print("=" * 50)
    print("SISTEMA DE GESTIÓN - SOFTWARE FJ")
    print("=" * 50)

    logging.info("El programa inició correctamente.")

    # Cliente válido para las pruebas
    cliente_prueba = Cliente(
        "1108456723",
        "Carlos Ramírez",
        "carlos@gmail.com",
        "3104567890"
    )

    cliente_prueba.mostrar_informacion()

    # Servicio de reserva de espacio
    servicio_prueba = ReservaEspacio(
        "Sala de reuniones",
        "Espacio para reuniones empresariales",
        50000
    )

    servicio_prueba.mostrar_descripcion()

    costo = servicio_prueba.calcular_costo(2)
    print(f"Costo de la reserva: ${costo:,.0f}")

    # Servicio de alquiler de equipos
    equipo_prueba = AlquilerEquipo(
        "Proyector",
        "Alquiler de proyector para eventos",
        80000
    )

    equipo_prueba.mostrar_descripcion()

    costo_equipo = equipo_prueba.calcular_costo(3)
    print(f"Costo del alquiler: ${costo_equipo:,.0f}")

    # Servicio de consultoría
    consultoria_prueba = ConsultoriaEspecializada(
        "Asesoría administrativa",
        "Consultoría para empresas y organizaciones",
        60000
    )

    consultoria_prueba.mostrar_descripcion()

    costo_consultoria = consultoria_prueba.calcular_costo(2)
    print(f"Costo de la consultoría: ${costo_consultoria:,.0f}")

    # Primera reserva: se confirma y después se cancela
    reserva_prueba = Reserva(
        "RES001",
        cliente_prueba,
        servicio_prueba,
        2
    )

    reserva_prueba.mostrar_informacion()
    reserva_prueba.confirmar_reserva()
    reserva_prueba.mostrar_informacion()
    reserva_prueba.cancelar_reserva()
    reserva_prueba.mostrar_informacion()

    # Segunda reserva: se confirma y después se procesa
    reserva_procesada = Reserva(
        "RES002",
        cliente_prueba,
        servicio_prueba,
        3
    )

    reserva_procesada.mostrar_informacion()
    reserva_procesada.confirmar_reserva()
    reserva_procesada.procesar_reserva()
    reserva_procesada.mostrar_informacion()

    # Prueba para comprobar el manejo de excepciones
    print("\nPRUEBA DE MANEJO DE EXCEPCIONES")

    try:
        cliente_invalido = Cliente(
            "1234567890",
            "Laura Gómez",
            "correo_incorrecto",
            "3101234567"
        )

    except ClienteInvalidoError as error:
        print(f"Error controlado: {error}")

        logging.error(
            "No se pudo registrar el cliente: %s",
            error
        )

    else:
        print("El cliente fue registrado correctamente.")
        cliente_invalido.mostrar_informacion()

    finally:
        print("La prueba del cliente terminó.")

    # Prueba para comprobar el encadenamiento de excepciones
    print("\nPRUEBA DE ENCADENAMIENTO DE EXCEPCIONES")

    try:
        duracion_prueba = convertir_duracion("tres horas")

    except DuracionInvalidaError as error:
        print(f"Error controlado: {error}")

        logging.error(
            "No se pudo convertir la duración: %s",
            error
        )

    else:
        print(f"Duración válida: {duracion_prueba}")

    finally:
        print("La prueba de duración terminó.")

    logging.info("El programa terminó correctamente.")


if __name__ == "__main__":
    main()
