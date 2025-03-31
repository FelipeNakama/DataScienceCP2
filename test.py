import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configura a página do Streamlit
st.set_page_config(page_title="Dashboard de Desempenho de Vendas", layout="wide")

# Carregamento do dataset (ajuste o caminho se necessário)
df = pd.read_excel("df_selecionado.xlsx")

# DEFINA AQUI OS NOMES CORRETOS DAS COLUNAS DO SEU DATASET:
col_order         = "ID_Pedido"          # Exemplo: "Order ID"
col_date          = "Data_Pedido"              # Exemplo: "Date" ou "Data"
col_status        = "Status_Pedido"            # Exemplo: "Status"
col_fulfilment    = "Tipo_Envio"        # Exemplo: "Fulfilment"
col_sales_channel = "Sales Channel"     # Exemplo: "Sales Channel"
col_ship_service  = "Nivel_Entrega" # Exemplo: "Ship Service Level"
col_style         = "Estilo"             # Exemplo: "Style" (modelo do produto)
col_sku           = "Codigo_Produto"               # Exemplo: "SKU"
col_category      = "Categoria"          # Exemplo: "Category"
col_currency      = "Moeda"          # Exemplo: "Currency"
col_amount        = "Valor_Pedido"            # Exemplo: "Amount"

# Converter a coluna de data para datetime (processamento necessário para todas as páginas)
df[col_date] = pd.to_datetime(df[col_date], errors='coerce')

# Criação do menu de navegação na lateral
paginas = [
    "Apresentação do Problema e Contexto de Mercado",
    "Descrição da Base de Dados e Variáveis",
    "Identificação de Perguntas e Hipóteses (Análise Interativa)",
    "Conexão entre o Problema e o Dashboard"
]
pagina_selecionada = st.sidebar.radio("Escolha a Página", paginas)

# Página 1: Apresentação do Problema e Contexto de Mercado
if pagina_selecionada == paginas[0]:
    st.title("Apresentação do Problema e Contexto de Mercado")
    st.markdown("""
    **Contexto:**  
    No ambiente do e-commerce, entender o desempenho de vendas é essencial para a otimização dos estoques...
    """)

# Página 2: Descrição da Base de Dados e Variáveis
elif pagina_selecionada == paginas[1]:
    st.title("Descrição da Base de Dados e Variáveis")
    st.write("Colunas disponíveis no DataFrame:", df.columns.tolist())  # Movido para cá
    st.markdown("""
    A base de dados utilizada contém informações detalhadas dos pedidos realizados no e-commerce...
    """)

# Página 3: Análise Interativa
elif pagina_selecionada == paginas[2]:
    st.title("Identificação de Perguntas e Hipóteses")
    
    # Filtros APENAS nesta página
    st.sidebar.markdown("### Filtros de Análise")
    data_inicio = st.sidebar.date_input("Data Início", value=df[col_date].min())
    data_fim = st.sidebar.date_input("Data Fim", value=df[col_date].max())
    categorias = st.sidebar.multiselect("Selecione as Categorias", options=df[col_category].unique())
    status_pedidos = st.sidebar.multiselect("Selecione os Status", options=df[col_status].unique())
    
    # Lógica dos filtros
    df_filtrado = df[(df[col_date] >= pd.to_datetime(data_inicio)) & (df[col_date] <= pd.to_datetime(data_fim))]
    if categorias:
        df_filtrado = df_filtrado[df_filtrado[col_category].isin(categorias)]
    if status_pedidos:
        df_filtrado = df_filtrado[df_filtrado[col_status].isin(status_pedidos)]
    
    # KPIs e gráficos (todo o conteúdo restante da página 3 aqui...)

# Página 4: Conexão com o Problema
elif pagina_selecionada == paginas[3]:
    st.title("Conexão entre o Problema Real e o Dashboard")
    st.markdown("""
    Esta seção demonstra como a análise dos dados e a visualização interativa auxiliam...
    """)