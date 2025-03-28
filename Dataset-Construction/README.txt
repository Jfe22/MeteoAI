Este zip contém os scripts de construção do dataset utilizado para treino do modelo, assim como o próprio dataset.

Para correr os scripts data_fetch e dataset_construction é necessário criar um ambiente virtual com o seguinte comando: 

python -m venv venv

e de seguida instalar as bibliotecas necessárias com o comando:

pip install -r requirements.txt

Para correr o modelo presente na pasta Network-Training é necessário copiar a pasta "precipitation_dataset" para dentro da pasta "datasets" do "Network-Training".