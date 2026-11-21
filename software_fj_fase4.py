"""
Sistema de gestiÃ³n de clientes, servicios y reservas.

Proyecto desarrollado para la Fase 4 del curso ProgramaciÃ³n.
"""

import logging
from abc import ABC, abstractmethod


# ConfiguraciÃ³n del archivo donde se guardarÃ¡n los eventos
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# Excepciones bÃ¡sicas del sistema
class ErrorSoftwareFJ(Exception):
    """Representa un error controlado dentro del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un cliente no son vÃ¡lidos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un servicio no son vÃ¡lidos."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando hay un problema al realizar una reserva."""


class DuracionInvalidaError(ReservaInvalidaError):
    """Se usa cuando la duraciÃ³n ingresada no es vÃ¡lida."""


def convertir_duracion(valor):
    """Convierte la duraciÃ³n a nÃºmero y encadena errores de conversiÃ³n."""
    try:
        if isinstance(valor, bool):
            raise TypeError("Un valor booleano no es una duraciÃ³n vÃ¡lida.")
        duracion = float(valor)
        if duracion <= 0:
            raise DuracionInvalidaError(
                "La duraciÃ³n debe ser un nÃºmero mayor que cero."
            )
        return duracion
    except (ValueError, TypeError) as error_original:
        raise DuracionInvalidaError(
            "La duraciÃ³n debe ser un nÃºmero vÃ¡lido."
        ) from error_original


# Clase abstracta que representa las entidades del sistema
class Entidad(ABC):

    def __init__(self, identificacion):
        self._identificacion = identificacion

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def mostrar_informacion(self):
        """MÃ©todo que deben implementar las clases derivadas."""
        pass


# Clase Cliente: hereda de Entidad
class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):

        # Validar identificaciÃ³n
        if not isinstance(identificacion, str) or not identificacion.isdigit():
            raise ClienteInvalidoError(
                "La identificaciÃ³n debe contener solamente nÃºmeros."
            )

        # Validar nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError(
                "El nombre del cliente es obligatorio."
            )

        # Validar correo electrÃ³nico
        if not isinstance(correo, str) or "@" not in correo or "." not in correo.split("@")[-1]:
            raise ClienteInvalidoError(
                "El correo electrÃ³nico no es vÃ¡lido."
            )

        # Validar telÃ©fono
        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) != 10:
            raise ClienteInvalidoError(
                "El telÃ©fono debe tener exactamente 10 dÃ­gitos."
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
        """Muestra la informaciÃ³n del cliente."""

        print("\nDATOS DEL CLIENTE")
        print(f"IdentificaciÃ³n: {self.identificacion}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")
        print(f"TelÃ©fono: {self.telefono}")



# Clase encargada de administrar la lista de clientes
class GestorClientes:

    def __init__(self):
        # Lista interna donde se almacenan los clientes
        self.__clientes = []

    # MÃ©todo para registrar un cliente
    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("El objeto ingresado no es un cliente vÃ¡lido.")

        # Evitar clientes con identificaciÃ³n duplicada
        for cliente_existente in self.__clientes:
            if cliente_existente.identificacion == cliente.identificacion:
                raise ClienteInvalidoError("Ya existe un cliente con esa identificaciÃ³n.")

        self.__clientes.append(cliente)
        logging.info("Cliente registrado correctamente.")
        print("Cliente registrado exitosamente.")

    # MÃ©todo para buscar un cliente por identificaciÃ³n
    def buscar_cliente(self, identificacion):

        for cliente in self.__clientes:
            if cliente.identificacion == identificacion:
                return cliente

        return None

    # MÃ©todo para eliminar un cliente
    def eliminar_cliente(self, identificacion):

        cliente = self.buscar_cliente(identificacion)

        if cliente is None:
            raise ClienteInvalidoError("No se encontrÃ³ el cliente que desea eliminar.")

        self.__clientes.remove(cliente)
        logging.info("Cliente eliminado correctamente.")
        print("Cliente eliminado exitosamente.")

    # MÃ©todo para mostrar todos los clientes
    def listar_clientes(self):

        if not self.__clientes:
            print("No hay clientes registrados.")
            return

        print("\nLISTADO DE CLIENTES")

        for cliente in self.__clientes:
            cliente.mostrar_informacion()


# Clase abstracta que representa los servicios del sistema
class Servicio(ABC):

    def __init__(self, nombre, descripcion):

        # Validar el nombre del servicio
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        # Validar la descripciÃ³n
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ServicioInvalidoError(
                "La descripciÃ³n del servicio es obligatoria."
            )

        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()

    # Propiedad para consultar el nombre
    @property
    def nombre(self):
        return self._nombre

    # Propiedad para consultar la descripciÃ³n
    @property
    def descripcion(self):
        return self._descripcion

    # MÃ©todo abstracto para calcular el costo
    @abstractmethod
    def calcular_costo(self, duracion, impuestos=0, descuento=0):
        pass

    # MÃ©todo abstracto para mostrar la informaciÃ³n
    @abstractmethod
    def mostrar_descripcion(self):
        pass


# Clase ReservaEspacio: hereda de Servicio
class ReservaEspacio(Servicio):

    def __init__(self, nombre, descripcion, tarifa_por_hora):

        # Validar la tarifa por hora
        if not isinstance(tarifa_por_hora, (int, float)) or tarifa_por_hora <= 0:
            raise ServicioInvalidoError(
                "La tarifa por hora debe ser un nÃºmero mayor que cero."
            )

        super().__init__(nombre, descripcion)

        self._tarifa_por_hora = tarifa_por_hora

    # Calcular el costo de la reserva

    # Calcular el costo de la reserva
    def calcular_costo(self, duracion, impuestos=0, descuento=0):

        # Validar la duraciÃ³n
        if (not isinstance(duracion, (int, float))
                or isinstance(duracion, bool) or duracion <= 0):
            raise ServicioInvalidoError(
                "La duraciÃ³n debe ser un nÃºmero mayor que cero."
            )

        # Validar que impuestos y descuentos sean numÃ©ricos
        if (not isinstance(impuestos, (int, float))
                or isinstance(impuestos, bool)):
            raise ServicioInvalidoError(
                "Los impuestos deben ser un valor numÃ©rico."
            )

        if (not isinstance(descuento, (int, float))
                or isinstance(descuento, bool)):
            raise ServicioInvalidoError(
                "El descuento debe ser un valor numÃ©rico."
            )

        # Validar porcentajes
        if impuestos < 0:
            raise ServicioInvalidoError(
                "Los impuestos no pueden ser negativos."
            )

        if descuento < 0 or descuento > 100:
            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )

        # Calcular el costo total
        subtotal = self._tarifa_por_hora * duracion
        valor_impuestos = subtotal * impuestos / 100
        valor_descuento = subtotal * descuento / 100

        total = subtotal + valor_impuestos - valor_descuento

        return total


    # Mostrar la descripciÃ³n del servicio
    def mostrar_descripcion(self):

        print("\nSERVICIO DE RESERVA DE ESPACIO")
        print(f"Nombre: {self.nombre}")
        print(f"DescripciÃ³n: {self.descripcion}")
        print(f"Tarifa por hora: ${self._tarifa_por_hora:,.0f}")

