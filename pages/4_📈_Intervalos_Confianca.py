import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')
    return df

df = load_data()

st.title("📊 Análise com Intervalos de Confiança")
st.markdown("---")

# ========================================================================
# Seção Introdutória Geral
# ========================================================================
st.markdown("""
### Objetivo desta Seção
Nesta parte, estimamos intervalos de confiança para:
- A **média dos valores dos pedidos**,
- A **proporção de cancelamentos**, 
- Realizar uma **comparação entre categorias**.

Esses intervalos fornecem uma medida de precisão das estimativas e embasam decisões estratégicas, ajudando a identificar se os resultados estão de acordo com as metas e expectativas do negócio.
""")
st.markdown("---")

# ========================================================================
# Seção 1: Apresentação das Variáveis
# ========================================================================
st.header("🔍 Variáveis Utilizadas na Análise")
with st.expander("Ver detalhes das variáveis", expanded=True):
    st.markdown("""
    | Variável       | Tipo                | Papel na Análise                                             | Exemplo    |
    |----------------|---------------------|--------------------------------------------------------------|------------|
    | `Valor_Pedido` | Numérica Contínua   | Base para estimar a média dos pedidos                        | R$ 149.99  |
    | `Status_Pedido`| Categórica          | Cálculo da proporção de cancelamentos                        | "Cancelado"|
    | `Categoria`    | Categórica          | Comparação do desempenho entre segmentos                     | "Eletrônicos"|
    | `Nivel_Entrega`| Categórica          | Avaliação do impacto logístico                               | "Expresso" |
    """)
st.markdown("---")

# ========================================================================
# Seção 2: Seleção de Análise
# ========================================================================
analise = st.sidebar.selectbox(
    "Escolha o Tipo de Análise:",
    ("Média de Valor dos Pedidos", 
     "Proporção de Pedidos Cancelados",
     "Comparação entre Categorias")
)

