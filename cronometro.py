#!/usr/bin/env python3
"""
cronometro_del_sofa.py - Monitor de Tiempo por Aplicación con Metáforas Temporales.
Versión 1.1 - Arquitectura Hexagonal + Marco TUSE.

Corrección: el tiempo se acumula en cada tick, no solo al cambiar de ventana.
Las alertas se emiten una sola vez por aplicación y sesión.
Incluye metáforas contextuales, registro subjetivo y resumen comparativo.

Licencia: AGPLv3
"""

import time
import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Set

# -----------------------------------------------------------------------------
# PUERTOS
# -----------------------------------------------------------------------------

class Reloj(ABC):
    @abstractmethod
    def ahora(self) -> float:
        pass

class RastreadorVentanaActiva(ABC):
    @abstractmethod
    def obtener_aplicacion_actual(self) -> str:
        pass

class RepositorioSesiones(ABC):
    @abstractmethod
    def guardar_registro(self, sesion: Dict) -> None:
        pass
    @abstractmethod
    def cargar_historial(self) -> List[Dict]:
        pass

class Notificador(ABC):
    @abstractmethod
    def notificar(self, mensaje: str) -> None:
        pass

# -----------------------------------------------------------------------------
# DOMINIO
# -----------------------------------------------------------------------------

class Aplicacion:
    def __init__(self, nombre: str, es_valiosa: bool = False):
        self.nombre = nombre
        self.es_valiosa = es_valiosa
        self.tiempo_acumulado: float = 0.0

class Limite:
    def __init__(self, app_nombre: str, segundos_limite: float):
        self.app_nombre = app_nombre
        self.segundos_limite = segundos_limite

class Percepcion:
    def __init__(self, app_nombre: str, duracion_real: float, etiqueta: str):
        self.app_nombre = app_nombre
        self.duracion_real = duracion_real
        self.etiqueta = etiqueta
        self.instante = datetime.now()

