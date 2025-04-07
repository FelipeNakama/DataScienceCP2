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

# Título com ícone para dar um toque visual
st.title("📚 Base de Dados e Variáveis")

# Introdução explicativa
st.markdown("""
### Bem-vindo à Página de Base de Dados

Esta seção apresenta o **dicionário de dados** que utilizamos para analisar o desempenho do e-commerce. Aqui você encontrará:
- **Descrição detalhada** de cada variável;
- **Exemplos** práticos que ajudam a entender o formato dos dados;
- A **finalidade** de cada informação para a análise estratégica.

O objetivo é que mesmo quem não tem familiaridade com conceitos estatísticos compreenda como os dados estão organizados e como eles podem auxiliar na tomada de decisões.
""")

# Elemento visual: caixa de destaque com informações adicionais
st.info("""
**Dica:** 
Antes de mergulhar na análise, é importante conhecer bem os dados! Este dicionário serve como um guia para entender o que cada coluna representa e como cada informação pode ser usada para melhorar a estratégia do e-commerce.
""")

# Seção 1: Dicionário de Todas as Variáveis
with st.expander("🔍 Dicionário de Todas as Variáveis", expanded=False):
    st.markdown("""
    | **Variável**       | **Descrição**                                              | **Tipo**                          | **Exemplo**   |
    |--------------------|------------------------------------------------------------|-----------------------------------|---------------|
    | ID_Pedido          | Identificador único para cada pedido.                      | Qualitativa Nominal               | 123456        |
    | Data_Pedido        | Data em que o pedido foi efetuado.                         | Quantitativa Contínua (Data)      | 2024-03-31    |
    | Status_Pedido      | Situação atual do pedido.                                  | Qualitativa Nominal               | Enviado, Cancelado |
    | Tipo_Envio         | Tipo de envio do pedido.                                   | Qualitativa Nominal               | Padrão, Expresso |
    | Sales Channel      | Plataforma pela qual o pedido foi realizado.               | Qualitativa Nominal               | Amazon.in     |
    | Nivel_Entrega      | Nível de serviço de envio escolhido pelo cliente.          | Qualitativa Nominal               | Padrão, Expresso |
    | Estilo             | Descrição ou nome do modelo do produto.                    | Qualitativa Nominal               | Camiseta Preta|
    | Codigo_Produto     | Código único para identificar produtos no inventário.      | Qualitativa Nominal               | XYZ123        |
    | Categoria          | Categoria ou segmento do produto.                          | Qualitativa Nominal               | Eletrônicos, Roupas |
    | Moeda              | Moeda utilizada na transação.                              | Qualitativa Nominal               | BRL, USD      |
    | Valor_Pedido       | Valor total do pedido.                                     | Quantitativa Contínua             | 199.99        |
    | Ship City          | Cidade de destino do pedido.                               | Qualitativa Nominal               | São Paulo     |
    | Ship State         | Estado ou província de destino do pedido.                  | Qualitativa Nominal               | SP            |
    | Ship Postal Code   | Código postal do endereço de entrega.                      | Qualitativa Nominal               | 01000-000     |
    | Ship Country       | País de destino do pedido.                                 | Qualitativa Nominal               | Brasil        |
    | Promotion IDs      | Identificadores de promoções aplicados ao pedido.          | Qualitativa Nominal               | PROMO10       |
    | B2B                | Transação business-to-business (V/F).                      | Qualitativa Binária               | Verdadeiro/Falso |
    | Fulfilled By       | Entidade responsável pelo envio do pedido.                 | Qualitativa Nominal               | Amazon, Easy Ship |
    """)

# Seção 2: Dicionário das Variáveis Essenciais para Análise
with st.expander("🔍 Dicionário das Variáveis Essenciais para Análise", expanded=True):
    st.markdown("""
    | **Variável**       | **Descrição**                                              | **Tipo**               | **Exemplo**   | **Motivo**                                               |
    |--------------------|------------------------------------------------------------|------------------------|---------------|----------------------------------------------------------|
    | Status_Pedido      | Situação atual do pedido.                                  | Qualitativa Nominal    | Enviado, Cancelado | Identificar gargalos operacionais                     |
    | Nivel_Entrega      | Nível de serviço de envio escolhido pelo cliente.          | Qualitativa Nominal    | Padrão, Expresso | Avaliar impacto no custo logístico                     |
    | Categoria          | Categoria ou segmento do produto.                          | Qualitativa Nominal    | Eletrônicos, Roupas | Analisar segmentação de mercado                        |
    | Valor_Pedido       | Valor total do pedido.                                     | Quantitativa Contínua  | 199.99        | Analisar ticket médio e identificar outliers           |
    | Promotion IDs      | Promoções ou descontos aplicados ao pedido.                | Qualitativa Nominal    | PROMO10       | Avaliar a eficácia de campanhas promocionais           |
    | B2B                | Transação business-to-business.                            | Qualitativa Binária    | Verdadeiro/Falso | Analisar o impacto de vendas B2B versus B2C            |
    """)

# Elemento visual extra: Gráfico simples para ilustrar a distribuição de categorias
st.markdown("### Visualização Rápida: Distribuição de Categorias")
categoria_counts = df['Categoria'].value_counts()
st.bar_chart(categoria_counts)

# Seção 3: Amostra dos Dados
st.subheader("🧪 Exemplificação com Amostra Aleatória")
st.markdown("""
A seguir, veja uma pequena amostra dos registros da base de dados. Essa visualização permite que você entenda como os dados são apresentados e como as informações estão estruturadas.
""")
st.dataframe(
    df.sample(5),  
    use_container_width=True,
    column_config={
        "Data_Pedido": st.column_config.DateColumn("📅 Data", format="DD/MM/YYYY"),
        "Valor_Pedido": st.column_config.NumberColumn("💰 Valor", format="R$ %.2f")
    }
)
