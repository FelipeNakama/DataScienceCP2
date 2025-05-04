import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Carregamento de dados (mesma função cache das outras páginas)
@st.cache_data
def load_data():
    df = pd.read_excel("df_selecionado.xlsx")
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')
    return df

df = load_data()

# Título e introdução
st.title("🧪 Parte 2: Testes de Hipótese")
st.markdown("---")
st.markdown("""
### Objetivos
Nesta seção, vamos responder duas perguntas-chave:

1. **Ticket Médio:** Será que certas categorias de produtos (por exemplo, Eletrônicos vs Roupas) têm preços médios diferentes?   
   _Insight_: entender onde está o maior valor agregado.

2. **Cancelamentos x Envio:** O método de envio (Padrão vs Expresso) influencia na taxa de cancelamentos?   
   _Insight_: avaliar se oferecer frete expresso reduz desistências.

Para cada pergunta, formulamos hipóteses, calculamos uma estatística e um p‑valor, e interpretamos o resultado de forma simples.
""")
st.markdown("---")

# Sidebar: filtros básicos
with st.sidebar:
    st.header("🔧 Filtros Gerais")
    date_range = st.date_input("Período", [df['Data_Pedido'].min(), df['Data_Pedido'].max()])
    df = df[(df['Data_Pedido'] >= pd.to_datetime(date_range[0])) & (df['Data_Pedido'] <= pd.to_datetime(date_range[1]))]

# -----------------------------
# Teste 1: Two-sample t-test
# -----------------------------
st.header("1. t‑test: Ticket Médio entre Categorias")
st.markdown("Queremos saber se existe diferença no valor médio dos pedidos entre duas categorias de produtos.")

# Seleção dinâmica de categorias para comparação
disponiveis = df['Categoria'].dropna().unique().tolist()
if len(disponiveis) < 2:
    st.warning("Não há categorias suficientes para realizar o t-test.")
else:
    colA, colB = st.columns(2)
    with colA:
        cat1 = st.selectbox("Categoria A", disponiveis, index=0)
    with colB:
        cat2 = st.selectbox("Categoria B", [c for c in disponiveis if c != cat1], index=0)

    sample1 = df[df['Categoria'] == cat1]['Valor_Pedido'].dropna()
    sample2 = df[df['Categoria'] == cat2]['Valor_Pedido'].dropna()

    if len(sample1) < 2 or len(sample2) < 2:
        st.warning("Amostras pequenas (menos de 2 observações) em uma das categorias, não é possível realizar o t-test.")
    else:
        with st.expander("📝 Hipóteses", expanded=True):
            st.markdown(f"""
            - **H₀ (nula):** O ticket médio de **{cat1}** é igual ao de **{cat2}**.  
            - **H₁ (alternativa):** O ticket médio de **{cat1}** é diferente do de **{cat2}**.
            """)

        # Cálculo do t‑test (Welch, variâncias desiguais)
        t_stat, p_val = stats.ttest_ind(sample1, sample2, equal_var=False)
        # graus de liberdade aproximado de Welch
        df_num = (sample1.var(ddof=1)/len(sample1) + sample2.var(ddof=1)/len(sample2))**2
        t_stat, p_val = stats.ttest_ind(sample1, sample2, equal_var=False)
        # graus de liberdade aproximado de Welch\        df_num = (sample1.var(ddof=1)/len(sample1) + sample2.var(ddof=1)/len(sample2))**2
        df_den = ((sample1.var(ddof=1)/len(sample1))**2)/(len(sample1)-1) + ((sample2.var(ddof=1)/len(sample2))**2)/(len(sample2)-1)
        gl = df_num/df_den

        # Exibir resultados numéricos
        col1, col2, col3 = st.columns(3)
        col1.metric("t-Statistic", f"{t_stat:.3f}")
        col2.metric("p-valor", f"{p_val:.3f}")
        col3.metric("Grau de liberdade (aprox.)", f"{gl:.0f}")

        # Explicação simplificada, incluindo gl
        st.markdown("""
        **O que é o t-Statistic?**  
        Quantifica em unidades de erro padrão a diferença entre médias.  
        
        **O que é grau de liberdade?**  
        Indica quantos valores independentes sustentam a estimativa de variância; afeta a forma da curva t.  
        - Maior gl → curva t mais próxima da normal.  
        
        **Como usar o p-valor?**  
        - Se p-valor ≤ 0.05, **rejeitamos H₀** (diferença significativa).  
        - Se p-valor > 0.05, **não rejeitamos H₀** (diferença não comprovada).  
        - P-valor = 0 indica evidência extremamente forte contra H₀.

        **Tomada de Decisão:**  
        - ✅ **p ≤ 0.05**: Há diferença real!  
          _Ação:_ Investir mais na categoria com maior ticket.  
        - ⚠️ **p > 0.05**: Diferença pode ser acaso  
          _Ação:_ Analisar outros fatores.
        """)

        # Boxplot com anotação de médias fora das caixas
        st.subheader("📦 Boxplot de Valor_Pedido por Categoria")
        fig, ax = plt.subplots()
        sns.boxplot(x='Categoria', y='Valor_Pedido', data=df[df['Categoria'].isin([cat1, cat2])], ax=ax)
        # Anotar médias acima das caixas
        for i, m in enumerate([sample1.mean(), sample2.mean()]):
            ax.text(i, m + 0.05*(df['Valor_Pedido'].max()-df['Valor_Pedido'].min()), f"Média: R$ {m:.2f}", ha='center', va='bottom', color='black')
        ax.set_title(f'Comparação de Ticket Médio: {cat1} vs {cat2}')
        st.pyplot(fig)

        # Interpretação e ligação com o negócio
        alpha = 0.05
        if p_val <= alpha:
            conclusão = f"**Rejeitamos H₀** (p≤{alpha}): há diferença significativa no ticket médio entre {cat1} e {cat2}."
            ação = f"💡 Conclusão de negócio: recomenda-se estratégias de preço diferenciadas para {cat1 if sample1.mean()>sample2.mean() else cat2}."
        else:
            conclusão = f"**Não rejeitamos H₀** (p>{alpha}): não há evidência de diferença significativa no ticket médio entre {cat1} e {cat2}."
            ação = f"💡 Conclusão de negócio: médias similares; investigar fatores adicionais antes de mudar preços."
        st.markdown(conclusão)
        st.markdown(ação)

