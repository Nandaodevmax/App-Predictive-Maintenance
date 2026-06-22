import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
#===============================
# GERAR DADOS
#===============================
dados_ml = pd.DataFrame({
    "temperatura_mancal": [50,60,70,80,90,100],
    "vibracao_mancal": [2,3,4,5,6,8],
    "corrente_motor": [20,25,30,35,40,45],
    "tensao_correia": [90,85,80,75,70,65],
    "falha": [0,0,0,1,1,1]
})
X = dados_ml[[
    "temperatura_mancal",
    "vibracao_mancal",
    "corrente_motor",
    "tensao_correia"
]]
y = dados_ml["falha"]

modelo = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
modelo.fit(X, y)


np.random.seed(42)

dados = {
    "temperatura_mancal": np.random.randint(50, 100, 100),
    "vibracao_mancal": np.random.uniform(0.1, 1.0, 100),
    "corrente_motor": np.random.randint(20, 50, 100),
    "tensao_correia": np.random.randint(100, 500, 100)
}

df = pd.DataFrame(dados)

df["falha"] = (
    (df["temperatura_mancal"] > 80) &
    (df["vibracao_mancal"] > 0.6)
).astype(int)

#===============================
#TREINAR MODELO
#===============================

X = df[["temperatura_mancal", "vibracao_mancal", "corrente_motor", "tensao_correia"]]
y = df["falha"]

modelo = DecisionTreeClassifier()
modelo.fit(X, y)

#==============================
#INTERFACE
#==============================

st.title("Predictive Maintenance App")

st.write("Sistema de previsão de falhas industriais")

temperatura_mancal = st.slider("Temperatura do mancal (ºC)", 20, 120, 60)
vibracao_mancal = st.slider("Vibração do mancal (mm/s)", 0.1, 20.0, 5.0)
corrente_motor = st.slider("Corrente do motor (A)", 20, 50, 30)
tensao_correia = st.slider("Tensao da correia(%)", 50, 100, 80)

entrada = [[
    temperatura_mancal,
    vibracao_mancal,
    corrente_motor,
    tensao_correia
]]

previsao_ml = modelo.predict(entrada)[0]


falha_score = (
    (temperatura_mancal / 120) * 40 +
    (vibracao_mancal / 10) * 30 +
    (corrente_motor / 50) * 20 +
    (tensao_correia / 100) * 10
)
falha_score = min(max(falha_score, 0), 100)

st.subheader("Probabilidade de falha")
st.metric(
    "Chance de falha",
    f"{falha_score:.1f}%"
)
if falha_score < 40:
    st.success("Baixa probabilidade de falha")

elif falha_score < 70:
    st.warning("Atenção necessária")
else:
    st.error("Alta probabilidade de falha")

    st.progress(falha_score / 100)



entrada = [[
    temperatura_mancal,
    vibracao_mancal,
    corrente_motor,
    tensao_correia
]]

historico = pd.DataFrame({
    "Tempo": range(20),
    "Temperatura": np.random.normal(temperatura_mancal, 3, 20),
    "Vibração": np.random.normal(vibracao_mancal, 0.5, 20),
    "Corrente": np.random.normal(corrente_motor, 2, 20),


})
st.subheader("Tendência da Temperatura")

st.line_chart(
    historico.set_index("Tempo")["Temperatura"]
)

st.subheader("Tendência da Vibração")

st.line_chart(
    historico.set_index("Tempo")["Vibração"]
)

st.subheader("Tendência da Corrente")

st.line_chart(
    historico.set_index("Tempo")["Corrente"]
)

st.subheader("Estimativa de Vida Útil")


if temperatura_mancal < 70:
    vida_util = 180
elif temperatura_mancal < 85:
    vida_util = 90
else:
    vida_util = 30
st.metric(
    "Dias estimados até manutenção",
    f"{vida_util} dias"
)

previsao = modelo.predict(entrada)[0]

