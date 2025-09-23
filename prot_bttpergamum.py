import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pandas as pd
import json
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

def _get_cardapio(data):
    cookies = {
        '_ga_3GKTCB3HHS': 'GS2.1.s1758646399$o2$g0$t1758646399$j60$l0$h0',
        '_ga': 'GA1.1.523303875.1758566439',
        'PHPSESSID': 'dovt95ssmutri5c3rbm069knk4',
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://cardapio.ufv.br',
        'referer': 'https://cardapio.ufv.br/',
        # 'cookie': '_ga_3GKTCB3HHS=GS2.1.s1758646399$o2$g0$t1758646399$j60$l0$h0; _ga=GA1.1.523303875.1758566439; PHPSESSID=dovt95ssmutri5c3rbm069knk4',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=0',
        # Requests doesn't support trailers
        # 'te': 'trailers',
    }

    data = {
        'data_selecionada': data,
    }

    response = requests.post(
        'https://cardapio.ufv.br/~Cevutaisdotantencharamautapas23usdenusjatepro/ajaxBuscaCardapioPorData.php',
        cookies=cookies,
        headers=headers,
        data=data,
    )



    print(json.dumps(response.json(), indent=4))

    cardapio = [[], [], [], [], [], []]

    for item in response.json()["dados"]:
        cardapio[int(item["refeicao_id"])].append(item["composicao"])
        #print(f"Item: {item["composicao"]}")

    return cardapio[3:]

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
    ["Login", "Buscar Livros", "Buscar Débito", "RU"]
)

if tab == "Login":
    #st.header("Criar Sessão")
    #if st.button("Criar nova sessão"):
    #    st.session_state.cookie = st.session_state.sessao._create_session()
    #    st.success("Sessão criada com sucesso!")
    #    st.write(f"id: `{st.session_state.cookie}`")
    st.header("Login")
    matricula = st.text_input("Matrícula")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        st.session_state.cookie = st.session_state.sessao._create_session()
        st.write(f"id: `{st.session_state.cookie}`")
        st.session_state.sessao.phpsessid = st.session_state.cookie
        st.session_state.sessao._login(matricula=matricula, senha=senha)
        st.session_state.logado = True
        st.success(f"Bem-vindo, {st.session_state.sessao.nome}!")

    #if st.session_state.logado:
    #    st.info(f"Usuário logado: {st.session_state.sessao.nome}")

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

elif tab == "RU":
    st.header("RU UFV")

    if not st.session_state.logado:
        st.warning("Faça login primeiro para usar o chat.")
    else:
        st_autorefresh(interval=10_000, key="chat_refresh")
        # Atualiza a cada 10 segundos
        #st.experimental_autorefresh(interval=10_000, key="chat_refresh")

        # Cria dataframe alinhando por colunas
        df = pd.DataFrame(_get_cardapio(datetime.now().strftime("%d/%m/%Y"))).T
        df.columns = ["Café da Manhã", "Almoço", "Jantar"]

        st.title("Cardápio do Dia")
        st.table(df.fillna(""))  # preenche espaços vazios

        # Carregar mensagens
        mensagens = see_chat()
        mensagens = mensagens[29:]  # descarta as iniciais

        st.subheader("Discussão")

        mensagens_html = ""
        for msg in mensagens:
            try:
                nome, conteudo = msg.split("] ", 1)
                nome = nome.strip("[]")
            except ValueError:
                nome, conteudo = "Desconhecido", msg

            mensagens_html += f"""
            <div style="margin-bottom:6px;">
                <span style="color:#4fc3f7; font-weight:bold;">{nome}:</span> 
                <span style="color:#ffffff;">{conteudo}</span>
            </div>
            """

        st.markdown(
            f"""
            <div id="chat-box" style="
                background-color:#000000;
                border:1px solid #444;
                border-radius:6px;
                padding:10px;
                height:250px;
                overflow-y:scroll;
            ">
                {mensagens_html}
            </div>

            <script>
                var chatBox = document.getElementById("chat-box");
                if (chatBox) {{
                    chatBox.scrollTop = chatBox.scrollHeight;
                }}
            </script>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Input de mensagem
        st.subheader("Enviar mensagem")
        mensagem_env = st.text_input("Digite sua mensagem aqui:")

        if st.button("Enviar", use_container_width=True):
            if mensagem_env.strip():
                send_msg(f"[{st.session_state.sessao.nome}] {mensagem_env}")
                st.success("Mensagem enviada!")
                st.rerun()  # força atualizar o chat logo após enviar
            else:
                st.error("Mensagem vazia não pode ser enviada.")

#
