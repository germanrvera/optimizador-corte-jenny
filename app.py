"""
APLICACIÓN DE OPTIMIZACIÓN DE CORTE DE MATERIAL + FUENTES DE ENERGÍA
======================================================================
Sistema profesional de optimización que minimiza desperdicios y calcula
las fuentes de energía necesarias para tiras LED de forma inteligente.

Características:
- Optimización avanzada de cortes (minimiza desperdicios)
- Manejo automático de cortes grandes
- Cálculo de fuentes de energía (modo individual y optimizado)
- Visualizaciones interactivas con métricas detalladas
- Estadísticas avanzadas de eficiencia
- Exportación de planes de corte y fuentes

Autor: Sistema de Optimización Industrial
Versión: 3.0 - Optimización Profesional
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Tuple
import collections
import math
from PIL import Image
import os
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, LpStatus

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
    /* ============================================
       INDUSTRIAL EDITORIAL - Instrumento de Corte
       Inspiración: Dieter Rams + Swiss Editorial
       ============================================ */
    
    /* Importar tipografías distintivas */
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,700;9..144,900&family=JetBrains+Mono:wght@400;500;700&family=Manrope:wght@300;400;500;600;700;800&display=swap');
    
    /* Variables - Paleta Industrial */
    :root {
        --ink: #0a0a0a;              /* Negro tinta */
        --paper: #f5f1e8;            /* Papel industrial (beige) */
        --paper-light: #faf7f0;      /* Papel más claro */
        --line: #1a1a1a;             /* Líneas técnicas */
        --signal: #ff4500;           /* Naranja señalización */
        --signal-dark: #cc3700;      /* Naranja oscuro */
        --tape: #ffcc00;             /* Amarillo cinta métrica */
        --graphite: #3d3d3d;         /* Grafito */
        --graphite-light: #6b6b6b;   /* Grafito claro */
        --grid: rgba(10, 10, 10, 0.08); /* Líneas de grid */
    }
    
    /* Logo con fondo blanco */
    img {
        background: white !important;
        padding: 12px;
        border: 2px solid var(--ink);
        border-radius: 0;
        box-shadow: 4px 4px 0 var(--ink);
    }
    
    [data-testid="stImage"] {
        background: transparent !important;
    }
    
    /* Fondo principal - papel industrial con grid */
    .main {
        background: var(--paper);
        background-image: 
            linear-gradient(var(--grid) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    .stApp {
        background: var(--paper);
    }
    
    /* Tipografía general */
    html, body, [class*="css"] {
        font-family: 'Manrope', -apple-system, sans-serif;
        color: var(--ink);
    }
    
    /* Títulos con serif editorial */
    h1 {
        font-family: 'Fraunces', Georgia, serif !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        letter-spacing: -0.03em !important;
        color: var(--ink) !important;
        line-height: 1 !important;
        margin-bottom: 0.25rem !important;
    }
    
    h2 {
        font-family: 'Fraunces', Georgia, serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        letter-spacing: -0.02em !important;
        color: var(--ink) !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: var(--ink) !important;
        border-bottom: 2px solid var(--ink) !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h4 {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: var(--graphite) !important;
    }
    
    /* Números y código en monoespaciada */
    code, .stNumberInput input, [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-variant-numeric: tabular-nums !important;
    }
    
    /* Métricas con estilo editorial */
    [data-testid="stMetricValue"] {
        font-family: 'Fraunces', serif !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: var(--ink) !important;
        letter-spacing: -0.03em !important;
        line-height: 1 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        color: var(--graphite) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.2em !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
    }
    
    /* Contenedor de métricas */
    [data-testid="stMetric"] {
        background: var(--paper-light);
        border: 2px solid var(--ink);
        padding: 1.25rem !important;
        position: relative;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: -2px;
        right: -2px;
        width: 20px;
        height: 20px;
        background: var(--signal);
    }
    
    /* Botones - Estilo industrial */
    .stButton > button {
        background: var(--ink) !important;
        color: var(--paper) !important;
        border: 2px solid var(--ink) !important;
        padding: 0.875rem 2rem !important;
        border-radius: 0 !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
        box-shadow: 4px 4px 0 var(--ink) !important;
        transition: all 0.15s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--signal) !important;
        color: var(--ink) !important;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 var(--ink) !important;
    }
    
    .stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0 var(--ink) !important;
    }
    
    /* Botón primario */
    .stButton > button[kind="primary"] {
        background: var(--signal) !important;
        color: var(--ink) !important;
        border-color: var(--ink) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: var(--tape) !important;
    }
    
    /* Inputs */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        border: 2px solid var(--ink) !important;
        border-radius: 0 !important;
        padding: 0.75rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.1rem !important;
        color: var(--ink) !important;
        background: var(--paper-light) !important;
        font-weight: 600 !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: var(--signal) !important;
        box-shadow: 4px 4px 0 var(--signal) !important;
        outline: none !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border: 2px solid var(--ink) !important;
        border-radius: 0 !important;
        background: var(--paper-light) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        color: var(--ink) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--ink) !important;
        border-right: 4px solid var(--signal);
    }
    
    [data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: var(--paper) !important;
        border-color: var(--signal) !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] span:not(.stNumberInput span) {
        color: var(--paper) !important;
    }
    
    [data-testid="stSidebar"] label {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
        color: var(--tape) !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput > div > div > input,
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: var(--paper-light) !important;
        color: var(--ink) !important;
        border: 2px solid var(--paper) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: var(--paper-light) !important;
        border: 2px solid var(--paper) !important;
    }
    
    /* Dataframes */
    .dataframe {
        border: 2px solid var(--ink) !important;
        border-radius: 0 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .dataframe thead tr th {
        background: var(--ink) !important;
        color: var(--paper) !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.1em !important;
        padding: 0.75rem !important;
        border: none !important;
    }
    
    .dataframe tbody tr td {
        font-family: 'JetBrains Mono', monospace !important;
        padding: 0.5rem 0.75rem !important;
        border-top: 1px solid var(--grid) !important;
    }
    
    .dataframe tbody tr:hover {
        background: var(--tape) !important;
    }
    
    /* Alertas - estilo editorial */
    .stAlert {
        border-radius: 0 !important;
        border: 2px solid var(--ink) !important;
        border-left: 8px solid var(--signal) !important;
        background: var(--paper-light) !important;
        font-family: 'Manrope', sans-serif !important;
        box-shadow: 4px 4px 0 var(--ink);
    }
    
    /* Info alerts */
    [data-baseweb="notification"] {
        border-radius: 0 !important;
        font-family: 'Manrope', sans-serif !important;
    }
    
    /* Divisor editorial */
    .custom-divider {
        height: 4px;
        background: var(--ink);
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .custom-divider::before {
        content: '';
        position: absolute;
        left: 0;
        top: -2px;
        width: 60px;
        height: 8px;
        background: var(--signal);
    }
    
    /* Hr personalizado */
    hr {
        border: none !important;
        border-top: 2px solid var(--ink) !important;
        margin: 2rem 0 !important;
    }
    
    /* Tarjetas con estilo Rams/Swiss */
    .ruler-card {
        background: var(--paper-light);
        border: 2px solid var(--ink);
        padding: 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        box-shadow: 6px 6px 0 var(--ink);
        transition: all 0.15s ease;
    }
    
    .ruler-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0 var(--ink);
    }
    
    /* Badge editorial */
    .editorial-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        border: 2px solid var(--ink);
        background: var(--paper-light);
    }
    
    .badge-signal {
        background: var(--signal);
        color: var(--ink);
    }
    
    .badge-tape {
        background: var(--tape);
        color: var(--ink);
    }
    
    .badge-ink {
        background: var(--ink);
        color: var(--paper);
    }
    
    /* Chips de piezas - estilo ticket */
    .piece-chip {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
        background: var(--paper-light);
        border: 2px solid var(--ink);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--ink);
        position: relative;
    }
    
    /* Texto caption */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 500 !important;
        color: var(--graphite-light) !important;
        font-size: 0.8rem !important;
    }
    
    /* Markdown text */
    .stMarkdown p {
        font-family: 'Manrope', sans-serif !important;
        color: var(--ink) !important;
        line-height: 1.6 !important;
    }
    
    /* Animación sutil al cargar */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .ruler-card {
        animation: slideUp 0.3s ease-out;
    }
    
    /* Contenedor de descarga */
    [data-testid="stDownloadButton"] > button {
        background: var(--paper-light) !important;
        color: var(--ink) !important;
        border: 2px solid var(--ink) !important;
        box-shadow: 3px 3px 0 var(--ink) !important;
    }
    
    [data-testid="stDownloadButton"] > button:hover {
        background: var(--tape) !important;
    }
    
    /* Checkboxes y radios */
    .stCheckbox, .stRadio {
        font-family: 'Manrope', sans-serif !important;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] > div {
        background: var(--graphite) !important;
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


class RolloResultado:
    """Representa un rollo resultado con información detallada."""
    
    def __init__(self, rollo_id: str, tipo_rollo: float, cortes: List[float], 
                 desperdicio: float, es_grande: bool = False):
        self.rollo_id = rollo_id
        self.tipo_rollo = tipo_rollo
        self.cortes = cortes
        self.desperdicio = desperdicio
        self.es_grande = es_grande
        self.espacio_usado = sum(cortes)
    
    @property
    def eficiencia(self) -> float:
        """Calcula el porcentaje de eficiencia del rollo."""
        if self.tipo_rollo > 0:
            return (self.espacio_usado / self.tipo_rollo) * 100
        return 0


# ============================================================================
# ALGORITMO DE OPTIMIZACIÓN AVANZADA
# ============================================================================

def optimizar_cortes_pulp(pedidos: List[Pedido], longitud_rollo: float, 
                          max_items_per_pattern: int = None) -> Tuple[str, List[RolloResultado], List[Dict]]:
    """
    Optimiza el corte de material usando algoritmo avanzado de optimización.
    
    Estrategia:
    1. Procesa cortes grandes (>rollo) dividiéndolos en segmentos
    2. Identifica "sobrantes" aprovechables de los segmentos parciales
    3. Intenta colocar cortes pequeños en esos sobrantes primero
    4. Optimiza los cortes restantes con programación lineal
    
    Args:
        pedidos: Lista de objetos Pedido con largo y cantidad
        longitud_rollo: Longitud del rollo madre
        max_items_per_pattern: Máximo número de piezas por patrón (opcional)
    
    Returns:
        Tuple[str, List[RolloResultado], List[Dict]]: (estado, rollos, info_grandes)
    """
    
    # Convertir pedidos a diccionario
    solicitudes_cortes = {}
    for p in pedidos:
        solicitudes_cortes[p.largo] = solicitudes_cortes.get(p.largo, 0) + p.cantidad
    
    # --- 1. Separar cortes normales y grandes ---
    cortes_para_optimizar = {}
    cortes_grandes_externos = []
    
    for largo, cantidad in solicitudes_cortes.items():
        if largo > longitud_rollo:
            cortes_grandes_externos.append({"largo": largo, "cantidad": cantidad})
        else:
            cortes_para_optimizar[largo] = cortes_para_optimizar.get(largo, 0) + cantidad
    
    # --- 2. Procesar cortes grandes ---
    # Para cada corte grande, se usan N-1 rollos completos y queda una "cola"
    # Ejemplo: corte 6m en rollo 5m → 1 rollo completo de 5m + cola de 1m
    rollos_grandes = []
    info_grandes = []
    colas_pendientes = []  # Lista de colas de cortes grandes que necesitan completarse
    
    if cortes_grandes_externos:
        for corte_grande in cortes_grandes_externos:
            largo = corte_grande["largo"]
            cantidad = corte_grande["cantidad"]
            
            for pieza_idx in range(cantidad):
                # Calcular cuántos rollos se necesitan para esta pieza
                rollos_necesarios = math.ceil(largo / longitud_rollo)
                restante = largo
                
                # Procesar los rollos COMPLETOS (todos menos el último)
                for rollo_idx in range(rollos_necesarios - 1):
                    # Rollo completo usado para el corte grande
                    rollo = RolloResultado(
                        rollo_id=f"GRANDE-{largo}m-P{pieza_idx+1}-R{rollo_idx+1}",
                        tipo_rollo=longitud_rollo,
                        cortes=[longitud_rollo],
                        desperdicio=0,
                        es_grande=True
                    )
                    rollos_grandes.append(rollo)
                    restante -= longitud_rollo
                
                # La "cola" es lo que queda al final (menor al rollo)
                # Esta cola se intentará combinar con otros cortes
                if restante > 0:
                    colas_pendientes.append(restante)
            
            # Guardar info para mostrar
            rollos_por_pieza = math.ceil(largo / longitud_rollo)
            info_grandes.append({
                "largo": largo,
                "cantidad": cantidad,
                "rollos_por_pieza": rollos_por_pieza,
                "total_rollos": rollos_por_pieza * cantidad
            })
    
    # --- 3. COMBINAR COLAS CON CORTES NORMALES ---
    # Las colas de cortes grandes + cortes normales se tratan TODOS juntos
    # como cortes normales para ser optimizados por PuLP
    cortes_para_optimizar_con_colas = dict(cortes_para_optimizar)
    
    for cola in colas_pendientes:
        # Redondear para evitar problemas de precisión flotante
        cola_redondeada = round(cola, 2)
        cortes_para_optimizar_con_colas[cola_redondeada] = cortes_para_optimizar_con_colas.get(cola_redondeada, 0) + 1
    
    # Si no hay nada que optimizar, retornar solo los rollos grandes
    if not cortes_para_optimizar_con_colas:
        return "Optimal (Solo Cortes Grandes)", rollos_grandes, info_grandes
    
    cortes_aprovechados_en_sobrantes = len(colas_pendientes)  # Para contabilizar
    
    # --- 4. Generar patrones de corte válidos ---
    # Incluye cortes normales + colas de cortes grandes
    largos_unicos = sorted(list(cortes_para_optimizar_con_colas.keys()), reverse=True)
    
    def generar_patrones(largos_disponibles, largo_maximo, current_pattern=[], max_items=None):
        patrones = []
        suma_actual = sum(current_pattern)
        
        # Límite de items
        if max_items is not None and len(current_pattern) >= max_items:
            if suma_actual <= largo_maximo and current_pattern:
                patrones.append(current_pattern)
            return patrones
        
        # Patrón válido
        if suma_actual <= largo_maximo and current_pattern:
            patrones.append(current_pattern)
        
        # Recursión
        for i, largo in enumerate(largos_disponibles):
            if suma_actual + largo <= largo_maximo:
                nuevos = generar_patrones(
                    largos_disponibles[i:], 
                    largo_maximo, 
                    current_pattern + [largo], 
                    max_items
                )
                patrones.extend(nuevos)
        
        return patrones
    
    todos_patrones = [
        tuple(sorted(p)) 
        for p in generar_patrones(largos_unicos, longitud_rollo, max_items=max_items_per_pattern)
    ]
    patrones_unicos = list(collections.OrderedDict.fromkeys(todos_patrones))
    
    if not patrones_unicos:
        return "No Optimal (Sin patrones válidos)", rollos_grandes, info_grandes
    
    # --- 5. Crear modelo de optimización ---
    problema = LpProblem("Minimizar_Desperdicio_Corte", LpMinimize)
    
    # Variables: cuántas veces usar cada patrón
    x = LpVariable.dicts("UsoPatron", range(len(patrones_unicos)), 0, None, LpInteger)
    
    # Función objetivo: minimizar rollos
    problema += lpSum([x[i] for i in range(len(patrones_unicos))]), "Total_Rollos"
    
    # Restricciones: cumplir todos los pedidos (normales + colas)
    for largo_req, cantidad_req in cortes_para_optimizar_con_colas.items():
        problema += lpSum([
            x[i] * patrones_unicos[i].count(largo_req)
            for i in range(len(patrones_unicos))
        ]) >= cantidad_req, f"Cumplir_Corte_{largo_req}"
    
    # --- 6. Resolver ---
    problema.solve()
    estado = LpStatus[problema.status]
    
    # --- 7. Procesar resultados ---
    rollos_optimizados = []
    
    if estado == 'Optimal':
        rollo_contador = 1
        for i in range(len(patrones_unicos)):
            num_usos = int(x[i].varValue)
            if num_usos > 0:
                for _ in range(num_usos):
                    patron = list(patrones_unicos[i])
                    uso = sum(patron)
                    desperdicio = longitud_rollo - uso
                    
                    rollo = RolloResultado(
                        rollo_id=f"OPT-{rollo_contador}",
                        tipo_rollo=longitud_rollo,
                        cortes=patron,
                        desperdicio=desperdicio,
                        es_grande=False
                    )
                    rollos_optimizados.append(rollo)
                    rollo_contador += 1
    
    # --- 8. Combinar resultados ---
    todos_rollos = rollos_grandes + rollos_optimizados
    
    estado_final = estado
    if cortes_aprovechados_en_sobrantes > 0:
        estado_final = f"Optimal (con {cortes_aprovechados_en_sobrantes} colas integradas)"
    
    return estado_final, todos_rollos, info_grandes


# ============================================================================
# FUNCIONES PARA CÁLCULO DE FUENTES DE ENERGÍA
# ============================================================================

def obtener_fuente_adecuada_individual(consumo_requerido_watts: float, 
                                      fuentes_disponibles_watts: List[float], 
                                      factor_seguridad: float = 1.2) -> Tuple[float, str]:
    """
    Calcula la fuente más pequeña que soporta el consumo con factor de seguridad.
    """
    consumo_ajustado = consumo_requerido_watts * factor_seguridad
    fuentes_suficientes = [f for f in fuentes_disponibles_watts if f >= consumo_ajustado]
    
    if not fuentes_suficientes:
        if fuentes_disponibles_watts:
            max_fuente = max(fuentes_disponibles_watts)
            return max_fuente, f"⚠️ Consumo {consumo_requerido_watts:.2f}W excede fuentes disponibles"
        return None, "❌ No hay fuentes disponibles"
    
    return min(fuentes_suficientes), ""


def optimizar_fuentes_agrupadas(pedidos_list: List[Pedido], 
                                watts_por_metro: float,
                                fuentes_disponibles: List[float],
                                factor_seguridad: float) -> Tuple[Dict, List, Dict]:
    """
    Optimiza asignación de fuentes agrupando cortes (FFD).
    """
    # Expandir a piezas individuales
    piezas_consumo = []
    for p in pedidos_list:
        consumo_real = p.largo * watts_por_metro
        consumo_ajustado = consumo_real * factor_seguridad
        for _ in range(p.cantidad):
            piezas_consumo.append({
                "largo": p.largo,
                "consumo_real": consumo_real,
                "consumo_ajustado": consumo_ajustado
            })
    
    # Ordenar descendente (FFD)
    piezas_consumo.sort(key=lambda x: x["consumo_ajustado"], reverse=True)
    
    # Asignar a fuentes
    fuentes_en_uso = []
    conteo_fuentes = collections.defaultdict(int)
    
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
        
        # Crear nueva fuente
        if not asignada:
            for fuente_w in sorted(fuentes_disponibles):
                if fuente_w >= consumo:
                    fuentes_en_uso.append({
                        "potencia": fuente_w,
                        "restante": fuente_w - consumo,
                        "piezas": [pieza]
                    })
                    conteo_fuentes[fuente_w] += 1
                    break
    
    # Formatear detalles
    detalles = []
    total_consumo = 0
    total_capacidad = 0
    fuentes_sobrecargadas = 0
    
    for idx, fuente in enumerate(fuentes_en_uso, 1):
        piezas_str = ", ".join([f"{p['largo']:.2f}m ({p['consumo_real']:.2f}W)" 
                                for p in fuente["piezas"]])
        consumo_fuente = fuente["potencia"] - fuente["restante"]
        uso_pct = (consumo_fuente / fuente["potencia"]) * 100 if fuente["potencia"] > 0 else 0
        
        total_consumo += consumo_fuente
        total_capacidad += fuente["potencia"]
        
        if fuente["restante"] < 0:
            fuentes_sobrecargadas += 1
            estado = "⚠️ SOBRECARGA"
        elif uso_pct >= 90:
            estado = "🟡 Casi al límite"
        elif uso_pct >= 70:
            estado = "🟢 Óptimo"
        else:
            estado = "🔵 Subutilizada"
        
        detalles.append({
            "ID": f"F-{idx}",
            "Potencia (W)": f"{fuente['potencia']:.0f}",
            "N° Piezas": len(fuente["piezas"]),
            "Cortes": piezas_str,
            "Consumo (W)": f"{consumo_fuente:.2f}",
            "Uso (%)": f"{uso_pct:.1f}%",
            "Disponible (W)": f"{max(0, fuente['restante']):.2f}",
            "Estado": estado
        })
    
    # Estadísticas
    eficiencia = (total_consumo / total_capacidad * 100) if total_capacidad > 0 else 0
    estadisticas = {
        "total_fuentes": len(fuentes_en_uso),
        "total_consumo_real": total_consumo,
        "total_capacidad_instalada": total_capacidad,
        "capacidad_desperdiciada": total_capacidad - total_consumo,
        "eficiencia_promedio": eficiencia,
        "fuentes_sobrecargadas": fuentes_sobrecargadas,
        "total_piezas": len(piezas_consumo)
    }
    
    return conteo_fuentes, detalles, estadisticas


# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def crear_visualizacion_rollo_pulp(rollo: RolloResultado, numero: int) -> go.Figure:
    """Crea visualización estilo instrumento de medición industrial."""
    fig = go.Figure()
    
    # Paleta industrial - como cinta métrica
    colores_industriales = [
        '#ff4500',  # Signal orange
        '#1a1a1a',  # Ink
        '#ffcc00',  # Tape yellow
        '#3d3d3d',  # Graphite
        '#cc3700',  # Signal dark
        '#6b6b6b',  # Graphite light
        '#ff6b35',  # Orange medium
        '#2d2d2d',  # Dark gray
    ]
    
    posicion = 0
    for idx, corte in enumerate(rollo.cortes):
        color = colores_industriales[idx % len(colores_industriales)]
        porcentaje = (corte / rollo.tipo_rollo) * 100
        
        # Color del texto según el color de fondo
        text_color = '#f5f1e8' if color in ['#1a1a1a', '#3d3d3d', '#2d2d2d', '#cc3700'] else '#0a0a0a'
        
        fig.add_trace(go.Bar(
            y=['Rollo'],
            x=[corte],
            orientation='h',
            name=f'Corte {idx+1}',
            marker=dict(
                color=color,
                line=dict(color='#0a0a0a', width=2)
            ),
            text=f'<b style="font-family:Fraunces,serif;font-size:18px;">{corte}m</b>',
            textposition='inside',
            textfont=dict(color=text_color, size=16, family='Fraunces'),
            hovertemplate=f'<b>Corte {idx+1}</b><br>Largo: {corte}m<br>{porcentaje:.1f}% del rollo<extra></extra>',
            base=posicion
        ))
        posicion += corte
    
    # Desperdicio con estilo de cinta
    if rollo.desperdicio > 0:
        porcentaje_desp = (rollo.desperdicio / rollo.tipo_rollo) * 100
        
        fig.add_trace(go.Bar(
            y=['Rollo'],
            x=[rollo.desperdicio],
            orientation='h',
            name='Desperdicio',
            marker=dict(
                color='#faf7f0',
                pattern=dict(
                    shape='/',
                    fgcolor='#1a1a1a',
                    size=8,
                    solidity=0.4
                ),
                line=dict(color='#0a0a0a', width=2)
            ),
            text=f'<b>{rollo.desperdicio:.2f}m</b>',
            textposition='inside',
            textfont=dict(color='#0a0a0a', size=13, family='JetBrains Mono'),
            hovertemplate=f'<b>Desperdicio</b><br>{rollo.desperdicio:.2f}m<br>{porcentaje_desp:.1f}% del rollo<extra></extra>',
            base=posicion
        ))
    
    # Layout estilo regla técnica
    fig.update_layout(
        barmode='stack',
        showlegend=False,
        height=120,
        margin=dict(l=20, r=20, t=20, b=40),
        plot_bgcolor='#faf7f0',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[0, rollo.tipo_rollo],
            showgrid=True,
            gridcolor='#0a0a0a',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='#0a0a0a',
            zerolinewidth=3,
            title=dict(
                text=f"ESCALA: 0 — {rollo.tipo_rollo:.0f}m",
                font=dict(size=10, color='#3d3d3d', family='Manrope')
            ),
            tickfont=dict(family='JetBrains Mono', size=10, color='#3d3d3d'),
            dtick=1 if rollo.tipo_rollo <= 10 else 2,
            showline=True,
            linecolor='#0a0a0a',
            linewidth=2,
            ticks='outside',
            ticklen=6,
            tickcolor='#0a0a0a'
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        hovermode='closest',
        font=dict(family='Manrope'),
        bargap=0.2
    )
    
    return fig


# ============================================================================
# INICIALIZACIÓN DEL ESTADO
# ============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# ============================================================================
# SISTEMA DE AUTENTICACIÓN
# ============================================================================

def check_authentication():
    """Verifica autenticación del usuario."""
    if st.session_state.authenticated:
        return True
    
    # Header editorial de login
    st.markdown("""
    <div style='padding: 3rem 0 2rem 0;'>
        <div style="
            display: inline-block;
            background: #0a0a0a;
            color: #ffcc00;
            padding: 0.3rem 0.8rem;
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-size: 0.7rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        ">
            ACCESO RESTRINGIDO
        </div>
        <h1 style="
            font-family: 'Fraunces', serif !important;
            font-size: 4rem !important;
            font-weight: 900 !important;
            color: #0a0a0a !important;
            line-height: 0.95 !important;
            letter-spacing: -0.04em !important;
            margin: 0 0 1rem 0 !important;
        ">
            Optimizador<br><span style="color: #ff4500;">Jenny</span>
        </h1>
        <p style="
            font-family: 'Manrope', sans-serif;
            font-size: 1rem;
            color: #3d3d3d;
            margin: 0;
            font-weight: 500;
        ">
            Instrumento profesional de corte y optimización
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo
    try:
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo, use_container_width=True)
    except:
        pass
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-size: 0.7rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: #0a0a0a;
            margin-bottom: 0.5rem;
        ">
            Correo Autorizado
        </div>
        """, unsafe_allow_html=True)
        
        email_input = st.text_input("Email", placeholder="operador@jenny.com", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("INGRESAR AL SISTEMA", type="primary", use_container_width=True):
            if email_input:
                email = email_input.strip().lower()
                
                try:
                    emails_str = st.secrets.get("emails_autorizados", "")
                    EMAILS_AUTORIZADOS = [e.strip().lower() for e in emails_str.split(',') if e.strip()]
                except:
                    EMAILS_AUTORIZADOS = ["admin@jenny.com", "gerencia@jenny.com", "ejemplo@gmail.com"]
                    st.warning("Usando emails de prueba")
                
                if email in EMAILS_AUTORIZADOS:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.success(f"Acceso concedido · {email}")
                    st.rerun()
                else:
                    st.error("Email no autorizado")
            else:
                st.warning("Ingresa un email válido")
    
    st.markdown("""
    <div style="
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 2px solid #0a0a0a;
        text-align: center;
    ">
        <p style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #6b6b6b;
            letter-spacing: 0.1em;
            margin: 0;
        ">
            v3.0 · INSTRUMENTO INDUSTRIAL
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    return False