st.subheader("Previsão da IA")

if previsao == 0:
      st.success(
      "IA prevê operação normal"

  )
else:
      st.error(
          "IA prevê risco de falha"
  )

if temperatura_mancal > 90:
  st.error("Risco crítico de superaquecimento")

elif temperatura_mancal > 75:
  st.warning("Temperatura elevada")

else:
  st.success("Temperatura normal")


if vibracao_mancal > 1.2:
  st.error("Risco de desalinhamento")

elif vibracao_mancal > 9.0:
  st.warning("Vibração elevada")

else:
  st.success("Vibração normal")

if corrente_motor > 40:
  st.error("Sobrecarga do motor")

elif corrente_motor > 60:
  st.warning("Corrente Elevada")

else:
  st.success("Corrente normal")

if tensao_correia < 60:
  st.error("Correia Frouxa")

elif tensao_correia > 80:
  st.warning("Tensao elevada")

else:
  st.success("Tensao normal")

riscos = 0

if temperatura_mancal > 90:
  riscos += 1

if vibracao_mancal > 1.2:
  riscos += 1

if corrente_motor > 40:
  riscos += 1

if tensao_correia > 50:
  riscos += 1

  st.subheader("Nível de Criticidade")

if riscos == 0:
   st.success("Baixo Risco")

elif riscos <= 2:
  st.warning("Médio risco")

else:
  st.error("Alto risco")



st.subheader("Diagnóstico Automático")
diagnostico = []

if temperatura_mancal > 90:
  diagnostico.append("Risco de superaquecimento")

if vibracao_mancal > 7:
  diagnostico.append("Risco de desalinhamento")

if corrente_motor > 40:
  diagnostico.append("Sobrecarga do motor")

if tensao_correia > 70:
  diagnostico.append("Correia Frouxa")

if len(diagnostico) == 0:
  diagnostico.append("Nenhuma anomalia detectada")

else:
    for item in diagnostico:
      st.warning(item)



st.subheader("Diagnóstico Automático")

for item in diagnostico:
  st.warning(item)

st.subheader("Ações Recomendadas")
acoes = []
if temperatura_mancal > 80:
  acoes.append("Verificar Lubrificação do Mancal")

if vibracao_mancal > 7:
  acoes.append("Executar alinhamento a laser")

if corrente_motor > 40:
  acoes.append("Inspecionar carga do transportador")

if tensao_correia < 70:
  acoes.append("Realizar tensionamento da correia")

if len(acoes) == 0:
  st.success("Equipamento operando dentro dos parâmetros")
else:
    for acao in acoes:
      st.info(acao)

#Limites de operação

limite_temp = 80
limite_vib = 7
limite_corrente = 40
limite_tensao = 60

temp_score = max(0, 100 - (temperatura_mancal / 120) * 100)

vib_score = max(0, 100 - (vibracao_mancal / 10) * 100)

corrente_score = max(0, 100 - (corrente_motor / 50) * 100)

tensao_score = min(100, (tensao_correia / 100) * 100)

health_score = (
    temp_score * 0.4 +
    vib_score  * 0.3 +
    corrente_score * 0.2 +
    tensao_score * 0.1
) / 4

col1, col2 = st.columns(2)

with col1:
  fig_temp = go.Figure(go.Indicator(
      mode ="gauge+number",
      value=temperatura_mancal,
      title={'text': "Temperatura ºC"},
      gauge={
          'axis': {'range':[0, 120]},
          'steps':[
              {'range': [0, 70], 'color': "green"},
              {'range': [70, 90], 'color': "yellow"},
              {'range': [90, 120], 'color': "red"}
          ]
      }
   ))

st.plotly_chart(fig_temp, use_container_width=True)

