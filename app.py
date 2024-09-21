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
    """Lista todos os pacientes cadastrados na base
    Args:
       none
        
    Returns:
        list: lista de pacientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os pacientes")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    person_routines = session.query(PersonRoutine).all()
    
    if not person_routines:
        # Se não houver person_routines
        return {"person_routines": []}, 200
    else:
        logger.debug(f"%d person_routines econtrados" % len(person_routines))
        print(person_routines)
        return apresenta_person_routine(person_routines), 200


# Rota de adição de paciente
@app.post('/person_routine', tags=[person_routine_tag],
          responses={"200": PersonRoutineViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PersonRoutineSchema):
    """Adiciona um novo paciente à base de dados
    Retorna uma representação dos pacientes e diagnósticos associados.
    
    Args:
        name (str): nome do paciente
        preg (int): número de vezes que engravidou: Pregnancies
        plas (int): concentração de glicose no plasma: Glucose
        pres (int): pressão diastólica (mm Hg): BloodPressure
        skin (int): espessura da dobra cutânea do tríceps (mm): SkinThickness
        test (int): insulina sérica de 2 horas (mu U/ml): Insulin
        mass (float): índice de massa corporal (peso em kg/(altura em m)^2): BMI
        pedi (float): função pedigree de diabetes: DiabetesPedigreeFunction
        age (int): idade (anos): Age
        
    Returns:
        dict: representação do paciente e diagnóstico associado
    """
    print('dados vindo do form: ',form)
    # Recuperando os dados do formulário
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
        
        # Checando se paciente já existe na base
        # if session.query(Paciente).filter(Paciente.name == form.name).first():
        #     error_msg = "Paciente já existente na base :/"
        #     logger.warning(f"Erro ao adicionar paciente '{person_routine.name}', {error_msg}")
        #     return {"message": error_msg}, 409
        
        # Adicionando paciente
        session.add(person_routine)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado paciente de nome: '{person_routine.id}'")
        return apresenta_person_routine(person_routine), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{person_routine}', {error_msg}")
        return {"message": error_msg}, 400
    

# # Métodos baseados em nome
# # Rota de busca de paciente por nome
# @app.get('/paciente', tags=[person_routine_tag],
#          responses={"200": PersonRoutineViewSchema, "404": ErrorSchema})
# def get_paciente(query: PersonRoutineSchema):    
#     """Faz a busca por um paciente cadastrado na base a partir do nome

#     Args:
#         nome (str): nome do paciente
        
#     Returns:
#         dict: representação do paciente e diagnóstico associado
#     """
    
#     paciente_nome = query.name
#     logger.debug(f"Coletando dados sobre produto #{paciente_nome}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
#     if not paciente:
#         # se o paciente não foi encontrado
#         error_msg = f"Paciente {paciente_nome} não encontrado na base :/"
#         logger.warning(f"Erro ao buscar produto '{paciente_nome}', {error_msg}")
#         return {"mesage": error_msg}, 404
#     else:
#         logger.debug(f"Paciente econtrado: '{paciente.name}'")
#         # retorna a representação do paciente
#         return apresenta_paciente(paciente), 200
   
    
# # Rota de remoção de paciente por nome
# @app.delete('/paciente', tags=[paciente_tag],
#             responses={"200": PacienteViewSchema, "404": ErrorSchema})
# def delete_paciente(query: PacienteBuscaSchema):
#     """Remove um paciente cadastrado na base a partir do nome

#     Args:
#         nome (str): nome do paciente
        
#     Returns:
#         msg: Mensagem de sucesso ou erro
#     """
    
#     paciente_nome = unquote(query.name)
#     logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    
#     # Criando conexão com a base
#     session = Session()
    
#     # Buscando paciente
#     paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
#     if not paciente:
#         error_msg = "Paciente não encontrado na base :/"
#         logger.warning(f"Erro ao deletar paciente '{paciente_nome}', {error_msg}")
#         return {"message": error_msg}, 404
#     else:
#         session.delete(paciente)
#         session.commit()
#         logger.debug(f"Deletado paciente #{paciente_nome}")
#         return {"message": f"Paciente {paciente_nome} removido com sucesso!"}, 200
    
# if __name__ == '__main__':
#     app.run(debug=True)