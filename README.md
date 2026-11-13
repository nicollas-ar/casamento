# Álbum de casamento — Flask + Google Drive

Site para convidados enviarem fotos por celular, diretamente para uma pasta privada do Google Drive. Sem banco de dados. Aceita JPG, PNG e WebP, até 10 imagens por envio e 16 MB por requisição.

## Passo 1 — Google Drive

1. Acesse https://console.cloud.google.com e crie um projeto.
2. Ative a **Google Drive API**.
3. Abra **Google Auth Platform** e configure a tela de consentimento OAuth. Se estiver no modo Testing, adicione seu endereço Google em **Test users**.
4. Em **Clients**, crie um cliente OAuth do tipo **Desktop app / Aplicativo para computador** e baixe o JSON. Renomeie para **credentials.json** e coloque na pasta local do projeto. Ele está no .gitignore: **não o publique**.
5. No computador, instale as dependências: `pip install -r requirements.txt`
6. Execute: `python obter_token.py`
7. Autorize com a conta Google que vai receber as fotos. O script já cria a pasta **Fotos do Casamento** e mostra os quatro valores para preencher no Render:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
   - GOOGLE_REFRESH_TOKEN
   - GOOGLE_DRIVE_FOLDER_ID

**Nunca envie tokens ou segredos em mensagens ou ao GitHub.** Se o app OAuth estiver em modo Testing (External), o refresh token pode expirar em 7 dias. Teste a autorização perto do evento e revise os requisitos de publicação do Google. A pasta é criada pelo próprio aplicativo para funcionar com o escopo limitado drive.file.

## Passo 2 — Render

1. Entre em https://dashboard.render.com > **New > Web Service** e conecte **nicollas-ar/casamento**, branch **main**. Alternativamente, use **New > Blueprint**, que lê o arquivo render.yaml.
2. Configure Runtime **Python**, Build Command `pip install -r requirements.txt`, Start Command `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`.
3. Em **Environment**, defina os 4 valores que o script mostrou no passo 1. Defina também:
   - SECRET_KEY: uma string aleatória longa
   - COUPLE_NAMES: nomes dos noivos
   - WEDDING_DATE: data do evento
   - WEDDING_HEADING: frase de destaque (opcional)
4. Clique em **Deploy**. Teste a rota `/saude`, depois envie uma foto e confira se apareceu na pasta Drive. A rota de saúde verifica o Flask, **não** a conexão com o Drive.

## Executar localmente

Depois de configurar as variáveis de ambiente, rode `python app.py` e acesse http://localhost:5000. O site abre mesmo sem as credenciais, mas o envio só funciona quando o Drive estiver configurado.

## Observações importantes

- A instância gratuita do Render pode adormecer por inatividade. A rota `/saude` não impede essa suspensão.
- O formulário público não exige login. Divulgue o link apenas aos convidados, monitore uploads e adicione rate limiting/moderação para grandes eventos.
- Não são salvas fotos no disco do Render. Faça backup das imagens após o evento.
- Teste um envio real de ponta a ponta antes de imprimir os QR Codes.
