

### README.md Atualizado

```markdown
# Monitoramento de Preços de Passagens Aéreas

## Descrição
Este projeto monitora os preços de passagens aéreas entre diferentes localidades específicas e envia alertas por e-mail quando o preço estiver igual ou abaixo de um valor predeterminado. O sistema utiliza recursos gratuitos da AWS para executar as tarefas de monitoramento de forma periódica e eficiente.

## Tecnologias Utilizadas
- **Linguagem de Programação:** Python 3
- **Serviços em Nuvem:**
  - AWS Lambda: Para executar o script de monitoramento de preços periodicamente
  - Amazon CloudWatch: Para agendar e monitorar a execução do script
  - Amazon Simple Email Service (SES): Para enviar notificações por e-mail
- **APIs Externas:**
  - API do Skyscanner: Para buscar os preços das passagens aéreas

## Funcionalidades do Sistema
- **Monitoramento de Preços:**
  - Busca os preços das passagens aéreas de locais de origem para destinos específicos utilizando a API do Skyscanner
  - Executa a busca em horários variados ao longo do dia, incluindo horários randomizados para otimizar a chance de encontrar promoções e evitar detecção por algoritmos de precificação dinâmica
- **Envio de Alertas:**
  - Compara os preços encontrados com um valor limite predeterminado
  - Envia um e-mail de alerta para um ou mais endereços de e-mail configurados quando um preço igual ou inferior ao limite é encontrado
- **Configuração e Gerenciamento:**
  - Utiliza variáveis de ambiente para armazenar informações sensíveis como credenciais de e-mail e chave da API do Skyscanner
  - Permite configuração de múltiplos destinos para monitoramento

## Estrutura do Projeto

```plaintext
app-passagens/
│
├── venv/                    # Ambiente virtual
├── .env                     # Arquivo de variáveis de ambiente
├── config.py                # Arquivo de configuração
├── email_service.py         # Serviço de envio de e-mails
├── price_alert.py           # Script principal
├── price_fetcher.py         # Serviço de busca de preços
├── README.md                # Documentação do projeto
└── requirements.txt         # Dependências do projeto
```

## Configuração do Ambiente

1. Clone este repositório.
2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais:
   ```plaintext
   SKYSCANNER_API_KEY=your_skyscanner_api_key
   TO_EMAILS=email1@example.com,email2@example.com  # Lista de emails separados por vírgula
   ```

## Execução do Script

Para executar o script localmente:
```bash
python price_alert.py
```

## Implantação na AWS

### Passo 1: Configuração do Amazon SES

1. **Verificar o Email**:
   - Acesse o console do Amazon SES.
   - No painel de navegação, escolha "Emails verificados".
   - Verifique o seu email que será usado como remetente. Você receberá um email de verificação. Clique no link para confirmar.

2. **Configurar Permissões de Envio**:
   - Certifique-se de que o seu email está autorizado a enviar mensagens pelo Amazon SES.

### Passo 2: Configuração da Função Lambda

1. **Criar a Função Lambda**:
   - Acesse o console do AWS Lambda.
   - Clique em "Create function".
   - Selecione "Author from scratch".
   - Dê um nome à função (por exemplo, `PriceAlertFunction`).
   - Escolha `Python 3.x` como runtime.
   - Clique em "Create function".

2. **Carregar o Script**:
   - No painel de configuração da função Lambda, role para baixo até a seção "Function code".
   - No campo "Code source", escolha "Upload a .zip file".
   - Crie um arquivo zip contendo `config.py`, `email_service.py`, `price_alert.py`, `price_fetcher.py` e `requirements.txt`.
   - Clique em "Upload" e selecione o arquivo zip.

3. **Configurar Variáveis de Ambiente**:
   - No painel de configuração da função Lambda, role para baixo até a seção "Environment variables".
   - Adicione as variáveis de ambiente `SKYSCANNER_API_KEY` e `TO_EMAILS`.

4. **Configurar o Handler**:
   - No painel de configuração da função Lambda, role para cima até a seção "Runtime settings".
   - Defina o handler como `price_alert.lambda_handler`.

### Passo 3: Configuração das Permissões da Função Lambda

1. **Adicionar Permissões para o SES**:
   - No painel de configuração da função Lambda, clique na aba "Permissions".
   - Clique no link para o papel de execução (role) associado à sua função Lambda.
   - No painel do IAM, clique em "Attach policies".
   - Adicione a política `AmazonSESFullAccess`.

### Passo 4: Configuração do Agendamento com Amazon CloudWatch

1. **Criar uma Regra de Evento**:
   - Acesse o console do CloudWatch.
   - No painel de navegação, escolha "Rules".
   - Clique em "Create rule".
   - Na seção "Event Source", escolha "Event Source" e selecione "Schedule".
   - Configure uma expressão cron ou taxa para definir a frequência de execução (por exemplo, `rate(1 hour)` para executar a cada hora).

2. **Adicionar o Alvo**:
   - Na seção "Targets", clique em "Add target".
   - Selecione "Lambda function".
   - Escolha a função Lambda que você criou (`PriceAlertFunction`).

3. **Configurar Permissões de Invocação**:
   - No painel de regras do CloudWatch, adicione permissões para permitir que o CloudWatch invoque sua função Lambda.

## Testes e Validação

### Testes Locais

1. **Ativar o Ambiente Virtual**:
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

2. **Executar o Script**:
   ```bash
   python price_alert.py
   ```

### Testes na AWS

1. **Criar um Evento de Teste**:
   - No console da AWS Lambda, vá para a função Lambda que você criou.
   - Clique em "Test".
   - Configure um evento de teste e execute.

2. **Verificar os Logs**:
   - Acesse o console do CloudWatch.
   - No painel de navegação, escolha "Logs".
   - Verifique os logs da função Lambda para garantir que está sendo executada corretamente.

## Monitoramento e Manutenção

- **Monitoramento**:
  - Use o CloudWatch para monitorar a execução da função Lambda e verificar os logs.
  - Configure alarmes no CloudWatch para notificá-lo sobre falhas ou comportamento inesperado.

- **Ajustes de Frequência**:
  - Ajuste a frequência e horários das buscas conforme necessário para otimizar as chances de encontrar promoções e evitar detecção por algoritmos de precificação dinâmica.

- **Manutenção Contínua**:
  - Atualize as dependências e revise o código regularmente para garantir a eficiência e segurança do sistema.
  - Monitore o uso dos recursos da AWS para garantir que está dentro dos limites gratuitos.

## Autor

Rafael Dias  
[rafasdiasdev@gmail.com](mailto:rafasdiasdev@gmail.com)
```
