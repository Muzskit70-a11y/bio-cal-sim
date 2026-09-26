import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Bio-Cal Sim V1.0", page_icon="🌱", layout="wide")

st.title("🌱 Bio-Cal Sim V1.0: Simulador Digital de Neutralización Química")
st.caption("Proyecto STEM - ODS 15: Vida de Ecosistemas Terrestres")

st.markdown("---")

# Columna izquierda: Entradas de usuario | Columna derecha: Visualización y Resultados
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("⚙️ Parámetros del Terreno")
    
    ph_inicial = st.slider("pH Inicial del Suelo", min_value=3.5, max_value=6.5, value=4.5, step=0.1)
    area = st.number_input("Área del Terreno (m²)", min_value=1, max_value=10000, value=25)
    tipo_suelo = st.selectbox("Tipo de Suelo", ["Arcilloso", "Arenoso", "Limoso"])
    
    ph_objetivo = 6.8
    
    # Factores de capacidad tampón según el tipo de suelo (g de Ca(OH)2 por m² por unidad de pH)
    factores_suelo = {"Arcilloso": 120, "Limoso": 80, "Arenoso": 40}
    k = factores_suelo[tipo_suelo]
    
    # Cálculo estequiométrico
    delta_ph = max(0.0, ph_objetivo - ph_inicial)
    gramos_caoh2 = k * delta_ph * area
    kg_caoh2 = gramos_caoh2 / 1000.0

with col2:
    st.header("🧪 Visualización Química de Neutralización")
    
    # Reacción química destacada
    st.latex(r"\text{Ca(OH)}_2 + 2\text{H}^+ \rightarrow \text{Ca}^{2+} + 2\text{H}_2\text{O}")
    
    st.subheader("📊 Resultados de la Simulación")
    m1, m2, m3 = st.columns(3)
    m1.metric("pH Final Estimado", f"{ph_objetivo if delta_ph > 0 else ph_inicial:.1f}")
    m2.metric("Ca(OH)₂ Requerido", f"{kg_caoh2:.2f} kg")
    
    # Porcentaje de viabilidad basado en el pH inicial vs final
    viabilidad_inicial = max(10, int((ph_inicial / 7.0) * 100))
    m3.metric("Viabilidad Final Cultivos", "95%", delta=f"+{95 - viabilidad_inicial}%")

    st.markdown("---")
    st.subheader("🌾 Viabilidad Estimada por Tipo de Cultivo")
    
    # Gráfica interactiva de cultivos
    cultivos = ['Maíz', 'Trigo', 'Alfalfa', 'Hortalizas']
    porcentajes = [95, 88, 92, 90] if ph_inicial >= 5.5 else [30, 25, 15, 20]
    
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(cultivos, porcentajes, color=['#4CAF50' if p > 50 else '#FF5722' for p in porcentajes])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Viabilidad (%)")
    ax.set_title("Predicción de Crecimiento Vegetal")
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval}%", ha='center', va='bottom')
        
    st.pyplot(fig)
