#Imports - Bibliotecas usadas
import requests
from bs4 import BeautifulSoup, Tag
from smtplib import SMTP
from email.message import EmailMessage
import os
from zoneinfo import ZoneInfo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


#variáveis
Cardapio = dict[str, list[str]]
TodosCardapios = dict[str, Cardapio]
url_sescs = {
    "SESC Pompeia 🏭":"https://www.sescsp.org.br/editorial/cardapio-semanal-sesc-pompeia-2/",
    "SESC Casa Verde 🌿":"https://www.sescsp.org.br/editorial/cardapio-semanal-sesc-casa-verde/",
    "SESC Carmo 🏛":"https://www.sescsp.org.br/editorial/cardapio-semanal-sesc-carmo-2/",
    # "SESC Pinheiros 🌲":"https://www.sescsp.org.br/editorial/cardapio-pinheiros/"
    }

custom_headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
"Accept-Language": "pt-BR"
}


def consultarsitesesc(url: str): 
    response = requests.get(url,custom_headers)
    html = response.text

    if response.status_code == 200:
        return BeautifulSoup(html, 'html.parser')
    
    else:
        return {}

     

def extrairdiasingredientes(url: str):
    soup = consultarsitesesc(url)
    cardapio: dict[str, list[str]] = {}

    classes_dias = [
    "has-light-green-cyan-background-color",
    "has-very-light-gray-to-cyan-bluish-gray-gradient-background",
    "has-very-light-gray-to-cyan-bluish-gray-gradient-background",
    ]

    datas = soup.find_all(
    'p',
    class_="has-medium-font-size",
    )

    datas = [
    d for d in datas
    if any(c in d.get("class", []) for c in classes_dias)
    ]

    for d in datas:
        d: Tag
        dia = d.get_text(strip=True).strip()
        cardapio[dia] = []

        ingredientes = d.find_next_siblings("p")

        for ingrediente in ingredientes:
            ingrediente:Tag

            if any(c in ingrediente.get("class", []) for c in classes_dias):
                break

            texto = ingrediente.get_text(strip=True)
            texto = texto. replace("-Fruta","– Fruta").replace("-Doce","– Doce").strip()
            
            if texto:
                cardapio[dia].append(texto)

    return cardapio



def enviar_email(todos_cardapaios: TodosCardapios):
    
    remetente = os.getenv("EMAIL_FROM")
    senha = os.getenv("SENHAAPP")
    destinatario = os.getenv("EMAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = "Cardápio SESC"
    msg["From"] = remetente
    msg["To"] = destinatario


    #Corpo do email
    corpo = []
    for unidade,cardapio in todos_cardapaios.items():
        corpo.append(f"\nUnidade: {unidade}")

        if not cardapio:
            corpo.append("Nenhum cardápio encontrado")
            continue

        for dia,itens in cardapio.items():
            corpo.append(f"\nDia: {dia}")
        
            
            for item in itens:
                corpo.append(item)

        corpo.append("\n")

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    data_envio = agora.strftime("%d/%m/%Y às %H:%M")

    corpo.append(f"\nEmail enviado: {data_envio}")

    msg.set_content("\n".join(corpo))

    #conexão SMTP
    with SMTP ("smtp.gmail.com",587) as smtp:
        smtp.starttls()
        smtp.login(remetente,senha)
        smtp.send_message(msg)

        print("Email enviado com sucesso", data_envio)

    



def main():

    todos_cardapios = {}

    for nome, url in url_sescs.items():
        print(f"Buscando {nome}")
        todos_cardapios[nome] = extrairdiasingredientes(url)


    enviar_email(todos_cardapios)
    


if __name__ == "__main__":
    main()