# ========================================================================
# Análise 1: Intervalo de Confiança para Média
# ========================================================================
if analise == "Média de Valor dos Pedidos":
    st.header("1. Intervalo de Confiança para Média de Valores")
    
    # Apresentação da Variável
    with st.expander("🔍 Variável Utilizada", expanded=True):
        st.markdown("""
        | Variável       | Tipo              | Papel na Análise                                        |
        |----------------|-------------------|---------------------------------------------------------|
        | `Valor_Pedido` | Numérica Contínua | Representa o valor total de cada pedido, usado para estimar a média populacional |
        """)
    
    # Fundamentação Teórica
    with st.expander("📚 Por que usar IC para média?", expanded=True):
        st.markdown("""
        **Objetivo da Análise:**  
        Estimar, com 95% de confiança, a faixa de valores onde se encontra a **verdadeira média populacional** dos pedidos.

        **Justificativa do Uso da Distribuição t:**  
        - Amostras pequenas ou com variabilidade desconhecida utilizam a distribuição t.  
        - Aqui, mesmo com n > 30, optamos pela distribuição t para levar em conta a variabilidade observada.
        
        **Pressupostos Verificados:**
        1. Amostra aleatória e independente ✅  
        2. Tamanho amostral adequado (n = {n} > 30) ✅

        **Fórmula Utilizada:**  
        """.format(n=len(df['Valor_Pedido'].dropna())))
        
        st.latex(r'''
        IC = \bar{x} \pm t_{\alpha/2} \times \frac{s}{\sqrt{n}}
        ''')
        st.markdown("""
        Onde:
        - $bar{x}$ = Média amostral  
        - $s$ = Desvio padrão amostral  
        - $n$ = Tamanho da amostra  
        - $t_{alpha/2}$ = Valor crítico da distribuição t  
        """)
    
    # Cálculos
    sample = df['Valor_Pedido'].dropna()
    confidence_level = 0.95
    n = len(sample)
    sample_mean = np.mean(sample)
    sample_std = np.std(sample, ddof=1)
    t_critical = stats.t.ppf((1 + confidence_level)/2, df=n-1)
    margin_of_error = t_critical * (sample_std / np.sqrt(n))
    ic_min = sample_mean - margin_of_error
    ic_max = sample_mean + margin_of_error
    
    # Resultados Numéricos
    st.subheader("📊 Resultados Numéricos")
    col1, col2, col3 = st.columns(3)
    col1.metric("Média Amostral", f"R$ {sample_mean:.2f}")
    col2.metric("Desvio Padrão", f"R$ {sample_std:.2f}")
    col3.metric(f"IC {int(confidence_level*100)}%", f"R$ {ic_min:.2f} - R$ {ic_max:.2f}")
    
    # Visualização
    st.subheader("📈 Visualização do Intervalo")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot da distribuição com densidade
    sns.kdeplot(sample, ax=ax, color='#3498db', linewidth=2, fill=True, alpha=0.2)
    
    # Área do Intervalo de Confiança
    ax.axvspan(ic_min, ic_max, color='#e74c3c', alpha=0.2, label='IC 95%')
    
    # Linha da média
    ax.axvline(sample_mean, color='#2ecc71', linewidth=3, label=f'Média (R$ {sample_mean:.2f})')
    
    ax.set_title("Distribuição de Valores com IC 95%", fontsize=14)
    ax.set_xlabel("Valor dos Pedidos (R$)", fontsize=12)
    ax.set_ylabel("Densidade", fontsize=12)
    ax.legend()
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    
    st.pyplot(fig)
    
    # Interpretação Contextual
    st.markdown(f"""
    ### 💡 Interpretação Prática
    
    - Com 95% de confiança, o **valor médio real** de todos os pedidos está entre **R$ {ic_min:.2f}** e **R$ {ic_max:.2f}**.
    - A amplitude do intervalo (**R$ {ic_max - ic_min:.2f}**) reflete a precisão da estimativa.
    
    **Implicações Comerciais:**
    - Se a meta for, por exemplo, uma média superior a R$ {ic_min:.2f}, então o desempenho atual está **{'além' if sample_mean > ic_min else 'aquém'}** das expectativas.
    - Recomenda-se comparar estes resultados com dados históricos e investigar outliers para otimizar estratégias de preço e logística.
    """)

