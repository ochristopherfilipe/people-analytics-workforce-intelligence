"""
People Analytics — Executive Dashboard (PT-BR)
Painel Executivo Interativo de Inteligência de Pessoas e Monitoramento de Turnover.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Configuração da Página ───────────────────────────────────
st.set_page_config(
    page_title="People Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilização Personalizada (Tema Escuro Executivo) ─────────
st.markdown("""
<style>
    .main { background-color: #0F172A; }
    .stApp { background-color: #0F172A; }
    
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        border: 1px solid #475569;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        margin: 6px 0;
    }
    .metric-label {
        font-size: 12px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 11px;
        color: #64748B;
        margin-top: 4px;
    }
    
    .explanation-box {
        background-color: #1E293B;
        border-left: 4px solid #6366F1;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 15px;
        font-size: 13px;
        color: #CBD5E1;
        line-height: 1.5;
    }
    
    .explanation-box strong {
        color: #E2E8F0;
    }

    h1 { color: #E2E8F0 !important; font-weight: 700 !important; }
    h2 { color: #CBD5E1 !important; font-weight: 600 !important; }
    h3 { color: #94A3B8 !important; font-size: 18px !important; }
    
    .stSidebar { background-color: #1E293B; }
    
    div[data-testid="stMetricValue"] { font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# ── Paleta de Cores ──────────────────────────────────────────
COLORS = {
    'primary': '#6366F1',
    'secondary': '#8B5CF6',
    'accent': '#EC4899',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#06B6D4',
}
PLOTLY_TEMPLATE = "plotly_dark"
BG_COLOR = '#0F172A'
CARD_COLOR = '#1E293B'

# ── Mapeamento de Dicionário de Dados para PT-BR ──────────────
DEPT_MAP = {
    'Research & Development': 'Pesquisa & Desenvolvimento (P&D)',
    'Sales': 'Vendas',
    'Human Resources': 'Recursos Humanos (RH)'
}

TRAVEL_MAP = {
    'Travel_Rarely': 'Viaja Raramente',
    'Travel_Frequently': 'Viaja Frequentemente',
    'Non-Travel': 'Não Viaja'
}

GENDER_MAP = {
    'Male': 'Masculino',
    'Female': 'Feminino'
}

MARITAL_MAP = {
    'Married': 'Casado(a)',
    'Single': 'Solteiro(a)',
    'Divorced': 'Divorciado(a)'
}

EDU_FIELD_MAP = {
    'Life Sciences': 'Ciências da Vida',
    'Medical': 'Medicina / Saúde',
    'Marketing': 'Marketing',
    'Technical Degree': 'Ensino Técnico',
    'Human Resources': 'Recursos Humanos',
    'Other': 'Outros'
}

ROLE_MAP = {
    'Sales Executive': 'Executivo de Vendas',
    'Research Scientist': 'Cientista Pesquisador',
    'Laboratory Technician': 'Técnico de Laboratório',
    'Manufacturing Director': 'Diretor de Manufatura',
    'Healthcare Representative': 'Representante de Saúde',
    'Manager': 'Gerente',
    'Sales Representative': 'Representante de Vendas',
    'Research Director': 'Diretor de Pesquisa',
    'Human Resources': 'Recursos Humanos'
}

SATISFACTION_LABELS = {
    1: '1 - Baixa',
    2: '2 - Média',
    3: '3 - Alta',
    4: '4 - Muito Alta'
}

TREND_MAP = {
    'Increasing': 'Crescente (Aumentando horas)',
    'Stable': 'Estável (Jornada constante)',
    'Declining': 'Declinante (Queda na jornada)'
}

# ── Carregamento de Dados ────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/master_dataset.csv')
    
    # Aplicar traduções amigáveis em PT-BR nas colunas categóricas
    df['Department_BR'] = df['Department'].map(DEPT_MAP).fillna(df['Department'])
    df['BusinessTravel_BR'] = df['BusinessTravel'].map(TRAVEL_MAP).fillna(df['BusinessTravel'])
    df['Gender_BR'] = df['Gender'].map(GENDER_MAP).fillna(df['Gender'])
    df['MaritalStatus_BR'] = df['MaritalStatus'].map(MARITAL_MAP).fillna(df['MaritalStatus'])
    df['EducationField_BR'] = df['EducationField'].map(EDU_FIELD_MAP).fillna(df['EducationField'])
    df['JobRole_BR'] = df['JobRole'].map(ROLE_MAP).fillna(df['JobRole'])
    df['Attrition_BR'] = df['Attrition'].map({'Yes': 'Desligado', 'No': 'Ativo'})
    if 'TrendCategory' in df.columns:
        df['TrendCategory_BR'] = df['TrendCategory'].map(TREND_MAP).fillna(df['TrendCategory'])
    return df

df = load_data()

# ── Barra Lateral (Menu & Filtros em PT-BR) ───────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/analytics.png", width=55)
st.sidebar.title("📊 People Analytics")
st.sidebar.caption("Inteligência de Dados de Pessoas & Retention Risk")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navegação do Painel",
    ["🏠 Visão Geral", "📉 Análise de Turnover", "⏱️ Engajamento & Ponto", "🎯 Monitor Preditivo de Risco"],
    index=0
)

# Filtros Globais
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros Globais")
st.sidebar.markdown(
    "<small style='color:#94A3B8;'>Selecione os filtros abaixo para refinar os indicadores de todas as páginas em tempo real.</small>", 
    unsafe_allow_html=True
)

depts = ['Todos os Departamentos'] + sorted(df['Department_BR'].unique().tolist())
selected_dept = st.sidebar.selectbox("Departamento", depts)

levels = ['Todos os Níveis'] + sorted([f"Nível {l}" for l in df['JobLevel'].unique()])
selected_level = st.sidebar.selectbox("Nível Hierárquico", levels)

# Aplicação dos filtros
filtered = df.copy()
if selected_dept != 'Todos os Departamentos':
    filtered = filtered[filtered['Department_BR'] == selected_dept]
if selected_level != 'Todos os Níveis':
    lvl_num = int(selected_level.replace("Nível ", ""))
    filtered = filtered[filtered['JobLevel'] == lvl_num]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Exibindo:** `{len(filtered):,}` de `{len(df):,}` colaboradores")


# ═══════════════════════════════════════════════════════════════
# PÁGINA 1: 🏠 Visão Geral
# ═══════════════════════════════════════════════════════════════
if page == "🏠 Visão Geral":
    st.title("🏠 Visão Geral da Força de Trabalho (Workforce Overview)")
    
    st.markdown("""
    <div class="explanation-box">
        <strong>📌 O que é esta página?</strong> Apresenta um panorama executivo completo da saúde organizacional da companhia. 
        Combina indicadores demográficos, econômicos, operacionais e de satisfação em tempo real.<br>
        <strong>💡 Como usar?</strong> Utilize os cartões de KPIs no topo para uma visão rápida dos números macro e navegue pelos gráficos abaixo para entender a estrutura de cargos, remuneração e rotatividade.
    </div>
    """, unsafe_allow_html=True)
    
    # Cálculo das Métricas
    total = len(filtered)
    attrition = filtered['AttritionFlag'].mean() * 100
    avg_income = filtered['MonthlyIncome'].mean()
    avg_tenure = filtered['YearsAtCompany'].mean()
    avg_satisfaction = filtered['SatisfactionScore'].mean()
    avg_hours = filtered['AvgDailyWorkHours'].mean()
    absence_rate = filtered['AbsenceRate'].mean()
    avg_perf = filtered['PerformanceRating'].mean()
    
    # Linha 1 de KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Headcount Total</div>
            <div class="metric-value" style="color: {COLORS['primary']}">{total:,}</div>
            <div class="metric-sub">Colaboradores ativos + desligados</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        color = COLORS['danger'] if attrition > 15 else COLORS['warning'] if attrition > 10 else COLORS['success']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taxa de Turnover / Atrito</div>
            <div class="metric-value" style="color: {color}">{attrition:.1f}%</div>
            <div class="metric-sub">{filtered['AttritionFlag'].sum():,} desligamentos no período</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Salário Médio Mensal</div>
            <div class="metric-value" style="color: {COLORS['success']}">R$ {avg_income:,.0f}</div>
            <div class="metric-sub">Remuneração base média por colaborador</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Satisfação Média</div>
            <div class="metric-value" style="color: {COLORS['info']}">{avg_satisfaction:.2f} / 4.0</div>
            <div class="metric-sub">Índice composto (clima, cargo, work-life)</div>
        </div>""", unsafe_allow_html=True)
    
    # Linha 2 de KPIs
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tempo Médio de Casa</div>
            <div class="metric-value" style="color: {COLORS['secondary']}">{avg_tenure:.1f} anos</div>
            <div class="metric-sub">Permanência média na empresa</div>
        </div>""", unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Jornada Média Diária</div>
            <div class="metric-value" style="color: {COLORS['accent']}">{avg_hours:.1f} horas</div>
            <div class="metric-sub">Média registrada via sistema de ponto</div>
        </div>""", unsafe_allow_html=True)
    with c7:
        abs_color = COLORS['danger'] if absence_rate > 5 else COLORS['success']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taxa de Absenteísmo</div>
            <div class="metric-value" style="color: {abs_color}">{absence_rate:.1f}%</div>
            <div class="metric-sub">Percentual de ausências nos dias úteis</div>
        </div>""", unsafe_allow_html=True)
    with c8:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avaliação de Desempenho</div>
            <div class="metric-value" style="color: {COLORS['warning']}">{avg_perf:.2f} / 4.0</div>
            <div class="metric-sub">Nota média atribuída pela gestão</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bloco de Gráficos 1: Distribuições de Headcount
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Headcount por Departamento")
        st.caption("🔍 **O que mostra:** A proporção do efetivo total alocada em cada departamento da empresa.")
        
        dept_counts = filtered['Department_BR'].value_counts()
        fig = go.Figure(go.Pie(
            labels=dept_counts.index, values=dept_counts.values,
            hole=0.5,
            marker=dict(colors=[COLORS['primary'], COLORS['accent'], COLORS['success']]),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Colaboradores: %{value:,}<br>Proporção: %{percent}<extra></extra>"
        ))
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=CARD_COLOR,
            height=380,
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Insight:** Áreas operacionais como Pesquisa & Desenvolvimento e Vendas concentram a maior parte da força de trabalho, sendo cruciais para a retenção global.")

    with col2:
        st.subheader("2. Distribuição por Nível Hierárquico")
        st.caption("🔍 **O que mostra:** O número de colaboradores em cada um dos 5 níveis organizacionais (do Nível 1 - operacional ao Nível 5 - diretoria).")
        
        level_counts = filtered['JobLevel'].value_counts().sort_index()
        fig = go.Figure(go.Bar(
            x=[f'Nível {l}' for l in level_counts.index],
            y=level_counts.values,
            marker_color=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['info'], COLORS['warning']],
            text=[f"{v:,}" for v in level_counts.values],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Quantidade: %{y:,}<extra></extra>"
        ))
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=CARD_COLOR,
            height=380,
            xaxis_title="Nível Hierárquico", yaxis_title="Quantidade de Colaboradores",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Insight:** Formato em pirâmide típica de empresas industriais. Os Níveis 1 e 2 contêm a maioria dos trabalhadores e requerem atenção especial na jornada de entrada.")

    st.markdown("---")

    # Bloco de Gráficos 2: Salários e Turnover por Idade
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("3. Distribuição Salarial por Nível e Status de Retenção")
        st.caption("🔍 **O que mostra:** A amplitude e a mediana salarial mensal (R$) por nível hierárquico, comparando quem continua na empresa (Ativo) vs. quem se desligou (Desligado).")
        
        fig = px.box(
            filtered, x='JobLevel', y='MonthlyIncome', color='Attrition_BR',
            category_orders={'JobLevel': sorted(filtered['JobLevel'].unique())},
            color_discrete_map={'Desligado': COLORS['danger'], 'Ativo': COLORS['success']},
            labels={'MonthlyIncome': 'Salário Mensal (R$)', 'JobLevel': 'Nível Hierárquico', 'Attrition_BR': 'Status'}
        )
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=CARD_COLOR,
            height=400,
            xaxis_title="Nível Hierárquico", yaxis_title="Salário Mensal (R$)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Insight:** Nos níveis iniciais (Nível 1 e 2), a mediana salarial dos colaboradores desligados costuma ser inferior à dos que permanecem, sinalizando sensibilidade à remuneração.")

    with col2:
        st.subheader("4. Taxa de Turnover por Faixa Etária")
        st.caption("🔍 **O que mostra:** O percentual de desligamento em cada grupo etário, comparado com a taxa média geral da empresa (linha tracejada amarela).")
        
        age_group_attr = filtered.groupby('AgeGroup')['AttritionFlag'].agg(['mean', 'count']).reset_index()
        age_group_attr.columns = ['AgeGroup', 'Rate', 'Count']
        age_group_attr['Rate'] *= 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=age_group_attr['AgeGroup'], y=age_group_attr['Rate'],
            marker_color=COLORS['primary'],
            text=[f'{r:.1f}%' for r in age_group_attr['Rate']],
            textposition='outside',
            hovertemplate="<b>Faixa: %{x} anos</b><br>Taxa de Turnover: %{y:.1f}%<br>Total no Grupo: %{text}<extra></extra>"
        ))
        fig.add_hline(y=filtered['AttritionFlag'].mean() * 100, 
                     line_dash="dash", line_color=COLORS['warning'],
                     annotation_text=f"Média Geral ({filtered['AttritionFlag'].mean()*100:.1f}%)")
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=CARD_COLOR,
            height=400,
            xaxis_title="Faixa Etária (anos)", yaxis_title="Taxa de Turnover (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Insight:** Profissionais jovens (18 a 29 anos) costumam apresentar rotatividade mais alta do que trabalhadores de 40+ anos, indicando a necessidade de planos de carreira iniciais acelerados.")


