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
url = "https://www.sescsp.org.br/editorial/cardapio-semanal-sesc-pompeia-2/"






def consultarsitesesc(url: str): 
    response = requests.get(url)
    html = response.text
    
    return BeautifulSoup(html, 'html.parser')

     

def extrairdiasingredientes():
    soup = consultarsitesesc(url)
    cardapio: dict[str, list[str]] = {}
    datas = soup.find_all(
    'p',
    class_='has-light-green-cyan-background-color has-background has-medium-font-size',
    )

    for d in datas:
        d: Tag
        dia = d.get_text(strip=True).strip()
        cardapio[dia] = []

        ingredientes = d.find_next_siblings("p")

        for ingrediente in ingredientes:
            ingrediente:Tag

            if "has-light-green-cyan-background-color" in ingrediente.get("class",[]):
                break

            texto = ingrediente.get_text(strip=True)
            texto = texto. replace("-Fruta","– Fruta").replace("-Doce","– Doce").strip()
            
            if texto:
                cardapio[dia].append(texto)

    return cardapio



def enviar_email(cardapio: dict[str, list[str]]):
    remetente = os.getenv("EMAIL_FROM")
    senha = os.getenv("SENHAAPP")
    destinatario = os.getenv("EMAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = "Cardápio Sesc Pompeia"
    msg["From"] = remetente
    msg["To"] = destinatario


    #Corpo do email
    corpo = []
    for dia,itens in cardapio.items():
        corpo.append(f"\nDia: {dia}")
        
        for item in itens:
            corpo.append(item)

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
    cardapio = extrairdiasingredientes()
    enviar_email(cardapio)
    


if __name__ == "__main__":
    main()