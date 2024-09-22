from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
person_routine_tag = Tag(name="Rotina", description="Adição, visualização, remoção e predição de rotina")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de rotina
@app.get('/person_routines', tags=[person_routine_tag],
         responses={"200": PersonRoutineViewSchema, "404": ErrorSchema})
def get_person_routines():
    """Lista todos as rotinas cadastrados na base
    Args:
       none
        
    Returns:
        list: lista das rotinas cadastrados na base
    """
    logger.debug("Coletando dados sobre todas as rotinas")
    # Criando conexão com a base
    session = Session()
    # Buscando todas as rotinas
    person_routines = session.query(PersonRoutine).all()
    
    if not person_routines:
        # Se não houver person_routines
        return {"person_routines": []}, 200
    else:
        logger.debug(f"%d person_routines econtrados" % len(person_routines))
        print(person_routines)
        return apresenta_person_routines(person_routines), 200


# Rota de adição de pessoas
@app.post('/person_routine', tags=[person_routine_tag],
          responses={"200": PersonRoutineViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PersonRoutineSchema):
    """Adiciona uma nova rotina à base de dados
    Retorna uma representação das pessoas e diagnósticos associados.
    
    Args:
        nome (str): nome da pessoa
        genero_masculino (int): 1 se masculino, 0 se feminino.
        idade (int): idade da pessoa.
        historico_familiar_sobrepeso (int): 1 se há histórico, 0 se não.
        consumo_alta_caloria_com_frequencia (int): 1 se consome frequentemente, 0 se não.
        consumo_vegetais_com_frequencia (int): 1 se consome frequentemente, 0 se não.
        refeicoes_dia (int): número de refeições por dia.
        consumo_alimentos_entre_refeicoes (int): 1 se consome, 0 se não.
        fumante (int): 1 se fuma, 0 se não.
        consumo_agua (int): quantidade de água consumida em litros por dia.
        monitora_calorias_ingeridas (int): 1 se monitora, 0 se não.
        nivel_atividade_fisica (int): nível de atividade física em uma escala de 1 a 10.
        nivel_uso_tela (int): nível de uso de telas em uma escala de 1 a 10.
        consumo_alcool (int): 1 se consome álcool, 0 se não.
        transporte_automovel (int): 1 se utiliza automóvel, 0 se não.
        transporte_bicicleta (int): 1 se utiliza bicicleta, 0 se não.
        transporte_motocicleta (int): 1 se utiliza motocicleta, 0 se não.
        transporte_publico (int): 1 se utiliza transporte público, 0 se não.
        transporte_caminhada (int): 1 se caminha, 0 se não.
        
    Returns:
        dict: representação da rotina da pessoa e diagnóstico associado
    """
    print('dados vindo do form: ',form)
    # Recuperando os dados do formulário
    nome = form.nome
    genero_masculino = form.genero_masculino
    idade = form.idade
    historico_familiar_sobrepeso = form.historico_familiar_sobrepeso
    consumo_alta_caloria_com_frequencia = form.consumo_alta_caloria_com_frequencia
    consumo_vegetais_com_frequencia = form.consumo_vegetais_com_frequencia
    refeicoes_dia = form.refeicoes_dia
    consumo_alimentos_entre_refeicoes = form.consumo_alimentos_entre_refeicoes
    fumante = form.fumante
    consumo_agua = form.consumo_agua
    monitora_calorias_ingeridas = form.monitora_calorias_ingeridas
    nivel_atividade_fisica = form.nivel_atividade_fisica
    nivel_uso_tela = form.nivel_uso_tela
    consumo_alcool = form.consumo_alcool
    transporte_automovel = form.transporte_automovel
    transporte_bicicleta = form.transporte_bicicleta
    transporte_motocicleta = form.transporte_motocicleta
    transporte_publico = form.transporte_publico
    transporte_caminhada = form.transporte_caminhada

        
    # Preparando os dados para o modelo
    X_input = PreProcessador.preparar_form(form)
    # Carregando modelo
    model_path = './MachineLearning/pipelines/rf_obesidade_pipeline.pkl'
    # modelo = Model.carrega_modelo(ml_path)
    modelo = Pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    outcome = int(Model.preditor(modelo, X_input)[0])
    
    person_routine = PersonRoutine(
        nome=nome,
        genero_masculino=genero_masculino,
        idade=idade,
        historico_familiar_sobrepeso=historico_familiar_sobrepeso,
        consumo_alta_caloria_com_frequencia=consumo_alta_caloria_com_frequencia,
        consumo_vegetais_com_frequencia=consumo_vegetais_com_frequencia,
        refeicoes_dia=refeicoes_dia,
        consumo_alimentos_entre_refeicoes=consumo_alimentos_entre_refeicoes,
        fumante=fumante,
        consumo_agua=consumo_agua,
        monitora_calorias_ingeridas=monitora_calorias_ingeridas,
        nivel_atividade_fisica=nivel_atividade_fisica,
        nivel_uso_tela=nivel_uso_tela,
        consumo_alcool=consumo_alcool,
        transporte_automovel=transporte_automovel,
        transporte_bicicleta=transporte_bicicleta,
        transporte_motocicleta=transporte_motocicleta,
        transporte_publico=transporte_publico,
        transporte_caminhada=transporte_caminhada,
        outcome=outcome
    )
    logger.debug(f"Adicionando dados da rotina no banco: '{person_routine.id}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando pessoa
        session.add(person_routine)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado rotina da pessoa de nome: '{person_routine.nome}'")
        return apresenta_person_routine(person_routine), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar nova rotina :/"
        logger.warning(f"Erro ao adicionar nova rotina '{person_routine}', {error_msg}")
        logger.error(f"Erro '{e}'")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca da rotina por nome
@app.get('/person_routine', tags=[person_routine_tag],
         responses={"200": PersonRoutineViewSchema, "404": ErrorSchema})
def get_person_routine(query: PersonRoutineBuscaSchema):    
    """Faz a busca por uma rotina cadastrado na base a partir do nome

    Args:
        nome (str): nome da pessoa
        
    Returns:
        dict: representação da rotina e diagnóstico associado
    """
    
    pessoa_nome = query.nome
    logger.debug(f"Coletando dados sobre produto #{pessoa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    person_routine = session.query(PersonRoutine).filter(PersonRoutine.nome == pessoa_nome).first()
    
    if not  person_routine:
        # se o  person_routine não foi encontrado
        error_msg = f"Pessoa {pessoa_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar pessoa '{pessoa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pessoa encontrada: '{ person_routine.nome}'")
        # retorna a representação da rotina da pessoa
        return apresenta_person_routine(person_routine), 200
   
    
# Rota de remoção da rotina por nome
@app.delete('/person_routine', tags=[person_routine_tag],

            responses={"200": PersonRoutineViewSchema, "404": ErrorSchema})
def delete_person_routine(query: PersonRoutineBuscaSchema):
    """Remove uma rotina cadastrado na base a partir do nome

    Args:
        nome (str): nome da pessoa
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    person_routine_nome = unquote(query.nome)
    logger.debug(f"Deletando dados sobre a rotina da pessoa #{person_routine_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando rotina
    person_routine = session.query(PersonRoutine).filter(PersonRoutine.nome == person_routine_nome).first()
    
    if not person_routine:
        error_msg = "Rotina peesooa não encontrado na base :/"
        logger.warning(f"Erro ao deletar person_routine '{person_routine_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(person_routine)
        session.commit()
        logger.debug(f"Deletado rotina #{person_routine_nome}")
        return {"message": f"Rotina {person_routine_nome} removido com sucesso!"}, 200
    
if __name__ == '__main__':
    app.run(debug=True)