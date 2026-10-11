"""Dominio del módulo Solicitudes de recojo (EcoRecicla AQP) - HU-01.

Esqueleto generado con IA a partir de docs/design/clases.puml (Prompt IA 2)
y revisado por el equipo. Los nombres de operaciones usan snake_case
(equivalencia con camelCase del diagrama documentada en round-trip.md, C5).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class EstadoSolicitud(Enum):
    PENDIENTE = "PENDIENTE"
    ASIGNADA = "ASIGNADA"
    RECOGIDA = "RECOGIDA"
    PESADA = "PESADA"
    PUNTOS_ACREDITADOS = "PUNTOS_ACREDITADOS"
    RECHAZADA = "RECHAZADA"


class ErrorValidacion(Exception):
    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class ErrorGeocodificacion(Exception):
    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


@dataclass
class Coordenadas:
    latitud: float
    longitud: float


@dataclass
class Direccion:
    texto: str
    coordenadas: Coordenadas | None = None  # 0..1 en el diagrama

    def esta_geocodificada(self) -> bool:
        return self.coordenadas is not None


@dataclass
class DetalleResiduo:
    tipo: str
    descripcion: str
    peso_kg: float

    def es_valido(self) -> bool:
        return bool(self.tipo) and self.peso_kg > 0


@dataclass
class Solicitud:
    vecino_id: str
    direccion: Direccion
    detalles: list[DetalleResiduo] = field(default_factory=list)  # 1..*
    # None = recién creada, aún sin estado (el diagrama no define estado inicial)
    estado: EstadoSolicitud | None = None
    motivo_rechazo: str | None = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid4()))
    # Atributos propuestos para cerrar C2 (ciclo de vida completo):
    reciclador_id: str | None = None
    peso_real_kg: float | None = None
    puntos: int | None = None

    @staticmethod
    def crear(vecino_id: str, direccion: Direccion,
              detalles: list[DetalleResiduo]) -> Solicitud:
        solicitud = Solicitud(vecino_id=vecino_id, direccion=direccion,
                              detalles=list(detalles))
        solicitud.validar_detalles()
        return solicitud

    def agregar_detalle(self, detalle: DetalleResiduo) -> None:
        self.detalles.append(detalle)

    def validar_detalles(self) -> None:
        # Criterio 3: lista vacía o peso 0 -> error de validación
        if not self.detalles or not all(d.es_valido() for d in self.detalles):
            raise ErrorValidacion("Debe ingresar al menos un residuo con peso mayor a 0")

    def asignar_coordenadas(self, coordenadas: Coordenadas) -> None:
        self.direccion.coordenadas = coordenadas

    def marcar_pendiente(self) -> None:
        if not self.direccion.esta_geocodificada():
            raise ErrorValidacion("La dirección no está geocodificada")
        self.estado = EstadoSolicitud.PENDIENTE

    def rechazar(self, motivo: str) -> None:
        self.estado = EstadoSolicitud.RECHAZADA
        self.motivo_rechazo = motivo

    def obtener_peso_total(self) -> float:
        return sum(d.peso_kg for d in self.detalles)

    # --- Operaciones propuestas por la máquina de estados (E3, regla C2) ---
    def asignar(self, reciclador_id: str) -> None:
        if self.estado is not EstadoSolicitud.PENDIENTE:
            raise ErrorValidacion("Solo una solicitud PENDIENTE puede asignarse")
        self.reciclador_id = reciclador_id
        self.estado = EstadoSolicitud.ASIGNADA

    def registrar_recojo(self) -> None:
        if self.estado is not EstadoSolicitud.ASIGNADA:
            raise ErrorValidacion("Solo una solicitud ASIGNADA puede recogerse")
        self.estado = EstadoSolicitud.RECOGIDA

    def registrar_pesaje(self, peso_kg: float) -> None:
        if self.estado is not EstadoSolicitud.RECOGIDA or peso_kg <= 0:
            raise ErrorValidacion("Pesaje inválido")
        self.peso_real_kg = peso_kg
        self.estado = EstadoSolicitud.PESADA

    def acreditar_puntos(self, puntos: int) -> None:
        if self.estado is not EstadoSolicitud.PESADA:
            raise ErrorValidacion("Solo una solicitud PESADA acredita puntos")
        self.puntos = puntos
        self.estado = EstadoSolicitud.PUNTOS_ACREDITADOS


# --------------------------- Puertos (interfaces) ---------------------------
class SolicitudRepository(ABC):
    @abstractmethod
    def guardar(self, solicitud: Solicitud) -> None: ...


class MapasGeocodificacionPort(ABC):
    @abstractmethod
    def geocodificar(self, direccion: str) -> Coordenadas: ...


class NotificacionPort(ABC):
    @abstractmethod
    def notificar_error_ubicacion(self, vecino_id: str, motivo: str) -> None: ...


# ------------------------------- Adaptador ---------------------------------
class GoogleMapsAdapter(MapasGeocodificacionPort):
    def geocodificar(self, direccion: str) -> Coordenadas:
        raise NotImplementedError("Integrar con la API de Google Maps")


# ---------------------------- Servicio de aplicación -----------------------
@dataclass
class SolicitarRecojoService:
    repositorio: SolicitudRepository
    mapas: MapasGeocodificacionPort
    notificacion: NotificacionPort

    def solicitar_recojo(self, vecino_id: str, texto_direccion: str,
                         detalles: list[DetalleResiduo]) -> Solicitud:
        direccion = Direccion(texto=texto_direccion)
        solicitud = Solicitud.crear(vecino_id, direccion, detalles)  # ErrorValidacion
        try:
            coordenadas = self.mapas.geocodificar(texto_direccion)
        except ErrorGeocodificacion:
            solicitud.rechazar("Dirección inválida")
            self.repositorio.guardar(solicitud)
            # En el diagrama de secuencia este mensaje es asíncrono (->>)
            self.notificacion.notificar_error_ubicacion(vecino_id, "Dirección inválida")
            return solicitud
        solicitud.asignar_coordenadas(coordenadas)
        solicitud.marcar_pendiente()
        self.repositorio.guardar(solicitud)
        return solicitud