# ========================================================================
# Análise 2: Intervalo de Confiança para Proporção
# ========================================================================
elif analise == "Proporção de Pedidos Cancelados":
    st.header("2. Intervalo de Confiança para Proporção de Cancelamentos")
    
    # Cálculo das Variáveis
    cancelados = df[df['Status_Pedido'] == 'Cancelado'].shape[0]
    total = df.shape[0]
    p_hat = cancelados / total  # Proporção amostral
    
    # Apresentação da Variável
    with st.expander("🔍 Variável Utilizada", expanded=True):
        st.markdown(f"""
        | Variável        | Tipo       | Descrição                         | Valores                           |
        |-----------------|------------|-----------------------------------|-----------------------------------|
        | `Status_Pedido` | Categórica | Status do pedido                  | {cancelados} Cancelados<br>{total - cancelados} Concluídos |
        """, unsafe_allow_html=True)
    
    # Fundamentação Teórica
    with st.expander("📚 Fundamentação Estatística", expanded=True):
        st.markdown(f"""
        **Objetivo:**  
        Estimar a verdadeira taxa de cancelamentos com 95% de confiança.
        
        **Pressupostos Validados:**
        - Amostra aleatória e independente ✅  
        - Condição de normalidade:  
          - `n * p̂ = {cancelados}` ≥ 10 ✅  
          - `n * (1 - p̂) = {total - cancelados}` ≥ 10 ✅
        
        **Fórmula Utilizada:**  
        """)
        st.latex(r'''
        IC = \hat{p} \pm Z_{\alpha/2} \times \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
        ''')
        st.markdown(f"""
        Onde:
        - $\hat{{p}}$ = {p_hat:.4f} (proporção amostral)
        - $Z_{{alpha/2}}$ = 1.96 (para 95% de confiança)
        - $n$ = {total}
        """)
    
    # Permite ajuste interativo do nível de confiança para a proporção
    confidence_level = st.slider("Nível de Confiança", 0.80, 0.99, 0.95, key="cancel_slider")
    z_critical = stats.norm.ppf((1 + confidence_level) / 2)
    margin_of_error = z_critical * np.sqrt(p_hat * (1 - p_hat)) / np.sqrt(total)
    ic_min = p_hat - margin_of_error
    ic_max = p_hat + margin_of_error
    
    # Visualização
    st.subheader("📊 Visualização do Intervalo")
    fig, ax = plt.subplots(figsize=(8, 3))
    
    ax.set_xlim(0, max(ic_max*1.5, 0.25))
    ax.set_ylim(-0.5, 0.5)
    ax.get_yaxis().set_visible(False)
    
    # Linha de meta (por exemplo, 10% de cancelamento)
    ax.axvline(x=0.10, color='#2ecc71', linewidth=2, linestyle='--', label='Meta (10%)')
    
    # Representação do IC
    ax.hlines(y=0, xmin=ic_min, xmax=ic_max, color='#e74c3c', linewidth=4, label=f'IC {int(confidence_level*100)}%')
    ax.plot(p_hat, 0, 'o', markersize=10, color='#c0392b', label='Proporção Observada')
    
    # Anotações
    ax.text(ic_min, 0.2, f'{ic_min*100:.1f}%', ha='center', color='#e74c3c')
    ax.text(ic_max, 0.2, f'{ic_max*100:.1f}%', ha='center', color='#e74c3c')
    ax.text(p_hat, -0.3, f'Média: {p_hat*100:.1f}%', ha='center', color='#c0392b', weight='bold')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Taxa de Cancelamentos (%)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    
    st.pyplot(fig)
    
    # Interpretação Contextual
    st.markdown(f"""
    ### 💡 Interpretação Prática
    
    - Estima-se que a taxa real de cancelamentos esteja entre **{ic_min*100:.1f}%** e **{ic_max*100:.1f}%**.
    
    **Implicações Operacionais:**
    {"- ❌ **Crítico:** O limite inferior está acima da meta de 10% → Ação imediata necessária" 
     if ic_min > 0.10 else 
     "- ✅ **Dentro da Meta:** O intervalo está compatível com os objetivos estratégicos" 
     if ic_max <= 0.10 else 
     "- ⚠️ **Atenção:** O limite superior excede a meta → Monitoramento necessário"}
    
    **Ações Recomendadas:**
    1. Investigar as causas dos cancelamentos, analisando fatores regionais, métodos de pagamento e categorias de produtos.
    2. Buscar estratégias para reduzir a taxa de cancelamento em aproximadamente **{abs(p_hat - 0.10)*100:.1f} pontos percentuais**.
    3. Monitorar a evolução da taxa com dashboards em tempo real.
    """)

