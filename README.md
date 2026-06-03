# ⏳ Cronómetro del Sofá

> Monitor de tiempo por aplicación con metáforas temporales, percepciones subjetivas y un toque de relatividad.  
> Inspirado en el marco **TUSE** (Teoría Unificada de Sistemas Emergentes).

---

## 🧠 ¿Qué hace esto?

Un programa ligero que registra cuánto tiempo pasas en cada aplicación de tu escritorio y te avisa cuando superas ciertos límites... pero sin usar números fríos. En lugar de "Has excedido 10 minutos", recibes frases como:

- *“En RedSocial, llevas el tiempo de tres parpadeos de gato.”*
- *“Si estuvieras en la ISS, habrías envejecido 0.0000001 segundos menos. Pero no.”*

Además, puedes añadir **percepciones subjetivas** (“esta reunión se me hizo eterna”) y al final de la sesión obtienes un **resumen comparativo** entre el tiempo real y cómo lo sentiste.

---

## 🎯 Características principales

- **Monitorización por aplicación** (ventana activa).  
- **Límites configurables** por app (con metáforas en lugar de avisos planos).  
- **Registro subjetivo del tiempo**: guarda cómo percibes cada intervalo.  
- **Comparador temporal** que contrasta la duración real con tu percepción.  
- **Arquitectura Hexagonal** (puertos y adaptadores intercambiables).  
- **Modo simulación** incorporado (no requiere dependencias externas).  
- **Persistencia en JSON** de todos los eventos.

---

## 🚀 Instalación y uso

### Requisitos
- Python 3.7 o superior.
- Opcional: `pygetwindow` para rastreo real de ventanas (`pip install pygetwindow`).

### Ejecución

```bash
python cronometro_del_sofa.py
Si pygetwindow no está instalado, el programa usará automáticamente un simulador que va cambiando de aplicación cada pocos segundos. Perfecto para probar la lógica.

Durante la ejecución
El monitor se actualiza cada segundo.

Cuando una aplicación supera su límite, verás la metáfora en pantalla.

Pulsa Ctrl+C para salir. Se mostrará un resumen de tiempos y el comparador subjetivo.

⚙️ Personalización
Edita la función main() para ajustar:

Límites (en segundos):

python
Limite("Navegador", 60*10),   # 10 minutos
Limite("RedSocial", 60*5)     # 5 minutos
Aplicaciones consideradas valiosas (su tiempo no se penaliza pero se monitoriza):

python
apps_valiosas = ["Editor", "Terminal", "Figma"]
Intervalo de muestreo: ciclo_principal(intervalo=2.0)

🧱 Arquitectura
El diseño sigue los principios de Arquitectura Hexagonal y el marco TUSE:

Componente	Rol
Reloj	Puerto para obtener el tiempo (real o simulado).
RastreadorVentanaActiva	Puerto para identificar la app activa.
RepositorioSesiones	Persistencia (JSON por defecto).
Notificador	Salida de avisos (consola, sistema...).
MonitorDominio	Lógica de negocio pura: acumula tiempo, detecta excesos, gestiona percepciones.
Metafora / ComparadorSubjetivo	Estrategias de comunicación temporal.
Los adaptadores concretos (RelojSistema, RastreadorVentanaReal, etc.) se inyectan en el orquestador CronometroDelSofa, permitiendo cambiar la fuente de datos sin tocar el dominio.

📁 Estructura del proyecto
text
.
├── cronometro_del_sofa.py   # Código fuente único y autocontenido
├── tuse_cronometro.json     # Historial de eventos (se genera al ejecutar)
└── README.md
🌐 Inspiración filosófica (TUSE)
Este proyecto materializa conceptos del documento TUSE:

Intención Fuerte: el código (herramienta del observador).

Intención Débil: la topología de flujos de atención que decides monitorizar.

Flecha del Tiempo Interna: la dirección de tu concentración entre aplicaciones.

Puntos de palanca: los límites que pones a las apps “contaminantes”.

Subjetividad como parámetro: el comparador entre tiempo real y percibido.

📜 Licencia
AGPLv3. Porque la sabiduría práctica debe ser libre.

¿Preguntas, ideas o metáforas nuevas? ¡Abre un issue!
“El tiempo no es un reloj externo, sino la dirección de tus flujos de atención.”

text

---

Ambos archivos están listos para usar. El código ahora **funciona correctamente**: acumula tiempo en cada pulso, lanza las metáforas cuando toca, y no repite avisos. Puedes probarlo sin instalar nada gracias al modo simulación.
