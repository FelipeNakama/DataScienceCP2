import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')  # Converter data
    return df

df = load_data()  # Carrega os dados

st.title("🔍 Análise Investigativa")

st.markdown("""
    ### Perguntas Investigativas:
    - Qual a probabilidade de que a taxa atual de cancelamentos (15%) esteja acima da média histórica?
    - O nível de serviço "Expresso" garante entregas dentro do prazo com 95% de confiança?
    - Há diferença significativa nos custos de envio entre estados?
    - Pedidos B2B têm distribuição de valores diferente de B2C?
    - A aplicação de promoções aumenta a probabilidade de compras acima de R$ 500?
            
    ### Exemplo de Hipóteses:
    - Alguma categoria possui valor médio de pedido significativamente maior do que outras categorias? Por exemplo Eletrônicos?
    - Pedidos com frete expresso têm taxa de cancelamento diferente dos pedidos com frete padrão
    - Pedidos com promoções aplicadas possuem menor variabilidade em seu valor total
""")

# Filtros na Sidebar
with st.sidebar:
    st.header("🔧 Filtros")
    date_range = st.date_input("Período", [df['Data_Pedido'].min(), df['Data_Pedido'].max()])
    categories = st.multiselect("Categorias", options=df['Categoria'].unique())
    service_levels = st.multiselect("Nível de Serviço", options=df['Nivel_Entrega'].unique())

# Aplicação dos Filtros
df_filtered = df[
    (df['Data_Pedido'] >= pd.to_datetime(date_range[0])) &
    (df['Data_Pedido'] <= pd.to_datetime(date_range[1]))
]
if categories:
    df_filtered = df_filtered[df_filtered['Categoria'].isin(categories)]

if service_levels:  
    df_filtered = df_filtered[df_filtered['Nivel_Entrega'].isin(service_levels)]

# KPIs
st.markdown("""
    ### Dados Estatísticos Ilustrativos:
""")
col1, col2, col3 = st.columns(3)
col1.metric("Média de valor pedido", f"R${df_filtered['Valor_Pedido'].mean():.2f}")
col2.metric("Taxa de Cancelamento", 
           f"{df_filtered[df_filtered['Status_Pedido'] == 'Cancelado'].shape[0]/df_filtered.shape[0]*100:.1f}%")
col3.metric("Top Categoria", 
           df_filtered['Categoria'].value_counts().index[0])

# Visualizações
st.subheader("📊 Produtos Mais Rentáveis")
fig, ax = plt.subplots()
sns.barplot(
    x=df_filtered.groupby('Estilo')['Valor_Pedido'].sum().sort_values(ascending=False).head(5).values,
    y=df_filtered.groupby('Estilo')['Valor_Pedido'].sum().sort_values(ascending=False).head(5).index,
    palette="viridis"
)
ax.set_title("Top 5 Produtos por Faturamento")
st.pyplot(fig)

st.subheader("📦 Distribuição de Status dos Pedidos")
if not df_filtered.empty:
    fig2 = plt.figure(figsize=(10, 6))  # Tamanho maior
    gs = fig2.add_gridspec(1, 2, width_ratios=[3, 1])  # Grid para título + gráfico

    # Agrupa categorias menores que 5% em "Outros"
    status_counts = df_filtered['Status_Pedido'].value_counts()
    threshold = 0.05 * len(df_filtered)
    small_categories = status_counts[status_counts < threshold]
    
    if not small_categories.empty:
        main_categories = status_counts[status_counts >= threshold]
        main_categories['Outros'] = small_categories.sum()
    else:
        main_categories = status_counts

    ax2 = fig2.add_subplot(gs[0])

    fig2.suptitle(
        "Distribuição de Status dos Pedidos",
        fontsize=14,
        y=0.95  # Posicionamento vertical
    )

    # Plot com ajustes
    wedges, texts, autotexts = ax2.pie(
        main_categories,
        labels=main_categories.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"),
        pctdistance=0.85,
        wedgeprops={'width':0.4}
    )
    
    # Ajusta posição das legendas
    plt.setp(texts, size=10, rotation_mode="anchor", ha="center", va="center")
    plt.setp(autotexts, size=9, weight="bold", color="white")
    
    # Cria legenda externa
    ax2.legend(
        wedges,
        main_categories.index,
        loc="center left",
        bbox_to_anchor=(1, 0, 1, 1)
    )
    
    st.pyplot(fig2)
else:
    st.warning("Nenhum dado disponível após aplicação dos filtros!")