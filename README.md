# People Analytics — Workforce Intelligence Project

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Scikit--Learn-1.3-F7931E?logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/SHAP-0.44-purple" />
  <img src="https://img.shields.io/badge/Streamlit-1.61-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Dataset-Kaggle%20HR%20Analytics-20BEFF?logo=kaggle&logoColor=white" />
</p>

## 📋 Sobre o Projeto

Projeto end-to-end de **People Analytics e Inteligência de Dados de Pessoas**, desenvolvido utilizando o dataset público **HR Analytics Case Study** (disponível no Kaggle). A análise abrange um quadro de **4.410 colaboradores** ao longo do ano de 2015, combinando dados demográficos, pesquisas de clima organizacional, avaliação gerencial de desempenho e mais de **1,1 milhão de registros reais de ponto eletrônico (check-in / check-out)**.

O projeto simula um cenário corporativo real do setor industrial, demonstrando a aplicação do ciclo completo de ciência de dados em Recursos Humanos: desde a estruturação de pipelines de ETL até a modelagem preditiva com inteligência artificial e a construção de um dashboard executivo interativo em Streamlit.

---

## 🎯 Objetivos de Negócio

Com uma **taxa de turnover (atrito) de 16,1%**, a empresa enfrenta perda recorrente de talentos, gerando custos expressivos de substituição e impactando a continuidade operacional. O projeto responde a quatro perguntas estratégicas:

1. **Diagnóstico**: Quais segmentos (cargos, áreas, perfis) possuem maior rotatividade e quais são os fatores determinantes?
2. **Engajamento Observado**: Como o comportamento real de jornada e pontualidade (registros de ponto) difere entre colaboradores retidos e aqueles que pedem demissão?
3. **Predição**: É possível prever a probabilidade de desligamento de cada colaborador ativo antes que ele peça demissão?
4. **Impacto Financeiro**: Qual é o custo estimado do turnover e qual o ROI de programas preventivos de retenção?

---

## 🔍 Principais Achados & Insights de Negócio

- **Custo do Turnover**: Calculado com base em multiplicadores do setor industrial (50% a 200% do salário anual por nível hierárquico). O atrito atual representa milhões em substituição e perda de conhecimento.
- **Principais Drivers de Saída**: Viagens a trabalho frequentes, posições operacionais de Nível 1, colaboradores solteiros e profissionais com estagnação de promoção (5+ anos sem progressão).
- **Sinal Comportamental no Ponto**: A análise temporal dos registros de ponto revelou que colaboradores que vieram a se desligar apresentavam uma **tendência declinante na jornada mensal** (queda progressiva nas horas cumpridas por dia) nos meses anteriores à rescisão — um indicador observável de *quiet quitting*.
- **Modelagem Preditiva**: Algoritmo preditivo de Machine Learning (Gradient Boosting com tratamento de desbalanceamento via SMOTE) alcançou elevada capacidade de separação (AUC-ROC), ranqueando os funcionários ativos em faixas de risco (🟢 Baixo, 🟡 Médio, 🔴 Alto).
- **Explicabilidade via SHAP**: Cada previsão de risco do modelo é acompanhada de explicações transparentes mostrando os principais fatores individuais que influenciaram a pontuação.
- **ROI de Retenção**: Ações preventivas focadas no grupo de alto risco com taxa de sucesso de 30% geram um retorno estimado de **2x a 3x o valor investido**.

---

## 📁 Estrutura do Repositório

