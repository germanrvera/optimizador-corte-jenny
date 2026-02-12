"""
APLICACIÓN DE OPTIMIZACIÓN DE CORTE DE MATERIAL + FUENTES DE ENERGÍA
======================================================================
Soluciona el problema de corte unidimensional (Cutting Stock Problem)
usando el algoritmo First Fit Decreasing (FFD) y calcula las fuentes
de energía necesarias para tiras LED con optimización inteligente.

Características:
- Optimización de cortes de material (minimiza desperdicios)
- Cálculo de fuentes de energía (modo individual y optimizado)
- Visualizaciones interactivas con métricas detalladas
- Estadísticas avanzadas de eficiencia
- Exportación de planes de corte y fuentes

Autor: Sistema de Optimización Industrial
Versión: 2.0 - Con Cálculo Inteligente de Fuentes
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Tuple
import collections
import math
from PIL import Image
import os

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Optimizador de Corte de Jenny",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS PERSONALIZADOS
# ============================================================================

st.markdown("""
<style>
    /* Importar fuentes distintivas */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Work+Sans:wght@300;500;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #0f172a;
        --secondary-color: #475569;
        --accent-color: #f97316;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --bg-color: #f8fafc;
        --card-bg: #ffffff;
    }
    
    /* Tipografía general */
    html, body, [class*="css"] {
        font-family: 'Work Sans', sans-serif;
        color: var(--primary-color);
    }
    
    /* Títulos */
    h1, h2, h3 {
        font-family: 'Work Sans', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 {
        color: var(--primary-color);
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Código y números */
    code, .stNumberInput input, .metric-value {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Fondo de la aplicación */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Tarjetas personalizadas */
    .custom-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 4px solid var(--accent-color);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Métricas personalizadas */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--accent-color) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--secondary-color) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-color) 0%, #ea580c 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(249, 115, 22, 0.4);
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
    }
    
    /* Inputs */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.2s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
    }
    
    /* Tablas */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-color) 0%, #1e293b 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Alertas */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Animaciones */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .custom-card {
        animation: slideIn 0.4s ease-out;
    }
    
    /* Divisor decorativo */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, var(--accent-color) 0%, transparent 100%);
        margin: 2rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CLASES Y ESTRUCTURAS DE DATOS
# ============================================================================

class Pedido:
    """Representa un pedido individual de piezas."""
    
    def __init__(self, largo: float, cantidad: int):
        self.largo = largo
        self.cantidad = cantidad
    
    def __repr__(self):
        return f"Pedido({self.largo}m × {self.cantidad})"


class Rollo:
    """Representa un rollo madre con las piezas cortadas."""
    
    def __init__(self, longitud_total: float):
        self.longitud_total = longitud_total
        self.piezas: List[float] = []
        self.espacio_usado = 0.0
    
    def puede_agregar(self, largo_pieza: float) -> bool:
        """Verifica si una pieza puede agregarse al rollo."""
        return (self.espacio_usado + largo_pieza) <= self.longitud_total
    
    def agregar_pieza(self, largo_pieza: float) -> bool:
        """Agrega una pieza al rollo si hay espacio."""
        if self.puede_agregar(largo_pieza):
            self.piezas.append(largo_pieza)
            self.espacio_usado += largo_pieza
            return True
        return False
    
    @property
    def desperdicio(self) -> float:
        """Calcula el desperdicio del rollo."""
        return self.longitud_total - self.espacio_usado
    
    @property
    def eficiencia(self) -> float:
        """Calcula el porcentaje de eficiencia del rollo."""
        return (self.espacio_usado / self.longitud_total) * 100 if self.longitud_total > 0 else 0


# ============================================================================
# ALGORITMO DE OPTIMIZACIÓN
# ============================================================================

def first_fit_decreasing(pedidos: List[Pedido], longitud_rollo: float) -> List[Rollo]:
    """
    Implementa el algoritmo First Fit Decreasing (FFD).
    
    Args:
        pedidos: Lista de pedidos con largo y cantidad
        longitud_rollo: Longitud del rollo madre
    
    Returns:
        Lista de rollos con las piezas asignadas
    """
    # Expandir pedidos a lista de piezas individuales
    piezas = []
    for pedido in pedidos:
        piezas.extend([pedido.largo] * pedido.cantidad)
    
    # Ordenar piezas de mayor a menor (Decreasing)
    piezas.sort(reverse=True)
    
    # Lista de rollos utilizados
    rollos: List[Rollo] = []
    
    # Colocar cada pieza en el primer rollo donde quepa
    for pieza in piezas:
        colocada = False
        
        # Intentar colocar en rollos existentes (First Fit)
        for rollo in rollos:
            if rollo.agregar_pieza(pieza):
                colocada = True
                break
        
        # Si no cabe en ningún rollo existente, crear uno nuevo
        if not colocada:
            nuevo_rollo = Rollo(longitud_rollo)
            nuevo_rollo.agregar_pieza(pieza)
            rollos.append(nuevo_rollo)
    
    return rollos


