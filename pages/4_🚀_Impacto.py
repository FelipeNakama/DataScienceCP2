import streamlit as st

st.title("🚀 Impacto Estratégico do Dashboard")
st.markdown("---")

# Seção 1: Justificativa do Streamlit
with st.expander("📌 **Por Que Usamos o Streamlit?**", expanded=True):
    st.markdown("""
    ### Vantagens Técnicas para Análise Estatística
    | Característica | Benefício para o Problema |
    |----------------|---------------------------|
    | **Interatividade em Tempo Real** | Teste dinâmico de hipóteses com filtros de categoria/região |
    | **Integração com Python** | Uso de bibliotecas estatísticas (SciPy, Statsmodels) |
    | **Visualização Customizável** | Gráficos com ICs e valores-p integrados |
    | **Deploy Facilitado** | Publicação online para acesso da equipe comercial |
    | **Front-End Simplificado**| Facilita o uso para profissionais de outras areas|
    
    """)

# Seção 2: Conexão Problema-Solução
st.subheader("🔗 Problema Real vs Funcionalidade do Dashboard")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Desafios Operacionais
    1. **Alto Custo Logístico**  
       - Variação de +30% nos custos por estado
    2. **Estoque Ineficiente**  
       - 40% dos produtos com baixa rotatividade
    3. **Cancelamentos**  
       - 15% dos pedidos cancelados pós-compra
    """)

with col2:
    st.markdown("""
    ### Visualização no Dashboard para traçar possiveis soluções
    1. **Análise por `Nivel_Entrega`**  
       - Comparação de custos entre fretes
    2. **Filtro de `Categoria`**  
       - Identificação de produtos obsoletos
    3. **Segmentação `Status_Pedido`**  
       - Drill-down nas causas de cancelamento
    """)

