import streamlit as st
from database.db import init_db
from services.cadastros_service import (
    get_maquinas, get_produtos, get_motivos,
    add_produto, update_produto, delete_produto,
    add_motivo, add_maquina, update_maquina, delete_maquina
)

st.title("Cadastros")
if st.button("Reinicializar banco / aplicar seed"):
    init_db()
    st.success("Banco inicializado.")

tab1, tab2, tab3 = st.tabs(["Máquinas", "Produtos", "Motivos da qualidade"])

with tab1:
    st.subheader("Máquinas")
    with st.expander("Adicionar máquina"):
        with st.form("nova_maquina", clear_on_submit=True):
            nome = st.text_input("Nome da máquina")
            processo = st.text_input("Processo")
            if st.form_submit_button("Adicionar máquina"):
                if nome and processo:
                    add_maquina(nome, processo)
                    st.success("Máquina adicionada.")
                    st.rerun()
                else:
                    st.warning("Preencha nome e processo.")
    maq = get_maquinas()
    st.dataframe(maq, use_container_width=True, hide_index=True)
    if not maq.empty:
        maq_id = st.selectbox("Selecione a máquina para editar/excluir", maq["id"].tolist(), format_func=lambda x: f"{x} - {maq.loc[maq['id']==x,'nome'].iloc[0]}")
        row = maq.loc[maq["id"] == maq_id].iloc[0]
        with st.form("editar_maquina"):
            nome_e = st.text_input("Nome", value=row["nome"])
            processo_e = st.text_input("Processo", value=row["processo"])
            ativo_e = st.selectbox("Ativo", [1,0], index=0 if int(row["ativo"]) == 1 else 1, format_func=lambda x: "Sim" if x == 1 else "Não")
            c1, c2 = st.columns(2)
            salvar = c1.form_submit_button("Salvar alterações")
            excluir = c2.form_submit_button("Excluir máquina")
            if salvar:
                update_maquina(int(maq_id), nome_e, processo_e, int(ativo_e))
                st.success("Máquina atualizada.")
                st.rerun()
            if excluir:
                delete_maquina(int(maq_id))
                st.success("Máquina excluída.")
                st.rerun()

with tab2:
    st.subheader("Produtos")
    with st.expander("Adicionar produto"):
        with st.form("novo_produto", clear_on_submit=True):
            codigo = st.text_input("Código")
            descricao = st.text_input("Descrição")
            familia = st.text_input("Família")
            unidade = st.text_input("Unidade", value="UN")
            if st.form_submit_button("Adicionar produto"):
                if codigo and descricao:
                    add_produto(codigo, descricao, familia, unidade)
                    st.success("Produto adicionado.")
                    st.rerun()
                else:
                    st.warning("Preencha código e descrição.")
    prod = get_produtos()
    st.dataframe(prod, use_container_width=True, hide_index=True)
    if not prod.empty:
        prod_id = st.selectbox("Selecione o produto para editar/excluir", prod["id"].tolist(), format_func=lambda x: f"{x} - {prod.loc[prod['id']==x,'descricao'].iloc[0]}")
        row = prod.loc[prod["id"] == prod_id].iloc[0]
        with st.form("editar_produto"):
            codigo_e = st.text_input("Código", value=row["codigo"])
            descricao_e = st.text_input("Descrição", value=row["descricao"])
            familia_e = st.text_input("Família", value=row["familia"] if row["familia"] else "")
            unidade_e = st.text_input("Unidade", value=row["unidade"] if row["unidade"] else "UN")
            ativo_e = st.selectbox("Ativo", [1,0], index=0 if int(row["ativo"]) == 1 else 1, format_func=lambda x: "Sim" if x == 1 else "Não")
            c1, c2 = st.columns(2)
            salvar = c1.form_submit_button("Salvar alterações")
            excluir = c2.form_submit_button("Excluir produto")
            if salvar:
                update_produto(int(prod_id), codigo_e, descricao_e, familia_e, unidade_e, int(ativo_e))
                st.success("Produto atualizado.")
                st.rerun()
            if excluir:
                delete_produto(int(prod_id))
                st.success("Produto excluído.")
                st.rerun()

with tab3:
    st.subheader("Motivos da qualidade")
    with st.form("nm", clear_on_submit=True):
        descricao = st.text_input("Motivo")
        categoria = st.text_input("Categoria")
        if st.form_submit_button("Adicionar motivo") and descricao:
            add_motivo(descricao, categoria)
            st.success("Motivo adicionado.")
            st.rerun()
    st.dataframe(get_motivos(), use_container_width=True, hide_index=True)
