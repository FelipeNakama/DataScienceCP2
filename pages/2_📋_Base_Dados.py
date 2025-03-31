import streamlit as st
import pandas as pd

# Função de carregamento centralizada (igual à da Home)
@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')  # Converter data
    return df

df = load_data()  # Carrega os dados

# ============ CONTEÚDO DA PÁGINA ============
st.title("📚 Base de Dados e Variáveis")

# Seção 1: Dicionário de Dados
with st.expander("🔍 **Dicionário de Todas as Variáveis**", expanded=False):
    st.markdown("""
    | Variável | Descrição | Tipo | Exemplo |
    |----------|-----------|------|---------|
    |ID_Pedido| Identificador único para cada pedido.| Qualitativa Nominal| 123456 |
    |Data_Pedido| Data em que o pedido foi efetuado.| Quantitativa Contínua (Data)| 2024-03-31|
    |Status_Pedido| Situação atual do pedido.| Qualitativa Nominal| Enviado, Cancelado|
    |Tipo_Envio| Tipo de envio do pedido.| Qualitativa Nominal| Padrão, Expresso|
    |Sales Channel| Plataforma pela qual o pedido foi realizado.| Qualitativa Nominal| Amazon.in|
    |Nivel_Entrega| Nível de serviço de envio escolhido pelo cliente.| Qualitativa Nominal| Padrão, Expresso|
    |Estilo| Descrição ou nome do modelo do produto.| Qualitativa Nominal| Camiseta Preta|
    |Codigo_Produto| Código único usado para identificar produtos no inventário.| Qualitativa Nominal| XYZ123|
    |Categoria| Categoria ou segmento do produto.| Qualitativa Nominal| Eletrônicos, Roupas|
    |Moeda| Moeda utilizada na transação.| Qualitativa Nominal| BRL, USD|
    |Valor_Pedido| Valor total do pedido na moeda especificada.| Quantitativa Contínua| 199.99|
    |Ship City| Cidade de destino do pedido.| Qualitativa Nominal| São Paulo|
    |Ship State| Estado ou província de destino do pedido.| Qualitativa Nominal| SP|
    |Ship Postal Code| Código postal do endereço de entrega.| Qualitativa Nominal| 01000-000|
    |Ship Country| País de destino do pedido.| Qualitativa Nominal| Brasil|
    |Promotion IDs| Identificadores de promoções ou descontos aplicados ao pedido.| Qualitativa Nominal| PROMO10|
    |B2B| Indica se o pedido foi uma transação business-to-business.| Qualitativa Binária| Verdadeiro/Falso|
    |Fulfilled By| Entidade responsável pelo cumprimento e envio do pedido.| Qualitativa Nominal| Amazon, Easy Ship|
    """)

with st.expander("🔍 **Dicionário das Variáveis Essencias para Análise**", expanded=True):
    st.markdown("""
    | Variável | Descrição | Tipo | Exemplo | Motivo |
    |----------|-----------|------|---------|--------|
    |Status_Pedido| Situação atual do pedido.| Qualitativa Nominal| Enviado, Cancelado|Para identificar gargalos operacionais|
    |Nivel_Entrega| Nível de serviço de envio escolhido pelo cliente.| Qualitativa Nominal| Padrão, Expresso|Para identificar o Impacto no custo logístico|
    |Categoria| Categoria ou segmento do produto.| Qualitativa Nominal| Eletrônicos, Roupas|Para verificar a segmentação de mercado|
    |Valor_Pedido| Valor total do pedido na moeda especificada.| Quantitativa Contínua| 199.99|Para análise de ticket médio e outliers|
    |Promotion IDs| Identificadores de promoções ou descontos aplicados ao pedido.| Qualitativa Nominal| PROMO10|Para analisar a eficácia de campanhas|
    |B2B| Indica se o pedido foi uma transação business-to-business.| Qualitativa Binária| Verdadeiro/Falso|Para avaliar o impacto de transações B2B|
    """)

# Seção 2: Amostra dos Dados
st.subheader("🧪 Exemplificação com Amostra Aleatória")
st.dataframe(
    df.sample(5),  
    use_container_width=True,
    column_config={
        "Data_Pedido": st.column_config.DateColumn("📅 Data", format="DD/MM/YYYY"),
        "Valor_Pedido": st.column_config.NumberColumn("💰 Valor", format="R$ %.2f")
    }
)
