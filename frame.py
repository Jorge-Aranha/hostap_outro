import streamlit as st
import pandas as pd
import pydeck as pdk
from analise import view, select2, select3

df = select2()
fig_mat = view()
df2 = select3()

st.title("Report Embargos")

st.pyplot(fig_mat)

st.subheader("Detalhamento por Unidade")

utep = st.selectbox(
    "Selecione a UTEP",
    sorted(df["UTEP"].unique())
)

df_filtrado = df[df["UTEP"] == utep]

st.metric(
    "Total da UTEP",
    int(df_filtrado["TOTAL"].sum())
)

st.dataframe(
    df_filtrado,
    use_container_width=True
)

st.subheader("Base Completa")

st.dataframe(
    df,
    use_container_width=True
)

st.markdown(
    """
    <h6 style='text-align: center; color: gray;'>
        Disponível até 14/07/2026
    </h6>
    """,
    unsafe_allow_html=True
)
