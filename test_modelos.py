from model import *

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros    
url_dados = "./MachineLearning/data/test_dataset_obesidade.csv"
colunas =[
    'genero_masculino', 'idade', 'historico_familiar_sobrepeso',
    'consumo_alta_caloria_com_frequencia', 'consumo_vegetais_com_frequencia',
    'refeicoes_dia', 'consumo_alimentos_entre_refeicoes', 'fumante',
    'consumo_agua', 'monitora_calorias_ingeridas', 'nivel_atividade_fisica',
    'nivel_uso_tela', 'consumo_alcool', 'transporte_automovel',
    'transporte_bicicleta', 'transporte_motocicleta', 'transporte_publico',
    'transporte_caminhada', 'outcome'
]

# Carga dos dados
dataset = Carregador.carregar_dados(url_dados, colunas)
array = dataset.values
X = array[:,0:-1]
y = array[:,-1]
 
# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = './MachineLearning/models/modelo_obesidade.pkl'
    modelo_knn = Model.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn = Avaliador.avaliar(modelo_knn, X, y)
    # Testando as métricas do KNN
    assert acuracia_knn >= 0.80