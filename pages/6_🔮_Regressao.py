import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

# ============ CARREGAMENTO ============
@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')
    if 'Venda_B2B' in df.columns:
        df['B2B_Flag'] = df['Venda_B2B'].map({True:1, False:0, 'Verdadeiro':1, 'Falso':0})
    return df.dropna(subset=['Valor_Pedido'])

df = load_data()

st.title("📉 Correlação & Regressão Simples")
st.markdown("""
Aqui investigamos se **clientes corporativos (B2B)** gastam diferente dos clientes finais (B2C),  
usando **scatterplot** e um modelo de regressão linear básico.
""")

# ============ FILTROS ============
with st.sidebar:
    st.header("🔧 Filtros")
    date_range = st.date_input(
        "Período",
        [df['Data_Pedido'].min().date(), df['Data_Pedido'].max().date()]
    )
start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
df = df[(df['Data_Pedido'] >= start) & (df['Data_Pedido'] <= end)]

if 'B2B_Flag' not in df.columns:
    st.warning("Coluna Venda_B2B não encontrada. Não é possível fazer essa análise.")
    st.stop()

# ============ 1. SCATTERPLOT SIMPLES ============
st.header("1. Scatterplot: Ticket Médio vs Tipo de Cliente")
with st.expander("📚 Interpretação deste Gráfico", expanded=True):
    st.markdown("""
    - Cada ponto é um pedido:  
      - **Eixo X:** valor do pedido (R$).  
      - **Eixo Y:** tipo de cliente (0 = B2C, 1 = B2B).  
    - Como Y é binária, os pontos alinham-se em duas linhas (0 e 1).  
    - **Limitações:**  
      - Não mostra densidade real — para isso, use o boxplot abaixo.  
      - A reta de regressão em dados binários tende a ficar muito plana.  
    - **O que observar:**  
      - Concentre-se na dispersão horizontal de cada linha:  
        valores mais à direita em Y=1 indicam tickets mais altos em B2B.
    """)

fig, ax = plt.subplots(figsize=(7, 4))
sns.scatterplot(x='Valor_Pedido', y='B2B_Flag', data=df, alpha=0.4, ax=ax)
ax.set_yticks([0,1])
ax.set_yticklabels(['B2C','B2B'])
ax.set_xlabel("Valor do Pedido (R$)")
ax.set_ylabel("Tipo de Cliente")
ax.set_title("Scatter: Valor_Pedido vs B2B_Flag")
st.pyplot(fig)

# Novo expander com boxplot para mostrar densidade real
with st.expander("📊 Boxplot para visualizar densidade real", expanded=False):
    st.markdown("""
    O boxplot mostra mediana, quartis e possíveis outliers de cada grupo,  
    permitindo enxergar como o ticket se distribui internamente em B2C e B2B.
    """)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='B2B_Flag', y='Valor_Pedido', data=df, ax=ax2)
    ax2.set_xticklabels(['B2C','B2B'])
    ax2.set_xlabel("Tipo de Cliente")
    ax2.set_ylabel("Valor do Pedido (R$)")
    ax2.set_title("Boxplot: Valor_Pedido por Tipo de Cliente")
    st.pyplot(fig2)

# Correlação
corr, pval = pearsonr(df['Valor_Pedido'], df['B2B_Flag'])
st.markdown(f"**Correlação de Pearson (r):** {corr:.2f}  |  **p-valor:** {pval:.4f}")
st.markdown("> Mesmo que r seja baixo, diferenças de média podem existir ")

# ============ 2. REGRESSÃO SIMPLIFICADA ============
st.header("2. Diferença Média de Ticket (Regressão Linear)")
with st.expander("📚 O que é Regressão Linear Simples?", expanded=True):
    st.markdown("""
    - Ajusta um modelo **Valor_Pedido = β₀ + β₁ × B2B_Flag**.  
    - **β₀**: ticket médio de B2C (flag=0).  
    - **β₁**: diferença média que clientes B2B pagam a mais (ou a menos).  
    - **R²**: proporção da variação de `Valor_Pedido` explicada por `B2B_Flag`.
    """)

