from pydantic import BaseModel
from typing import Optional, List
from model.person_routine import PersonRoutine
import json
import numpy as np

class PersonRoutineSchema(BaseModel):
    """ Define como uma nova rotina a ser inserido deve ser representado
    """
    genero_masculino: int = 0  # Mulher
    idade: int = 25  # Idade 25 anos
    historico_familiar_sobrepeso: int = 0  # Sem histórico familiar de obesidade
    consumo_alta_caloria_com_frequencia: int = 0  # Não consome alta caloria com frequência
    consumo_vegetais_com_frequencia: int = 1  # Alto consumo de vegetais
    refeicoes_dia: int = 3  # Três refeições por dia
    consumo_alimentos_entre_refeicoes: int = 0  # Não consome alimentos entre refeições
    fumante: int = 0  # Não fumante
    consumo_agua: float = 2.3  # Consumo moderado de água
    monitora_calorias_ingeridas: int = 1  # Monitora calorias ingeridas
    nivel_atividade_fisica: int = 3  # Alto nível de atividade física
    nivel_uso_tela: int = 1  # Uso moderado de telas
    consumo_alcool: int = 0  # Não consome álcool
    transporte_automovel: int = 0  # Não usa carro como principal transporte
    transporte_bicicleta: int = 1  # Usa bicicleta
    transporte_motocicleta: int = 0  # Não usa motocicleta
    transporte_publico: int = 1  # Usa transporte público
    transporte_caminhada: int = 1  # Caminha como meio de transporte

    
class PersonRoutineViewSchema(BaseModel):
    """Define como uma rotina será retornado
    """
    id: int = 1
    genero_masculino: int = 0  # Mulher
    idade: int = 25  # Idade 25 anos    
    historico_familiar_sobrepeso: int = 0  # Sem histórico familiar de obesidade
    consumo_alta_caloria_com_frequencia: int = 0  # Não consome alta caloria com frequência
    consumo_vegetais_com_frequencia: int = 1  # Alto consumo de vegetais
    refeicoes_dia: int = 3  # Três refeições por dia
    consumo_alimentos_entre_refeicoes: int = 0  # Não consome alimentos entre refeições
    fumante: int = 0  # Não fumante
    consumo_agua: float = 2.2  # Consumo moderado de água
    monitora_calorias_ingeridas: int = 1  # Monitora calorias ingeridas
    nivel_atividade_fisica: int = 3  # Alto nível de atividade física
    nivel_uso_tela: int = 1  # Uso moderado de telas
    consumo_alcool: int = 0  # Não consome álcool
    transporte_automovel: int = 0  # Não usa carro como principal transporte
    transporte_bicicleta: int = 1  # Usa bicicleta
    transporte_motocicleta: int = 0  # Não usa motocicleta
    transporte_publico: int = 1  # Usa transporte público
    transporte_caminhada: int = 1  # Caminha como meio de transporte
    outcome: int = None
    
class PersonRoutineBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do paciente.
    """
    name: str = "Maria"

class ListaPersonRoutineSchema(BaseModel):
    """Define como uma lista de pacientes será representada
    """
    person_routine: List[PersonRoutineBuscaSchema]

    
class PersonRoutineDelSchema(BaseModel):
    """Define como um paciente para deleção será representado
    """
    name: str = "Maria"
    
# Apresenta apenas os dados de um paciente    
def apresenta_person_routine(person_routine: PersonRoutine):
    """ Retorna uma representação do paciente seguindo o schema definido em
        HealthRoutineViewSchema.
    """
    return {
        "genero_masculino": person_routine.genero_masculino,
        "idade": person_routine.idade,
        "historico_familiar_sobrepeso": person_routine.historico_familiar_sobrepeso,
        "consumo_alta_caloria_com_frequencia": person_routine.consumo_alta_caloria_com_frequencia,
        "consumo_vegetais_com_frequencia": person_routine.consumo_vegetais_com_frequencia,
        "refeicoes_dia": person_routine.refeicoes_dia,
        "consumo_alimentos_entre_refeicoes": person_routine.consumo_alimentos_entre_refeicoes,
        "fumante": person_routine.fumante,
        "consumo_agua": person_routine.consumo_agua,
        "monitora_calorias_ingeridas": person_routine.monitora_calorias_ingeridas,
        "nivel_atividade_fisica": person_routine.nivel_atividade_fisica,
        "nivel_uso_tela": person_routine.nivel_uso_tela,
        "consumo_alcool": person_routine.consumo_alcool,
        "transporte_automovel": person_routine.transporte_automovel,
        "transporte_bicicleta": person_routine.transporte_bicicleta,
        "transporte_motocicleta": person_routine.transporte_motocicleta,
        "transporte_publico": person_routine.transporte_publico,
        "transporte_caminhada": person_routine.transporte_caminhada,
        "data_insercao": person_routine.data_insercao,
        "outcome": person_routine.outcome
    }
    
# Apresenta uma lista de pacientes
def apresenta_person_routines(person_routine: List[PersonRoutine]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    result = []
    for person_routine in person_routine:
        result.append({
            "id": person_routine.id,
            "genero_masculino": person_routine.genero_masculino,
            "idade": person_routine.idade,
            "historico_familiar_sobrepeso": person_routine.historico_familiar_sobrepeso,
            "consumo_alta_caloria_com_frequencia": person_routine.consumo_alta_caloria_com_frequencia,
            "consumo_vegetais_com_frequencia": person_routine.consumo_vegetais_com_frequencia,
            "refeicoes_dia": person_routine.refeicoes_dia,
            "consumo_alimentos_entre_refeicoes": person_routine.consumo_alimentos_entre_refeicoes,
            "fumante": person_routine.fumante,
            "consumo_agua": person_routine.consumo_agua,
            "monitora_calorias_ingeridas": person_routine.monitora_calorias_ingeridas,
            "nivel_atividade_fisica": person_routine.nivel_atividade_fisica,
            "nivel_uso_tela": person_routine.nivel_uso_tela,
            "consumo_alcool": person_routine.consumo_alcool,
            "transporte_automovel": person_routine.transporte_automovel,
            "transporte_bicicleta": person_routine.transporte_bicicleta,
            "transporte_motocicleta": person_routine.transporte_motocicleta,
            "transporte_publico": person_routine.transporte_publico,
            "transporte_caminhada": person_routine.transporte_caminhada,
            "data_insercao": person_routine.data_insercao,
            "outcome": person_routine.outcome
        })

    return {"person_routines": result}