# Clase AlquilerEquipo: hereda de Servicio
class AlquilerEquipo(Servicio):

    def __init__(self, nombre, descripcion, tarifa_por_dia):

        # Validar la tarifa diaria
        if not isinstance(tarifa_por_dia, (int, float)) or tarifa_por_dia <= 0:
            raise ServicioInvalidoError(
                "La tarifa diaria debe ser mayor que cero."
            )

        super().__init__(nombre, descripcion)

        self._tarifa_por_dia = tarifa_por_dia

    # Calcular el costo del alquiler

    # Calcular el costo del alquiler
    def calcular_costo(self, duracion, impuestos=0, descuento=0):

        # Validar la duraciÃ³n
        if (not isinstance(duracion, (int, float))
                or isinstance(duracion, bool) or duracion <= 0):
            raise ServicioInvalidoError(
                "La duraciÃ³n debe ser un nÃºmero mayor que cero."
            )

        # Validar que impuestos y descuentos sean numÃ©ricos
        if (not isinstance(impuestos, (int, float))
                or isinstance(impuestos, bool)):
            raise ServicioInvalidoError(
                "Los impuestos deben ser un valor numÃ©rico."
            )

        if (not isinstance(descuento, (int, float))
                or isinstance(descuento, bool)):
            raise ServicioInvalidoError(
                "El descuento debe ser un valor numÃ©rico."
            )

        # Validar porcentajes
        if impuestos < 0:
            raise ServicioInvalidoError(
                "Los impuestos no pueden ser negativos."
            )

        if descuento < 0 or descuento > 100:
            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )

        # Calcular el costo total
        subtotal = self._tarifa_por_dia * duracion
        valor_impuestos = subtotal * impuestos / 100
        valor_descuento = subtotal * descuento / 100

        total = subtotal + valor_impuestos - valor_descuento

        return total


    # Mostrar la descripciÃ³n del servicio
    def mostrar_descripcion(self):

        print("\nSERVICIO DE ALQUILER DE EQUIPOS")
        print(f"Nombre: {self.nombre}")
        print(f"DescripciÃ³n: {self.descripcion}")
        print(f"Tarifa por dÃ­a: ${self._tarifa_por_dia:,.0f}")