# Preparar dados e ajustar modelo
X = df[['B2B_Flag']].values
y = df['Valor_Pedido'].values
model = LinearRegression().fit(X, y)
b0, b1 = model.intercept_, model.coef_[0]
r2 = model.score(X, y)

# Mostrar coeficientes
st.markdown(f"""
- **β₀ (ticket B2C):** R$ {b0:.2f}  
- **β₁ (diferença B2B – B2C):** R$ {b1:.2f}  
- **R²:** {r2:.3f}
""")

# Gráfico de barras comparativo
st.subheader("Gráfico de Barras: Ticket Médio Estimado para B2C e B2B")
fig, ax = plt.subplots(figsize=(6,4))
heights = [b0, b0 + b1]
ax.bar(['B2C','B2B'], heights, color=['#4C78A8','#F58518'])
ax.set_ylabel("Ticket Médio Estimado (R$)")
ax.set_title("Estimativa de Ticket Médio via Regressão Linear")
for i, v in enumerate(heights):
    ax.text(i, v + (max(heights) * 0.01), f"R$ {v:.2f}", ha='center')
st.pyplot(fig)

# Explicação sobre a escolha do gráfico
with st.expander("ℹ️ Por que não usamos o scatter + linha de regressão usual?", expanded=False):
    st.markdown("""
    **Desafios com o scatter + reta em dados binários (0/1):**  
    - Todos os valores de `B2B_Flag` ficam em apenas dois níveis (0 ou 1),  
      o que agrupa todos os pontos em duas linhas horizontais e torna a reta quase plana.  
    - Fica difícil visualizar a variação real do ticket dentro de cada grupo  
      e interpretar o coeficiente β₁ apenas pela inclinação da reta.

    **Vantagens do gráfico de barras de médias estimadas:**  
    - **Clareza:** mostra diretamente a estimativa de ticket para cada grupo (β₀ e β₀+β₁).  
    - **Leiturabilidade:** rótulos numéricos sobre as barras facilitam a comparação.  
    - **Foco no insight:** destaca a diferença média de ticket entre B2C e B2B (β₁).

    **Desvantagens:**  
    - **Perda de variabilidade:** não mostra dispersão e outliers dentro de cada grupo.  
    - **Abstração maior:** requer o entendimento de que a barra B2B = β₀ + β₁,  
      em vez de visualizar o ajuste no próprio scatter.

    Em resumo, optamos pelo bar chart para comunicar de forma imediata e intuitiva  
    a diferença média de ticket entre clientes B2C e B2B, mantendo a clareza do insight principal.
    """)

# ============ 3. INTERPRETAÇÃO FINAL E APLICAÇÕES ============
st.header("💡 Interpretação Final e Aplicações Práticas")
st.markdown(f"""
- **Ticket médio B2C (β₀):** R$ {b0:.2f}  
- **Diferença média B2B – B2C (β₁):** R$ {b1:.2f}  
- **R²:** {r2:.3f} indica que {r2*100:.1f}% da variação no valor do pedido é explicada pelo tipo de cliente.

**Principais insights para o negócio:**
1. Clientes corporativos (B2B) compram em média **R$ {abs(b1):.2f} {'a mais' if b1>0 else 'a menos'}** que clientes finais.  
2. O valor de R² sugere que o fato de ser B2B explica uma parte significativa da variação de ticket, mas outros fatores (categoria, promoções, sazonalidade) também são importantes.  

**Recomendações de ação:**
- 🎯 **Campanhas Segmentadas:** criar ofertas e condições especiais para clientes corporativos, uma vez que exibem maior ticket médio.  
- 📊 **Aprofundar Análise:** incluir variáveis adicionais (e.g., categoria de produto, promoção aplicada) em uma regressão múltipla para melhorar o poder preditivo.  
- 🔄 **Monitoramento Contínuo:** acompanhar periodicamente a diferença de ticket entre B2C e B2B para ajustar estratégias de vendas e precificação.
""")