class Metafora:
    """Genera frases contextuales basadas en el tiempo excedido."""
    @staticmethod
    def generar(tiempo_excedido: float, app_nombre: str) -> str:
        minutos = int(tiempo_excedido // 60)
        if minutos < 1:
            return f"En {app_nombre}, has estado el tiempo que tarda un suspiro en volverse queja."
        elif minutos < 5:
            return f"Tiempo en {app_nombre}: lo que se tarda en cocer un huevo perfecto."
        elif minutos < 15:
            return f"{app_nombre} ya te ha robado el tiempo de un capítulo de una serie mala."
        elif minutos < 30:
            return f"Si estuvieras en la ISS, en tu {app_nombre} habrías envejecido 0.0000001 segundos menos. Pero no."
        else:
            return f"En {app_nombre} llevas tanto que hasta la luz ha recorrido {minutos * 18_000_000} km mientras tanto."

class ComparadorSubjetivo:
    @staticmethod
    def resumen(percepciones: List[Percepcion]) -> Dict:
        if not percepciones:
            return {"mensaje": "Aún no hay percepciones registradas."}
        total_real = sum(p.duracion_real for p in percepciones)
        eternas = sum(p.duracion_real for p in percepciones if p.etiqueta == "eterno")
        breves = sum(p.duracion_real for p in percepciones if p.etiqueta == "breve")
        msg = f"Tiempo total registrado: {total_real/60:.1f} min. "
        if eternas > 0:
            msg += f"Sentiste eternos {eternas/60:.1f} min que realmente fueron eso. "
        if breves > 0:
            msg += f"Se te pasaron volando {breves/60:.1f} min. El tiempo es relativo, como dice TUSE."
        return {"mensaje": msg, "total_real": total_real, "eternas": eternas, "breves": breves}

class MonitorDominio:
    def __init__(self, limites: List[Limite], apps_valiosas: List[str]):
        self.aplicaciones: Dict[str, Aplicacion] = {}
        self.limites: Dict[str, Limite] = {lim.app_nombre: lim for lim in limites}
        self.apps_valiosas = set(apps_valiosas)
        self.percepciones: List[Percepcion] = []
        self.ultima_app: Optional[str] = None
        self.ultimo_tick: float = 0.0
        self.apps_alertadas: Set[str] = set()   # para no repetir avisos

    def tick(self, app_actual: str, timestamp: float) -> Optional[str]:
        """
        Procesa un pulso temporal.
        - Acumula el tiempo transcurrido para la app anterior.
        - Verifica si esa app superó su límite y aún no ha sido alertada.
        - Actualiza la app actual.
        Retorna un mensaje de metáfora si corresponde, o None.
        """
        mensaje = None

        if self.ultima_app is not None:
            delta = timestamp - self.ultimo_tick
            # Asegurar que la app existe en el diccionario
            if self.ultima_app not in self.aplicaciones:
                self.aplicaciones[self.ultima_app] = Aplicacion(
                    self.ultima_app,
                    self.ultima_app in self.apps_valiosas
                )
            self.aplicaciones[self.ultima_app].tiempo_acumulado += delta

            # Comprobar límite para la app que acaba de recibir tiempo
            if self.ultima_app in self.limites and self.ultima_app not in self.apps_alertadas:
                tiempo = self.aplicaciones[self.ultima_app].tiempo_acumulado
                limite = self.limites[self.ultima_app].segundos_limite
                if tiempo > limite:
                    excedido = tiempo - limite
                    mensaje = Metafora.generar(excedido, self.ultima_app)
                    self.apps_alertadas.add(self.ultima_app)

        # Actualizar contexto
        self.ultima_app = app_actual
        self.ultimo_tick = timestamp
        if app_actual not in self.aplicaciones:
            self.aplicaciones[app_actual] = Aplicacion(app_actual, app_actual in self.apps_valiosas)

        return mensaje

    def finalizar(self, timestamp: float):
        """Añade el último tramo de tiempo antes de cerrar."""
        if self.ultima_app is not None:
            delta = timestamp - self.ultimo_tick
            if self.ultima_app in self.aplicaciones:
                self.aplicaciones[self.ultima_app].tiempo_acumulado += delta

    def registrar_percepcion(self, app_nombre: str, duracion_real: float, etiqueta: str):
        self.percepciones.append(Percepcion(app_nombre, duracion_real, etiqueta))

    def obtener_resumen_comparativo(self) -> Dict:
        return ComparadorSubjetivo.resumen(self.percepciones)

    def estado_actual(self) -> Dict:
        """Devuelve un resumen del tiempo acumulado por aplicación."""
        return {
            app: int(datos.tiempo_acumulado)
            for app, datos in self.aplicaciones.items()
        }

# -----------------------------------------------------------------------------
# ADAPTADORES
# -----------------------------------------------------------------------------

class RelojSistema(Reloj):
    def ahora(self) -> float:
        return time.time()

class RastreadorVentanaSimulado(RastreadorVentanaActiva):
    """Simula cambios de aplicación cíclicos (modo demo)."""
    def __init__(self, duracion_por_app: float = 8.0):
        self.apps = ["Terminal", "Navegador", "Editor", "RedSocial", "Correo"]
        self.indice = 0
        self.duracion = duracion_por_app
        self.ultimo_cambio = time.time()

    def obtener_aplicacion_actual(self) -> str:
        ahora = time.time()
        if ahora - self.ultimo_cambio >= self.duracion:
            self.indice = (self.indice + 1) % len(self.apps)
            self.ultimo_cambio = ahora
        return self.apps[self.indice]

class RastreadorVentanaReal(RastreadorVentanaActiva):
    """Requiere pygetwindow. Captura la ventana activa real."""
    def __init__(self):
        try:
            import pygetwindow as gw
            self.gw = gw
        except ImportError:
            raise ImportError("Instala pygetwindow para usar el rastreador real.")

    def obtener_aplicacion_actual(self) -> str:
        try:
            ventana = self.gw.getActiveWindow()
            if ventana:
                return ventana.title.split(" - ")[0].strip()
        except Exception:
            pass
        return "Desconocido"

class RepositorioJSON(RepositorioSesiones):
    def __init__(self, archivo: str = "sesiones_tuse.json"):
        self.archivo = archivo

    def guardar_registro(self, sesion: Dict) -> None:
        datos = self.cargar_historial()
        datos.append(sesion)
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2)

    def cargar_historial(self) -> List[Dict]:
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

