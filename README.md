# Álbum de fotos de casamento

Site Flask responsivo para convidados enviarem fotos para uma pasta privada no Google Drive. Sem banco de dados. Aceita até 10 fotos JPG/PNG/WebP por envio, com limite de 16 MB por requisição. As imagens são otimizadas e convertidas em JPEG.

## Configurar Google Drive

1. Entre no https://console.cloud.google.com e crie um projeto.
2. Ative a **Google Drive API** em APIs e serviços > Biblioteca.
3. Configure a tela de consentimento em **Google Auth Platform**. Se estiver em modo Testing, adicione o e-mail que autorizará o Drive como usuário de teste.
4. Crie um cliente OAuth do tipo **Aplicativo para computador**. Baixe o JSON e coloque na pasta local deste projeto com o nome **credentials.json**. Nunca envie esse arquivo ao GitHub.
5. No seu computador, execute: pip install -r requirements.txt
6. Execute: python obter_token.py
7. Autorize com a conta Google que receberá as fotos. O script mostrará GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET e GOOGLE_REFRESH_TOKEN. Guarde os valores somente em local seguro.
8. Configure essas três variáveis de ambiente no computador. Execute: python criar_pasta.py
9. Copie o GOOGLE_DRIVE_FOLDER_ID retornado. Essa pasta será criada no Google Drive da conta que autorizou o app.

**Atenção:** pastas criadas manualmente podem gerar erro 403 ou 404 quando o app usa o escopo drive.file. O arquivo criar_pasta.py evita isso criando a pasta pelo próprio aplicativo. Em modo de teste externo, tokens OAuth podem expirar após 7 dias: antes do casamento, revise o status de publicação do aplicativo Google e teste a autorização novamente. O Google pode exigir verificações para determinados modos de publicação e escopos.

## Configurar Render

1. Acesse https://dashboard.render.com.
2. Clique em **New > Web Service**, escolha o repositório **nicollas-ar/casamento** (branch main) ou use **New > Blueprint**, que lê o render.yaml.
3. Para Web Service manual, configure:
   - Runtime: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
4. No ambiente (Environment), adicione:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
   - GOOGLE_REFRESH_TOKEN
   - GOOGLE_DRIVE_FOLDER_ID
   - SECRET_KEY (string aleatória longa)
   - COUPLE_NAMES (nomes do casal)
   - WEDDING_DATE (data do casamento)
   - WEDDING_HEADING (frase de destaque opcional)
5. Faça o Deploy. Abra o site e envie uma foto real. Confira a pasta no Drive para validar a integração. A rota /saude apenas verifica se o Flask está respondendo, não se o Drive está conectado.

## Executar localmente

Instale as dependências, defina as variáveis de ambiente e execute python app.py. A página ficará em http://localhost:5000, mesmo sem o Drive configurado; mas enviar fotos exigirá a autorização.

## Cuidados de produção

- Nunca publique secrets ou refresh tokens no GitHub; use Environment no Render.
- O formulário não exige login dos convidados: divulgue o link apenas entre participantes e monitore envios maliciosos.
- Para eventos grandes, acrescente proteção anti-spam e moderação.
- A instância gratuita do Render pode suspender por inatividade; a rota /saude não impede essa suspensão.
- Não há armazenamento local persistente no Render: o aplicativo envia as imagens diretamente para o Drive.
- Faça testes com celulares reais e preserve backups das fotos após o casamento.
