import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Carrega e processa os dados do Excel
def load_data():
    df = pd.read_excel('ABRIL.xlsx')
    # Remove colunas extras
    df = df.drop(columns=[c for c in df.columns if c.lower().startswith('x')], errors='ignore')
    # Converte datas e horas
    df['DATA VEICULAÇÃO'] = pd.to_datetime(df['DATA VEICULAÇÃO'], dayfirst=True)
    df['HORA'] = pd.to_timedelta(df['HORA'].astype(str))
    df['DATETIME'] = df['DATA VEICULAÇÃO'] + df['HORA']
    return df

# Cache para não recarregar toda vez
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# Layout do dashboard
st.title('Dashboard de Frequência de Comerciais de Rádio e TV')

# Filtros
companies = st.sidebar.multiselect(
    'Selecione Empresas:', options=df['EMPRESA'].unique(), default=df['EMPRESA'].unique()
)
media_types = st.sidebar.multiselect(
    'Selecione Mídias:', options=df['MIDIA'].unique(), default=df['MIDIA'].unique()
)
date_min = df['DATA VEICULAÇÃO'].min().date()
date_max = df['DATA VEICULAÇÃO'].max().date()
date_range = st.sidebar.date_input(
    'Período de exibição:', [date_min, date_max]
)

# Filtra dados
filtered = df[
    (df['EMPRESA'].isin(companies)) &
    (df['MIDIA'].isin(media_types)) &
    (df['DATA VEICULAÇÃO'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# Tabela resumo
st.subheader('Contagem de Comerciais por Empresa e Mídia')
counts = filtered.groupby(['EMPRESA', 'MIDIA']).size().unstack(fill_value=0)
st.dataframe(counts)

# Gráfico 1: Total por Empresa
st.subheader('Total de Comerciais por Empresa')
total_counts = filtered['EMPRESA'].value_counts()
fig1 = plt.figure()
plt.bar(total_counts.index, total_counts.values)
plt.xlabel('Empresa')
plt.ylabel('Total de Comerciais')
plt.xticks(rotation=45)
st.pyplot(fig1)

# Gráfico 2: Total por Mídia
st.subheader('Total de Comerciais por Mídia')
media_counts = filtered['MIDIA'].value_counts()
fig2 = plt.figure()
plt.bar(media_counts.index, media_counts.values)
plt.xlabel('Mídia')
plt.ylabel('Total de Comerciais')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Gráfico 3: Evolução Diária por Empresa
st.subheader('Evolução Diária de Comerciais')
daily = filtered.groupby(['DATA VEICULAÇÃO', 'EMPRESA']).size().unstack(fill_value=0)
fig3 = plt.figure()
for company in daily.columns:
    plt.plot(daily.index, daily[company], label=company)
plt.xlabel('Data')
plt.ylabel('Número de Comerciais')
plt.legend()
plt.xticks(rotation=45)
st.pyplot(fig3)