with col2:
  fig_vib = go.Figure(go.Indicator(
      mode ="gauge+number",
      value=vibracao_mancal,
      title={'text': "vibracao mm/s"},
      gauge={
          'axis': {'range': [0, 10]},
          'steps': [
              {'range': [0, 4], 'color': "green"},
              {'range': [4, 7], 'color': "yellow"},
              {'range': [7, 10], 'color': "red"}
          ]

      }
   ))

st.plotly_chart(fig_vib, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
     fig_cor = go.Figure(go.Indicator(
         mode ="gauge+number",
         value=corrente_motor,
         title={'text': "corrente A"},
         gauge={
             'axis': {'range': [0, 100]},
             'steps': [
                 {'range': [0, 40], 'color': "green"},
                 {'range': [40, 70], 'color': "yellow"},
                 {'range': [70, 100], 'color': "red"}
             ]
         }
     ))
     st.plotly_chart(fig_cor, use_container_width=True)


with col4:
    fig_tensao = go.Figure(go.Indicator(
        mode ="gauge+number",
        value=tensao_correia,
        title={'text': "tensao %"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps':[
                {'range': [0, 60], 'color': "red"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig_tensao, use_container_width=True)


st.subheader("Temperatura do mancal")

fig_temp = go.Figure(go.Indicator(
    mode = "gauge+number",
    value=temperatura_mancal,
    title={'text': "ºC"},
    gauge={
        'axis': {'range': [0, 120]},
        'bar': {'color': "red"},
        'steps': [
            {'range': [0, 70], 'color': "green"},
            {'range': [70, 90], 'color': "yellow"},
            {'range': [90, 120], 'color': "red"}
        ]
    }

))

st.plotly_chart(fig_temp)

st.subheader("Vibração do mancal")

fig_vib = go.Figure(go.Indicator(
    mode = "gauge+number",
    value=vibracao_mancal,
    title={'text': "mm/s"},
    gauge={
        'axis':{'range': [0, 10]},
        'bar': {'color': "blue"},
        'steps': [
            {'range': [0, 4], 'color': "green"},
            {'range': [4, 7], 'color': "yellow"},
            {'range': [7, 10], 'color': "red"}
        ]
    }

))

st.plotly_chart(fig_vib)

st.subheader("Corrente do motor")

fig_cor = go.Figure(go.Indicator(
    mode = "gauge+number",
    value=corrente_motor,
    title={'text': "A"},
    gauge={
        'axis': {'range': [0, 50]},
        'bar': {'color': "blue"},
        'steps': [
            {'range': [0, 20], 'color': "green"},
            {'range': [20, 0], 'color': "yellow"},
            {'range': [0, 0], 'color': "red"}


        ]
    }

))

historico = pd.DataFrame({
    "Tempo": range(20),
    "Temperatura": np.random.normal(temperatura_mancal, 3, 20),
    "Vibração": np.random.normal(vibracao_mancal, 0.5, 20),
    "Corrente": np.random.normal(corrente_motor, 2, 20),
    "Tensão": np.random.normal(tensao_correia, 3, 20)

})
st.subheader("Histórico dos Sensores")

st.line_chart(
    historico.set_index("Tempo")
)

historico = pd.DataFrame

st.subheader("Health Score")

health = 87

st.progress(health/100)

st.metric(
    "Saúde do Equipamento",
    f"{health_score}%"
)
st.plotly_chart(fig_cor)

st.subheader("Health Score do Equipamento")

st.progress(int(health_score))

st.metric(
    "Saúde Geral",
    f"{health_score:.1f}%"
)

if health_score >= 80:

  st.success(
      "Equipamento saudável"
  )

elif health_score >= 60:
  st.warning(
      "Atenção: monitorar condições equipamento"
  )
else:

  st.error(
      "Alto risco de falha"
  )

# previsão
st.subheader("Previsão Machine Learning")

if previsao_ml == 1:
  st.error("IA detectou risco de falha")

else:
  st.success("IA prevê operação normal")

st.subheader("Central de Alertas Inteligentes")

if temperatura_mancal >= 90:
  st.error("CRÍTICO: Temperatura muito elevada no mancal")

elif vibracao_mancal >= 7:
  st.warning("ATENÇÃO: Vibração acima do normal!")

elif corrente_motor >= 45:
  st.warning("ATENÇÃ0: Sobrecarga do motor detectada!")

elif tensao_correia <= 60:
  st.warning("ATENÇÃO: Correia com baixa tensão detectada!")

else:
  st.success("Equipamento operando dentro dos parâmetros")

st.subheader("Nível de Risco")

if health_score >= 80:
  st.success("Baixo RISCO")

elif health_score >= 60:
  st.warning("Médio RISCO")

else:
  st.error("ALTO RISCO")

st.subheader("Recomendação de Intervenção")

if health_score >= 80:
  st.info("Próxima inspeção recomendada em 30 dias")

elif health_score >= 50:
  st.info("Próxima inspeção recomendada em 15 dias")

else: st.error("Intervenção imediata recomendada")

st.subheader("Indicadores do Equipamento")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Health Score",
        f"{health_score:.1f}%"
   )

with col2:
    st.metric(
        "Probabilidade de Falha",
        f"{falha_score:.1f}%"
    )
with col3:
    st.metric(
        "Temperatura Atual",
        f"{temperatura_mancal} ºC"
   )

st.subheader("Status Operacional")

if health_score >= 80:
  st.success("Equipamento Saudável")

elif health_score >= 50:
  st.warning("Atenção: Monitorar condições do equipamento")

else:
  st.error("Equipamento em estado Crítico")

st.subheader("Resumo Executivo")

resumo = f"""
Resumo Executivo

Temperatura do Mancal: {temperatura_mancal} ºC
Vibração atual: {vibracao_mancal} mm/s
Corrente do Motor: {corrente_motor} A
Tensão da Correia: {tensao_correia} %

Health Score: {health_score:.1f}%
Probabilidade de Falha: {falha_score:.1f}%
"""

st.text_area(
    "Resumo da Condição do Equipamento",
    resumo,
    height=220
)

# resultado

if temperatura_mancal > 90:
  st.error(
      "Possível superaquecimento do mancal"
  )
elif vibracao_mancal > 7:
  st.warning(
      "Possível desalinhamento do mancal"
  )
st.subheader("Histórico da Temperatura")

historico = pd.DataFrame({
    "Tempo": range(20),
    "Temperatura": np.random.normal(temperatura_mancal, 3, 20)
})

st.line_chart(
    historico.set_index("Tempo")
)

st.subheader("Histórico da Vibração")

historico = pd.DataFrame({
    "Tempo": range(20),
    "Vibração": np.random.normal(vibracao_mancal, 0.5, 20)
})

st.line_chart(
    historico.set_index("Tempo")
)

if st.button("Gerar Relatório"):
  st.write("### Relatório de Manutenção")

  st.write(f"Temperatura do Mancal:{temperatura_mancal} ºC")
  st.write(f"Vibração do Mancal:{vibracao_mancal} mm/s")
  st.write(f"Corrente do Motor:{corrente_motor} A")
  st.write(f"Tensão da Correia:{tensao_correia} %")

  st.write(f"Health Score: {health_score:.1f}%")

  st.write(f"Probabilidade de Falha: {falha_score:.1f}%")
st.subheader("Relatório Automático")
st.success("Relatório gerado com sucesso!")

import io
relatorio = f"""
RELATÓRIO DE MANUTENÇÃO

Temperatura: {temperatura_mancal} ºC
Vibração: {vibracao_mancal} mm/s
Corrente: {corrente_motor} A
Tensão: {tensao_correia} %

Health Score: {health_score:.1f}%
Probabilidade de Falha: {falha_score:.1f}%
"""

st.download_button(
    label="Baixar Relatório",
    data=relatorio,
    file_name="relatorio_manutencao.txt",

)
