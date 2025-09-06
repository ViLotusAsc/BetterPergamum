import requests
import os
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import urllib3
import json


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Session:
    def __init__(self):
        self.phpsessid = "-1"
        self.nome = "Not informed"

    def _create_session(self):
        headers = {
            'Host': 'pergamum.ufv.br',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        response = requests.get('https://pergamum.ufv.br/biblioteca/index.php', headers=headers, verify=False)

        self.phpsessid = response.cookies.get_dict()["PHPSESSID"]
        return (response.cookies.get_dict()["PHPSESSID"])
    

    def _login(self, matricula, senha):
        cookies = {
            '_ga': 'GA1.1.2037255739.1755903321',
            '_ga_3GKTCB3HHS': 'GS2.1.s1755903320' + os.getenv('o1', '') + os.getenv('g0', '') + os.getenv('t1755903320', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            '_ga_V5B0KG5WW5': 'GS2.1.s1756825688' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756825845', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            'PHPSESSID': self.phpsessid,
            '_ga_KLR8GVHKBC': 'GS2.1.s1756844283' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756844343', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            '_ga_7H6KMW913P': 'GS2.1.s1756847215' + os.getenv('o2', '') + os.getenv('g1', '') + os.getenv('t1756848763', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
        }

        headers = {
            'Host': 'pergamum.ufv.br',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://pergamum.ufv.br',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://pergamum.ufv.br/biblioteca_s/php/login_usu.php?flag=index.php',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'Cookie': '_ga=GA1.1.2037255739.1755903321; _ga_3GKTCB3HHS=GS2.1.s1755903320' + os.getenv('o1', '') + os.getenv('g0', '') + os.getenv('t1755903320', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; _ga_V5B0KG5WW5=GS2.1.s1756825688' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756825845', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; PHPSESSID=mfskjgprjp9bkjg4l7llgsbdr1; _ga_KLR8GVHKBC=GS2.1.s1756844283' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756844343', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; _ga_7H6KMW913P=GS2.1.s1756847215' + os.getenv('o2', '') + os.getenv('g1', '') + os.getenv('t1756848763', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'flag': 'index.php',
            'login': matricula,
            'password': senha,
            'button': 'Acessar',
            'numero_mestre': '',
            'ifsp_categ': '',
            'lab_com_solicitacao': '',
        }

        if self.phpsessid == -1:
            return ("No PHPSESSID value provided, should use Session()._create_session first.")

        response = requests.post('https://pergamum.ufv.br/biblioteca_s/php/login_usu.php', cookies=cookies, headers=headers, data=data, verify=False)

        nomes = re.findall(r"<strong>(.*?)</strong>", response.text)
        self.nome = nomes[1]

        return response
    
    def _book_search(self,_nome):
        cookies = {
            '_ga': 'GA1.1.2037255739.1755903321',
            '_ga_3GKTCB3HHS': 'GS2.1.s1755903320' + os.getenv('o1', '') + os.getenv('g0', '') + os.getenv('t1755903320', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            '_ga_V5B0KG5WW5': 'GS2.1.s1756825688' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756825845', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            '_ga_KLR8GVHKBC': 'GS2.1.s1756844283' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756844343', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            '_ga_7H6KMW913P': 'GS2.1.s1756847215' + os.getenv('o2', '') + os.getenv('g1', '') + os.getenv('t1756848763', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', ''),
            'PHPSESSID': 'jn9lib1hk5dcf7tt3sh0jbtn75',
        }

        headers = {
            'Host': 'www.pergamum.ufv.br',
            'Method': 'POST /biblioteca/index.php HTTP/1.1',
            'sec-ch-ua-platform': '"Windows"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'Accept': '*/*',
            'Origin': 'https://www.pergamum.ufv.br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.pergamum.ufv.br/biblioteca/index.php',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'Cookie': '_ga=GA1.1.2037255739.1755903321; _ga_3GKTCB3HHS=GS2.1.s1755903320' + os.getenv('o1', '') + os.getenv('g0', '') + os.getenv('t1755903320', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; _ga_V5B0KG5WW5=GS2.1.s1756825688' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756825845', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; _ga_KLR8GVHKBC=GS2.1.s1756844283' + os.getenv('o1', '') + os.getenv('g1', '') + os.getenv('t1756844343', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; _ga_7H6KMW913P=GS2.1.s1756847215' + os.getenv('o2', '') + os.getenv('g1', '') + os.getenv('t1756848763', '') + os.getenv('j60', '') + os.getenv('l0', '') + os.getenv('h0', '') + '; PHPSESSID=jn9lib1hk5dcf7tt3sh0jbtn75',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = f'rs=ajax_resultados&rst=&rsrnd=1756848921468&rsargs[]=20&rsargs[]=0&rsargs[]=1&rsargs[]={quote(_nome)}&rsargs[]=&rsargs[]=%2C&rsargs[]=indice&rsargs[]=&rsargs[]=&rsargs[]=&rsargs[]=&rsargs[]=1&rsargs[]=&rsargs[]=&rsargs[]=obra&rsargs[]=68b738dbdeeaf&rsargs[]=&rsargs[]=&rsargs[]=&rsargs[]='

        response = requests.post('https://www.pergamum.ufv.br/biblioteca/index.php', cookies=cookies, headers=headers, data=data, verify=False)

        soup = BeautifulSoup(response.text, "html.parser")

        def extrair_itens(html: str):
            soup = BeautifulSoup(html, "html.parser")

            itens = []
            for a_titulo in soup.find_all("a", attrs={"class": re.compile(r"\blink_azul\b")}):
                # Nome/título
                nome = a_titulo.get_text(" ", strip=True).replace("\xa0", " ")

                tr_titulo = a_titulo.find_parent("tr")
                numero = None

                if tr_titulo:
                    tr_num = tr_titulo.find_next_sibling("tr")
                    if tr_num:
                        a_num = tr_num.find("a", attrs={"class": re.compile(r"\blink_reserva\b")})
                        if a_num:
                            numero = a_num.get_text(" ", strip=True).replace("\xa0", " ")

                if numero is None:
                    prox_reserva = a_titulo.find_all_next("a", attrs={"class": re.compile(r"\blink_reserva\b")}, limit=1)
                    if prox_reserva:
                        numero = prox_reserva[0].get_text(" ", strip=True).replace("\xa0", " ")

                itens.append({"nome": nome, "numero_chamada": numero})

            return itens

        resultados = extrair_itens(response.text)
        return resultados
    
    def _search_debt(self):
        cookies = {
            'PHPSESSID': self.phpsessid,
        }

        headers = {
            'Host': 'pergamum.ufv.br',
            'Method': 'POST /biblioteca_s/meu_pergamum/emp_debito.php HTTP/1.1',
            'sec-ch-ua-platform': '"Windows"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'Accept': '*/*',
            'Origin': 'https://pergamum.ufv.br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://pergamum.ufv.br/biblioteca_s/meu_pergamum/emp_debito.php',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # 'Cookie': 'PHPSESSID=odu5s15j1qtbo6tta41806def2',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'rs=ajax_mostra_tabela&rst=&rsrnd=1757165872989&rsargs[]=06/09/2024&rsargs[]=06/09/2025'

        response = requests.post(
            'https://pergamum.ufv.br/biblioteca_s/meu_pergamum/emp_debito.php',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )

        pattern = re.compile(
            r"class=\\'box_azul_left\\'>(.*?)</td>",
            re.S
        )
        pattern_multa = re.compile(
            r"class=\\'box_magenta_c\\'>(.*?)</td>",
            re.S
        )

        matches = pattern.findall(response.text)
        matches_multa = pattern_multa.findall(response.text)
        matches.pop(0)
        matches_multa.pop(0)


        result = []
        for nome in matches:
            # Remove tags HTML (<i>, <strong>, etc.)
            nome_limpo = re.sub(r"<.*?>", "", nome).strip()
            result.append(nome_limpo)
        
        retorno = []
        for nome_ in result:
            retorno.append({"nome":nome_, "debt":"0"})

        counter = 0
        for preco in matches_multa:
            retorno[counter]["debt"] = preco
            counter+=1


        return retorno




# sessao = Session()
# sessao._create_session()
# print(sessao.phpsessid)
# sessao._login("120570", "4432")
# sessao._search_debt()



# nome_livro = input("Digite o titulo do livro que quer procurar: ")
# livros = sessao._book_search(nome_livro)
# for livro in livros:
#     print(f"Nome do livro: {livro['nome']}\nN. de Chamada: {livro['numero_chamada']}\n\n")
