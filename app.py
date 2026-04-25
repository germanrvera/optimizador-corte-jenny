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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

    :root {
        --brand: #16a34a;
        --brand-light: #dcfce7;
        --brand-dark: #15803d;
        --bg: #f9fafb;
        --white: #ffffff;
        --text: #111827;
        --text-muted: #6b7280;
        --border: #e5e7eb;
        --radius: 12px;
        --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.06);
        --shadow-lg: 0 4px 6px rgba(0,0,0,0.05), 0 10px 30px rgba(0,0,0,0.08);
    }

    /* Fondo y tipografía base */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    .main { background-color: var(--bg) !important; }

    /* Logo */
    img {
        background: white !important;
        padding: 10px !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
        border: 1px solid var(--border) !important;
    }
    [data-testid="stImage"] { background: transparent !important; }

    /* Títulos */
    h1, h2, h3, h4 { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    h1 { font-size: 2rem !important; font-weight: 800 !important; color: var(--text) !important; }
    h2 { font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text) !important; }
    h3 { font-size: 0.85rem !important; font-weight: 700 !important; color: var(--text-muted) !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }

    /* Métricas */
    [data-testid="stMetric"] {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1.25rem !important;
        box-shadow: var(--shadow) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'DM Mono', monospace !important;
        font-size: 2rem !important;
        font-weight: 500 !important;
        color: var(--brand) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    /* Botones */
    .stButton > button {
        background: var(--white) !important;
        color: var(--text) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.6rem 1.25rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        border-color: var(--brand) !important;
        color: var(--brand) !important;
        box-shadow: 0 0 0 3px var(--brand-light) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--brand) !important;
        color: white !important;
        border-color: var(--brand) !important;
        box-shadow: 0 2px 8px rgba(22,163,74,0.35) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--brand-dark) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(22,163,74,0.4) !important;
    }

    /* Inputs */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        border: 1.5px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.875rem !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 1rem !important;
        color: var(--text) !important;
        background: var(--white) !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    }
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: var(--brand) !important;
        box-shadow: 0 0 0 3px var(--brand-light) !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.12) !important;
        color: white !important;
        border-color: rgba(255,255,255,0.2) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border: 1.5px solid var(--border) !important;
        border-radius: 8px !important;
        background: var(--white) !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.2) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%) !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] span:not(.stNumberInput span) {
        color: white !important;
    }
    [data-testid="stSidebar"] h3 { color: rgba(255,255,255,0.5) !important; border: none !important; }
    [data-testid="stSidebar"] label {
        color: rgba(255,255,255,0.7) !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
    }

    /* Divisor */
    .custom-divider {
        height: 1px;
        background: var(--border);
        margin: 1.5rem 0;
    }

    /* Alertas */
    .stAlert { border-radius: var(--radius) !important; }

    /* Dataframe */
    .dataframe {
        border-radius: var(--radius) !important;
        overflow: hidden !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow) !important;
    }
    .dataframe thead tr th {
        background: var(--bg) !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-muted) !important;
        padding: 0.75rem 1rem !important;
    }
    .dataframe tbody tr td { padding: 0.6rem 1rem !important; font-family: 'DM Mono', monospace !important; font-size: 0.875rem !important; }
    .dataframe tbody tr:hover { background: var(--brand-light) !important; }

    /* Download button */
    [data-testid="stDownloadButton"] > button {
        background: var(--white) !important;
        color: var(--brand) !important;
        border: 1.5px solid var(--brand) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: var(--brand-light) !important;
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
        '#16a34a',  # Verde (brand)
        '#2563eb',  # Azul
        '#7c3aed',  # Violeta
        '#db2777',  # Rosa
        '#d97706',  # Ámbar
        '#0891b2',  # Cyan
        '#059669',  # Esmeralda
        '#dc2626',  # Rojo
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
    st.markdown(
        '<div style="max-width:420px;margin:3rem auto 2rem auto;text-align:center;">'
        '<div style="font-size:2.5rem;margin-bottom:1rem;">📏</div>'
        '<h1 style="font-size:1.75rem;font-weight:800;color:#111827;margin:0 0 0.5rem 0;">Optimizador de Jenny</h1>'
        '<p style="color:#6b7280;font-size:0.95rem;margin:0;">Ingresa tu email para acceder</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
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
        
        if st.button("Ingresar", type="primary", use_container_width=True):
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
                    st.success(f"✅ ¡Bienvenido! Acceso concedido para {email}")
                    st.rerun()
                else:
                    st.error("❌ Email no autorizado. Contacta al administrador.")
            else:
                st.warning("⚠️ Por favor ingresa tu email")
    
    st.markdown('<p style="text-align:center;color:#9ca3af;font-size:0.8rem;margin-top:2rem;">¿Necesitas acceso? Contacta al administrador</p>', unsafe_allow_html=True)
    
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

col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        if os.path.exists("logo.png"):
            logo = Image.open("logo.png")
            st.image(logo, width=100)
    except:
        pass

with col_titulo:
    st.markdown("# 📏 Optimizador de Jenny")
    st.markdown('<p style="color:#6b7280;margin-top:-0.5rem;">Sistema de corte inteligente · Minimiza desperdicios</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    st.markdown(f'<p style="text-align:right;color:#6b7280;font-size:0.82rem;margin-top:0.5rem;">👤 {st.session_state.user_email}</p>', unsafe_allow_html=True)
with col3:
    if st.button("Cerrar sesión", use_container_width=True):
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
    st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.75rem;">Optimizador Jenny v3.0</p>', unsafe_allow_html=True)

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

if st.session_state.resultados is None:
    # Pantalla de bienvenida limpia
    st.markdown('<div style="background:white;border-radius:16px;padding:2.5rem;margin:1rem 0;box-shadow:0 1px 3px rgba(0,0,0,0.08),0 4px 12px rgba(0,0,0,0.06);text-align:center;">'
                '<div style="font-size:3rem;margin-bottom:1rem;">📏</div>'
                '<h2 style="font-size:1.5rem;font-weight:700;color:#111827;margin:0 0 0.5rem 0;">¡Listo para calcular!</h2>'
                '<p style="color:#6b7280;font-size:0.95rem;max-width:400px;margin:0 auto;">Agrega tus cortes en el panel izquierdo y presiona <strong style="color:#16a34a;">Calcular Optimización</strong></p>'
                '</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    pasos = [
        ("01", "📐", "Selecciona el rollo", "Elige 5m, 10m o 20m según el material disponible"),
        ("02", "✏️", "Agrega los cortes", "Indica el largo y cantidad de cada pieza"),
        ("03", "🚀", "Calcula y descarga", "Obtén el plan optimizado con mínimo desperdicio"),
    ]
    for col, (num, icon, titulo, texto) in zip([col1, col2, col3], pasos):
        with col:
            st.markdown(
                f'<div style="background:white;border-radius:12px;padding:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.08),0 4px 12px rgba(0,0,0,0.06);height:100%;">'
                f'<div style="font-size:1.75rem;margin-bottom:0.75rem;">{icon}</div>'
                f'<div style="font-size:0.7rem;font-weight:700;color:#16a34a;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Paso {num}</div>'
                f'<div style="font-size:0.95rem;font-weight:700;color:#111827;margin-bottom:0.5rem;">{titulo}</div>'
                f'<div style="font-size:0.85rem;color:#6b7280;line-height:1.5;">{texto}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

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
        # Estado del rollo
        if rollo.eficiencia >= 95:
            badge_bg, badge_color, badge_text = "#dcfce7", "#15803d", "✅ Óptimo"
        elif rollo.eficiencia >= 80:
            badge_bg, badge_color, badge_text = "#dbeafe", "#1d4ed8", "👍 Eficiente"
        elif rollo.eficiencia >= 60:
            badge_bg, badge_color, badge_text = "#fef9c3", "#854d0e", "⚠️ Aceptable"
        else:
            badge_bg, badge_color, badge_text = "#fee2e2", "#991b1b", "🔴 Revisar"

        tipo_rollo = "Empalme" if rollo.es_grande else "Directo"

        with st.container():
            # Card header
            st.markdown(
                f'<div style="background:white;border-radius:12px 12px 0 0;border:1px solid #e5e7eb;border-bottom:none;padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;margin-top:1rem;">'
                f'<div style="display:flex;align-items:center;gap:0.75rem;">'
                f'<span style="font-size:1.1rem;font-weight:800;color:#111827;">Rollo #{idx}</span>'
                f'<span style="font-size:0.75rem;color:#6b7280;background:#f3f4f6;padding:0.2rem 0.6rem;border-radius:20px;">{tipo_rollo}</span>'
                f'</div>'
                f'<span style="background:{badge_bg};color:{badge_color};font-size:0.78rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;">{badge_text}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Card body
            st.markdown(
                '<div style="background:white;border-radius:0 0 12px 12px;border:1px solid #e5e7eb;border-top:none;padding:1rem 1.5rem 1.5rem 1.5rem;">',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown('<p style="font-size:0.75rem;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.5rem;">Piezas del corte</p>', unsafe_allow_html=True)
                chips_style = "display:inline-block;padding:0.35rem 0.75rem;margin:0.2rem 0.2rem 0.2rem 0;background:#f9fafb;border:1.5px solid #e5e7eb;border-radius:8px;font-family:'DM Mono',monospace;font-size:0.9rem;color:#111827;font-weight:500;"
                piezas_html = "".join(f'<span style="{chips_style}">{pieza}m</span>' for pieza in rollo.cortes)
                st.markdown(piezas_html, unsafe_allow_html=True)

            with col2:
                st.metric("Eficiencia", f"{rollo.eficiencia:.1f}%")

            with col3:
                st.metric("Desperdicio", f"{rollo.desperdicio:.2f}m")
            
            # Visualización gráfica
            fig = crear_visualizacion_rollo_pulp(rollo, idx)
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False},
                key=f"rollo_chart_{idx}_{rollo.rollo_id}"
            )
            
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

# Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#9ca3af;font-size:0.8rem;">Optimizador Jenny v3.0 · Minimiza desperdicios · Maximiza eficiencia</p>', unsafe_allow_html=True)
