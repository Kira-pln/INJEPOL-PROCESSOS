import streamlit as st
from datetime import date, timedelta
from services.cadastros_service import get_maquinas, get_produtos
from services.producao_service import inserir_producao, listar_producao, resumo_por_maquina, resumo_diario, excluir_producao
from components.graficos import bar, line
from utils.helpers import to_excel_bytes

st.title("Produção")
maquinas = get_maquinas()
produtos = get_produtos()
tab1, tab2, tab3 = st.tabs(["Lançamento", "Consulta / exclusão", "Indicadores"])

with tab1:
    with st.form("f", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        data = c1.date_input("Data", value=date.today())
        maq = c2.selectbox("Máquina", maquinas["nome"].tolist() if not maquinas.empty else [])
        prod = c3.selectbox("Produto", produtos["descricao"].tolist() if not produtos.empty else [])

        c4, c5, c6 = st.columns(3)
        meta = c4.number_input("Meta", 0.0, step=1.0)
        qtd = c5.number_input("Quantidade produzida", 0.0, step=1.0)
        hd = c6.number_input("Horas disponíveis", 0.0, step=0.5)

        c7, c8, c9 = st.columns(3)
        hp = c7.number_input("Horas paradas", 0.0, step=0.5)
        ref = c8.number_input("Refugo", 0.0, step=1.0)
        retr = c9.number_input("Retrabalho", 0.0, step=1.0)

        obs = st.text_area("Observação")
        if st.form_submit_button("Salvar") and maq and prod:
            inserir_producao(data, int(maquinas.loc[maquinas['nome']==maq,'id'].iloc[0]), int(produtos.loc[produtos['descricao']==prod,'id'].iloc[0]), meta, qtd, hd, hp, ref, retr, obs)
            st.success("Registro de produção salvo.")

with tab2:
    c1, c2 = st.columns(2)
    di = c1.date_input("Data inicial", value=date.today() - timedelta(days=30), key="pi")
    df = c2.date_input("Data final", value=date.today(), key="pf")
    dados = listar_producao(di, df)
    st.dataframe(dados, use_container_width=True, hide_index=True)

    if not dados.empty:
        st.download_button("Baixar Excel", data=to_excel_bytes(dados), file_name="producao.xlsx")
        st.markdown("### Excluir registro")
        registro_id = st.selectbox("Selecione o ID do registro para excluir", dados["id"].tolist())
        confirmar = st.checkbox("Confirmo que desejo excluir o registro selecionado", key="conf_exc_prod")
        if st.button("Excluir registro de produção", type="primary"):
            if confirmar:
                excluir_producao(int(registro_id))
                st.success(f"Registro {registro_id} excluído com sucesso.")
                st.rerun()
            else:
                st.warning("Marque a confirmação antes de excluir.")

with tab3:
    c1, c2 = st.columns(2)
    di = c1.date_input("Data inicial", value=date.today() - timedelta(days=30), key="prod_ind_i")
    df = c2.date_input("Data final", value=date.today(), key="prod_ind_f")
    maq = resumo_por_maquina(di, df)
    dia = resumo_diario(di, df)

    if not maq.empty:
        st.plotly_chart(bar(maq, "maquina", "produzido", "Produção por máquina"), use_container_width=True)
        meta_real = maq[["maquina","meta","produzido"]].melt(id_vars="maquina", var_name="tipo", value_name="valor")
        st.plotly_chart(bar(meta_real, "maquina", "valor", "Meta x realizado por máquina", color="tipo", barmode="group"), use_container_width=True)

    if not dia.empty:
        meta_real_dia = dia[["data","meta","produzido"]].melt(id_vars="data", var_name="tipo", value_name="valor")
        st.plotly_chart(bar(meta_real_dia, "data", "valor", "Meta x realizado por dia", color="tipo", barmode="group"), use_container_width=True)
        st.plotly_chart(line(dia, "data", "produzido", "Produção diária"), use_container_width=True)
