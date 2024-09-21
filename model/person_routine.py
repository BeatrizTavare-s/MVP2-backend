from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class PersonRoutine(Base):
    __tablename__ = 'person_routine'
    
    id = Column(Integer, primary_key=True)
    genero_masculino = Column(Integer)
    idade = Column(Integer)
    historico_familiar_sobrepeso = Column(Integer)
    consumo_alta_caloria_com_frequencia = Column(Integer)
    consumo_vegetais_com_frequencia = Column(Integer)
    refeicoes_dia = Column(Integer)
    consumo_alimentos_entre_refeicoes = Column(Integer)
    fumante = Column(Integer)
    consumo_agua = Column(Float)
    monitora_calorias_ingeridas = Column(Integer)
    nivel_atividade_fisica = Column(Integer)
    nivel_uso_tela = Column(Integer)
    consumo_alcool = Column(Integer)
    transporte_automovel = Column(Integer)
    transporte_bicicleta = Column(Integer)
    transporte_motocicleta = Column(Integer)
    transporte_publico = Column(Integer)
    transporte_caminhada = Column(Integer)
    outcome = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now)

    def __init__(self, genero_masculino: bool, idade: int, historico_familiar_sobrepeso: bool,
                 consumo_alta_caloria_com_frequencia: bool, consumo_vegetais_com_frequencia: bool,
                 refeicoes_dia: int, consumo_alimentos_entre_refeicoes: bool, fumante: bool,
                 consumo_agua: float, monitora_calorias_ingeridas: bool, nivel_atividade_fisica: str,
                 nivel_uso_tela: int, consumo_alcool: bool, transporte_automovel: bool, 
                 transporte_bicicleta: bool, transporte_motocicleta: bool, transporte_publico: bool,
                 transporte_caminhada: bool, outcome: int, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma rotina
        Arguments:
            genero_masculino: bool - Gênero masculino
            idade: int - Idade da pessoa
            historico_familiar_sobrepeso: bool - Histórico familiar de sobrepeso
            consumo_alta_caloria_com_frequencia: bool - Consumo frequente de alimentos com alta caloria
            consumo_vegetais_com_frequencia: bool - Consumo frequente de vegetais
            refeicoes_dia: int - Número de refeições por dia
            consumo_alimentos_entre_refeicoes: bool - Consumo de alimentos entre refeições
            fumante: bool - Se a pessoa é fumante
            consumo_agua: float - Consumo diário de água em litros
            monitora_calorias_ingeridas: bool - Se monitora a ingestão de calorias
            nivel_atividade_fisica: str - Nível de atividade física (Baixo, Moderado, Alto)
            nivel_uso_tela: int - Quantidade de horas de uso de tela por dia
            consumo_alcool: bool - Se consome álcool
            transporte_automovel: bool - Se utiliza automóvel como principal meio de transporte
            transporte_bicicleta: bool - Se utiliza bicicleta como principal meio de transporte
            transporte_motocicleta: bool - Se utiliza motocicleta como principal meio de transporte
            transporte_publico: bool - Se utiliza transporte público
            transporte_caminhada: bool - Se utiliza caminhada como meio de transporte
            data_insercao: Union[DateTime, None] - Data de inserção do registro
        """
        self.genero_masculino = genero_masculino
        self.idade = idade
        self.historico_familiar_sobrepeso = historico_familiar_sobrepeso
        self.consumo_alta_caloria_com_frequencia = consumo_alta_caloria_com_frequencia
        self.consumo_vegetais_com_frequencia = consumo_vegetais_com_frequencia
        self.refeicoes_dia = refeicoes_dia
        self.consumo_alimentos_entre_refeicoes = consumo_alimentos_entre_refeicoes
        self.fumante = fumante
        self.consumo_agua = consumo_agua
        self.monitora_calorias_ingeridas = monitora_calorias_ingeridas
        self.nivel_atividade_fisica = nivel_atividade_fisica
        self.nivel_uso_tela = nivel_uso_tela
        self.consumo_alcool = consumo_alcool
        self.transporte_automovel = transporte_automovel
        self.transporte_bicicleta = transporte_bicicleta
        self.transporte_motocicleta = transporte_motocicleta
        self.transporte_publico = transporte_publico
        self.transporte_caminhada = transporte_caminhada
        self.outcome = outcome
        self.data_insercao = data_insercao if data_insercao else datetime.now()