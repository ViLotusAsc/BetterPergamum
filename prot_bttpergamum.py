import streamlit as st
from pergamum import Session
import base64
from PIL import Image

# ---------- Função para converter imagem local em base64 ----------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64("image.png")

# ---------- Inicialização segura ----------
if "sessao" not in st.session_state:
    st.session_state.sessao = Session()
if "cookie" not in st.session_state:
    st.session_state.cookie = None
if "logado" not in st.session_state:
    st.session_state.logado = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

img = Image.open("image copy.png")

st.set_page_config(page_title="BetterPergamum", page_icon=img)

st.image("image copy.png", width=200)
st.title("*Better Pergamum*")
st.subheader("Protótipo INF112")

# ---------- Navegação com botões ----------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Login"):
        st.session_state.pagina = "login"
with col2:
    if st.button("Buscar Livros"):
        st.session_state.pagina = "buscar"
with col3:
    if st.button("Empréstimos"):
        st.session_state.pagina = "emprestimos"

# ---------- Página Login ----------
if st.session_state.pagina == "login":
    st.header("Login no sistema")

    if st.button("Criar sessão"):
        st.session_state.cookie = st.session_state.sessao._create_session()
        st.success("Sessão criada!")
        st.write(f"id: `{st.session_state.cookie}`")

    matricula = st.text_input("Matrícula")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        st.session_state.sessao.phpsessid = st.session_state.cookie
        st.session_state.sessao._login(matricula=matricula, senha=senha)
        st.session_state.logado = True
        st.success(f"Bem-vindo, {st.session_state.sessao.nome}!")

    if st.session_state.logado:
        st.info(f"Usuário logado: {st.session_state.sessao.nome}")

# ---------- Página Buscar Livros ----------
elif st.session_state.pagina == "buscar":
    st.header("Buscar livros")

    if not st.session_state.logado:
        st.warning("⚠️ Você precisa estar logado para buscar livros.")
    else:
        termo = st.text_input("Digite o título:")
        if st.button("Pesquisar"):
            resultados = st.session_state.sessao._book_search(termo)
            st.write("Resultados da busca:")
            for i, livro in enumerate(resultados, start=1):
                st.write(f"{i}) **{livro['nome']}** - {livro['numero_chamada']}")

# ---------- Página Empréstimos ----------
elif st.session_state.pagina == "emprestimos":
    st.header(f"Empréstimos de {st.session_state.sessao.nome}")

    if not st.session_state.logado:
        st.warning("⚠️ Você precisa estar logado para ver seus empréstimos.")
    else:
        emprestimos = [
            {"titulo": "Algoritmos Avançados", "data_devolucao": "2025-09-15"},
            {"titulo": "Banco de Dados", "data_devolucao": "2025-09-22"},
        ]
        for emp in emprestimos:
            st.write(f"📘 **{emp['titulo']}** - Devolução até {emp['data_devolucao']}")

st.markdown('</div>', unsafe_allow_html=True)
