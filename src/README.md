# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

Todo o código-fonte está no arquivo `app.py`

## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit/Gradio)
├── .env                # Configurações (API keys, etc.)
├── /images               # imagem usada no README.md
└── requirements.txt    # Dependências


```

## Exemplo de requirements.txt

```
streamlit
pandas
openai
python-dotenv
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação, estando na pasta onde o app.py está localizado ou definindo seu caminho
streamlit run app.py
```

Não rodar o app.py diretamente usando python.

## Evidência da execução

![Captura de tela](/images/preview.png)