st.markdown("---")

# ---------------------------------------------
# Teste 2: Qui-quadrado de independência
# ---------------------------------------------
st.header("2. Qui‑Quadrado: Cancelamento x Nível de Entrega")
st.markdown("Queremos verificar se o tipo de frete influencia a decisão de cancelar pedidos.")

contingency = pd.crosstab(df['Nivel_Entrega'], df['Status_Pedido'])
if contingency.shape[0] < 2 or contingency.shape[1] < 2:
    st.warning("Dados insuficientes para o teste qui-quadrado.")
else:
    with st.expander("📝 Hipóteses", expanded=True):
        st.markdown("""
        - **H₀ (nula):** O status do pedido (Cancelado/Enviado) é **independente** do nível de entrega.  
        - **H₁ (alternativa):** Há **relação** entre status do pedido e nível de entrega.
        """)

    chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)

    col1, col2, col3 = st.columns(3)
    col1.metric("Chi2", f"{chi2:.3f}")
    col2.metric("p-valor", f"{p_chi:.3f}")
    col3.metric("Grau de liberdade", f"{dof}")

    # Mostrar tabela observada vs esperada
    with st.expander("🔢 Observado vs Esperado", expanded=False):
        st.markdown("**Objetivo:** Ver onde ocorrem os maiores desvios da independência esperado vs real.")
        obs = contingency
        exp_df = pd.DataFrame(expected, index=contingency.index, columns=contingency.columns)
        st.write("**Observado**")
        st.dataframe(obs)
        st.write("**Esperado**")
        st.dataframe(exp_df)

    st.markdown("""
    **O que é o Chi‑square?**  
    Mede o quanto a distribuição observada difere da esperada sob independência.  
    - 📊 **Chi2 alto** indica forte padrão de cancelamento diferenciado.  

    **Por que mostramos Observado vs Esperado?**  
    - Para identificar quais combinações (frete x status) mais contribuem para o desvio.  
    - Linhas com maior diferença mostram pontos críticos de atenção.

    **Como usar o p‑valor?**  
    - Se p‑valor ≤ 0.05, **rejeitamos H₀**: existe relação entre frete e cancelamento.  
    - Se p‑valor > 0.05, **não rejeitamos H₀**: sem evidência de relação.
    """)

    # Gráfico de proporção ajustado
    st.subheader("📊 Proporção de Status por Nível de Entrega")
    # Agrupar status menos frequentes em 'Outros' para visualização clara
    status_counts = df['Status_Pedido'].value_counts()
    top_status = status_counts.nlargest(3).index.tolist()
    # Remap df for plotting
    df_plot = df.copy()
    df_plot['Status_Agrupado'] = df_plot['Status_Pedido'].where(df_plot['Status_Pedido'].isin(top_status), other='Outros')
    prop = pd.crosstab(df_plot['Nivel_Entrega'], df_plot['Status_Agrupado']).div(
        pd.crosstab(df_plot['Nivel_Entrega'], df_plot['Status_Agrupado']).sum(axis=1), axis=0
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    prop.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('Proporção')
    ax.set_title('Cancelamento vs Nível de Entrega')
    ax.legend(title='Status_Pedido', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    # Anotar percentuais corretos
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2,
                    f"{height*100:.1f}%", ha='center', va='center')
    st.pyplot(fig)

    # Interpretação e ligação com o negócio
    alpha = 0.05
    if p_chi <= alpha:
        concl_chi = f"**Rejeitamos H₀** (p≤{alpha}): há associação significativa entre nível de entrega e cancelamento."
        ação_chi = "💡 Conclusão de negócio: o tipo de frete impacta diretamente a taxa de cancelamento; recomendamos revisar processos de frete expresso (prazo, custo) para reduzir desistências."
    else:
        concl_chi = f"**Não rejeitamos H₀** (p>{alpha}): não há evidência de associação entre nível de entrega e cancelamento."
        ação_chi = "💡 Conclusão de negócio: o frete não parece influenciar cancelamentos; investigar outras causas."
    st.markdown(concl_chi)
    st.markdown(ação_chi)

st.success("✨ Testes concluídos! Use estes resultados para apoiar decisões de preço e logística.")