# Clase que representa los servicios de consultorÃ­a especializada
class ConsultoriaEspecializada(Servicio):

    def __init__(self, nombre, descripcion, tarifa_por_hora):
        super().__init__(nombre, descripcion)

        if not isinstance(tarifa_por_hora, (int, float)) or tarifa_por_hora <= 0:
            raise ServicioInvalidoError(
                "La tarifa por hora debe ser un nÃºmero positivo."
            )

        self._tarifa_por_hora = tarifa_por_hora


    def calcular_costo(self, duracion, impuestos=0, descuento=0):

        # Validar la duraciÃ³n
        if (not isinstance(duracion, (int, float))
                or isinstance(duracion, bool) or duracion <= 0):
            raise ServicioInvalidoError(
                "La duraciÃ³n de la consultorÃ­a debe ser un nÃºmero positivo."
            )

        # Validar que impuestos y descuentos sean numÃ©ricos
        if (not isinstance(impuestos, (int, float))
                or isinstance(impuestos, bool)):
            raise ServicioInvalidoError(
                "Los impuestos deben ser un valor numÃ©rico."
            )

        if (not isinstance(descuento, (int, float))
                or isinstance(descuento, bool)):
            raise ServicioInvalidoError(
                "El descuento debe ser un valor numÃ©rico."
            )

        # Validar porcentajes
        if impuestos < 0:
            raise ServicioInvalidoError(
                "Los impuestos no pueden ser negativos."
            )

        if descuento < 0 or descuento > 100:
            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )

        # Calcular el costo total
        subtotal = self._tarifa_por_hora * duracion
        valor_impuestos = subtotal * impuestos / 100
        valor_descuento = subtotal * descuento / 100

        total = subtotal + valor_impuestos - valor_descuento

        return total


    def mostrar_descripcion(self):
        print("\nSERVICIO DE CONSULTORÃA ESPECIALIZADA")
        print(f"Nombre: {self.nombre}")
        print(f"DescripciÃ³n: {self.descripcion}")
        print(f"Tarifa por hora: ${self._tarifa_por_hora:,.0f}")




# Clase que representa una reserva realizada por un cliente
class Reserva:

    def __init__(self, id_reserva, cliente, servicio, duracion):

        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ReservaInvalidaError("El cÃ³digo de la reserva es obligatorio.")

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Debe seleccionar un cliente vÃ¡lido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Debe seleccionar un servicio vÃ¡lido.")

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ReservaInvalidaError("La duraciÃ³n debe ser positiva.")

        self.__id_reserva = id_reserva.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__costo_total = servicio.calcular_costo(duracion)
        self.__estado = "Pendiente"

        logging.info("Reserva %s registrada correctamente.", self.__id_reserva)

    @property
    def id_reserva(self):
        return self.__id_reserva

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def mostrar_informacion(self):
        print("\nINFORMACIÃ“N DE LA RESERVA")
        print(f"CÃ³digo: {self.__id_reserva}")
        print(f"Cliente: {self.__cliente.nombre}")
        print(f"Servicio: {self.__servicio.nombre}")
        print(f"DuraciÃ³n: {self.__duracion}")
        print(f"Costo total: ${self.__costo_total:,.0f}")
        print(f"Estado: {self.__estado}")

    # Confirmar una reserva pendiente
    def confirmar_reserva(self):

        if self.__estado != "Pendiente":
            raise ReservaInvalidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = "Activa"

        logging.info("Reserva %s confirmada.", self.__id_reserva)
        print(f"Reserva {self.__id_reserva} confirmada exitosamente.")

    # Cancelar una reserva
    def cancelar_reserva(self):

        if self.__estado in ("Cancelada", "Procesada"):
            raise ReservaInvalidaError(
                "No se puede cancelar una reserva cancelada o procesada."
            )

        self.__estado = "Cancelada"

        logging.info("Reserva %s cancelada.", self.__id_reserva)
        print(f"Reserva {self.__id_reserva} cancelada exitosamente.")

    # Procesar una reserva confirmada
    def procesar_reserva(self):

        if self.__estado != "Activa":
            raise ReservaInvalidaError(
                "Solo se pueden procesar reservas activas."
            )

        self.__estado = "Procesada"

        logging.info("Reserva %s procesada.", self.__id_reserva)
        print(f"Reserva {self.__id_reserva} procesada exitosamente.")



