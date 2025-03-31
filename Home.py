import streamlit as st
import pandas as pd

# Configurações da Página
st.set_page_config(
    page_title="Análise de E-Commerce",
    layout="wide",
    page_icon="📦"
)

# Carregamento de Dados
@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    
    # CONVERSÃO DA COLUNA DE DATA (AJUSTE O NOME SE NECESSÁRIO)
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')  # ← Correção aqui
    
    return df

df = load_data()

# ============ CONTEÚDO PRINCIPAL ============ 
st.title("Análise Estratégica de Vendas em E-Commerce")
st.markdown("---")

# Seção 1: Contexto do Problema
with st.expander("🎯 **Contexto de Mercado & Objetivos**", expanded=True):
    st.markdown("""
    ### Desafios de Vendas E-Commerce
    - **Altas taxas de cancelamento de pedidos
    - **Alta variabilidade nos prazos de entrega
    - **Concentração de vendas em poucos produtos

    ### Objetivo deste Dashboard:
    - Identificar padroes estatisticamente significativos para:
        - Reduzir custos logísticos
        - Otimizar estrategias de promoção
        - Aumentar a satisfação do cliente
    """)

# Seção 2: Visão Geral do Dataset
st.subheader("📦 Visão Geral dos Dados")
col1, col2, col3 = st.columns(3)

# Verificação de conversão bem-sucedida
if not pd.api.types.is_datetime64_any_dtype(df['Data_Pedido']):
    st.error("Erro: A coluna 'Data_Pedido' não foi convertida para datetime!")
else:
    # Métricas ajustadas
    col2.metric(
        "Período Analisado", 
        f"{df['Data_Pedido'].min().date()} a {df['Data_Pedido'].max().date()}"  # ← Funcionará agora
    )

col1.metric("Total de Pedidos", df['ID_Pedido'].nunique())
col3.metric("Categorias Únicas", df['Categoria'].nunique())
# Guia de Navegação
st.markdown("""
### 📍 Como Utilizar Este Dashboard
1. **Menu Lateral** → Selecione a análise desejada
2. **Páginas Disponíveis:**
   - `Base de Dados`: Detalhes técnicos das variáveis
   - `Análise Investigativa`: Teste suas hipóteses
   - `Impacto Estratégico`: Conexão com decisões reais
""")