import streamlit as st
import pandas as pd
from pergamum import Session
import requests



def see_chat():
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/plain, */*',
        'sec-fetch-site': 'cross-site',
        'accept-language': 'pt-BR,pt;q=0.9',
        'sec-fetch-mode': 'cors',
        'origin': 'moodleappfs://localhost',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MoodleMobile 5.0.0 (50003)',
        'sec-fetch-dest': 'empty',
    }

    params = {
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_message_get_conversation_messages',
    }

    data = {
        'currentuserid': '53099',
        'convid': '413792',
        'limitfrom': '0',
        'limitnum': '51',
        'newest': '1',
        'timefrom': '0',
        'moodlewssettingfilter': 'true',
        'moodlewssettingfileurl': 'true',
        'moodlewssettinglang': 'pt_br',
        'wsfunction': 'core_message_get_conversation_messages',
        'wstoken': '2081f53b8dac5ba4cba2899144696945',
    }

    response = requests.post('https://ava.ufv.br/webservice/rest/server.php', params=params, headers=headers, data=data)

    mensagens = []
    for mensagem in response.json()["messages"]:
        mensagens.append(mensagem["text"].replace("<p>", "").replace("</p>", ""))

    mensagens.reverse()

    return mensagens

    for msg in mensagens:
        print(f"- {msg}")

#print(json.dumps(response.json(), indent=4))



def send_msg(msg):
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/plain, */*',
        'sec-fetch-site': 'cross-site',
        'accept-language': 'pt-BR,pt;q=0.9',
        'sec-fetch-mode': 'cors',
        'origin': 'moodleappfs://localhost',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MoodleMobile 5.0.0 (50003)',
        'sec-fetch-dest': 'empty',
    }

    params = {
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_message_send_messages_to_conversation',
    }

    data = {
        'conversationid': '413792',
        'messages[0][text]': msg,
        'messages[0][textformat]': '1',
        'moodlewssettingfilter': 'true',
        'moodlewssettingfileurl': 'true',
        'moodlewssettinglang': 'pt_br',
        'wsfunction': 'core_message_send_messages_to_conversation',
        'wstoken': '2081f53b8dac5ba4cba2899144696945',
    }


    response = requests.post('https://ava.ufv.br/webservice/rest/server.php', params=params, headers=headers, data=data)
    return response.text

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
    ["Login", "Buscar Livros", "Buscar Débito", "Chat"]
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

elif tab == "Chat":
    st.header("Chat Online")

    if not st.session_state.logado:
        st.warning("Faça login primeiro para usar o chat.")
    else:
        # Carregar mensagens
        mensagens = see_chat()
        mensagens = mensagens[29:]  # descarta as iniciais

        st.subheader("Histórico")
        chat_box = st.container()
        with chat_box:
            for msg in mensagens:
                st.markdown(f"""
                <div style="
                    background-color:#f0f2f6;
                    padding:10px;
                    border-radius:8px;
                    margin-bottom:5px;
                    color:black;
                ">
                    {msg}
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # Input de mensagem
        st.subheader("Enviar mensagem")
        mensagem_env = st.text_input("Digite sua mensagem aqui:")

        if st.button("Enviar", use_container_width=True):
            if mensagem_env.strip():
                send_msg(f"[{st.session_state.sessao.nome}] {mensagem_env}")
                st.success("Mensagem enviada!")
            else:
                st.error("Mensagem vazia não pode ser enviada.")
