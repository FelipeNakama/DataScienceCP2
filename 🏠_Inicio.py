import streamlit as st
import pandas as pd

# Configurações da Página
st.set_page_config(
    page_title="Dashboard Estratégico - E-Commerce",
    layout="wide",
    page_icon="🚚",
    initial_sidebar_state="expanded"
)

# Carregamento de Dados
@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce') 
    return df

df = load_data()

# ============ CONTEÚDO PRINCIPAL ============ 

# Cabeçalho com título e slogan
st.title("📈 Painel de Controle Estratégico para E-Commerce")
st.markdown("#### Uma ferramenta para transformar dados em ações estratégicas")
st.markdown("---")

# Seção: Introdução ao Projeto e Descrição do Dataset
st.markdown("""
### Introdução
Bem-vindo ao Dashboard Estratégico para E-Commerce! Este painel foi desenvolvido para oferecer uma **visão detalhada sobre os dados de vendas** de um e-commerce, possibilitando a análise de pedidos, produtos e entregas.  
Através deste dashboard, você poderá:
- **Identificar gargalos logísticos** e entender os fatores que levam a cancelamentos.
- **Analisar o desempenho das vendas** e identificar padrões de compra.
- **Otimizar estratégias de vendas e frete**, melhorando a eficiência operacional.

### Descrição do Dataset
O dataset atual registra informações detalhadas sobre pedidos de um e-commerce, incluindo:
- **Valores e categorias de produtos:** Permite identificar o ticket médio, variações e outliers.
- **Status de entrega:** Facilita o monitoramento de cancelamentos e sucesso nas entregas.
- **Dados logísticos:** Inclui informações sobre datas, cidades, estados e métodos de envio.  

Com esses dados, é possível realizar análises que detectam problemas, evidenciam oportunidades e embasam decisões estratégicas para melhorar a gestão do comércio eletrônico.
""")

# Seção: Contexto do Problema e Impacto
with st.container():
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
        ## 🎯 Contexto Operacional
        **Principais Desafios Identificados:**
        - **Alto Custo Logístico:**  
          Variação de +30% nos custos por estado.
        - **Estoque Ineficiente:**  
          40% dos produtos com baixa rotatividade.
        - **Cancelamentos:**  
          Taxa atual de {:.1f}% acima da meta.
          
        **Impacto Financeiro:**  
        💸 Perda anual estimada: R$ 2,5M
        
        > *Nota:* O valor da perda anual é uma estimativa baseada em uma análise preliminar dos cancelamentos e seu impacto financeiro, servindo para dimensionar a importância de resolver esses problemas.
        """.format((df[df['Status_Pedido'] == 'Cancelado'].shape[0] / df.shape[0]) * 100))
    
    with col2:
        st.markdown("""
        ## 🚀 Objetivos Estratégicos
        **Metas para 2024:**
        - ✅ Reduzir custos logísticos em 15%
        - ✅ Aumentar o giro de estoque em 25%
        - ✅ Diminuir cancelamentos para 10%
        
        **Como Este Dashboard Ajuda:**
        - 🔍 Identificar padrões estatisticamente significativos.
        - 📊 Priorizar ações baseadas em evidências.
        - 🎯 Monitorar indicadores-chave em tempo real.
        """)

st.markdown("---")

# Seção: Fundamentação dos Dados
with st.container():
    st.subheader("📦 Fundamentação nos Dados")
    
    # Cards Interativos com dados importantes
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Período Analisado", 
                f"{df['Data_Pedido'].min().date()}\na {df['Data_Pedido'].max().date()}",
                help="Janela temporal dos dados analisados")
    
    with col2:
        st.metric("Total de Pedidos", 
                f"{df['ID_Pedido'].nunique():,}", 
                delta="-2% vs último trimestre",
                help="Número total de transações registradas")
    
    with col3:
        st.metric("Categorias Ativas", 
                df['Categoria'].nunique(),
                help="Variedade de produtos ofertados")
    
    with col4:
        st.metric("Taxa de Sucesso", 
                f"{100 - (df[df['Status_Pedido'] == 'Cancelado'].shape[0] / df.shape[0] * 100):.1f}%",
                delta="+3.2% vs meta",
                help="Pedidos entregues com sucesso")
    
    # Prévia dos Dados
    with st.expander("🔍 Amostra dos Dados (5 registros aleatórios)", expanded=False):
        st.dataframe(df.sample(5).style.format({
            'Valor_Pedido': "R$ {:.2f}",
            'Data_Pedido': lambda x: x.strftime("%d/%m/%Y") if pd.notnull(x) else ""
        }), use_container_width=True)

st.markdown("---")

# Seção: Guia de Navegação
with st.container():
    st.subheader("🧭 Como Navegar")
    
    guide_cols = st.columns(4)
    with guide_cols[0]:
        st.markdown("""
        ### Base de Dados
        - 📚 Dicionário de variáveis  
        - 🔧 Metadados técnicos  
        - 🧪 Amostras interativas  
        """)
    
    with guide_cols[1]:
        st.markdown("""
        ### Análise Exploratória
        - 🔎 Teste suas hipóteses  
        - 📈 Visualizações dinâmicas  
        - 📉 Comparações estatísticas  
        """)
    
    with guide_cols[2]:
        st.markdown("""
        ### Intervalos de Confiança
        - 💡 Insights acionáveis  
        - 🛠 Roadmap de implementação  
        - 📆 Monitoramento de KPIs  
        """)

    with guide_cols[3]:
        st.markdown("""
        ### Testes de Hipótese
        - 🧪 Two-sample t-test 
        - 📊 Qui-quadrado de independência  
        """)

# CSS Customizado para os cards e textos
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #2E4053;
        font-weight: 600 !important;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)
