import streamlit as st
from datetime import date, timedelta
from services.cadastros_service import get_maquinas, get_produtos
from services.processos_service import inserir_processo, listar_processos, resumo_maquina, excluir_processo
from components.graficos import bar
from utils.helpers import to_excel_bytes

st.title("Processos")
maquinas = get_maquinas()
produtos = get_produtos()
tab1, tab2, tab3 = st.tabs(["Lançamento", "Consulta / exclusão", "Indicadores"])

with tab1:
    with st.form("fp", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        data = c1.date_input("Data", value=date.today())
        maq = c2.selectbox("Máquina", maquinas["nome"].tolist() if not maquinas.empty else [])
        prod = c3.selectbox("Produto", produtos["descricao"].tolist() if not produtos.empty else [])

        c4, c5, c6 = st.columns(3)
        setup = c4.number_input("Tempo de setup", 0.0, step=0.1)
        inj = c5.number_input("Tempo de injeção / ciclo", 0.0, step=0.1)
        qtd = c6.number_input("Quantidade movimentada", 0.0, step=1.0)

        obs = st.text_area("Observação")
        if st.form_submit_button("Salvar") and maq and prod:
            inserir_processo(data, int(maquinas.loc[maquinas['nome']==maq,'id'].iloc[0]), int(produtos.loc[produtos['descricao']==prod,'id'].iloc[0]), setup, inj, qtd, obs)
            st.success("Registro de processo salvo.")

with tab2:
    dados = listar_processos(date.today() - timedelta(days=30), date.today())
    st.dataframe(dados, use_container_width=True, hide_index=True)

    if not dados.empty:
        st.download_button("Baixar Excel", data=to_excel_bytes(dados), file_name="processos.xlsx")
        registro_id = st.selectbox("Selecione o ID do registro para excluir", dados["id"].tolist(), key="exc_proc")
        confirmar = st.checkbox("Confirmo que desejo excluir o registro selecionado", key="conf_exc_proc")
        if st.button("Excluir registro de processo", type="primary"):
            if confirmar:
                excluir_processo(int(registro_id))
                st.success(f"Registro {registro_id} excluído com sucesso.")
                st.rerun()
            else:
                st.warning("Marque a confirmação antes de excluir.")

with tab3:
    dados = resumo_maquina(date.today() - timedelta(days=30), date.today())
    if not dados.empty:
        st.plotly_chart(bar(dados, "maquina", "setup_medio", "Setup médio por máquina"), use_container_width=True)
        st.plotly_chart(bar(dados, "maquina", "injecao_media", "Tempo médio de injeção"), use_container_width=True)
        st.plotly_chart(bar(dados, "maquina", "qtd_movimentada", "Quantidade movimentada por máquina"), use_container_width=True)
