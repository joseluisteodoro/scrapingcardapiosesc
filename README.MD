# Scraping Cardápio SESC

![GitHub repo size](https://img.shields.io/github/repo-size/joseluisteodoro/scrappingcardapiosesc?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/joseluisteodoro/scrappingcardapiosesc?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/joseluisteodoro/scrappingcardapiosesc?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/joseluisteodoro/scrappingcardapiosesc?style=for-the-badge)


> Esse projeto é apenas para estudo de automações, ele consulta o site do cardápio, faz um web scraping do site, quardando em dicionário, o dia e os ingredientes. Ao final ele envia aos emails dos destinatários.

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas para as seguintes tarefas:

- [x] Extrair informações do site
- [x] Enviar por email
- [ ] Enviar via SMS
- [ ] Puxar cardápio de outras unidades


## 💻 Pré-requisitos e Instalação

Antes de começar, verifique se você atendeu aos seguintes requisitos:
- requests
- beautifulsoup4
- python-dotenv

```bash
git clone https://github.com/joseluisteodoro/scrappingcardapiosesc
cd scrappingcardapiosesc

pip install -r requirements.txt
```
## 🧾 Como usar

Configure o seu arquivo .env ou ambiente com as chaves necessárias, como:

- SENHAAPP - Senha App
    - *Não é a senha do seu gmail*
- EMAIL_FROM - Remetente
- EMAIL_TO - Emails destino, separado por vírgula


*Não se esqueça de configurar o .gitignore para que não vaze seus emails e chaves privadas.*

Após isso execute pela sua IDE ou no CMD digite:

```bash
python main.py
```