Para executar o Flask-Framework é recomendado o uso da versão Python 3.12.10 e é necessário criar um ambiente virtual com o seguinte comando:

python -m venv .venv

e de seguida instalar as bibliotecas necessárias com o comando:

pip install -r requirements.txt

É necessário também copiar os ficheiros dos pesos dos modelos para dentro da pasta "model_weights".

Para executar o projeto, basta correr o comando:

py app.py run