# ============================================================================
# FUNCIONES PARA CÁLCULO DE FUENTES DE ENERGÍA
# ============================================================================

def obtener_fuente_adecuada_individual(consumo_requerido_watts: float, 
                                      fuentes_disponibles_watts: List[float], 
                                      factor_seguridad: float = 1.2) -> Tuple[float, str]:
    """
    Calcula la fuente de poder más pequeña que soporta el consumo requerido
    aplicando un factor de seguridad (modo individual).
    
    Returns:
        Tuple[float, str]: (fuente_asignada, mensaje_advertencia)
    """
    consumo_ajustado = consumo_requerido_watts * factor_seguridad
    
    fuentes_suficientes = [f for f in fuentes_disponibles_watts if f >= consumo_ajustado]
    
    if not fuentes_suficientes:
        if fuentes_disponibles_watts:
            max_fuente = max(fuentes_disponibles_watts)
            return max_fuente, f"⚠️ El consumo de {consumo_requerido_watts:.2f}W (ajustado a {consumo_ajustado:.2f}W) excede todas las fuentes. Se asigna {max_fuente:.0f}W."
        else:
            return None, "❌ No hay fuentes disponibles."
    
    return min(fuentes_suficientes), ""


def optimizar_fuentes_agrupadas(pedidos_list: List[Pedido], 
                                watts_por_metro: float,
                                fuentes_disponibles: List[float],
                                factor_seguridad: float) -> Tuple[Dict, List, Dict]:
    """
    Optimiza la asignación de fuentes para agrupar cortes usando FFD mejorado.
    
    Algoritmo:
    1. Expande todos los pedidos a piezas individuales
    2. Calcula consumo real y ajustado para cada pieza
    3. Ordena piezas por consumo descendente (FFD)
    4. Asigna cada pieza a la primera fuente con capacidad suficiente
    5. Si no cabe en ninguna fuente existente, abre una nueva fuente
    
    Args:
        pedidos_list: Lista de objetos Pedido
        watts_por_metro: Consumo de la tira LED por metro
        fuentes_disponibles: Lista de potencias disponibles
        factor_seguridad: Factor multiplicador de seguridad (ej: 1.2 para 20%)
    
    Returns:
        Tuple[Dict, List, Dict]: (conteo_fuentes, detalles_asignacion, estadisticas)
    """
    # Crear diccionario de pedidos
    pedidos_dict = {}
    for p in pedidos_list:
        pedidos_dict[p.largo] = pedidos_dict.get(p.largo, 0) + p.cantidad
    
    # Expandir pedidos a piezas individuales con su consumo
    piezas_consumo = []
    for largo, cantidad in pedidos_dict.items():
        consumo_real = largo * watts_por_metro
        consumo_ajustado = consumo_real * factor_seguridad
        for _ in range(cantidad):
            piezas_consumo.append({
                "largo": largo,
                "consumo_real": consumo_real,
                "consumo_ajustado": consumo_ajustado
            })
    
    # Ordenar por consumo descendente (FFD)
    piezas_consumo.sort(key=lambda x: x["consumo_ajustado"], reverse=True)
    
    # Fuentes en uso
    fuentes_en_uso = []
    conteo_fuentes = collections.defaultdict(int)
    
    # Asignar cada pieza a una fuente
    for pieza in piezas_consumo:
        consumo = pieza["consumo_ajustado"]
        asignada = False
        
        # Intentar en fuentes existentes
        for fuente in fuentes_en_uso:
            if fuente["restante"] >= consumo:
                fuente["restante"] -= consumo
                fuente["piezas"].append(pieza)
                asignada = True
                break
        
        # Si no cabe, crear nueva fuente
        if not asignada:
            fuente_encontrada = False
            for fuente_w in sorted(fuentes_disponibles):
                if fuente_w >= consumo:
                    fuentes_en_uso.append({
                        "potencia": fuente_w,
                        "restante": fuente_w - consumo,
                        "piezas": [pieza]
                    })
                    conteo_fuentes[fuente_w] += 1
                    fuente_encontrada = True
                    break
            
            if not fuente_encontrada:
                # Asignar la fuente más grande aunque exceda
                max_fuente = max(fuentes_disponibles) if fuentes_disponibles else None
                if max_fuente:
                    fuentes_en_uso.append({
                        "potencia": max_fuente,
                        "restante": max_fuente - consumo,
                        "piezas": [pieza]
                    })
                    conteo_fuentes[max_fuente] += 1
    
    # Formatear detalles con información mejorada
    detalles = []
    total_consumo_real = 0
    total_capacidad_desperdiciada = 0
    fuentes_sobrecargadas = 0
    
    for idx, fuente in enumerate(fuentes_en_uso, 1):
        piezas_info = []
        for p in fuente["piezas"]:
            piezas_info.append(f"{p['largo']:.2f}m ({p['consumo_real']:.2f}W)")
        
        piezas_str = ", ".join(piezas_info)
        num_piezas = len(fuente["piezas"])
        consumo_total = fuente["potencia"] - fuente["restante"]
        porcentaje_uso = (consumo_total / fuente["potencia"]) * 100 if fuente["potencia"] > 0 else 0
        
        total_consumo_real += consumo_total
        total_capacidad_desperdiciada += max(0, fuente["restante"])
        
        if fuente["restante"] < 0:
            fuentes_sobrecargadas += 1
            estado = "⚠️ SOBRECARGA"
            estado_color = "#ef4444"
        elif porcentaje_uso >= 90:
            estado = "🟡 Casi al límite"
            estado_color = "#f59e0b"
        elif porcentaje_uso >= 70:
            estado = "🟢 Óptimo"
            estado_color = "#10b981"
        else:
            estado = "🔵 Subutilizada"
            estado_color = "#3b82f6"
        
        detalles.append({
            "ID": f"F-{idx}",
            "Potencia (W)": f"{fuente['potencia']:.0f}",
            "N° Piezas": num_piezas,
            "Cortes Asignados": piezas_str,
            "Consumo (W)": f"{consumo_total:.2f}",
            "Uso (%)": f"{porcentaje_uso:.1f}%",
            "Disponible (W)": f"{max(0, fuente['restante']):.2f}",
            "Estado": estado,
            "_color": estado_color
        })
    
    # Calcular estadísticas generales
    total_fuentes = len(fuentes_en_uso)
    eficiencia_promedio = 0
    if total_fuentes > 0:
        eficiencia_promedio = (total_consumo_real / sum(f["potencia"] for f in fuentes_en_uso)) * 100
    
    estadisticas = {
        "total_fuentes": total_fuentes,
        "total_consumo_real": total_consumo_real,
        "total_capacidad_instalada": sum(f["potencia"] for f in fuentes_en_uso),
        "capacidad_desperdiciada": total_capacidad_desperdiciada,
        "eficiencia_promedio": eficiencia_promedio,
        "fuentes_sobrecargadas": fuentes_sobrecargadas,
        "total_piezas": len(piezas_consumo)
    }
    
    return conteo_fuentes, detalles, estadisticas


# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def crear_visualizacion_rollo(rollo: Rollo, numero_rollo: int) -> go.Figure:
    """
    Crea una visualización horizontal de un rollo con sus cortes.
    
    Args:
        rollo: Objeto Rollo a visualizar
        numero_rollo: Número identificador del rollo
    
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    # Colores para las piezas
    colores = ['#f97316', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b']
    
    posicion_actual = 0
    
    # Agregar cada pieza como un segmento
    for idx, pieza in enumerate(rollo.piezas):
        color = colores[idx % len(colores)]
        
        fig.add_trace(go.Bar(
            y=[f'Rollo {numero_rollo}'],
            x=[pieza],
            orientation='h',
            name=f'{pieza}m',
            marker=dict(
                color=color,
                line=dict(color='white', width=2)
            ),
            text=f'{pieza}m',
            textposition='inside',
            textfont=dict(color='white', size=12, family='JetBrains Mono'),
            hovertemplate=f'<b>Pieza:</b> {pieza}m<br><extra></extra>',
            base=posicion_actual
        ))
        
        posicion_actual += pieza
    
    # Agregar desperdicio si existe
    if rollo.desperdicio > 0:
        fig.add_trace(go.Bar(
            y=[f'Rollo {numero_rollo}'],
            x=[rollo.desperdicio],
            orientation='h',
            name='Desperdicio',
            marker=dict(
                color='#e5e7eb',
                pattern=dict(shape='/', fgcolor='#9ca3af', size=8, solidity=0.3),
                line=dict(color='#6b7280', width=2)
            ),
            text=f'{rollo.desperdicio:.2f}m',
            textposition='inside',
            textfont=dict(color='#4b5563', size=11, family='JetBrains Mono'),
            hovertemplate=f'<b>Desperdicio:</b> {rollo.desperdicio:.2f}m<br><extra></extra>',
            base=posicion_actual
        ))
    
    # Configuración del layout
    fig.update_layout(
        barmode='stack',
        showlegend=False,
        height=100,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[0, rollo.longitud_total],
            showgrid=True,
            gridcolor='#e5e7eb',
            zeroline=False,
            title=dict(text='Longitud (m)', font=dict(size=11, color='#64748b')),
            tickfont=dict(family='JetBrains Mono', size=10, color='#64748b')
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        hovermode='closest',
        font=dict(family='Work Sans')
    )
    
    return fig


def mostrar_resumen_rollo(rollo: Rollo, numero_rollo: int):
    """Muestra el resumen detallado de un rollo."""
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Rollo #{numero_rollo}**")
        detalles = ", ".join([f"{p}m" for p in rollo.piezas])
        st.caption(f"Piezas: {detalles}")
    
    with col2:
        eficiencia_color = "🟢" if rollo.eficiencia >= 80 else "🟡" if rollo.eficiencia >= 60 else "🔴"
        st.metric("Eficiencia", f"{rollo.eficiencia:.1f}%", delta=f"{eficiencia_color}")
    
    with col3:
        st.metric("Desperdicio", f"{rollo.desperdicio:.2f}m")


# ============================================================================
# INICIALIZACIÓN DEL ESTADO DE LA SESIÓN
# ============================================================================

# Estado de autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# ============================================================================
# SISTEMA DE AUTENTICACIÓN
# ============================================================================

def check_authentication():
    """Verifica si el usuario está autenticado."""
    
    if st.session_state.authenticated:
        return True
    
    # Pantalla de login
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #1f2937; margin-bottom: 1rem;'>🔐 Acceso al Optimizador de Jenny</h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>Ingresa tu email autorizado para acceder al sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Intentar cargar el logo
    try:
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo, use_container_width=True)
    except Exception as e:
        st.info("📋 Logo no disponible - continuando con login")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Formulario de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        email_input = st.text_input(
            "📧 Email",
            placeholder="tu-email@ejemplo.com",
            key="email_input"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Ingresar al Sistema", type="primary", use_container_width=True):
            if email_input:
                email_normalizado = email_input.strip().lower()
                
                # Cargar emails autorizados desde Streamlit Secrets
                try:
                    # Intentar cargar desde secrets (para producción)
                    emails_str = st.secrets.get("emails_autorizados", "")
                    EMAILS_AUTORIZADOS = [email.strip().lower() for email in emails_str.split(',') if email.strip()]
                except:
                    # Si no hay secrets configurados, usar lista por defecto (desarrollo)
                    EMAILS_AUTORIZADOS = [
                        "admin@jenny.com",
                        "gerencia@jenny.com",
                        "produccion@jenny.com",
                        "ejemplo@gmail.com"
                    ]
                    st.warning("⚠️ Usando emails de prueba. Configura secrets en producción.")
                
                if email_normalizado in EMAILS_AUTORIZADOS:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email_normalizado
                    st.success(f"✅ ¡Bienvenido! Acceso concedido para {email_normalizado}")
                    st.rerun()
                else:
                    st.error("❌ Email no autorizado. Contacta al administrador para obtener acceso.")
            else:
                st.warning("⚠️ Por favor, ingresa un email válido.")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>
        <p>¿Necesitas acceso? Contacta al administrador del sistema</p>
        <p style='font-size: 0.8rem; margin-top: 1rem;'>Sistema de Optimización Jenny v2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    return False

# Verificar autenticación
if not check_authentication():
    st.stop()

# ============================================================================
# ESTADOS DE LA APLICACIÓN (Solo si está autenticado)
# ============================================================================

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

if 'resultados' not in st.session_state:
    st.session_state.resultados = None

if 'resultados_fuentes' not in st.session_state:
    st.session_state.resultados_fuentes = None

if 'calcular_fuentes_enabled' not in st.session_state:
    st.session_state.calcular_fuentes_enabled = False

# ============================================================================
# INTERFAZ DE USUARIO - HEADER
# ============================================================================

# Mostrar logo y título
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    try:
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png")
            st.image(logo, width=150)
    except:
        st.markdown("### 📏")

with col_titulo:
    st.markdown("# 📏⚡ Optimizador de Jenny + Fuentes")
    st.markdown("### Sistema inteligente de minimización de desperdicio y cálculo de fuentes")

# Información de usuario y botón de cerrar sesión
col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    st.markdown(f"<p style='text-align: right; color: #6b7280; font-size: 0.9rem;'>👤 {st.session_state.user_email}</p>", unsafe_allow_html=True)
with col3:
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.pedidos = []
        st.session_state.resultados = None
        st.session_state.resultados_fuentes = None
        st.rerun()

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CONFIGURACIÓN
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    st.markdown("---")
    
    # Configuración del rollo madre
    st.markdown("### 📐 Rollo Madre")
    longitud_rollo = st.number_input(
        "Longitud estándar (metros)",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.1,
        help="Define la longitud del rollo madre disponible"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Gestión de cortes")
    
    # Inputs para agregar pedidos
    col1, col2 = st.columns(2)
    
    with col1:
        largo_pieza = st.number_input(
            "Largo (m)",
            min_value=0.1,
            max_value=float(longitud_rollo),
            value=2.0,
            step=0.1,
            key="input_largo"
        )
    
    with col2:
        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            max_value=1000,
            value=1,
            step=1,
            key="input_cantidad"
        )
    
    # Botón para agregar pedido
    if st.button("➕ Agregar Corte", use_container_width=True):
        if largo_pieza > longitud_rollo:
            st.error(f"⚠️ Error: La pieza ({largo_pieza}m) es más grande que el rollo madre ({longitud_rollo}m)")
        else:
            nuevo_pedido = Pedido(largo_pieza, cantidad)
            st.session_state.pedidos.append(nuevo_pedido)
            st.success(f"✅ Agregado: {cantidad}× {largo_pieza}m")
            st.rerun()
    
    st.markdown("---")
    
    # Mostrar pedidos actuales
    if st.session_state.pedidos:
        st.markdown("### 📦 Cortes Actuales")
        
        pedidos_df = pd.DataFrame([
            {"Largo (m)": p.largo, "Cantidad": p.cantidad, "Total (m)": p.largo * p.cantidad}
            for p in st.session_state.pedidos
        ])
        
        st.dataframe(
            pedidos_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Resumen de pedidos
        total_piezas = sum(p.cantidad for p in st.session_state.pedidos)
        total_metros = sum(p.largo * p.cantidad for p in st.session_state.pedidos)
        
        st.info(f"**Total:** {total_piezas} piezas • {total_metros:.2f}m")
        
        # Botón para limpiar pedidos
        if st.button("🗑️ Limpiar Lista", use_container_width=True):
            st.session_state.pedidos = []
            st.session_state.resultados = None
            st.session_state.resultados_fuentes = None
            st.rerun()
    else:
        st.info("No hay cortes agregados")
    
    st.markdown("---")
    
    # Opción para calcular fuentes
    st.markdown("### ⚡ Cálculo de Fuentes (Opcional)")
    st.session_state.calcular_fuentes_enabled = st.checkbox(
        "Calcular fuentes",
        value=st.session_state.calcular_fuentes_enabled,
        help="Activa esta opción si necesitas calcular las fuentes"
    )
    
    if st.session_state.calcular_fuentes_enabled:
        st.markdown("**Configuración de Fuentes:**")
        
        watts_por_metro = st.number_input(
            "Consumo (W/m)",
            min_value=1.0,
            value=10.0,
            step=0.5,
            help="Watts por metro de Jenny (ej: 10 W/m, 14.4 W/m)",
            key="watts_per_meter"
        )
        
        fuentes_input = st.text_input(
            "Fuentes disponibles (W)",
            value="30, 60, 100, 150, 240, 320",
            help="Potencias de fuentes separadas por comas",
            key="fuentes_disponibles"
        )
        
        factor_seguridad = st.slider(
            "Factor de seguridad (%)",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help="Margen adicional para que las fuentes no trabajen al límite",
            key="factor_seguridad"
        )
        
        modo_fuentes = st.radio(
            "Modo de asignación",
            ["Una fuente por corte", "Optimizar fuentes (agrupar)"],
            help="Optimizar agrupa varios cortes en una misma fuente",
            key="modo_asignacion_fuentes"
        )
    
    st.markdown("---")
    
    # Botón de calcular optimización
    if st.button("🚀 Calcular Optimización", type="primary", use_container_width=True, disabled=len(st.session_state.pedidos) == 0):
        with st.spinner("Calculando la distribución óptima..."):
            # Calcular optimización de cortes
            rollos = first_fit_decreasing(st.session_state.pedidos, longitud_rollo)
            st.session_state.resultados = rollos
            
            # Calcular fuentes si está habilitado
            if st.session_state.calcular_fuentes_enabled:
                try:
                    # Parsear fuentes disponibles
                    fuentes_disponibles = sorted([float(w.strip()) 
                                                 for w in st.session_state.fuentes_disponibles.split(',') 
                                                 if w.strip()])
                    
                    if fuentes_disponibles:
                        factor = st.session_state.factor_seguridad / 100 + 1
                        watts_metro = st.session_state.watts_per_meter
                        
                        # Crear diccionario de pedidos para cálculo de fuentes
                        pedidos_dict = {}
                        for p in st.session_state.pedidos:
                            pedidos_dict[p.largo] = pedidos_dict.get(p.largo, 0) + p.cantidad
                        
                        if st.session_state.modo_asignacion_fuentes == "Una fuente por corte":
                            # Modo individual
                            conteo_fuentes = collections.defaultdict(int)
                            detalles = []
                            
                            for largo, cant in pedidos_dict.items():
                                consumo = largo * watts_metro
                                fuente, advertencia = obtener_fuente_adecuada_individual(
                                    consumo, fuentes_disponibles, factor
                                )
                                
                                if fuente:
                                    conteo_fuentes[fuente] += cant
                                    detalles.append({
                                        "Largo (m)": f"{largo:.2f}",
                                        "Cantidad": cant,
                                        "Consumo por Pieza (W)": f"{consumo:.2f}",
                                        "Consumo Ajustado (W)": f"{consumo * factor:.2f}",
                                        "Fuente Asignada (W)": f"{fuente:.0f}",
                                        "Estado": advertencia if advertencia else "✅ OK"
                                    })
                            
                            st.session_state.resultados_fuentes = {
                                "modo": "individual",
                                "conteo": conteo_fuentes,
                                "detalles": detalles
                            }
                        
                        else:
                            # Modo optimizado con estadísticas mejoradas
                            conteo, detalles, estadisticas = optimizar_fuentes_agrupadas(
                                st.session_state.pedidos,
                                watts_metro,
                                fuentes_disponibles,
                                factor
                            )
                            
                            st.session_state.resultados_fuentes = {
                                "modo": "optimizado",
                                "conteo": conteo,
                                "detalles": detalles,
                                "estadisticas": estadisticas
                            }
                    else:
                        st.warning("No se pudieron procesar las fuentes disponibles")
                        st.session_state.resultados_fuentes = None
                
                except Exception as e:
                    st.error(f"Error al calcular fuentes: {e}")
                    st.session_state.resultados_fuentes = None
            else:
                st.session_state.resultados_fuentes = None
        
        st.success("✅ Optimización completada")
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;'>
        <small>Algoritmo: First Fit Decreasing (FFD)</small><br>
        <small style='opacity: 0.7;'>v1.0 • Industrial Optimization System</small>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ÁREA PRINCIPAL - RESULTADOS
# ============================================================================

if st.session_state.resultados is None:
    # Pantalla de bienvenida
    st.markdown("""
    <div class="custom-card" style="text-align: center; padding: 3rem;">
        <h2 style="color: #1f2937; font-weight: 700;">Bienvenido al Optimizador de Jenny</h2>
        <p style="font-size: 1.1rem; color: #374151; margin-top: 1rem;">
            Para comenzar, agrega tus cortes en el panel lateral y presiona 
            <strong style="color: #f97316;">Calcular Optimización</strong>
        </p>
        <br>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <div style="flex: 1; max-width: 300px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📐</div>
                <h4>Define tu rollo</h4>
                <p style="font-size: 0.9rem; color: #64748b;">Configura la longitud estándar del material</p>
            </div>
            <div style="flex: 1; max-width: 300px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
                <h4>Agrega cortes</h4>
                <p style="font-size: 0.9rem; color: #64748b;">Especifica largos y cantidades necesarias</p>
            </div>
            <div style="flex: 1; max-width: 300px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                <h4>Optimiza</h4>
                <p style="font-size: 0.9rem; color: #64748b;">Obtén la mejor distribución de cortes</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Información adicional
    st.markdown("---")
    st.markdown("### 💡 ¿Cómo funciona?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Algoritmo First Fit Decreasing (FFD)**
        
        1. 🔽 Ordena todas las piezas de mayor a menor
        2. 🎯 Coloca cada pieza en el primer rollo donde quepa
        3. ➕ Si no cabe, abre un nuevo rollo
        4. ✨ Minimiza el desperdicio total
        """)
    
    with col2:
        st.markdown("""
        **Beneficios**
        
        - ⚡ Optimización rápida y eficiente
        - 📊 Visualización clara de resultados
        - 💰 Reducción significativa de desperdicios
        - 🎯 Solución probada industrialmente
        """)

else:
    # Mostrar resultados de optimización
    rollos = st.session_state.resultados
    
    # Calcular métricas totales
    total_rollos = len(rollos)
    desperdicio_total = sum(r.desperdicio for r in rollos)
    eficiencia_promedio = sum(r.eficiencia for r in rollos) / len(rollos) if rollos else 0
    metros_utilizados = sum(r.espacio_usado for r in rollos)
    
    # Métricas principales
    st.markdown("## 📊 Resultados de Optimización")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Rollos Utilizados",
            value=total_rollos,
            delta="Optimizado" if total_rollos > 0 else None
        )
    
    with col2:
        st.metric(
            label="Desperdicio Total",
            value=f"{desperdicio_total:.2f}m",
            delta=f"{(desperdicio_total/metros_utilizados*100):.1f}%" if metros_utilizados > 0 else "0%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Eficiencia Promedio",
            value=f"{eficiencia_promedio:.1f}%",
            delta="Excelente" if eficiencia_promedio >= 80 else "Bueno" if eficiencia_promedio >= 60 else "Regular"
        )
    
    with col4:
        st.metric(
            label="Material Usado",
            value=f"{metros_utilizados:.2f}m",
            delta=f"{len(st.session_state.pedidos)} pedidos"
        )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Visualización detallada por rollo
    st.markdown("## 🎨 Distribución de Cortes")
    
    for idx, rollo in enumerate(rollos, 1):
        with st.container():
            st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
            
            # Resumen del rollo
            mostrar_resumen_rollo(rollo, idx)
            
            # Visualización gráfica
            fig = crear_visualizacion_rollo(rollo, idx)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabla detallada de cortes
    st.markdown("---")
    st.markdown("## 📋 Detalle Completo de Cortes")
    
    # Crear tabla con todos los cortes
    datos_tabla = []
    for idx, rollo in enumerate(rollos, 1):
        for num_pieza, pieza in enumerate(rollo.piezas, 1):
            datos_tabla.append({
                "Rollo": f"#{idx}",
                "Pieza": num_pieza,
                "Largo (m)": pieza,
                "Posición": f"{sum(rollo.piezas[:num_pieza-1]):.2f}m - {sum(rollo.piezas[:num_pieza]):.2f}m"
            })
    
    if datos_tabla:
        df_cortes = pd.DataFrame(datos_tabla)
        st.dataframe(
            df_cortes,
            use_container_width=True,
            hide_index=True
        )
        
        # Botón de descarga
        csv = df_cortes.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Descargar Plan de Corte (CSV)",
            data=csv,
            file_name="plan_de_corte.csv",
            mime="text/csv",
            use_container_width=False
        )
    
    # Análisis adicional
    st.markdown("---")
    st.markdown("## 📈 Análisis de Eficiencia")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de eficiencia por rollo
        eficiencias = [r.eficiencia for r in rollos]
        fig_eficiencia = go.Figure()
        
        fig_eficiencia.add_trace(go.Bar(
            x=[f"Rollo {i+1}" for i in range(len(eficiencias))],
            y=eficiencias,
            marker=dict(
                color=eficiencias,
                colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
                showscale=False,
                line=dict(color='white', width=2)
            ),
            text=[f"{e:.1f}%" for e in eficiencias],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=12, color='#0f172a'),
            hovertemplate='<b>%{x}</b><br>Eficiencia: %{y:.1f}%<extra></extra>'
        ))
        
        fig_eficiencia.update_layout(
            title="Eficiencia por Rollo",
            xaxis_title="Rollo",
            yaxis_title="Eficiencia (%)",
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Work Sans', color='#0f172a'),
            title_font=dict(size=16, color='#0f172a'),
            yaxis=dict(range=[0, 100], showgrid=True, gridcolor='#e5e7eb'),
            xaxis=dict(showgrid=False),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        st.plotly_chart(fig_eficiencia, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        # Estadísticas resumen
        st.markdown("### 📊 Estadísticas")
        
        mejor_rollo = max(rollos, key=lambda r: r.eficiencia)
        peor_rollo = min(rollos, key=lambda r: r.eficiencia)
        
        st.markdown(f"""
        - **Mejor rollo:** {rollos.index(mejor_rollo) + 1} ({mejor_rollo.eficiencia:.1f}% eficiencia)
        - **Peor rollo:** {rollos.index(peor_rollo) + 1} ({peor_rollo.eficiencia:.1f}% eficiencia)
        - **Desperdicio promedio:** {desperdicio_total/total_rollos:.2f}m por rollo
        - **Total de piezas:** {sum(len(r.piezas) for r in rollos)} cortadas
        """)
        
        # Indicador de calidad
        if eficiencia_promedio >= 85:
            st.success("✅ Excelente optimización - Desperdicio mínimo")
        elif eficiencia_promedio >= 70:
            st.info("ℹ️ Buena optimización - Desperdicio aceptable")
        else:
            st.warning("⚠️ Optimización mejorable - Considere ajustar los pedidos")
    
    # Resultados de fuentes de energía
    if st.session_state.resultados_fuentes:
        st.markdown("---")
        st.markdown("## ⚡ Resultados de Fuentes")
        
        res_fuentes = st.session_state.resultados_fuentes
        
        # Resumen de fuentes necesarias
        st.markdown("### 📊 Resumen de Fuentes Necesarias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_fuentes_count = sum(res_fuentes["conteo"].values())
            st.metric("Total de Fuentes Requeridas", total_fuentes_count)
            
            st.markdown("**Desglose por potencia:**")
            for potencia, cantidad in sorted(res_fuentes["conteo"].items()):
                st.write(f"- **{potencia:.0f}W**: {cantidad} unidades")
        
        with col2:
            if res_fuentes["modo"] == "individual":
                st.info("**Modo de asignación:** Una fuente por cada corte")
                st.markdown("""
                Cada corte tiene su propia fuente, 
                asegurando máxima independencia y flexibilidad.
                """)
            else:
                st.success("**Modo de asignación:** Fuentes optimizadas (agrupadas)")
                st.markdown("""
                Múltiples cortes agrupados en cada fuente mediante 
                algoritmo FFD, minimizando el número total de fuentes.
                """)
                
                # Mostrar estadísticas mejoradas solo en modo optimizado
                if "estadisticas" in res_fuentes:
                    stats = res_fuentes["estadisticas"]
                    
                    st.markdown("---")
                    st.markdown("**Estadísticas de Eficiencia:**")
                    st.metric(
                        "Eficiencia Promedio", 
                        f"{stats['eficiencia_promedio']:.1f}%",
                        help="Porcentaje de capacidad utilizada vs capacidad total instalada"
                    )
                    
                    if stats["fuentes_sobrecargadas"] > 0:
                        st.warning(f"⚠️ {stats['fuentes_sobrecargadas']} fuente(s) sobrecargada(s)")
                    else:
                        st.success("✅ Todas las fuentes dentro de capacidad")
        
        # Métricas adicionales en modo optimizado
        if res_fuentes["modo"] == "optimizado" and "estadisticas" in res_fuentes:
            st.markdown("---")
            st.markdown("### 📊 Métricas Detalladas de Fuentes")
            
            stats = res_fuentes["estadisticas"]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Consumo Total Real",
                    f"{stats['total_consumo_real']:.1f}W",
                    help="Suma del consumo de todas las piezas"
                )
            
            with col2:
                st.metric(
                    "Capacidad Instalada",
                    f"{stats['total_capacidad_instalada']:.1f}W",
                    help="Suma de potencia de todas las fuentes asignadas"
                )
            
            with col3:
                st.metric(
                    "Capacidad Disponible",
                    f"{stats['capacidad_desperdiciada']:.1f}W",
                    delta=f"{(stats['capacidad_desperdiciada']/stats['total_capacidad_instalada']*100):.1f}% spare",
                    help="Capacidad no utilizada en las fuentes"
                )
            
            with col4:
                st.metric(
                    "Total de Piezas",
                    stats['total_piezas'],
                    help="Número total de cortes a alimentar"
                )
            
            # Gráfico de distribución de uso de fuentes
            if res_fuentes["detalles"]:
                st.markdown("---")
                st.markdown("### 📈 Distribución de Uso de Fuentes")
                
                # Extraer porcentajes de uso
                usos = []
                labels = []
                colors = []
                
                for detalle in res_fuentes["detalles"]:
                    uso_str = detalle["Uso (%)"].replace("%", "")
                    uso = float(uso_str)
                    usos.append(uso)
                    labels.append(detalle["ID"])
                    
                    # Color según el estado
                    if uso >= 90:
                        colors.append('#f59e0b')  # Amarillo - casi al límite
                    elif uso >= 70:
                        colors.append('#10b981')  # Verde - óptimo
                    else:
                        colors.append('#3b82f6')  # Azul - subutilizada
                
                fig_uso = go.Figure()
                
                fig_uso.add_trace(go.Bar(
                    x=labels,
                    y=usos,
                    marker=dict(
                        color=colors,
                        line=dict(color='white', width=2)
                    ),
                    text=[f"{u:.1f}%" for u in usos],
                    textposition='outside',
                    textfont=dict(family='JetBrains Mono', size=11, color='#0f172a'),
                    hovertemplate='<b>%{x}</b><br>Uso: %{y:.1f}%<br><extra></extra>'
                ))
                
                # Líneas de referencia
                fig_uso.add_hline(
                    y=90, line_dash="dash", line_color="#ef4444", 
                    annotation_text="Límite recomendado (90%)",
                    annotation_position="right"
                )
                fig_uso.add_hline(
                    y=70, line_dash="dot", line_color="#10b981",
                    annotation_text="Uso óptimo (70%)",
                    annotation_position="right"
                )
                
                fig_uso.update_layout(
                    title="Porcentaje de Uso por Fuente",
                    xaxis_title="Fuente",
                    yaxis_title="Uso (%)",
                    height=350,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Work Sans', color='#0f172a'),
                    title_font=dict(size=16, color='#0f172a'),
                    yaxis=dict(range=[0, 110], showgrid=True, gridcolor='#e5e7eb'),
                    xaxis=dict(showgrid=False),
                    margin=dict(l=40, r=40, t=80, b=40)
                )
                
                st.plotly_chart(fig_uso, use_container_width=True, config={'displayModeBar': False})
                
                # Interpretación de resultados
                promedio_uso = sum(usos) / len(usos) if usos else 0
                
                if promedio_uso >= 85:
                    st.success("✅ **Excelente optimización:** Las fuentes están bien aprovechadas sin estar sobrecargadas.")
                elif promedio_uso >= 65:
                    st.info("ℹ️ **Buena optimización:** Uso equilibrado de las fuentes con margen de seguridad.")
                else:
                    st.warning("⚠️ **Optimización mejorable:** Las fuentes están subutilizadas. Considera usar fuentes de menor potencia.")
        
        # Detalle de asignación
        if res_fuentes["detalles"]:
            st.markdown("---")
            st.markdown("### 📋 Detalle de Asignación de Fuentes")
            
            df_fuentes = pd.DataFrame(res_fuentes["detalles"])
            
            # Remover la columna interna de color si existe
            if "_color" in df_fuentes.columns:
                df_fuentes = df_fuentes.drop(columns=["_color"])
            
            st.dataframe(df_fuentes, use_container_width=True, hide_index=True)
            
            # Botón de descarga
            csv_fuentes = df_fuentes.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar Plan de Fuentes (CSV)",
                data=csv_fuentes,
                file_name="plan_de_fuentes.csv",
                mime="text/csv",
                use_container_width=False
            )
            
            # Notas importantes
            st.info("""
            💡 **Nota importante:** Cada modelo de fuente de poder tiene un máximo de 
            tiras o metros que puede alimentar según su ficha técnica. Verifica estas 
            especificaciones antes de la instalación final.
            """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 1rem;'>
    <p>Desarrollado con Streamlit • Algoritmo FFD (First Fit Decreasing)</p>
    <p style='font-size: 0.8rem; opacity: 0.7;'>Sistema de Optimización Industrial v2.0 - Con Cálculo Inteligente de Fuentes</p>
</div>
""", unsafe_allow_html=True)
