import streamlit as st
import pandas as pd
import numpy as np

# Gerando dados de exemplo (substitua com os dados reais do agente)
np.random.seed(42)  # Para reprodutibilidade

# Criando a lista de protocolos
protocolos = [f"202410010000{str(i).zfill(5)}" for i in range(1, 101)]  # Protocolos de 00001 a 00100

# Criando um período de 2 semanas (14 dias)
periodo = pd.date_range(start='2024-09-25', periods=14, freq='D')

# Distribuindo 100 atendimentos aleatoriamente ao longo do período de 2 semanas
dados_agente = []
for protocolo in protocolos:
    # Escolhendo uma data aleatória dentro do período
    data_atendimento = np.random.choice(periodo)
    
    # Convertendo para pd.Timestamp para garantir acesso aos atributos
    data_atendimento = pd.Timestamp(data_atendimento)
    
    # Gerando uma hora aleatória entre 9:00 e 18:00
    hora_atendimento = np.random.randint(9, 19)  # Horas de 9 a 18
    minuto_atendimento = np.random.choice([0, 15, 30, 45])  # Minutos em intervalos de 15 minutos
    
    # Criando a data e hora completa
    data_hora_atendimento = pd.Timestamp(year=data_atendimento.year, month=data_atendimento.month, 
                                          day=data_atendimento.day, hour=hora_atendimento, 
                                          minute=minuto_atendimento)
    
    # Adicionando dados do atendimento à lista
    dados_agente.append({
        'data': data_hora_atendimento,
        'agente': 'Agente 1',
        'tempo_atendimento': np.random.randint(100, 500),  # Tempo em segundos
        'tempo_entre_atendimentos': np.random.randint(50, 300),  # Tempo em segundos
        'satisfacao_cliente': np.random.randint(1, 6),  # Avaliação de 1 a 5
        'primeira_resposta': np.random.randint(10, 100),  # Tempo em segundos
        'protocolo': protocolo  # Adicionando a lista de protocolos
    })

# Convertendo a lista de dicionários para um DataFrame
dados_agente = pd.DataFrame(dados_agente)

# Exibindo o título do dashboard
st.title("Dashboard de Performance do Agente")

# Filtro de datas
st.sidebar.header("Filtro de Data")
data_inicial = st.sidebar.date_input("Data Inicial", min_value=dados_agente['data'].min(), 
                                      max_value=dados_agente['data'].max(), value=dados_agente['data'].min())
data_final = st.sidebar.date_input("Data Final", min_value=data_inicial, 
                                    max_value=dados_agente['data'].max(), value=dados_agente['data'].max())

# Filtrando os dados com base nas datas selecionadas
dados_filtrados = dados_agente[(dados_agente['data'].dt.date >= data_inicial) & 
                                (dados_agente['data'].dt.date <= data_final)]

# Exibindo o histórico de atendimentos filtrados
if st.checkbox('Exibir protocolos do atendente'):
    st.subheader("Histórico de Atendimentos")
    st.dataframe(dados_filtrados[['data', 'protocolo', 'tempo_atendimento', 'satisfacao_cliente']])

# Gráfico de barras para o tempo médio de atendimento
if not dados_filtrados.empty:
     # Criando 4 colunas
    col1, col2, col3, col4 = st.columns(4)

    # Adicionando as métricas nas colunas
    with col1:
        tempo_medio_atendimento = dados_filtrados['tempo_atendimento'].mean()
        st.metric(label="Tempo Médio de Atendimento (s)", value=round(tempo_medio_atendimento, 2))

    with col2:
        st.metric(label="Satisfação Média do Cliente", value=round(dados_filtrados['satisfacao_cliente'].mean(), 2))

    with col3:
        st.metric(label="Tempo Médio Entre Atendimentos (s)", value=round(dados_filtrados['tempo_entre_atendimentos'].mean(), 2))

    with col4:
        st.metric(label="Tempo Médio da Primeira Resposta (s)", value=round(dados_filtrados['primeira_resposta'].mean(), 2))
   

    # Criando o histograma baseado nas horas
    hist_values = np.histogram(dados_filtrados['data'].dt.hour, bins=24, range=(0, 24))[0]

    # Gráfico de barras para distribuição de atendimentos por hora
    st.subheader("Distribuição de Atendimentos por Hora")
    st.bar_chart(hist_values)


 # Contando atendimentos por dia
    atendimentos_por_dia = dados_filtrados.groupby(dados_filtrados['data'].dt.date)['protocolo'].count()
    st.subheader("Atendimentos por Dia")
    st.bar_chart(atendimentos_por_dia)
else:
    st.warning("Nenhum atendimento encontrado para o intervalo de datas selecionado.")