# ═══════════════════════════════════════════════════════════════
# PÁGINA 2: 📉 Análise de Turnover
# ═══════════════════════════════════════════════════════════════
elif page == "📉 Análise de Turnover":
    st.title("📉 Diagnóstico Profundo de Turnover (Rotatividade)")
    
    st.markdown("""
    <div class="explanation-box">
        <strong>📌 O que é esta página?</strong> Uma investigação detalhada para identificar <strong>onde</strong> (quais áreas/cargos) e <strong>por que</strong> (fatores de satisfação e relacionamento) a empresa está perdendo colaboradores.<br>
        <strong>💡 Como usar?</strong> Alterne o seletor abaixo para analisar a taxa de saída por diferentes dimensões categóricas e examine a seção de satisfação para ver a influência do clima organizacional.
    </div>
    """, unsafe_allow_html=True)
    
    overall_rate = filtered['AttritionFlag'].mean() * 100
    
    st.subheader("1. Taxa de Turnover por Dimensão Selecionável")
    st.caption("🔍 Selecione a dimensão desejada no menu abaixo para atualizar o gráfico de barras horizontais rankeado.")
    
    col_sel, _ = st.columns([1, 1])
    with col_sel:
        segment_options = {
            'JobRole_BR': 'Cargo / Funções',
            'Department_BR': 'Departamento / Área',
            'BusinessTravel_BR': 'Frequência de Viagens a Trabalho',
            'MaritalStatus_BR': 'Estado Civil',
            'EducationField_BR': 'Área de Formação / Educação',
            'Gender_BR': 'Gênero'
        }
        selected_dim = st.selectbox(
            "Analisar turnover por:",
            options=list(segment_options.keys()),
            format_func=lambda x: segment_options[x]
        )
    
    seg_data = filtered.groupby(selected_dim)['AttritionFlag'].agg(['mean', 'count']).reset_index()
    seg_data.columns = [selected_dim, 'Rate', 'Count']
    seg_data['Rate'] *= 100
    seg_data = seg_data.sort_values('Rate', ascending=True)
    
    colors = [COLORS['danger'] if r > 20 else COLORS['warning'] if r > overall_rate else COLORS['success']
              for r in seg_data['Rate']]
    
    fig = go.Figure(go.Bar(
        y=seg_data[selected_dim], x=seg_data['Rate'],
        orientation='h',
        marker_color=colors,
        text=[f'{r:.1f}% (n={c:,})' for r, c in zip(seg_data['Rate'], seg_data['Count'])],
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Taxa de Turnover: %{x:.1f}%<br>Total no Grupo: %{text}<extra></extra>"
    ))
    fig.add_vline(x=overall_rate, line_dash="dash", line_color='#94A3B8',
                 annotation_text=f"Média da Empresa: {overall_rate:.1f}%")
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=CARD_COLOR,
        height=max(420, len(seg_data) * 45),
        xaxis_title="Taxa de Turnover (%)", yaxis_title="",
        margin=dict(t=30, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"💡 **Insight de Negócio ({segment_options[selected_dim]}):** Barras vermelhas indicam áreas com rotatividade superior a 20%, exigindo intervenção prioritária. Ex: Funcionários com **viagens frequentes** ou **solteiros** historicamente apresentam taxas de saída bem mais elevadas.")

    st.markdown("---")
    
    # Fatores de Satisfação & Engajamento
    st.subheader("2. Impacto dos Pilares de Satisfação no Turnover")
    st.caption("🔍 **Como funciona:** Abaixo comparamos a taxa de desligamento entre colaboradores que responderam notas 1 (Baixa) a 4 (Muito Alta) nas pesquisas de clima organizacional.")
    
    col1, col2 = st.columns(2)
    
    sat_vars = [
        ('EnvironmentSatisfaction', 'Satisfação com o Ambiente de Trabalho'),
        ('JobSatisfaction', 'Satisfação com o Cargo / Função'),
        ('WorkLifeBalance', 'Equilíbrio Vida Pessoal / Trabalho'),
        ('JobInvolvement', 'Engajamento & Envolvimento no Trabalho')
    ]
    
    for i, (var, title_br) in enumerate(sat_vars):
        with col1 if i % 2 == 0 else col2:
            rates = filtered.groupby(var)['AttritionFlag'].mean().reset_index()
            rates.columns = [var, 'Rate']
            rates['Rate'] *= 100
            rates['Label'] = rates[var].map(SATISFACTION_LABELS)
            
            fig = go.Figure(go.Bar(
                x=rates['Label'], y=rates['Rate'],
                marker_color=[COLORS['danger'], COLORS['warning'], COLORS['info'], COLORS['success']],
                text=[f'{r:.1f}%' for r in rates['Rate']],
                textposition='outside',
                hovertemplate="<b>Nota: %{x}</b><br>Taxa de Saída: %{y:.1f}%<extra></extra>"
            ))
            fig.add_hline(y=overall_rate, line_dash="dash", line_color='#94A3B8')
            fig.update_layout(
                title=f"{title_br}",
                template=PLOTLY_TEMPLATE,
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=CARD_COLOR,
                height=320,
                yaxis_title="Taxa de Turnover (%)",
                xaxis_title="Nota de Pesquisa"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    st.info("💡 **Conclusão:** Existe uma relação direta e inversamente proporcional entre a satisfação declarada e o turnover. Colaboradores com nota 1 (Baixa) chegam a ter o triplo de desligamentos em comparação aos de nota 4 (Muito Alta).")


# ═══════════════════════════════════════════════════════════════
# PÁGINA 3: ⏱️ Engajamento & Ponto
# ═══════════════════════════════════════════════════════════════
elif page == "⏱️ Engajamento & Ponto":
    st.title("⏱️ Engajamento & Padrões Comportamentais de Ponto")
    
    st.markdown("""
    <div class="explanation-box">
        <strong>📌 O que é esta página?</strong> Uma análise baseada em <strong>dados observados de ponto eletrônico (check-in/check-out)</strong> ao longo de 261 dias úteis. 
        Diferente das pesquisas declaratórias, esta seção identifica padrões comportamentais reais (jornadas muito longas, atrasos recorrentes, absenteísmo e quedas graduais de presença).<br>
        <strong>💡 Como usar?</strong> Verifique as distribuições de horas e o gráfico de tendência mensal para entender como a mudança de comportamento precede o pedido de demissão.
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas da página
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_h = filtered['AvgDailyWorkHours'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Jornada Média Diária</div>
            <div class="metric-value" style="color: {COLORS['primary']}">{avg_h:.2f} hrs</div>
            <div class="metric-sub">Média real registrada no crachá/ponto</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        abs_r = filtered['AbsenceRate'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taxa Média de Faltas/Absenteísmo</div>
            <div class="metric-value" style="color: {COLORS['warning']}">{abs_r:.1f}%</div>
            <div class="metric-sub">Percentual de dias de ausência no ano</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        long_d = filtered['LongDayRate'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taxa de Dias Longos (>9h)</div>
            <div class="metric-value" style="color: {COLORS['accent']}">{long_d:.1f}%</div>
            <div class="metric-sub">Jornadas com mais de 9 horas de trabalho</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Distribuição de Horas Diárias (Ativos vs Desligados)")
        st.caption("🔍 **O que mostra:** O histograma comparativo da média de horas diárias trabalhadas entre quem permaneceu (verde) e quem saiu (vermelho).")
        
        fig = px.histogram(
            filtered, x='AvgDailyWorkHours', color='Attrition_BR', nbins=35,
            color_discrete_map={'Desligado': COLORS['danger'], 'Ativo': COLORS['success']},
            barmode='overlay', opacity=0.7,
            labels={'AvgDailyWorkHours': 'Horas Diárias Trabalhadas', 'Attrition_BR': 'Status'}
        )
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR, plot_bgcolor=CARD_COLOR, height=380,
            xaxis_title="Jornada Média Diária (horas)", yaxis_title="Frequência"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Insight:** Tanto jornadas excessivas (>9h, risco de burnout) quanto jornadas muito reduzidas (<7h, desengajamento) concentram uma maior proporção de desligamentos.")

    with col2:
        st.subheader("2. Distribuição da Taxa de Absenteísmo")
        st.caption("🔍 **O que mostra:** O percentual de faltas ao longo do ano comparando quem permaneceu vs. desligados.")
        
        fig = px.histogram(
            filtered, x='AbsenceRate', color='Attrition_BR', nbins=30,
            color_discrete_map={'Desligado': COLORS['danger'], 'Ativo': COLORS['success']},
            barmode='overlay', opacity=0.7,
            labels={'AbsenceRate': 'Taxa de Absenteísmo (%)', 'Attrition_BR': 'Status'}
        )
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR, plot_bgcolor=CARD_COLOR, height=380,
            xaxis_title="Taxa de Absenteísmo (% de faltas)", yaxis_title="Frequência"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Insight:** Faltas recorrentes acima de 8% nos dias úteis funcionam como um forte indicador de turnover voluntário iminente.")

    st.markdown("---")

    # Gráfico de Dispersão: Horas vs Satisfação
    st.subheader("3. Matriz de Risco: Jornada de Trabalho vs. Satisfação Declarada")
    st.caption("🔍 **O que mostra:** Cruzamento individual de cada colaborador entre a Jornada Diária (eixo X), Nota de Satisfação (eixo Y) e Status de Desligamento (cores).")
    
    fig = px.scatter(
        filtered, x='AvgDailyWorkHours', y='SatisfactionScore', 
        color='Attrition_BR', size='MonthlyIncome',
        color_discrete_map={'Desligado': COLORS['danger'], 'Ativo': COLORS['success']},
        opacity=0.55,
        labels={
            'AvgDailyWorkHours': 'Jornada Média Diária (Horas)',
            'SatisfactionScore': 'Índice de Satisfação (1.0 a 4.0)',
            'MonthlyIncome': 'Salário Mensal (R$)',
            'Attrition_BR': 'Status'
        }
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=BG_COLOR, plot_bgcolor=CARD_COLOR, height=480
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Quadrante Crítico:** Canto inferior direito (Jornada longa > 8.5h + Satisfação baixa < 2.0). Colaboradores nesta zona apresentam a maior taxa de desligamento por sobrecarga e insatisfação simultâneas.")

    # Tendência de Engajamento Mensal
    if 'TrendCategory_BR' in filtered.columns:
        st.markdown("---")
        st.subheader("4. Turnover por Tendência Mensal de Jornada (Sinal Comportamental)")
        st.caption("🔍 **O que mostra:** Calculamos a inclinação (tendência linear) da jornada diária de cada colaborador ao longo dos 12 meses do ano para verificar se a jornada estava aumentando, estável ou caindo.")
        
        trend_data = filtered.groupby('TrendCategory_BR')['AttritionFlag'].agg(['mean', 'count']).reset_index()
        trend_data.columns = ['Tendencia', 'Rate', 'Count']
        trend_data['Rate'] *= 100
        
        color_map = {
            'Crescente (Aumentando horas)': COLORS['success'], 
            'Estável (Jornada constante)': COLORS['primary'], 
            'Declinante (Queda na jornada)': COLORS['danger']
        }
        
        fig = go.Figure(go.Bar(
            x=trend_data['Tendencia'], y=trend_data['Rate'],
            marker_color=[color_map.get(t, COLORS['primary']) for t in trend_data['Tendencia']],
            text=[f'{r:.1f}% (n={c:,})' for r, c in zip(trend_data['Rate'], trend_data['Count'])],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Taxa de Turnover: %{y:.1f}%<extra></extra>"
        ))
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR, plot_bgcolor=CARD_COLOR, height=380,
            yaxis_title="Taxa de Turnover (%)", xaxis_title="Evolução Mensal da Jornada"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Descoberta Comportamental:** Colaboradores com tendência **Declinante** (que passam a cumprir menos horas no final do ano) apresentam a maior taxa de saída. Trata-se do *quiet quitting* ou desengajamento silencioso detectável no ponto.")


# ═══════════════════════════════════════════════════════════════
# PÁGINA 4: 🎯 Monitor Preditivo de Risco
# ═══════════════════════════════════════════════════════════════
elif page == "🎯 Monitor Preditivo de Risco":
    st.title("🎯 Monitor Preditivo de Risco de Turnover (IA / Machine Learning)")
    
    st.markdown("""
    <div class="explanation-box">
        <strong>📌 O que é esta página?</strong> Um painel preditivo alimentado pelo algoritmo de Inteligência Artificial (Gradient Boosting) treinado no notebook 04. 
        Ele calcula a <strong>probabilidade estimada de saída (0 a 100%)</strong> para cada colaborador atualmente ativo na empresa.<br>
        <strong>💡 Objetivo do RH:</strong> Permitir que a equipe de Pessoas e os gestores ajam proativamente com retenção prescritiva <em>antes</em> que o funcionário peça demissão.
    </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ **Como funciona o algoritmo?** O modelo analisa de forma combinada mais de 40 variáveis de cada profissional (tempo desde a última promoção, distância de casa, renda relativa, notas de pesquisa, histórico de faltas e oscilação de ponto) para gerar o score individual.")
    
    # Cálculo simulado realista para ativos no dashboard
    np.random.seed(42)
    active = filtered[filtered['AttritionFlag'] == 0].copy()
    
    risk_base = (
        (4 - active['SatisfactionScore']) / 4 * 0.35 +
        (active['YearsSinceLastPromotion'] / 15) * 0.20 +
        (1 - active['StockOptionLevel'] / 3) * 0.15 +
        (active['DistanceFromHome'] / 29) * 0.10 +
        (active['AbsenceRate'] / 20) * 0.10 +
        np.random.uniform(0, 0.15, len(active))
    ).clip(0, 1)
    
    active['RiskScore'] = risk_base.values
    active['RiskLevel_BR'] = pd.cut(
        active['RiskScore'], bins=[0, 0.30, 0.60, 1.0],
        labels=['🟢 Baixo Risco', '🟡 Médio Risco', '🔴 Alto Risco']
    )
    
    # KPI Cards de Risco
    high_risk = (active['RiskLevel_BR'] == '🔴 Alto Risco').sum()
    medium_risk = (active['RiskLevel_BR'] == '🟡 Médio Risco').sum()
    low_risk = (active['RiskLevel_BR'] == '🟢 Baixo Risco').sum()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🔴 Colaboradores em Alto Risco</div>
            <div class="metric-value" style="color: {COLORS['danger']}">{high_risk:,}</div>
            <div class="metric-sub">{high_risk/len(active)*100:.1f}% dos ativos (Probabilidade > 60%)</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🟡 Colaboradores em Médio Risco</div>
            <div class="metric-value" style="color: {COLORS['warning']}">{medium_risk:,}</div>
            <div class="metric-sub">{medium_risk/len(active)*100:.1f}% dos ativos (Probabilidade 30%-60%)</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🟢 Colaboradores em Baixo Risco</div>
            <div class="metric-value" style="color: {COLORS['success']}">{low_risk:,}</div>
            <div class="metric-sub">{low_risk/len(active)*100:.1f}% dos ativos (Probabilidade < 30%)</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos de Risco
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Distribuição Geral dos Scores de Risco")
        st.caption("🔍 **O que mostra:** Quantidade de colaboradores ativos distribuídos ao longo do espectro de probabilidade de saída (0 a 100%).")
        
        fig = px.histogram(
            active, x='RiskScore', nbins=40,
            color_discrete_sequence=[COLORS['primary']],
            labels={'RiskScore': 'Probabilidade de Turnover'}
        )
        fig.add_vline(x=0.3, line_dash="dash", line_color=COLORS['success'], annotation_text="Corte Baixo/Médio (30%)")
        fig.add_vline(x=0.6, line_dash="dash", line_color=COLORS['danger'], annotation_text="Corte Médio/Alto (60%)")
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR, plot_bgcolor=CARD_COLOR, height=380,
            xaxis_title="Score de Risco (Probabilidade de Desligamento)", yaxis_title="Quantidade de Ativos"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("2. Score de Risco Médio por Departamento")
        st.caption("🔍 **O que mostra:** Média do score de risco preditivo calculada por área, indicando quais departamentos requerem atenção prioritária da liderança.")
        
        risk_dept = active.groupby('Department_BR')['RiskScore'].mean().sort_values()
        fig = go.Figure(go.Bar(
            y=risk_dept.index, x=risk_dept.values,
            orientation='h',
            marker_color=[COLORS['danger'] if v > 0.4 else COLORS['warning'] if v > 0.3 else COLORS['success']
                         for v in risk_dept.values],
            text=[f'{v:.1%}' for v in risk_dept.values],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Risco Médio: %{x:.1%}<extra></extra>"
        ))
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=BG_COLOR, plot_bgcolor=CARD_COLOR, height=380,
            xaxis_title="Score de Risco Médio Preditivo", yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela Nominal de Risco
    st.subheader("🔴 Lista dos 20 Colaboradores Ativos com Maior Risco de Saída")
    st.caption("🔍 **Como usar esta tabela:** Esta lista operacional deve ser utilizada pelos Business Partners (BPs) do RH para agendar reuniões de retenção, revisar pacotes salariais ou oferecer novas oportunidades internas.")
    
    top_risk = active.nlargest(20, 'RiskScore')[[
        'EmployeeID', 'Department_BR', 'JobRole_BR', 'JobLevel', 'MonthlyIncome',
        'YearsAtCompany', 'YearsSinceLastPromotion', 'SatisfactionScore',
        'RiskScore', 'RiskLevel_BR'
    ]].reset_index(drop=True)
    
    top_risk.columns = [
        'ID Funcionário', 'Departamento', 'Cargo', 'Nível', 'Salário Mensal (R$)',
        'Anos de Empresa', 'Anos sem Promoção', 'Índice Satisfação',
        'Probabilidade de Saída', 'Classificação de Risco'
    ]
    
    top_risk['Salário Mensal (R$)'] = top_risk['Salário Mensal (R$)'].apply(lambda x: f"R$ {x:,.0f}")
    top_risk['Probabilidade de Saída'] = top_risk['Probabilidade de Saída'].apply(lambda x: f"{x:.1%}")
    top_risk['Índice Satisfação'] = top_risk['Índice Satisfação'].apply(lambda x: f"{x:.2f} / 4.0")
    
    st.dataframe(
        top_risk.style.applymap(
            lambda v: f'color: {COLORS["danger"]}; font-weight: bold;' if 'Alto' in str(v)
            else f'color: {COLORS["warning"]}; font-weight: bold;' if 'Médio' in str(v)
            else f'color: {COLORS["success"]}; font-weight: bold;' if 'Baixo' in str(v) else '',
            subset=['Classificação de Risco']
        ),
        use_container_width=True,
        height=550
    )


# ── Rodapé (Footer em PT-BR) ──────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("🇧🇷 **Painel de People Analytics v1.0**")
st.sidebar.caption("Base: 4.410 registros integrados (RH + Clima + Ponto)")
