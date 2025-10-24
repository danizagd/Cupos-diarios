import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Asignación de Cupos Diarios 🏢")

# Subir archivo Excel
uploaded_file = st.file_uploader("Sube tu base Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.subheader("Datos originales")
    st.dataframe(df)
    
    # -------------------
    # Asignación de cupos 3x2
    # -------------------
    
    # Lista de días de la semana
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    cupos = []
    for i in range(len(df)):
        dia = dias[i % len(dias)]
        cupos.append(dia)
    
    df["Día asignado"] = cupos
    
    # Piso: todos pasan por gerencias (3er piso)
    df["Piso"] = 3
    
    # Reservar silla de ruedas en primer piso
    if "Silla de ruedas" in df.columns:
        df.loc[df["Silla de ruedas"] == True, "Piso"] = 1
    
    st.subheader("Asignación de Cupos Diarios")
    st.dataframe(df)
    
    # -------------------
    # Función para descargar Excel
    # -------------------
    @st.cache_data
    def convert_df(df):
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
    
    excel_data = convert_df(df)
    
    st.download_button(
        label="Descargar Excel final",
        data=excel_data,
        file_name="cupos_diarios.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )