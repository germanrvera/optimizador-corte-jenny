# Optimizador de Jenny

Sistema de optimización de cortes de material para tiras LED. Minimiza el desperdicio y calcula las fuentes de energía necesarias.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## ¿Qué hace?

Dado un conjunto de cortes solicitados y un rollo madre estándar (5m, 10m o 20m), el sistema calcula la mejor manera de distribuir los cortes para usar la menor cantidad de rollos posible y minimizar el material desperdiciado.

También maneja automáticamente cortes que superan el largo del rollo, dividiéndolos en segmentos y aprovechando los sobrantes para otros cortes.

---

## Funcionalidades

**Optimización de cortes**
- Algoritmo de programación lineal (PuLP) para solución matemáticamente óptima
- Rollos estandarizados: 5m, 10m y 20m
- Cortes mayores al rollo: se dividen automáticamente en segmentos
- Los sobrantes de cortes grandes se aprovechan para cortes pequeños
- Resultados ordenados de menor a mayor desperdicio
- Exportación del plan de corte en CSV

**Cálculo de fuentes de energía (opcional)**
- Modo individual: una fuente por cada corte
- Modo optimizado: agrupa cortes para usar menos fuentes
- Factor de seguridad configurable
- Estadísticas de consumo y eficiencia
- Exportación del plan de fuentes en CSV

**Acceso y seguridad**
- Login por email autorizado
- Gestión de usuarios vía Streamlit Secrets
- Sesiones seguras con cierre de sesión

---

## Tecnologías

- [Streamlit](https://streamlit.io) — interfaz web
- [PuLP](https://coin-or.github.io/pulp/) — optimización lineal
- [Plotly](https://plotly.com) — visualizaciones
- [Pandas](https://pandas.pydata.org) — manejo de datos
- Python 3.10+

---

## Instalación local

```bash
git clone https://github.com/TU-USUARIO/optimizador-corte-jenny.git
cd optimizador-corte-jenny

pip install -r requirements.txt

streamlit run app.py
```

La app se abre automáticamente en `http://localhost:8501`

---

## Despliegue en Streamlit Cloud

1. Subir el repositorio a GitHub (sin incluir `secrets.toml`)
2. Crear la app en [share.streamlit.io](https://share.streamlit.io)
3. En **Settings → Secrets**, agregar los emails autorizados:

```toml
emails_autorizados = "usuario1@empresa.com,usuario2@empresa.com"
```

---

## Estructura del proyecto

```
optimizador-corte-jenny/
├── app.py
├── requirements.txt
├── logo.png
├── README.md
├── LICENSE
├── .gitignore
└── .streamlit/
    └── config.toml
```

---

## Requisitos

```
streamlit>=1.31.0
pandas>=2.0.0
plotly>=5.18.0
pillow>=10.0.0
PuLP>=2.7.0
```

---

## Licencia

MIT
