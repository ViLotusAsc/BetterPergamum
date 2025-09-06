import streamlit as st
import pandas as pd
from pergamum import Session

if "sessao" not in st.session_state:
    st.session_state.sessao = Session()
if "cookie" not in st.session_state:
    st.session_state.cookie = None
if "logado" not in st.session_state:
    st.session_state.logado = False
if "livros" not in st.session_state:
    st.session_state.livros = []
if "debitos" not in st.session_state:
    st.session_state.debitos = []

st.image("image copy.png", width=200)
st.title("*BetterPergamum*")
st.write("Reversed Engineered Pergamum (UFV)")

tab = st.sidebar.radio(
    "Escolha a ação:",
    ["Login", "Buscar Livros", "Buscar Débito"]
)

if tab == "Login":
    st.header("Criar Sessão")
    if st.button("Criar nova sessão"):
        st.session_state.cookie = st.session_state.sessao._create_session()
        st.success("Sessão criada com sucesso!")
        st.write(f"id: `{st.session_state.cookie}`")
    st.header("Login")
    matricula = st.text_input("Matrícula")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if not st.session_state.cookie:
            st.warning("Crie uma sessão primeiro!")
        else:
            st.session_state.sessao.phpsessid = st.session_state.cookie
            st.session_state.sessao._login(matricula=matricula, senha=senha)
            st.session_state.logado = True
            st.success(f"Bem-vindo, {st.session_state.sessao.nome}!")

    if st.session_state.logado:
        st.info(f"Usuário logado: {st.session_state.sessao.nome}")

elif tab == "Buscar Livros":
    st.header("Buscar Livros")

    termo = st.text_input("Digite o título do livro:")
    if st.button("Buscar"):
        resultados = st.session_state.sessao._book_search(termo)

        # Converte para DataFrame e exibe
        if resultados:
            df_livros = pd.DataFrame(resultados)
            # Seleciona colunas que quer mostrar (ajuste conforme a estrutura do retorno)
            colunas = []
            if 'nome' in df_livros.columns:
                colunas.append('nome')
            if 'numero_chamada' in df_livros.columns:
                colunas.append('numero_chamada')
            st.table(df_livros[colunas])
        else:
            st.info("Nenhum livro encontrado.")
elif tab == "Buscar Débito":
    st.header("Buscar Débito")
    if not st.session_state.logado:
        st.warning("⚠️ Você precisa estar logado para ver seus débitos.")
    else:
        st.write(f"Histórico de Débito de {st.session_state.sessao.nome}:")
        if st.button("Atualizar débitos"):
            # Aqui você integra a função real de busca de débitos
            debitos = st.session_state.sessao._search_debt()
            st.session_state.debitos = debitos

                # Exibir em tabela
    if st.session_state.debitos:
        df_debitos = pd.DataFrame(st.session_state.debitos)

        # Seleciona apenas colunas de interesse
        colunas = []
        if 'nome' in df_debitos.columns:
            colunas.append('nome')
        if 'debt' in df_debitos.columns:
            colunas.append('debt')

        st.table(df_debitos[colunas])
    else:
        st.info("Nenhum débito encontrado.")
