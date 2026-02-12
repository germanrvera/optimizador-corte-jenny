# 📏⚡ Optimizador de Corte + Fuentes de Energía

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

Sistema inteligente para optimizar cortes de material y calcular fuentes de energía para tiras LED.

## 🎯 Características

### 📏 Optimización de Cortes
- **Algoritmo FFD** (First Fit Decreasing) para minimizar desperdicios
- **Visualización interactiva** de cada rollo
- **Métricas detalladas**: eficiencia, desperdicio, material usado
- **Exportación a CSV** del plan de corte

### ⚡ Cálculo de Fuentes de Energía
- **Dos modos de asignación:**
  - Una fuente por corte (independiente)
  - Optimización inteligente (agrupa cortes)
- **Estadísticas avanzadas:**
  - Consumo total real
  - Capacidad instalada
  - Eficiencia del sistema
  - Alertas de sobrecarga
- **Visualización de uso** por fuente con código de colores
- **Recomendaciones automáticas**
- **Exportación a CSV** del plan de fuentes

## 🚀 Demo en Vivo

[🔗 Prueba la aplicación aquí](https://tu-app.streamlit.app) _(Actualiza este enlace después del despliegue)_

## 📖 Uso Rápido

1. **Configura** el largo del rollo madre
2. **Agrega** tus pedidos (largo y cantidad)
3. **(Opcional)** Activa cálculo de fuentes para LED
4. **Presiona** "🚀 Calcular Optimización"
5. **Descarga** los planes en CSV

## 🛠️ Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/optimizador-corte-fuentes.git
cd optimizador-corte-fuentes

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

## 📦 Tecnologías

- **Streamlit** - Framework de la aplicación
- **Plotly** - Visualizaciones interactivas
- **Pandas** - Manipulación de datos
- **Python 3.8+** - Lenguaje base

## 💡 Casos de Uso

- Fabricación de muebles
- Industria textil
- Metalurgia
- Construcción
- Instalaciones LED

## 📄 Licencia

MIT License

---

Desarrollado con ❤️ usando Streamlit
