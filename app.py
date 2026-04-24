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
    /* Logo con fondo blanco */
    img {
        background: white !important;
        background-color: white !important;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Contenedor de imágenes sin fondo */
    [data-testid="stImage"] {
        background: transparent !important;
    }
    
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
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Forzar color en inputs del sidebar */
    [data-testid="stSidebar"] .stNumberInput > div > div > input {
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Labels de inputs en sidebar */
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
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
    
    /* Solo títulos y textos en blanco, NO inputs */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span:not(.stNumberInput span),
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
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
    """Crea visualización profesional horizontal de un rollo."""
    fig = go.Figure()
    
    # Paleta de colores profesional con gradientes
    colores_base = [
        '#f97316',  # Naranja vibrante
        '#10b981',  # Verde esmeralda
        '#3b82f6',  # Azul vibrante
        '#8b5cf6',  # Violeta
        '#ec4899',  # Rosa
        '#14b8a6',  # Turquesa
        '#f59e0b',  # Ámbar
        '#6366f1',  # Índigo
    ]
    
    posicion = 0
    for idx, corte in enumerate(rollo.cortes):
        color = colores_base[idx % len(colores_base)]
        
        # Calcular porcentaje del corte respecto al rollo
        porcentaje = (corte / rollo.tipo_rollo) * 100
        
        fig.add_trace(go.Bar(
            y=['Rollo'],
            x=[corte],
            orientation='h',
            name=f'Corte {idx+1}',
            marker=dict(
                color=color,
                line=dict(color='white', width=3),
                pattern=dict(shape="", fillmode="overlay")
            ),
            text=f'<b>{corte}m</b><br><span style="font-size:10px;opacity:0.9;">{porcentaje:.0f}%</span>',
            textposition='inside',
            textfont=dict(color='white', size=14, family='Work Sans'),
            hovertemplate=f'<b>Corte {idx+1}</b><br>Largo: {corte}m<br>% del rollo: {porcentaje:.1f}%<extra></extra>',
            base=posicion
        ))
        posicion += corte
    
    # Desperdicio con diseño distintivo
    if rollo.desperdicio > 0:
        porcentaje_desp = (rollo.desperdicio / rollo.tipo_rollo) * 100
        
        fig.add_trace(go.Bar(
            y=['Rollo'],
            x=[rollo.desperdicio],
            orientation='h',
            name='Desperdicio',
            marker=dict(
                color='#fef3c7',
                pattern=dict(
                    shape='/',
                    fgcolor='#d97706',
                    size=10,
                    solidity=0.3
                ),
                line=dict(color='#f59e0b', width=3)
            ),
            text=f'<b>✂️ {rollo.desperdicio:.2f}m</b><br><span style="font-size:10px;">{porcentaje_desp:.0f}%</span>',
            textposition='inside',
            textfont=dict(color='#92400e', size=12, family='Work Sans'),
            hovertemplate=f'<b>Desperdicio</b><br>{rollo.desperdicio:.2f}m<br>{porcentaje_desp:.1f}% del rollo<extra></extra>',
            base=posicion
        ))
    
    # Layout profesional
    fig.update_layout(
        barmode='stack',
        showlegend=False,
        height=140,
        margin=dict(l=20, r=20, t=30, b=40),
        plot_bgcolor='rgba(248, 250, 252, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[0, rollo.tipo_rollo],
            showgrid=True,
            gridcolor='#e5e7eb',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='#cbd5e1',
            zerolinewidth=2,
            title=dict(
                text=f"Metros (0 - {rollo.tipo_rollo:.0f}m)",
                font=dict(size=11, color='#64748b', family='Work Sans')
            ),
            tickfont=dict(family='JetBrains Mono', size=10, color='#64748b'),
            dtick=1 if rollo.tipo_rollo <= 10 else 2
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        hovermode='closest',
        font=dict(family='Work Sans'),
        bargap=0.3
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
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #1f2937;'>🔐 Acceso al Optimizador de Jenny</h1>
        <p style='color: #6b7280; font-size: 1.1rem;'>Ingresa tu email autorizado</p>
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
        email_input = st.text_input("📧 Email", placeholder="tu-email@ejemplo.com")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Ingresar al Sistema", type="primary", use_container_width=True):
            if email_input:
                email = email_input.strip().lower()
                
                try:
                    emails_str = st.secrets.get("emails_autorizados", "")
                    EMAILS_AUTORIZADOS = [e.strip().lower() for e in emails_str.split(',') if e.strip()]
                except:
                    EMAILS_AUTORIZADOS = ["admin@jenny.com", "gerencia@jenny.com", "ejemplo@gmail.com"]
                    st.warning("⚠️ Usando emails de prueba")
                
                if email in EMAILS_AUTORIZADOS:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.success(f"✅ Acceso concedido para {email}")
                    st.rerun()
                else:
                    st.error("❌ Email no autorizado")
            else:
                st.warning("⚠️ Ingresa un email válido")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #9ca3af;'>
        <p>¿Necesitas acceso? Contacta al administrador</p>
        <p style='font-size: 0.8rem;'>Optimizador Jenny v3.0 - Optimización Profesional</p>
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
            st.image(logo, width=150)
    except:
        st.markdown("### 📏")

with col_titulo:
    st.markdown("# 📏⚡ Optimizador de Jenny + Fuentes")
    st.markdown("### Sistema profesional de minimización de desperdicio")

col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    st.markdown(f"<p style='text-align: right; color: #6b7280; font-size: 0.9rem;'>👤 {st.session_state.user_email}</p>", unsafe_allow_html=True)
with col3:
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
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
    st.markdown("## ⚙️ Configuración")
    st.markdown("---")
    
    st.markdown("### 📐 Rollo Madre")
    longitud_rollo = st.selectbox(
        "Longitud del rollo",
        options=[5.0, 10.0, 20.0],
        index=1,  # 10m por defecto
        format_func=lambda x: f"{x:.0f} metros"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Gestión de Cortes")
    
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
    
    if st.button("➕ Agregar Corte", use_container_width=True):
        st.session_state.pedidos.append(Pedido(largo_pieza, cantidad))
        st.success(f"✅ Agregado: {cantidad}× {largo_pieza}m")
        st.rerun()
    
    st.markdown("---")
    
    # Mostrar pedidos
    if st.session_state.pedidos:
        st.markdown("### 📦 Cortes Actuales")
        
        df = pd.DataFrame([
            {"Largo (m)": p.largo, "Cantidad": p.cantidad, "Total (m)": p.largo * p.cantidad}
            for p in st.session_state.pedidos
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total_piezas = sum(p.cantidad for p in st.session_state.pedidos)
        total_metros = sum(p.largo * p.cantidad for p in st.session_state.pedidos)
        st.info(f"**Total:** {total_piezas} piezas • {total_metros:.2f}m")
        
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.pedidos = []
            st.session_state.resultados = None
            st.rerun()
    else:
        st.info("No hay cortes agregados")
    
    st.markdown("---")
    
    # Fuentes (opcional)
    st.markdown("### ⚡ Fuentes (Opcional)")
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
    if st.button("🚀 Calcular Optimización", type="primary", use_container_width=True, 
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
    <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;'>
        <small>Sistema de Optimización Avanzada</small><br>
        <small style='opacity: 0.7;'>v3.0 • Minimiza desperdicios</small>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

if st.session_state.resultados is None:
    # Pantalla de bienvenida
    st.markdown("""
    <div class="custom-card" style="text-align: center; padding: 3rem;">
        <h2 style="color: #1f2937; font-weight: 700;">Bienvenido al Optimizador de Jenny</h2>
        <p style="font-size: 1.1rem; color: #374151; margin-top: 1rem;">
            Agrega tus cortes en el panel lateral y presiona 
            <strong style="color: #f97316;">Calcular Optimización</strong>
        </p>
        <br>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <div style="flex: 1; max-width: 300px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2rem;">📐</div>
                <h4>Define tu rollo</h4>
                <p style="font-size: 0.9rem; color: #64748b;">Longitud estándar del material</p>
            </div>
            <div style="flex: 1; max-width: 300px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2rem;">📋</div>
                <h4>Agrega cortes</h4>
                <p style="font-size: 0.9rem; color: #64748b;">Largos y cantidades (incluso mayores al rollo)</p>
            </div>
            <div style="flex: 1; max-width: 300px; background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2rem;">🚀</div>
                <h4>Optimiza</h4>
                <p style="font-size: 0.9rem; color: #64748b;">Obtén la mejor distribución con mínimo desperdicio</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 ¿Cómo funciona?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Sistema de Optimización Avanzada**
        
        1. 🔍 Analiza todos tus cortes
        2. 📐 Calcula las mejores combinaciones
        3. 🎯 Minimiza desperdicios al máximo
        4. ✨ Garantiza el mejor aprovechamiento
        5. 📏 Maneja cortes de cualquier tamaño
        """)
    
    with col2:
        st.markdown("""
        **Beneficios**
        
        - ⚡ Optimización rápida y precisa
        - 📊 Visualización clara de resultados
        - 💰 Máxima reducción de desperdicios
        - 🎯 Solución profesional certificada
        - 🔬 Tecnología de vanguardia
        """)

else:
    # Resultados
    rollos = st.session_state.resultados
    info_grandes = st.session_state.info_grandes
    estado = st.session_state.estado_solucion
    
    st.markdown("## 📊 Resultados de Optimización")
    
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
        # Determinar estado visual
        if rollo.eficiencia >= 95:
            badge_color = "#10b981"  # Verde
            badge_text = "PERFECTO"
            badge_icon = "✨"
        elif rollo.eficiencia >= 80:
            badge_color = "#3b82f6"  # Azul
            badge_text = "EXCELENTE"
            badge_icon = "✅"
        elif rollo.eficiencia >= 60:
            badge_color = "#f59e0b"  # Ámbar
            badge_text = "BUENO"
            badge_icon = "⚠️"
        else:
            badge_color = "#ef4444"  # Rojo
            badge_text = "REVISAR"
            badge_icon = "🔴"
        
        tipo_rollo = "Corte Grande" if rollo.es_grande else "Optimizado"
        
        with st.container():
            # Header de la tarjeta con diseño profesional
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                border-left: 5px solid {badge_color};
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <span style="
                            font-size: 1.4rem; 
                            font-weight: 700; 
                            color: #0f172a;
                            font-family: 'Work Sans', sans-serif;
                        ">
                            Rollo #{idx}
                        </span>
                        <span style="
                            margin-left: 0.75rem;
                            padding: 0.25rem 0.75rem;
                            background: {badge_color}20;
                            color: {badge_color};
                            border-radius: 20px;
                            font-size: 0.75rem;
                            font-weight: 600;
                            letter-spacing: 0.05em;
                        ">
                            {badge_icon} {badge_text}
                        </span>
                        <span style="
                            margin-left: 0.5rem;
                            padding: 0.25rem 0.75rem;
                            background: #e2e8f0;
                            color: #475569;
                            border-radius: 20px;
                            font-size: 0.75rem;
                            font-weight: 500;
                        ">
                            {tipo_rollo}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas y visualización
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Lista de piezas con formato mejorado (una sola línea)
                chips_style = "display:inline-block;padding:0.25rem 0.75rem;margin:0.25rem 0.25rem 0.25rem 0;background:#f1f5f9;border-radius:6px;font-family:'JetBrains Mono',monospace;font-size:0.9rem;color:#334155;font-weight:600;"
                
                piezas_html = ""
                for pieza in rollo.cortes:
                    piezas_html += f'<span style="{chips_style}">{pieza}m</span>'
                
                st.markdown(f"**Piezas cortadas:**<br>{piezas_html}", unsafe_allow_html=True)
            
            with col2:
                st.metric("Eficiencia", f"{rollo.eficiencia:.1f}%", 
                         label_visibility="visible")
            
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
            
            st.markdown("<br>", unsafe_allow_html=True)
    
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 1rem;'>
    <p>Optimizador Jenny v3.0 • Sistema Profesional de Optimización</p>
    <p style='font-size: 0.8rem;'>Minimiza desperdicios • Maximiza eficiencia</p>
</div>
""", unsafe_allow_html=True)