class NotificadorConsola(Notificador):
    def notificar(self, mensaje: str) -> None:
        print("\n" + "="*60)
        print(f"⏳ {mensaje}")
        print("="*60 + "\n")

# -----------------------------------------------------------------------------
# ORQUESTADOR
# -----------------------------------------------------------------------------

class CronometroDelSofa:
    def __init__(self,
                 reloj: Reloj,
                 rastreador: RastreadorVentanaActiva,
                 repositorio: RepositorioSesiones,
                 notificador: Notificador,
                 dominio: MonitorDominio):
        self.reloj = reloj
        self.rastreador = rastreador
        self.repositorio = repositorio
        self.notificador = notificador
        self.dominio = dominio
        self.activo = False

    def ciclo_principal(self, intervalo: float = 1.0):
        self.activo = True
        print("⏳ Cronómetro del Sofá iniciado. Pulsa Ctrl+C para salir.")
        print("   (Inspirado en TUSE: la flecha del tiempo de tu atención)\n")
        try:
            while self.activo:
                app = self.rastreador.obtener_aplicacion_actual()
                ahora = self.reloj.ahora()

                mensaje = self.dominio.tick(app, ahora)
                if mensaje:
                    self.notificador.notificar(mensaje)
                    self.repositorio.guardar_registro({
                        "tipo": "exceso",
                        "app": app,
                        "timestamp": ahora,
                        "mensaje": mensaje
                    })

                time.sleep(intervalo)
        except KeyboardInterrupt:
            print("\nFinalizando sesión...")
            self.activo = False
            self.dominio.finalizar(self.reloj.ahora())
            self._mostrar_estado_final()

    def _mostrar_estado_final(self):
        print("\n--- Resumen de tiempo por aplicación (segundos) ---")
        estado = self.dominio.estado_actual()
        for app, segundos in estado.items():
            print(f"  {app}: {segundos} s")
        print("----------------------------------------------------")
        self.mostrar_resumen()

    def agregar_percepcion_manual(self, app: str, duracion_real: float, etiqueta: str):
        self.dominio.registrar_percepcion(app, duracion_real, etiqueta)

    def mostrar_resumen(self):
        resumen = self.dominio.obtener_resumen_comparativo()
        print(resumen["mensaje"])

# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA
# -----------------------------------------------------------------------------

def main():
    limites = [
        Limite("Navegador", 20),   # 20 segundos para probar rápido
        Limite("RedSocial", 30),
        Limite("Correo", 40)
    ]
    apps_valiosas = ["Editor", "Terminal"]

    reloj = RelojSistema()

    try:
        rastreador = RastreadorVentanaReal()
        print("Rastreador real activo.\n")
    except ImportError:
        print("pygetwindow no instalado. Usando rastreador simulado (demo).\n")
        rastreador = RastreadorVentanaSimulado(duracion_por_app=5.0)

    repositorio = RepositorioJSON("tuse_cronometro.json")
    notificador = NotificadorConsola()
    dominio = MonitorDominio(limites, apps_valiosas)

    app = CronometroDelSofa(reloj, rastreador, repositorio, notificador, dominio)

    # Percepciones de ejemplo
    app.agregar_percepcion_manual("Correo", 1200, "eterno")
    app.agregar_percepcion_manual("Editor", 600, "breve")

    app.ciclo_principal(intervalo=1.0)

if __name__ == "__main__":
    main()