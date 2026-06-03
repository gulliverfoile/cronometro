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

Versión Web: El Reloj del Sofá (reloj_del_sofa.html)
Una interfaz visual y autocontenida del Cronómetro del Sofá, lista para usar desde cualquier navegador, sin instalar nada.

¿Qué aporta respecto al script Python?
Característica	Script Python (cronometro_del_sofa.py)	Interfaz Web (reloj_del_sofa.html)
Ejecución	Requiere Python 3.7+	Solo necesitas un navegador
Rastreo de apps	Automático (ventana activa real o simulada)	Manual consciente: pulsas un botón al cambiar de app
Persistencia	Archivo JSON local	localStorage del navegador (recupera la sesión al recargar)
Feedback	Metáforas por consola	Metáforas animadas, preguntas de percepción, resumen visual
Perfiles de intención	No (solo límites)	Sí: cada app puede marcarse como "Quiero más", "Quiero menos" o "Solo observar"
Personalidad de los mensajes	Fija	Configurable (estilo amable, neutro, sarcástico, estoico)
Exportación	JSON manual al finalizar	Botón de exportación a JSON en cualquier momento
Cómo usarla
Abre reloj_del_sofa.html en tu navegador.

Verás cuatro aplicaciones preconfiguradas: Editor, Navegador, Redes, Correo.

Pulsa el botón de la app en la que estás. El reloj central empezará a contar.

Al cambiar a otra app, pulsa su botón. Aparecerá una pregunta rápida: "¿Cómo se pasó el tiempo?" (Voló / Normal / Eterno).

Si superas el límite en una app con perfil "Quiero menos", verás una metáfora que te invita a reflexionar (sin castigo).

Al final del día, pulsa "Terminar día" para ver un resumen comparativo entre tiempo real, intención y percepción.

Usa "Exportar JSON" para descargar los datos si quieres analizarlos con el script Python más tarde.

Personalización
Edita el bloque <script> al final del HTML, en la sección appsConfig:

javascript
const appsConfig = [
  new Aplicacion('Editor', PERFIL.QUIERO_MAS, 0, 'Dedica tiempo profundo a crear'),
  new Aplicacion('Navegador', PERFIL.SOLO_OBSERVAR, 0, 'Navegar con propósito'),
  new Aplicacion('Redes', PERFIL.QUIERO_MENOS, 30, 'No más de 30 minutos al día'),
  new Aplicacion('Correo', PERFIL.QUIERO_MENOS, 20, 'Solo lo necesario')
];
Cambia los nombres, los perfiles (QUIERO_MAS, QUIERO_MENOS, SOLO_OBSERVAR), los límites en segundos y las descripciones de intención.

Para cambiar el tono de los mensajes, modifica la variable estiloInicial:

javascript
const estiloInicial = 'amable'; // 'neutro', 'sarcástico', 'estoico'
Filosofía TUSE en esta versión
Intención Débil: los perfiles que tú defines (lo que consideras valioso, lo que quieres limitar, lo que solo observas).

Intención Fuerte: el código que mide, pregunta y muestra. La herramienta no decide por ti; te devuelve un espejo de tus propias decisiones.

Flecha del Tiempo Interna: la secuencia de cambios conscientes de aplicación. No mide el tiempo absoluto, sino la sucesión de tus elecciones de atención.

Punto de palanca: la pregunta subjetiva justo al cambiar de app. Ese instante de fricción es donde puedes reorientar tu atención.

Integración con el script Python
Ambos archivos son complementarios:

El script Python rastrea tu actividad real sin intervención humana. Es ideal para diagnóstico pasivo.

La interfaz web te entrena en la observación consciente de tu atención. Es una prótesis para la phronesis.

Puedes exportar datos desde la web en JSON e importarlos en el script Python para análisis más profundos, o simplemente usar cada uno en el contexto que prefieras.