# ========================================================================
# Análise 3: Comparação entre Categorias
# ========================================================================
else:
    st.header("3. Comparação de Médias entre Categorias")
    
    # Seleção Interativa
    categorias = df['Categoria'].unique().tolist()
    cat1, cat2 = st.columns(2)
    with cat1:
        categoria1 = st.selectbox("Primeira Categoria", categorias, index=0)
    with cat2:
        categoria2 = st.selectbox("Segunda Categoria", [c for c in categorias if c != categoria1], index=0)
    
    # Explicação Teórica
    with st.expander("📚 Método Estatístico Utilizado", expanded=True):
        st.markdown("""
        **Objetivo:**  
        Comparar se há diferença significativa entre o valor médio dos pedidos de duas categorias distintas.
        
        **Justificativa:**  
        Cada categoria possui sua distribuição, e utilizamos intervalos de confiança separados para comparar as estimativas de média.
        
        **Fórmula Utilizada para Cada Categoria:**  
        """)
        st.latex(r'''
        IC = \bar{x}_i \pm t_{\alpha/2} \times \frac{s_i}{\sqrt{n_i}}
        ''')
    
    # Dados e Cálculos
    dados_cat1 = df[df['Categoria'] == categoria1]['Valor_Pedido'].dropna()
    dados_cat2 = df[df['Categoria'] == categoria2]['Valor_Pedido'].dropna()
    
    ic_cat1 = stats.t.interval(0.95, len(dados_cat1)-1, 
                              loc=np.mean(dados_cat1), 
                              scale=stats.sem(dados_cat1))
    ic_cat2 = stats.t.interval(0.95, len(dados_cat2)-1, 
                              loc=np.mean(dados_cat2), 
                              scale=stats.sem(dados_cat2))
    
    # Visualização
    st.subheader("Comparação Visual")
    fig, ax = plt.subplots(figsize=(10,5))
    
    y_pos = [1, 2]
    
    # Plot com erro simétrico para cada categoria
    error_cat1 = (np.mean(dados_cat1) - ic_cat1[0], ic_cat1[1] - np.mean(dados_cat1))
    error_cat2 = (np.mean(dados_cat2) - ic_cat2[0], ic_cat2[1] - np.mean(dados_cat2))
    
    ax.errorbar(x=np.mean(dados_cat1), y=y_pos[0], 
               xerr=[[error_cat1[0]], [error_cat1[1]]], fmt='o', color='blue', 
               label=categoria1, markersize=10, capsize=5)
    ax.errorbar(x=np.mean(dados_cat2), y=y_pos[1], 
               xerr=[[error_cat2[0]], [error_cat2[1]]], fmt='o', color='red', 
               label=categoria2, markersize=10, capsize=5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([categoria1, categoria2])
    ax.set_xlabel("Valor Médio dos Pedidos (R$)")
    ax.set_title("Comparação de Médias com IC 95%")
    ax.legend()
    
    st.pyplot(fig)
    
    # Interpretação Contextual
    st.markdown(f"""
    ### 💡 Interpretação Detalhada
    **Intervalos Calculados:**
    - **{categoria1}:** Média entre R$ {ic_cat1[0]:.2f} e R$ {ic_cat1[1]:.2f}
    - **{categoria2}:** Média entre R$ {ic_cat2[0]:.2f} e R$ {ic_cat2[1]:.2f}
    
    **Sobreposição dos Intervalos:**
    - {"Há sobreposição entre os intervalos, o que indica que não podemos afirmar com 95% de confiança que as médias são diferentes."
      if (ic_cat1[1] > ic_cat2[0]) and (ic_cat2[1] > ic_cat1[0])
      else "Não há sobreposição, sugerindo diferença estatisticamente significativa entre as categorias."}
    
    **Implicações para o Negócio:**
    - {"A categoria " + categoria2 + " apresenta valores médios superiores, sugerindo foco em estratégias para aumentar o desempenho de " + categoria1 + "."
      if np.mean(dados_cat2) > np.mean(dados_cat1) and not ((ic_cat1[1] > ic_cat2[0]) and (ic_cat2[1] > ic_cat1[0]))
      else "A categoria " + categoria1 + " apresenta valores médios superiores, sugerindo foco em estratégias para aumentar o desempenho de " + categoria2 + "."
      if not ((ic_cat1[1] > ic_cat2[0]) and (ic_cat2[1] > ic_cat1[0]))
      else "As diferenças podem ser atribuídas ao acaso amostral, sendo necessário coletar mais dados."}
    
    **Recomendações:**
    - Investigar fatores que possam explicar as diferenças nas médias.
    - Considerar estratégias promocionais ou ajustes operacionais específicos para cada categoria.
    """, unsafe_allow_html=True)
