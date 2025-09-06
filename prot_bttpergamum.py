import streamlit as st
from pergamum import Session
import base64


def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64("image.png")

if "sessao" not in st.session_state:
    st.session_state.sessao = Session()
if "cookie" not in st.session_state:
    st.session_state.cookie = None
if "logado" not in st.session_state:
    st.session_state.logado = False

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        background-size: 227px 160px;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("*Better Pergamum*")
#st.subheader("Protótipo - INF112")

# ---------- Aba de navegação ----------
abas = st.tabs(["-- Login", "-- Buscar Livros", "-- Empréstimos"])

# ---------- Aba Login ----------
with abas[0]:
    st.header("Login no sistema")

    if st.button("Criar sessão"):
        st.session_state.cookie = st.session_state.sessao._create_session()
        st.success("Sessão criada!")
        st.write(f"Cookie: `{st.session_state.cookie}`")

    matricula = st.text_input("Matrícula")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        st.session_state.sessao.phpsessid = st.session_state.cookie
        st.session_state.sessao._login(matricula=matricula, senha=senha)
        st.session_state.logado = True
        st.success(f"Bem-vindo, {st.session_state.sessao.nome}!")

    if st.session_state.logado:
        st.info(f"Usuário logado: {st.session_state.sessao.nome}")

# ---------- Aba Buscar Livros ----------
with abas[1]:
    st.header("Buscar livros")

    if not st.session_state.logado:
        st.warning("⚠️ Você precisa estar logado para buscar livros.")
    else:
        termo = st.text_input("Digite o título:")
        if st.button("Buscar"):
            # Exemplo fake de resposta
            resultados = st.session_state.sessao._book_search(termo)
            st.write("Resultados da busca:")
            counter = 1
            for livro in resultados:
                st.write(f"-- **{livro['nome']}** - {livro['numero_chamada']})")
                counter+=1

# ---------- Aba Empréstimos ----------
with abas[2]:
    st.header(f"Empréstimos de {st.session_state.sessao.nome}")

    if not st.session_state.logado:
        st.warning("⚠️ Você precisa estar logado para ver seus empréstimos.")
    else:
        # Exemplo fake de empréstimos
        emprestimos = [
            {"titulo": "Algoritmos Avançados", "data_devolucao": "2025-09-15"},
            {"titulo": "Banco de Dados", "data_devolucao": "2025-09-22"},
        ]
        for emp in emprestimos:
            st.write(f"📘 **{emp['titulo']}** - Devolução até {emp['data_devolucao']}")
