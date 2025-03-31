# Usa uma imagem leve do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY requirements.txt .

# Instala as dependências a partir do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o diretório de trabalho
COPY . .

# Comando para rodar a API Flask
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