if not check_authentication():
    st.stop()

# ============================================================================
# ESTADOS DE LA APLICACIÓN
# ============================================================================

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

if 'resultados' not in st.session_state:
    st.session_state.resultados = None

if 'info_grandes' not in st.session_state:
    st.session_state.info_grandes = []

if 'resultados_fuentes' not in st.session_state:
    st.session_state.resultados_fuentes = None

if 'calcular_fuentes_enabled' not in st.session_state:
    st.session_state.calcular_fuentes_enabled = False

# ============================================================================
# HEADER
# ============================================================================

col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    try:
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png")
            st.image(logo, width=140)
    except:
        st.markdown("""
        <div style="
            width: 100px;
            height: 100px;
            background: #0a0a0a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Fraunces', serif;
            font-size: 3rem;
            font-weight: 900;
            color: #f5f1e8;
            border: 3px solid #0a0a0a;
            box-shadow: 6px 6px 0 #ff4500;
        ">
            J
        </div>
        """, unsafe_allow_html=True)

with col_titulo:
    st.markdown("""
    <div style="margin-top: 0.5rem;">
        <div style="
            display: inline-block;
            background: #0a0a0a;
            color: #ffcc00;
            padding: 0.2rem 0.75rem;
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-size: 0.65rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        ">
            INSTRUMENTO DE CORTE · JENNY
        </div>
        <h1 style="
            font-family: 'Fraunces', serif !important;
            font-size: 3.5rem !important;
            font-weight: 900 !important;
            color: #0a0a0a !important;
            line-height: 0.95 !important;
            letter-spacing: -0.04em !important;
            margin: 0 !important;
        ">
            Optimizador<br><span style="color: #ff4500;">de Corte</span>
        </h1>
        <p style="
            font-family: 'Manrope', sans-serif;
            color: #3d3d3d;
            font-size: 0.9rem;
            margin-top: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.05em;
        ">
            Minimización de desperdicio · Cálculo de fuentes
        </p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    st.markdown(f"""
    <div style="
        text-align: right;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #3d3d3d;
        margin-top: 0.5rem;
    ">
        OPERADOR: <strong style="color: #0a0a0a;">{st.session_state.user_email}</strong>
    </div>
    """, unsafe_allow_html=True)
with col3:
    if st.button("CERRAR SESIÓN", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.pedidos = []
        st.session_state.resultados = None
        st.rerun()

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        font-size: 0.7rem;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: #ffcc00;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ffcc00;
        margin-bottom: 1.5rem;
    ">
        Panel de Control
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Rollo Madre")
    longitud_rollo = st.selectbox(
        "Longitud del rollo",
        options=[5.0, 10.0, 20.0],
        index=1,  # 10m por defecto
        format_func=lambda x: f"{x:.0f} metros"
    )
    
    st.markdown("---")
    st.markdown("### Gestión de Cortes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        largo_pieza = st.number_input(
            "Largo (m)",
            min_value=0.1,
            max_value=1000.0,
            value=2.0,
            step=0.1,
            help="Puede ser mayor al rollo"
        )
    
    with col2:
        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            max_value=1000,
            value=1
        )
    
    # Info si es grande
    if largo_pieza > longitud_rollo:
        rollos_necesarios = math.ceil(largo_pieza / longitud_rollo)
        st.info(f"📏 Corte de {largo_pieza}m requiere {rollos_necesarios} rollos")
    
    if st.button("AGREGAR CORTE", use_container_width=True):
        st.session_state.pedidos.append(Pedido(largo_pieza, cantidad))
        st.success(f"✅ Agregado: {cantidad}× {largo_pieza}m")
        st.rerun()
    
    st.markdown("---")
    
    # Mostrar pedidos
    if st.session_state.pedidos:
        st.markdown("### Cortes Actuales")
        
        df = pd.DataFrame([
            {"Largo (m)": p.largo, "Cantidad": p.cantidad, "Total (m)": p.largo * p.cantidad}
            for p in st.session_state.pedidos
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total_piezas = sum(p.cantidad for p in st.session_state.pedidos)
        total_metros = sum(p.largo * p.cantidad for p in st.session_state.pedidos)
        st.info(f"**Total:** {total_piezas} piezas • {total_metros:.2f}m")
        
        if st.button("LIMPIAR", use_container_width=True):
            st.session_state.pedidos = []
            st.session_state.resultados = None
            st.rerun()
    else:
        st.info("No hay cortes agregados")
    
    st.markdown("---")
    
    # Fuentes (opcional)
    st.markdown("### Fuentes (Opcional)")
    calc_fuentes = st.checkbox("Calcular fuentes", value=st.session_state.calcular_fuentes_enabled)
    st.session_state.calcular_fuentes_enabled = calc_fuentes
    
    if calc_fuentes:
        watts_metro = st.number_input("Consumo (W/m)", min_value=1.0, value=10.0, step=0.5)
        fuentes_input = st.text_input("Fuentes (W)", value="30, 60, 100, 150, 240")
        factor_seg = st.slider("Factor seguridad (%)", 5, 50, 20, 5)
        modo_fuentes = st.radio("Modo", ["Una fuente por corte", "Optimizar (agrupar)"])
        
        st.session_state.watts_metro = watts_metro
        st.session_state.fuentes_input = fuentes_input
        st.session_state.factor_seg = factor_seg
        st.session_state.modo_fuentes = modo_fuentes
    
    st.markdown("---")
    
    # Botón optimizar
    if st.button("CALCULAR OPTIMIZACIÓN", type="primary", use_container_width=True, 
                 disabled=len(st.session_state.pedidos) == 0):
        with st.spinner("Calculando la mejor optimización..."):
            # Lógica automática para max_items según complejidad
            num_cortes_diferentes = len(set(p.largo for p in st.session_state.pedidos))
            
            if num_cortes_diferentes <= 5:
                max_items = None  # Óptimo absoluto (pocos cortes, rápido)
            elif num_cortes_diferentes <= 10:
                max_items = 7     # Muy bueno (equilibrado)
            elif num_cortes_diferentes <= 20:
                max_items = 5     # Bueno (rápido)
            else:
                max_items = 3     # Suficiente (muy rápido para casos complejos)
            
            estado, rollos, info_grandes = optimizar_cortes_pulp(
                st.session_state.pedidos, 
                longitud_rollo,
                max_items
            )
            
            st.session_state.resultados = rollos
            st.session_state.info_grandes = info_grandes
            st.session_state.estado_solucion = estado
            
            # Calcular fuentes si está habilitado
            if st.session_state.calcular_fuentes_enabled:
                try:
                    fuentes_disp = sorted([float(w.strip()) for w in st.session_state.fuentes_input.split(',') if w.strip()])
                    factor = st.session_state.factor_seg / 100 + 1
                    
                    if st.session_state.modo_fuentes == "Una fuente por corte":
                        pedidos_dict = {}
                        for p in st.session_state.pedidos:
                            pedidos_dict[p.largo] = pedidos_dict.get(p.largo, 0) + p.cantidad
                        
                        conteo = collections.defaultdict(int)
                        detalles = []
                        
                        for largo, cant in pedidos_dict.items():
                            consumo = largo * st.session_state.watts_metro
                            fuente, adv = obtener_fuente_adecuada_individual(consumo, fuentes_disp, factor)
                            
                            if fuente:
                                conteo[fuente] += cant
                                detalles.append({
                                    "Largo (m)": f"{largo:.2f}",
                                    "Cantidad": cant,
                                    "Consumo (W)": f"{consumo:.2f}",
                                    "Fuente (W)": f"{fuente:.0f}",
                                    "Estado": adv if adv else "✅ OK"
                                })
                        
                        st.session_state.resultados_fuentes = {
                            "modo": "individual",
                            "conteo": conteo,
                            "detalles": detalles
                        }
                    else:
                        conteo, detalles, stats = optimizar_fuentes_agrupadas(
                            st.session_state.pedidos,
                            st.session_state.watts_metro,
                            fuentes_disp,
                            factor
                        )
                        
                        st.session_state.resultados_fuentes = {
                            "modo": "optimizado",
                            "conteo": conteo,
                            "detalles": detalles,
                            "estadisticas": stats
                        }
                except Exception as e:
                    st.error(f"Error en fuentes: {e}")
                    st.session_state.resultados_fuentes = None
            else:
                st.session_state.resultados_fuentes = None
        
        st.success("✅ Optimización completada")
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1rem 0;
        margin-top: 1rem;
    ">
        <div style="
            font-family: 'Fraunces', serif;
            font-size: 1.5rem;
            font-weight: 900;
            color: #ffcc00;
            letter-spacing: -0.02em;
            line-height: 1;
        ">
            Jenny
        </div>
        <div style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #888;
            letter-spacing: 0.15em;
            margin-top: 0.5rem;
        ">
            v3.0 · INDUSTRIAL
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

if st.session_state.resultados is None:
    # Pantalla de bienvenida estilo editorial industrial
    st.markdown("""
    <div style="
        background: #faf7f0;
        border: 2px solid #0a0a0a;
        padding: 3rem 2.5rem;
        margin: 2rem 0;
        box-shadow: 8px 8px 0 #0a0a0a;
        position: relative;
    ">
        <div style="
            position: absolute;
            top: -2px;
            left: -2px;
            background: #ff4500;
            color: #0a0a0a;
            padding: 0.3rem 0.8rem;
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-size: 0.65rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            border: 2px solid #0a0a0a;
        ">
            INICIO
        </div>
        
        <div style="margin-top: 1rem;">
            <h2 style="
                font-family: 'Fraunces', serif !important;
                font-size: 2.5rem !important;
                font-weight: 900 !important;
                color: #0a0a0a !important;
                margin: 0 0 1rem 0 !important;
                letter-spacing: -0.03em !important;
                line-height: 1 !important;
            ">
                Listo para<br>calcular.
            </h2>
            <p style="
                font-family: 'Manrope', sans-serif;
                font-size: 1rem;
                color: #3d3d3d;
                margin: 1rem 0 2rem 0;
                max-width: 500px;
                line-height: 1.5;
            ">
                Configura el rollo y agrega los cortes en el panel lateral. 
                El sistema calculará la distribución óptima minimizando desperdicios.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Proceso en 3 pasos - estilo editorial
    col1, col2, col3 = st.columns(3)
    
    pasos = [
        {
            "num": "01",
            "titulo": "CONFIGURAR",
            "texto": "Selecciona la longitud del rollo madre",
            "color": "#ff4500"
        },
        {
            "num": "02", 
            "titulo": "INGRESAR",
            "texto": "Agrega los cortes con su largo y cantidad",
            "color": "#ffcc00"
        },
        {
            "num": "03",
            "titulo": "CALCULAR",
            "texto": "Obtén el plan de corte optimizado",
            "color": "#0a0a0a"
        }
    ]
    
    for col, paso in zip([col1, col2, col3], pasos):
        with col:
            st.markdown(f"""
            <div style="
                background: #f5f1e8;
                border: 2px solid #0a0a0a;
                padding: 1.5rem;
                min-height: 180px;
                position: relative;
                box-shadow: 4px 4px 0 #0a0a0a;
            ">
                <div style="
                    font-family: 'Fraunces', serif;
                    font-size: 3rem;
                    font-weight: 900;
                    color: {paso['color']};
                    line-height: 1;
                    margin-bottom: 0.5rem;
                    letter-spacing: -0.05em;
                ">
                    {paso['num']}
                </div>
                <div style="
                    font-family: 'Manrope', sans-serif;
                    font-weight: 800;
                    font-size: 0.85rem;
                    letter-spacing: 0.2em;
                    text-transform: uppercase;
                    color: #0a0a0a;
                    margin-bottom: 0.5rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 2px solid #0a0a0a;
                ">
                    {paso['titulo']}
                </div>
                <div style="
                    font-family: 'Manrope', sans-serif;
                    font-size: 0.85rem;
                    color: #3d3d3d;
                    line-height: 1.4;
                ">
                    {paso['texto']}
                </div>
            </div>
            """, unsafe_allow_html=True)

else:
    # Resultados
    rollos = st.session_state.resultados
    info_grandes = st.session_state.info_grandes
    estado = st.session_state.estado_solucion
    
    st.markdown("## Resultados")
    
    # Info de cortes grandes
    if info_grandes:
        st.warning("### 📏 Cortes Grandes Detectados")
        for detalle in info_grandes:
            st.info(f"""
            - **{detalle['cantidad']}× piezas de {detalle['largo']}m**
              - Cada pieza requiere **{detalle['rollos_por_pieza']} rollos**
              - Total: **{detalle['total_rollos']} rollos**
            """)
        st.markdown("---")
    
    # Métricas
    total_rollos = len(rollos)
    desperdicio_total = sum(r.desperdicio for r in rollos)
    metros_usados = sum(r.espacio_usado for r in rollos)
    eficiencia = (metros_usados / (total_rollos * rollos[0].tipo_rollo) * 100) if total_rollos > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rollos", total_rollos, estado)
    
    with col2:
        st.metric("Desperdicio", f"{desperdicio_total:.2f}m", 
                 delta=f"{(desperdicio_total/metros_usados*100):.1f}%" if metros_usados > 0 else "0%",
                 delta_color="inverse")
    
    with col3:
        st.metric("Eficiencia", f"{eficiencia:.1f}%",
                 "Excelente" if eficiencia >= 80 else "Bueno")
    
    with col4:
        st.metric("Material Usado", f"{metros_usados:.2f}m", 
                 f"{len(st.session_state.pedidos)} cortes")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Visualización
    st.markdown("## 🎨 Distribución de Cortes")
    st.caption("📊 Ordenados de menor a mayor desperdicio (más eficientes primero)")
    
    # Ordenar rollos: primero los más eficientes (menos desperdicio)
    rollos_ordenados = sorted(rollos, key=lambda r: r.desperdicio)
    
    for idx, rollo in enumerate(rollos_ordenados, 1):
        # Determinar estado con paleta industrial
        if rollo.eficiencia >= 95:
            badge_bg = "#ff4500"  # Signal orange
            badge_color = "#0a0a0a"
            badge_text = "ÓPTIMO"
        elif rollo.eficiencia >= 80:
            badge_bg = "#ffcc00"  # Tape yellow
            badge_color = "#0a0a0a"
            badge_text = "EFICIENTE"
        elif rollo.eficiencia >= 60:
            badge_bg = "#faf7f0"  # Paper light
            badge_color = "#0a0a0a"
            badge_text = "ACEPTABLE"
        else:
            badge_bg = "#0a0a0a"  # Ink
            badge_color = "#f5f1e8"
            badge_text = "REVISAR"
        
        tipo_rollo = "EMPALME" if rollo.es_grande else "CORTE DIRECTO"
        
        with st.container():
            # Header estilo editorial/industrial
            st.markdown(f"""
            <div style="
                background: #faf7f0;
                border: 2px solid #0a0a0a;
                padding: 1.5rem 1.75rem;
                margin-bottom: 0;
                box-shadow: 6px 6px 0 #0a0a0a;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: -2px;
                    right: -2px;
                    background: {badge_bg};
                    color: {badge_color};
                    padding: 0.5rem 1rem;
                    border: 2px solid #0a0a0a;
                    font-family: 'Manrope', sans-serif;
                    font-weight: 800;
                    font-size: 0.75rem;
                    letter-spacing: 0.2em;
                    text-transform: uppercase;
                ">
                    {badge_text}
                </div>
                
                <div style="display: flex; align-items: baseline; gap: 1rem; margin-bottom: 0.5rem;">
                    <span style="
                        font-family: 'Fraunces', serif;
                        font-size: 2.5rem;
                        font-weight: 900;
                        color: #0a0a0a;
                        line-height: 1;
                        letter-spacing: -0.03em;
                    ">
                        N°{idx:02d}
                    </span>
                    <span style="
                        font-family: 'Manrope', sans-serif;
                        font-weight: 700;
                        font-size: 0.7rem;
                        letter-spacing: 0.2em;
                        text-transform: uppercase;
                        color: #3d3d3d;
                        padding: 0.25rem 0.75rem;
                        border: 1px solid #3d3d3d;
                    ">
                        {tipo_rollo}
                    </span>
                </div>
                
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.85rem;
                    color: #3d3d3d;
                    font-weight: 500;
                    letter-spacing: 0.05em;
                ">
                    ROLLO DE {rollo.tipo_rollo:.0f}M · {len(rollo.cortes)} PIEZAS
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Contenedor de datos
            st.markdown("""
            <div style="
                background: #f5f1e8;
                border: 2px solid #0a0a0a;
                border-top: none;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            ">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Label de piezas
                st.markdown("""
                <div style="
                    font-family: 'Manrope', sans-serif;
                    font-weight: 700;
                    font-size: 0.7rem;
                    letter-spacing: 0.2em;
                    text-transform: uppercase;
                    color: #3d3d3d;
                    margin-bottom: 0.5rem;
                ">
                    Composición del Corte
                </div>
                """, unsafe_allow_html=True)
                
                # Chips estilo ticket industrial
                chips_style = "display:inline-block;padding:0.5rem 0.9rem;margin:0.25rem 0.25rem 0.25rem 0;background:#faf7f0;border:2px solid #0a0a0a;font-family:'JetBrains Mono',monospace;font-size:0.95rem;color:#0a0a0a;font-weight:700;box-shadow:2px 2px 0 #0a0a0a;"
                
                piezas_html = ""
                for pieza in rollo.cortes:
                    piezas_html += f'<span style="{chips_style}">{pieza}m</span>'
                
                st.markdown(piezas_html, unsafe_allow_html=True)
            
            with col2:
                st.metric("Eficiencia", f"{rollo.eficiencia:.1f}%")
            
            with col3:
                st.metric("Desperdicio", f"{rollo.desperdicio:.2f}m",
                         label_visibility="visible")
            
            # Visualización gráfica
            fig = crear_visualizacion_rollo_pulp(rollo, idx)
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False},
                key=f"rollo_chart_{idx}_{rollo.rollo_id}"
            )
            
            # Cerrar el contenedor de datos
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Tabla detallada
    st.markdown("---")
    st.markdown("## 📋 Detalle Completo")
    
    datos = []
    for idx, rollo in enumerate(rollos_ordenados, 1):
        for num, pieza in enumerate(rollo.cortes, 1):
            datos.append({
                "Rollo": f"#{idx}",
                "Tipo": "Grande" if rollo.es_grande else "Optimizado",
                "Pieza": num,
                "Largo (m)": pieza,
                "Eficiencia (%)": f"{rollo.eficiencia:.1f}"
            })
    
    if datos:
        df_cortes = pd.DataFrame(datos)
        st.dataframe(df_cortes, use_container_width=True, hide_index=True)
        
        csv = df_cortes.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Descargar Plan de Corte (CSV)",
            csv,
            "plan_corte_jenny.csv",
            "text/csv"
        )
    
    # Resultados de fuentes (si los hay)
    if st.session_state.resultados_fuentes:
        st.markdown("---")
        st.markdown("## ⚡ Resultados de Fuentes")
        
        res_f = st.session_state.resultados_fuentes
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_f = sum(res_f["conteo"].values())
            st.metric("Total Fuentes", total_f)
            
            st.markdown("**Desglose:**")
            for pot, cant in sorted(res_f["conteo"].items()):
                st.write(f"- **{pot:.0f}W**: {cant} unidades")
        
        with col2:
            if res_f["modo"] == "individual":
                st.info("**Modo:** Una fuente por corte")
            else:
                st.success("**Modo:** Optimizado (agrupado)")
                
                if "estadisticas" in res_f:
                    stats = res_f["estadisticas"]
                    st.metric("Eficiencia", f"{stats['eficiencia_promedio']:.1f}%")
                    
                    if stats["fuentes_sobrecargadas"] > 0:
                        st.warning(f"⚠️ {stats['fuentes_sobrecargadas']} sobrecargada(s)")
                    else:
                        st.success("✅ Todo OK")
        
        # Detalles
        if res_f["detalles"]:
            st.markdown("---")
            st.markdown("### 📋 Detalle de Fuentes")
            
            df_f = pd.DataFrame(res_f["detalles"])
            st.dataframe(df_f, use_container_width=True, hide_index=True)
            
            csv_f = df_f.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Descargar Plan de Fuentes (CSV)",
                csv_f,
                "plan_fuentes.csv",
                "text/csv"
            )

# Footer editorial
st.markdown("""
<div style="
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 2px solid #0a0a0a;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #0a0a0a;
        letter-spacing: -0.02em;
    ">
        Optimizador <span style="color: #ff4500;">Jenny</span>
    </div>
    <div style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #6b6b6b;
        letter-spacing: 0.1em;
    ">
        v3.0 · INSTRUMENTO INDUSTRIAL
    </div>
</div>
""", unsafe_allow_html=True)
