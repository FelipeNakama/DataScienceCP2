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

# Título com ícone para atrair a atenção
st.title("🔍 Análise Exploratória")

# Introdução explicativa
st.markdown("""
### Visão Geral da Análise
Nesta seção, exploramos os dados de vendas do e-commerce para responder a perguntas estratégicas que ajudam na tomada de decisões. 
Aqui você encontrará:
- **Perguntas Investigativas:** Questões relevantes para entender o desempenho dos pedidos.
- **Hipóteses:** Suposições que serão testadas para identificar padrões e insights.
- **Visualizações Interativas:** Gráficos e KPIs que facilitam a compreensão dos dados.

Mesmo que você não seja especialista em estatística, os elementos visuais e explicações ajudarão a interpretar os resultados e a identificar oportunidades de melhoria.
""")

# Caixa de informação extra
st.info("""
**Dica:**  
Utilize os filtros na barra lateral para refinar os dados por período, categoria ou nível de serviço. Isso permite que você explore os dados conforme o seu interesse e veja os impactos em tempo real.
""")

# Seção de Perguntas Investigativas e Hipóteses
st.markdown("""
#### Perguntas Investigativas:
- Qual a probabilidade de que a taxa atual de cancelamentos (15%) esteja acima da média?
- O nível de serviço "Expresso" garante entregas dentro do prazo com 95% de confiança?
- Há diferença significativa nos custos de envio entre estados?
- Pedidos B2B têm distribuição de valores diferente de B2C?
- A aplicação de promoções aumenta a probabilidade de compras acima de R$ 500?

#### Exemplos de Hipóteses:
- Alguma categoria possui valor médio de pedido significativamente maior do que outras? Por exemplo, Eletrônicos.
- Pedidos com frete expresso apresentam taxa de cancelamento diferente dos pedidos com frete padrão.
- Pedidos com promoções aplicadas têm menor variabilidade no valor total.
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

# Exibição de KPIs com explicação
st.markdown("### Indicadores-Chave (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Média de Valor do Pedido", f"R${df_filtered['Valor_Pedido'].mean():.2f}", 
            help="Valor médio dos pedidos, útil para identificar ticket médio e possíveis outliers.")
col2.metric("Taxa de Cancelamento", 
           f"{df_filtered[df_filtered['Status_Pedido'] == 'Cancelado'].shape[0] / df_filtered.shape[0] * 100:.1f}%", 
           help="Proporção de pedidos cancelados em relação ao total, um indicador crítico de desempenho.")
col3.metric("Top Categoria", 
           df_filtered['Categoria'].value_counts().index[0],
           help="A categoria com maior número de pedidos, revelando o segmento de maior demanda.")

# Visualizações
st.markdown("### Visualizações Interativas")

# Gráfico: Produtos Mais Rentáveis
st.subheader("📊 Produtos Mais Rentáveis")
fig, ax = plt.subplots()
# Agrupa os produtos e soma o valor dos pedidos
vendas_por_produto = df_filtered.groupby('Estilo')['Valor_Pedido'].sum().sort_values(ascending=False).head(5)
sns.barplot(
    x=vendas_por_produto.values,
    y=vendas_por_produto.index,
    palette="viridis",
    ax=ax
)
ax.set_title("Top 5 Produtos por Faturamento")
ax.set_xlabel("Faturamento (R$)")
ax.set_ylabel("Produto")
st.pyplot(fig)

# Gráfico: Distribuição de Status dos Pedidos
st.subheader("📦 Distribuição de Status dos Pedidos")
if not df_filtered.empty:
    fig2 = plt.figure(figsize=(10, 6))
    gs = fig2.add_gridspec(1, 2, width_ratios=[3, 1])
    
    # Agrupa categorias com base no status e agrupa as menores que 5% em "Outros"
    status_counts = df_filtered['Status_Pedido'].value_counts()
    threshold = 0.05 * len(df_filtered)
    small_categories = status_counts[status_counts < threshold]
    if not small_categories.empty:
        main_categories = status_counts[status_counts >= threshold]
        main_categories['Outros'] = small_categories.sum()
    else:
        main_categories = status_counts

    ax2 = fig2.add_subplot(gs[0])
    fig2.suptitle("Distribuição de Status dos Pedidos", fontsize=14, y=0.95)
    
    wedges, texts, autotexts = ax2.pie(
        main_categories,
        labels=main_categories.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"),
        pctdistance=0.85,
        wedgeprops={'width':0.4}
    )
    plt.setp(texts, size=10, rotation_mode="anchor", ha="center", va="center")
    plt.setp(autotexts, size=9, weight="bold", color="white")
    
    # Legenda externa
    ax2.legend(
        wedges,
        main_categories.index,
        loc="center left",
        bbox_to_anchor=(1, 0, 1, 1)
    )
    st.pyplot(fig2)
else:
    st.warning("Nenhum dado disponível após aplicação dos filtros!")
