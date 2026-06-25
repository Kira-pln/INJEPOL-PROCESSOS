import streamlit as st
from datetime import date, timedelta
from services.dashboard_service import indicadores_gerais, datasets_dashboard
from components.graficos import bar, line

st.title("Dashboard geral")
c1, c2 = st.columns(2)
data_ini = c1.date_input("Data inicial", value=date.today() - timedelta(days=30))
data_fim = c2.date_input("Data final", value=date.today())

ind = indicadores_gerais(data_ini, data_fim)
c = st.columns(4)
c[0].metric("Produção total", f"{ind['produzido']:.0f}")
c[1].metric("Meta total", f"{ind['meta']:.0f}")
c[2].metric("Atingimento", f"{ind['atingimento']:.1f}%")
c[3].metric("Qualidade", f"{ind['qualidade']:.1f}%")

data = datasets_dashboard(data_ini, data_fim)
df = data["prod_maquina"]
if not df.empty:
    st.plotly_chart(bar(df, "maquina", "produzido", "Produção por máquina"), use_container_width=True)
df = data["prod_diario"]
if not df.empty:
    st.plotly_chart(line(df, "data", "produzido", "Produção diária"), use_container_width=True)