# Clase encargada de administrar las reservas
class GestorReservas:

    def __init__(self):
        self.__reservas = []

    # Registrar una reserva
    def registrar_reserva(self, reserva):

        if not isinstance(reserva, Reserva):
            raise ReservaInvalidaError("Debe ingresar una reserva vÃ¡lida.")

        for existente in self.__reservas:
            if existente.id_reserva == reserva.id_reserva:
                raise ReservaInvalidaError("El cÃ³digo de reserva ya existe.")

        self.__reservas.append(reserva)

        logging.info("Reserva %s agregada al gestor.", reserva.id_reserva)
        print(f"Reserva {reserva.id_reserva} registrada en el sistema.")

    # Buscar una reserva por su cÃ³digo
    def buscar_reserva(self, id_reserva):

        for reserva in self.__reservas:
            if reserva.id_reserva == id_reserva:
                return reserva

        return None

    # Mostrar todas las reservas
    def listar_reservas(self):

        if not self.__reservas:
            print("\nNo hay reservas registradas.")
            return

        print("\nLISTADO DE RESERVAS")

        for reserva in self.__reservas:
            reserva.mostrar_informacion()

    # Confirmar una reserva
    def confirmar_reserva(self, id_reserva):

        reserva = self.buscar_reserva(id_reserva)

        if reserva is None:
            raise ReservaInvalidaError("No se encontrÃ³ la reserva.")

        reserva.confirmar_reserva()

    # Cancelar una reserva
    def cancelar_reserva(self, id_reserva):

        reserva = self.buscar_reserva(id_reserva)

        if reserva is None:
            raise ReservaInvalidaError("No se encontrÃ³ la reserva.")

        reserva.cancelar_reserva()

    # Procesar una reserva
    def procesar_reserva(self, id_reserva):

        reserva = self.buscar_reserva(id_reserva)

        if reserva is None:
            raise ReservaInvalidaError("No se encontrÃ³ la reserva.")

        reserva.procesar_reserva()



def demostrar_manejo_excepciones():
    """Demuestra try/except, try/except/else/finally y encadenamiento."""

    print("\nPRUEBAS DE MANEJO DE EXCEPCIONES")

    # Ejemplo de try/except/else/finally con una conversiÃ³n correcta.
    try:
        duracion = convertir_duracion("2")
    except DuracionInvalidaError as error:
        logging.exception("Error al convertir la duraciÃ³n.")
        print(f"Error controlado: {error}")
    else:
        print(f"DuraciÃ³n convertida correctamente: {duracion}")
        logging.info("ConversiÃ³n de duraciÃ³n realizada correctamente.")
    finally:
        print("FinalizÃ³ la prueba de conversiÃ³n.")
        logging.info("FinalizÃ³ la prueba try/except/else/finally.")

    # Ejemplo de encadenamiento de excepciones.
    try:
        convertir_duracion("tres horas")
    except DuracionInvalidaError as error:
        logging.exception("Se produjo un error de duraciÃ³n.")
        print(f"Error controlado: {error}")
        if error.__cause__ is not None:
            print(
                "Causa original del error: "
                f"{type(error.__cause__).__name__}"
            )

    # Ejemplo de try/except/finally ante datos de cliente invÃ¡lidos.
    try:
        Cliente("", " ", "correo-invalido", "123")
    except ClienteInvalidoError as error:
        logging.exception("Se capturÃ³ un error de validaciÃ³n de cliente.")
        print(f"ValidaciÃ³n controlada: {error}")
    finally:
        logging.info("FinalizÃ³ la prueba de validaciÃ³n del cliente.")


def main():
    print("=" * 50)
    print("SISTEMA DE GESTIÃ“N - SOFTWARE FJ")
    print("=" * 50)

    logging.info("El programa iniciÃ³ correctamente.")

    demostrar_manejo_excepciones()

    # Crear un cliente de prueba
    cliente_prueba = Cliente(
        "1108456723",
        "Carlos RamÃ­rez",
        "carlos@gmail.com",
        "3104567890"
    )

    cliente_prueba.mostrar_informacion()

    # Crear el administrador de clientes
    gestor_clientes = GestorClientes()

    # Registrar y listar el cliente
    gestor_clientes.registrar_cliente(cliente_prueba)
    gestor_clientes.listar_clientes()

    # Buscar el cliente
    cliente_encontrado = gestor_clientes.buscar_cliente("1108456723")

    if cliente_encontrado:
        print("\nCLIENTE ENCONTRADO")
        cliente_encontrado.mostrar_informacion()
    else:
        print("\nEl cliente no fue encontrado.")

    # Crear un servicio de reserva de espacio
    servicio_prueba = ReservaEspacio(
        "Sala de reuniones",
        "Espacio para reuniones empresariales",
        50000
    )

    servicio_prueba.mostrar_descripcion()

    costo = servicio_prueba.calcular_costo(2)
    print(f"Costo de la reserva: ${costo:,.0f}")
    costo_con_descuento = servicio_prueba.calcular_costo(
        2, impuestos=19, descuento=10
    )
    print(
        f"Costo con impuestos y descuento: "
        f"${costo_con_descuento:,.0f}"
    )

    # Crear un servicio de alquiler de equipos
    equipo_prueba = AlquilerEquipo(
        "Proyector",
        "Alquiler de proyector para eventos",
        80000
    )

    equipo_prueba.mostrar_descripcion()

    costo_equipo = equipo_prueba.calcular_costo(3)
    print(f"Costo del alquiler: ${costo_equipo:,.0f}")
    costo_equipo_descuento = equipo_prueba.calcular_costo(
        3, impuestos=19, descuento=10
    )
    print(
        f"Costo del alquiler con impuestos y descuento: "
        f"${costo_equipo_descuento:,.0f}"
    )

    # Crear un servicio de consultorÃ­a especializada
    consultoria_prueba = ConsultoriaEspecializada(
        "AsesorÃ­a administrativa",
        "ConsultorÃ­a para empresas y organizaciones",
        60000
    )

    consultoria_prueba.mostrar_descripcion()

    costo_consultoria = consultoria_prueba.calcular_costo(2)
    print(f"Costo de la consultorÃ­a: ${costo_consultoria:,.0f}")
    costo_consultoria_descuento = consultoria_prueba.calcular_costo(
        2, impuestos=19, descuento=10
    )
    print(
        f"Costo de la consultorÃ­a con impuestos y descuento: "
        f"${costo_consultoria_descuento:,.0f}"
    )

    # Crear el administrador de reservas
    gestor_reservas = GestorReservas()

    # Crear la primera reserva
    reserva_prueba = Reserva(
        "RES001",
        cliente_prueba,
        servicio_prueba,
        2
    )

    # Registrar la primera reserva
    gestor_reservas.registrar_reserva(reserva_prueba)

    # Mostrar las reservas registradas
    gestor_reservas.listar_reservas()

    # Confirmar la primera reserva
    gestor_reservas.confirmar_reserva("RES001")

    # Procesar la primera reserva
    gestor_reservas.procesar_reserva("RES001")

    # Crear una segunda reserva
    segunda_reserva = Reserva(
        "RES002",
        cliente_prueba,
        equipo_prueba,
        3
    )

    # Registrar y cancelar la segunda reserva
    gestor_reservas.registrar_reserva(segunda_reserva)
    gestor_reservas.cancelar_reserva("RES002")

    # Buscar una reserva por su cÃ³digo
    reserva_encontrada = gestor_reservas.buscar_reserva("RES001")

    if reserva_encontrada:
        print("\nRESERVA ENCONTRADA")
        reserva_encontrada.mostrar_informacion()

    # Mostrar el listado final de reservas
    gestor_reservas.listar_reservas()


    # Prueba de creaciÃ³n incorrecta de un servicio
    try:
        ReservaEspacio(
            "Sala invÃ¡lida",
            "Prueba de tarifa incorrecta",
            0
        )
    except ServicioInvalidoError as error:
        logging.exception("Prueba de servicio invÃ¡lido.")
        print(f"Servicio invÃ¡lido controlado: {error}")

    # Prueba de creaciÃ³n incorrecta de una reserva
    try:
        Reserva(
            "RES003",
            cliente_prueba,
            servicio_prueba,
            0
        )
    except ReservaInvalidaError as error:
        logging.exception("Prueba de reserva invÃ¡lida.")
        print(f"Reserva invÃ¡lida controlada: {error}")

    # Prueba de operaciÃ³n no permitida
    try:
        gestor_reservas.procesar_reserva("RES002")
    except ReservaInvalidaError as error:
        logging.exception("Prueba de operaciÃ³n no permitida.")
        print(f"OperaciÃ³n no permitida controlada: {error}")

    logging.info("El programa finalizÃ³ correctamente.")


if __name__ == "__main__":
    main()


# Proyecto colaborativo Fase 4 - Software FJ
