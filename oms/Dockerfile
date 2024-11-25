# Dockerfile para oms
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o requirements.txt para o diretório /app
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do diretório local para /app dentro do contêiner
COPY . /app/

# Expor a porta 8001 para a aplicação
EXPOSE 8001

# Comando para rodar a aplicação
CMD ["uvicorn", "oms.main:app", "--host", "0.0.0.0", "--port", "8001"]