```
People Analytics/
├── README.md                               # Documentação principal do projeto
├── requirements.txt                        # Dependências Python
├── .gitignore                              # Regras de exclusão do Git
├── data/
│   ├── raw/                                # Datasets originais do Kaggle (HR Analytics Case Study)
│   │   ├── general_data.csv                # Dados demográficos, cargo, salário, tempo de casa
│   │   ├── employee_survey_data.csv        # Pesquisa de clima (ambiente, cargo, work-life)
│   │   ├── manager_survey_data.csv         # Avaliação gerencial de desempenho e envolvimento
│   │   ├── in_time.csv                     # Registros diários de entrada (261 dias úteis)
│   │   ├── out_time.csv                    # Registros diários de saída (261 dias úteis)
│   │   └── data_dictionary.xlsx            # Dicionário de dados original
│   └── processed/
│       ├── master_dataset.csv              # Dataset mestre integrado (4.410 x 51 features)
│       └── daily_events.csv                # Base de eventos de ponto processada
├── notebooks/
│   ├── 00_data_preparation.ipynb           # Pipeline ETL, merge de 5 fontes e engenharia de features
│   ├── 01_workforce_profiling.ipynb        # EDA completo, perfil demográfico, salarial e equidade de gênero
│   ├── 02_turnover_deep_dive.ipynb         # Diagnóstico profundo de atrito, drivers e custo financeiro
│   ├── 03_engagement_attendance.ipynb      # Análise comportamental de jornada, absenteísmo e tendência
│   └── 04_predictive_attrition_model.ipynb # Modelagem preditiva (Logística, RF, GB) + SHAP + Risk Scoring
├── dashboard/
│   └── app.py                              # Dashboard executivo interativo em Streamlit (4 páginas em PT-BR)
└── reports/
    ├── executive_report.md                 # Relatório executivo completo para a Diretoria/Board
    └── *.png                               # 27 visualizações executivas geradas em alta resolução
```

---

## 🛠️ Tecnologias & Bibliotecas Utilizadas

| Categoria | Tecnologias |
|-----------|-------------|
| **Linguagem & Manipulação** | Python 3.11, Pandas, NumPy, OpenPyXL |
| **Visualização de Dados** | Matplotlib, Seaborn, Plotly Express & Graph Objects |
| **Machine Learning & IA** | Scikit-learn, Gradient Boosting, Random Forest, SMOTE (imbalanced-learn) |
| **Explicabilidade de IA** | SHAP (SHapley Additive exPlanations) |
| **Dashboard Executivo** | Streamlit |
| **Análise Estatística** | SciPy (Regressão linear para detecção de tendência temporal) |

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o repositório e instalar dependências
```bash
git clone <URL_DO_REPOSITORIO>
cd "People Analytics"
pip install -r requirements.txt
```

### 2. Rodar os Notebooks de Análise (Jupyter)
```bash
jupyter notebook notebooks/
```

### 3. Iniciar o Dashboard Executivo Interativo (Streamlit)
```bash
streamlit run dashboard/app.py
```
O dashboard abrirá automaticamente no seu navegador padrão no endereço `http://localhost:8501`.

---

## 🖥️ Telas do Dashboard Streamlit

O aplicativo em `dashboard/app.py` é 100% interativo e estruturado em 4 páginas:

1. **🏠 Visão Geral**: KPIs executivos (Headcount, Turnover, Salário Média, Satisfação), distribuições organizacionais e análise salarial.
2. **📉 Análise de Turnover**: Filtros dinâmicos por cargo, área, viagens, estado civil e formação, além do impacto das notas de clima no atrito.
3. **⏱️ Engajamento & Ponto**: Histogramas de jornada diária, curva de faltas, matriz de risco (jornada x satisfação) e indicador comportamental de tendência.
4. **🎯 Monitor Preditivo de Risco**: Ranqueamento de colaboradores ativos em faixas de risco (🟢 Baixo, 🟡 Médio, 🔴 Alto) com tabela interativa detalhada.

---

## 📊 Origem dos Dados

Os dados utilizados neste estudo são provenientes do dataset público **[HR Analytics Case Study](https://www.kaggle.com/datasets/vjchoudhary7/hr-analytics-case-study)** hospedado no Kaggle. Todos os nomes, identificadores e métricas foram consolidados e enriquecidos para fins de demonstração técnica e analítica de People Analytics.
