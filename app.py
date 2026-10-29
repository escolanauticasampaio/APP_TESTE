import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, time, timedelta, date
import base64
import urllib.parse
import io
import os

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Stúdio de Pilates e Fisioterapia Ítalo e Letícia Sampaio",
    page_icon="",
    layout="wide"
)

# ==============================================================================
# FUNÇÃO PARA CONVERTER IMAGEM DE FUNDO EM BASE64 (PARA O CSS)
# ==============================================================================
def obter_fundo_base64(caminho_imagem):
    if os.path.exists(caminho_imagem):
        with open(caminho_imagem, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

img_bg_base64 = obter_fundo_base64("fundo_studio.jpg")

# ==============================================================================
# ESTILIZAÇÃO CSS CUSTOMIZADA (MENUS MAIORES, TEXTOS VIVOS E SIDEBAR REFINADA)
# ==============================================================================
if img_bg_base64:
    css_fundo = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(244, 247, 245, 0.50), rgba(244, 247, 245, 0.50)), url("data:image/jpeg;base64,{img_bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* Estilização Destacada e Arredondada da Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {{
        background-color: rgba(240, 245, 242, 0.92) !important;
        backdrop-filter: blur(12px);
        border-right: 2px solid rgba(45, 106, 79, 0.2) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.05);
    }}
    
    /* Cantos Arredondados e Estilo dos Blocos na Sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        padding: 20px 15px;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: #05150E !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] .stTextInput input, 
    [data-testid="stSidebar"] .stSelectbox select, 
    [data-testid="stSidebar"] .stNumberInput input {{
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #a3b18a !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }}
    
    /* Cabeçalho Principal com Gradiente Premium */
    .header-container {{
        background: linear-gradient(135deg, #0F291E 0%, #1b4332 50%, #2d6a4f 100%);
        padding: 32px 40px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 12px 30px rgba(15, 41, 30, 0.25);
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .main-title {{
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        margin: 0 !important;
    }}
    .sub-title {{
        font-size: 1.15rem !important;
        color: #d8f3dc !important;
        margin-top: 10px !important;
        font-weight: 400;
        opacity: 0.9;
    }}

    /* Cartões de Métricas (KPIs) Modernizados */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 6px 20px rgba(15, 41, 30, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-left: 6px solid #2d6a4f;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(15, 41, 30, 0.12);
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 1rem !important;
        color: #1b4332 !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem !important;
        color: #05150E !important;
        font-weight: 800 !important;
    }}

    /* Abas Superiores Estilizadas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background-color: transparent;
        padding-bottom: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 14px;
        padding: 14px 26px;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(8px);
        color: #05150E !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 1px solid #b7e4c7;
        box-shadow: 0 3px 8px rgba(0,0,0,0.06);
        transition: all 0.2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #d8f3dc !important;
        color: #05150E !important;
        transform: translateY(-1px);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #0F291E !important;
        color: #ffffff !important;
        border-color: #0F291E !important;
        box-shadow: 0 6px 16px rgba(15, 41, 30, 0.3) !important;
    }}
    .stTabs [aria-selected="true"] p {{
        color: #ffffff !important;
    }}
    .stTabs p {{
        color: #05150E !important;
        font-weight: 700 !important;
    }}

    /* Botões Padrão Arredondados e Elegantes */
    div.stButton > button {{
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px 22px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }}
    div.stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.12);
    }}

    /* Inputs, Selects e Textareas Arredondados com Preto Vivo */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {{
        border-radius: 12px !important;
        border: 1px solid #a3b18a !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }}
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {{
        border-color: #2d6a4f !important;
        box-shadow: 0 0 0 2px rgba(45, 106, 79, 0.2) !important;
    }}

    /* Containers, Títulos e Expanders */
    h1, h2, h3, h4 {{
        color: #05150E !important;
        font-weight: 700 !important;
    }}
    .streamlit-expanderHeader {{
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 14px;
        border: 1px solid #cbd5e1;
        color: #05150E !important;
        font-weight: 700 !important;
    }}
    
    /* Tabelas e Dataframes com Leitura Nítida */
    [data-testid="stDataFrame"] {{
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        background-color: rgba(255, 255, 255, 0.95);
    }}
    </style>
    """
else:
    css_fundo = """
    <style>
    .stApp {
        background-color: #f4f7f5;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    </style>
    """

st.markdown(css_fundo, unsafe_allow_html=True)

# ==============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLite)
# ==============================================================================
def conectar_bd():
    conn = sqlite3.connect("clientes_studio_v2.db", check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            email TEXT,
            data_nascimento TEXT,
            idade INTEGER,
            endereco TEXT,
            telefone TEXT,
            contato_emergencia TEXT,
            objetivo TEXT,
            plano TEXT,
            dias_semana TEXT,
            horarios TEXT
        )
    ''')
    
    cursor.execute("PRAGMA table_info(clientes)")
    colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]
    for col, tipo in {"email": "TEXT", "data_nascimento": "TEXT", "contato_emergencia": "TEXT"}.items():
        if col not in colunas_existentes:
            cursor.execute(f"ALTER TABLE clientes ADD COLUMN {col} {tipo}")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_prof TEXT NOT NULL,
            conselho TEXT NOT NULL,
            registro TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prontuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf_cliente TEXT NOT NULL,
            data_atendimento TEXT NOT NULL,
            profissional TEXT NOT NULL,
            atividades TEXT NOT NULL,
            evolucao TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas_laudos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf_cliente TEXT NOT NULL,
            data_recebimento TEXT NOT NULL,
            titulo TEXT NOT NULL,
            origem TEXT NOT NULL,
            descricao_conteudo TEXT,
            nome_arquivo TEXT,
            arquivo_bin BLOB
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financeiro_mensalidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf_cliente TEXT NOT NULL,
            mes_referencia TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL,
            data_pagamento TEXT
        )
    ''')
    
    conn.commit()
    return conn

conn = conectar_bd()

def adicionar_cliente(cpf, nome, email, data_nasc, idade, endereco, telefone, contato_emergencia, objetivo, plano, dias_semana, horarios):
    cursor = conn.cursor()
    dias_str = ", ".join(dias_semana)
    horarios_str = ", ".join(horarios)
    
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE cpf = ?", (cpf,))
    existe = cursor.fetchone()[0] > 0
    
    if existe:
        return False, "⚠️ Já existe um cliente cadastrado com este CPF!"
    
    try:
        cursor.execute('''
            INSERT INTO clientes (cpf, nome, email, data_nascimento, idade, endereco, telefone, contato_emergencia, objetivo, plano, dias_semana, horarios)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, email, data_nasc, idade, endereco, telefone, contato_emergencia, objetivo, plano, dias_str, horarios_str))
        conn.commit()
        return True, "🎉 Cadastro realizado com Sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Já existe um cliente cadastrado com este CPF!"

def atualizar_cliente(cpf_antigo, nome, email, data_nasc, idade, endereco, telefone, contato_emergencia, objetivo, plano, dias_semana, horarios):
    cursor = conn.cursor()
    dias_str = ", ".join(dias_semana)
    horarios_str = ", ".join(horarios)
    cursor.execute('''
        UPDATE clientes 
        SET nome = ?, email = ?, data_nascimento = ?, idade = ?, endereco = ?, telefone = ?, contato_emergencia = ?, objetivo = ?, plano = ?, dias_semana = ?, horarios = ?
        WHERE cpf = ?
    ''', (nome, email, data_nasc, idade, endereco, telefone, contato_emergencia, objetivo, plano, dias_str, horarios_str, cpf_antigo))
    conn.commit()
    return True, "Cliente atualizado com sucesso!"

def deletar_cliente(cpf):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
    cursor.execute("DELETE FROM receitas_laudos WHERE cpf_cliente = ?", (cpf,))
    cursor.execute("DELETE FROM prontuarios WHERE cpf_cliente = ?", (cpf,))
    cursor.execute("DELETE FROM financeiro_mensalidades WHERE cpf_cliente = ?", (cpf,))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='clientes'")
        conn.commit()

def limpa_todos_clientes():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes")
    cursor.execute("DELETE FROM receitas_laudos")
    cursor.execute("DELETE FROM prontuarios")
    cursor.execute("DELETE FROM financeiro_mensalidades")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='clientes'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='receitas_laudos'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='prontuarios'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='financeiro_mensalidades'")
    conn.commit()

def carregar_clientes():
    return pd.read_sql_query("SELECT * FROM clientes", conn)

def adicionar_profissional(nome, conselho, registro):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO profissionais (nome_prof, conselho, registro)
        VALUES (?, ?, ?)
    ''', (nome, conselho, registro))
    conn.commit()

def atualizar_profissional(prof_id, nome, conselho, registro):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE profissionais 
        SET nome_prof = ?, conselho = ?, registro = ?
        WHERE id = ?
    ''', (nome, conselho, registro, prof_id))
    conn.commit()

def deletar_profissional(prof_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profissionais WHERE id = ?", (prof_id,))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM profissionais")
    if cursor.fetchone()[0] == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='profissionais'")
        conn.commit()

def carregar_profissionais():
    return pd.read_sql_query("SELECT * FROM profissionais", conn)

def adicionar_prontuario(cpf, data_hora, profissional, atividades, evolucao):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prontuarios (cpf_cliente, data_atendimento, profissional, atividades, evolucao)
        VALUES (?, ?, ?, ?, ?)
    ''', (cpf, data_hora, profissional, atividades, evolucao))
    conn.commit()

def atualizar_prontuario(prontuario_id, atividades, evolucao):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE prontuarios 
        SET atividades = ?, evolucao = ?
        WHERE id = ?
    ''', (atividades, evolucao, prontuario_id))
    conn.commit()

def deletar_prontuario(prontuario_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prontuarios WHERE id = ?", (prontuario_id,))
    conn.commit()

def carregar_prontuarios(cpf=""):
    if cpf:
        return pd.read_sql_query("SELECT * FROM prontuarios WHERE cpf_cliente = ?", conn, params=(cpf,))
    return pd.read_sql_query("SELECT * FROM prontuarios", conn)

def adicionar_receita_laudo(cpf, data_hora, titulo, origem, descricao, nome_arq, bin_arq):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO receitas_laudos (cpf_cliente, data_recebimento, titulo, origem, descricao_conteudo, nome_arquivo, arquivo_bin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (cpf, data_hora, titulo, origem, descricao, nome_arq, bin_arq))
    conn.commit()

def deletar_receita_laudo(doc_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receitas_laudos WHERE id = ?", (doc_id,))
    conn.commit()

def carregar_receitas_laudos(cpf=""):
    if cpf:
        return pd.read_sql_query("SELECT * FROM receitas_laudos WHERE cpf_cliente = ?", conn, params=(cpf,))
    return pd.read_sql_query("SELECT * FROM receitas_laudos", conn)

def carregar_financeiro(mes=""):
    if mes:
        return pd.read_sql_query("SELECT * FROM financeiro_mensalidades WHERE mes_referencia = ?", conn, params=(mes,))
    return pd.read_sql_query("SELECT * FROM financeiro_mensalidades", conn)

def salvar_status_mensalidade(cpf, mes, valor, status, data_pgto):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM financeiro_mensalidades WHERE cpf_cliente = ? AND mes_referencia = ?", (cpf, mes))
    res = cursor.fetchone()
    if res:
        cursor.execute("UPDATE financeiro_mensalidades SET valor = ?, status = ?, data_pagamento = ? WHERE id = ?", (valor, status, data_pgto, res[0]))
    else:
        cursor.execute("INSERT INTO financeiro_mensalidades (cpf_cliente, mes_referencia, valor, status, data_pagamento) VALUES (?, ?, ?, ?, ?)", (cpf, mes, valor, status, data_pgto))
    conn.commit()

def gerar_dataframe_financeiro_completo(mes_referencia="Outubro/2026", precos_dict=None):
    if precos_dict is None:
        precos_dict = {
            "Plano 1x por semana": 250.0,
            "Plano 2x por semana": 380.0,
            "Plano 3x por semana": 480.0,
            "Plano Ilimitado": 650.0
        }
    
    df_cli = carregar_clientes()
    if df_cli.empty:
        return pd.DataFrame(columns=["CPF", "Nome", "Plano", "Mês Referência", "Valor (R$)", "Status", "Data Pagamento / Alerta"])

    df_fin_banco = carregar_financeiro(mes_referencia)
    
    linhas_fin = []
    for _, cli in df_cli.iterrows():
        cpf_c = cli['cpf']
        nome_c = cli['nome']
        plano_c = cli['plano']
        valor_padrao = precos_dict.get(plano_c, 300.0)
        
        reg_existente = df_fin_banco[df_fin_banco['cpf_cliente'] == cpf_c]
        if not reg_existente.empty:
            status = reg_existente.iloc[0]['status']
            valor = reg_existente.iloc[0]['valor']
            dt_pgto = reg_existente.iloc[0]['data_pagamento'] or ""
        else:
            status = "Pendente"
            valor = valor_padrao
            dt_pgto = ""
            
        if status in ["Pendente", "Atrasado"]:
            data_ou_alerta = f"⚠️ {status.upper()} - AGUARDANDO PAGAMENTO"
        elif status == "Isento":
            data_ou_alerta = "ℹ️ ISENTO"
        else:
            data_ou_alerta = f"✅ PAGO em {dt_pgto}" if dt_pgto and dt_pgto != "-" else "✅ PAGO"

        linhas_fin.append({
            "CPF": cpf_c,
            "Nome": nome_c,
            "Plano": plano_c,
            "Mês Referência": mes_referencia,
            "Valor (R$)": valor,
            "Status": status,
            "Data Pagamento / Alerta": data_ou_alerta
        })
        
    return pd.DataFrame(linhas_fin)

def gerar_excel_geral():
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        carregar_clientes().to_excel(writer, sheet_name="Clientes", index=False)
        carregar_profissionais().to_excel(writer, sheet_name="Profissionais", index=False)
        carregar_prontuarios().to_excel(writer, sheet_name="Prontuarios", index=False)
        
        df_laudos = carregar_receitas_laudos()
        if 'arquivo_bin' in df_laudos.columns:
            df_laudos = df_laudos.drop(columns=['arquivo_bin'])
        df_laudos.to_excel(writer, sheet_name="Laudos_Receitas", index=False)
        
        df_fin_export = gerar_dataframe_financeiro_completo("Outubro/2026")
        df_fin_export.to_excel(writer, sheet_name="Financeiro", index=False)
        
    buffer.seek(0)
    return buffer

def formatar_cpf(texto):
    nums = "".join(filter(str.isdigit, texto))[:11]
    if len(nums) == 11:
        return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"
    return texto.upper()

def formatar_telefone(texto):
    nums = "".join(filter(str.isdigit, texto))[:11]
    if len(nums) == 11:
        return f"({nums[:2]}) {nums[2:7]}-{nums[7:]}"
    elif len(nums) == 10:
        return f"({nums[:2]}) {nums[2:6]}-{nums[6:]}"
    return texto.upper()

def formatar_data(texto):
    nums = "".join(filter(str.isdigit, texto))[:8]
    if len(nums) == 8:
        return f"{nums[:2]}/{nums[2:4]}/{nums[4:]}"
    return texto.upper()

# ==============================================================================
# CABEÇALHO PERSONALIZADO E BOTÃO DE BACKUP EXCEL
# ==============================================================================
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Stúdio de Pilates e Fisioterapia Ítalo e Letícia Sampaio</h1>
        <p class="sub-title">Painel Integrado: Financeiro Avançado, Agenda Visual, Clientes, Laudos e Prontuários</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("💾 Backup do Banco de Dados")
excel_data = gerar_excel_geral()
st.sidebar.download_button(
    label="📊 Baixar Banco Completo (.xlsx)",
    data=excel_data,
    file_name=f"backup_studio_sampaio_{datetime.now().strftime('%Y_%m_%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

aba_financeiro, aba_novo_cadastro, aba_clientes_cadastrados, aba_mapa, aba_profissionais, aba_prontuario = st.tabs([
    "📊 Painel Financeiro & Mensalidades", 
    "➕ Novo Cadastro & Agendamento", 
    "👥 Clientes Cadastrados", 
    "🧩 Mapa de Ocupação",
    "👩‍⚕️ Profissionais", 
    "📝 Prontuário & Laudos"
])

# ==============================================================================
# ABA 1: PAINEL FINANCEIRO & CONTROLE DE MENSALIDADES
# ==============================================================================
with aba_financeiro:
    st.header("📊 Painel Financeiro e Controle de Mensalidades")
    st.caption("Ajuste os parâmetros na barra lateral e gerencie os pagamentos mensais dos alunos.")

    st.sidebar.header("⚙️ Parâmetros do Estúdio")
    st.sidebar.subheader("1. Estrutura e Capacidade")
    vagas_por_turma = st.sidebar.number_input("Alunos/Vagas por Turma", min_value=1, max_value=10, value=5, key="vagas_sidebar")
    horas_por_dia = st.sidebar.number_input("Horas de Aula por Dia", min_value=1, max_value=18, value=8)
    dias_por_semana = st.sidebar.number_input("Dias de Funcionamento/Semana", min_value=1, max_value=7, value=5)

    st.sidebar.subheader("2. Custos e Remuneração de Professores")
    comissao_prof_hora = st.sidebar.number_input("Comissão do Professor (R$/hora)", min_value=0.0, value=40.0, step=5.0)
    custos_fixos = st.sidebar.number_input("Custos Fixos Mensais (R$)", min_value=0.0, value=5000.0, step=500.0)
    imposto_pct = st.sidebar.slider("Imposto / Simples Nacional (%)", min_value=0.0, max_value=20.0, value=6.0) / 100

    st.sidebar.subheader("3. Preços dos Planos (Mensalidade)")
    preco_1x = st.sidebar.number_input("Plano 1x por semana (R$)", value=200.0, step=10.0)
    preco_2x = st.sidebar.number_input("Plano 2x por semana (R$)", value=380.0, step=10.0)
    preco_3x = st.sidebar.number_input("Plano 3x por semana (R$)", value=480.0, step=10.0)
    preco_ilimitado = st.sidebar.number_input("Plano Ilimitado (R$)", value=650.0, step=10.0)

    tabela_precos = {
        "Plano 1x por semana": preco_1x,
        "Plano 2x por semana": preco_2x,
        "Plano 3x por semana": preco_3x,
        "Plano Ilimitado": preco_ilimitado
    }

    # CÁLCULOS DOS CARDS SUPERIORES (Capacidade Máxima / Parâmetros da Sidebar)
    aulas_semanais = horas_por_dia * dias_por_semana
    aulas_mensais = aulas_semanais * 4.33
    capacidade_slots_semanais = aulas_semanais * vagas_por_turma
    custo_professores_projecao = aulas_mensais * comissao_prof_hora

    cenarios = [
        {"Nome": "1. Baixa Ocupação (~30%)", "Alunos_1x": int(capacidade_slots_semanais * 0.1), "Alunos_2x": int(capacidade_slots_semanais * 0.15), "Alunos_3x": int(capacidade_slots_semanais * 0.05)},
        {"Nome": "2. Ponto de Equilíbrio (~55%)", "Alunos_1x": int(capacidade_slots_semanais * 0.15), "Alunos_2x": int(capacidade_slots_semanais * 0.25), "Alunos_3x": int(capacidade_slots_semanais * 0.15)},
        {"Nome": "3. Alta Ocupação (~85%)", "Alunos_1x": int(capacidade_slots_semanais * 0.2), "Alunos_2x": int(capacidade_slots_semanais * 0.4), "Alunos_3x": int(capacidade_slots_semanais * 0.25)},
        {"Nome": "4. Capacidade Máxima (100%)", "Alunos_1x": int(capacidade_slots_semanais * 0.2), "Alunos_2x": int(capacidade_slots_semanais * 0.5), "Alunos_3x": int(capacidade_slots_semanais * 0.3)}
    ]

    dados_resultados = []
    for c in cenarios:
        total_alunos = c["Alunos_1x"] + c["Alunos_2x"] + c["Alunos_3x"]
        slots_ocupados = (c["Alunos_1x"] * 1) + (c["Alunos_2x"] * 2) + (c["Alunos_3x"] * 3)
        taxa_ocupacao = (slots_ocupados / capacidade_slots_semanais) * 100 if capacidade_slots_semanais > 0 else 0
        fat_bruto = (c["Alunos_1x"] * preco_1x) + (c["Alunos_2x"] * preco_2x) + (c["Alunos_3x"] * preco_3x)
        impostos = fat_bruto * imposto_pct
        custo_total = custos_fixos + impostos + custo_professores_projecao
        lucro_liquido = fat_bruto - custo_total
        
        dados_resultados.append({
            "Cenário": c["Nome"],
            "Total Alunos": total_alunos,
            "Ocupação (%)": round(taxa_ocupacao, 1),
            "Faturamento Bruto": fat_bruto,
            "Impostos": impostos,
            "Custo Fixos": custos_fixos,
            "Comissão Professores": custo_professores_projecao,
            "Custo Total": custo_total,
            "Lucro Líquido": lucro_liquido,
            "Margem Líquida (%)": round((lucro_liquido / fat_bruto * 100) if fat_bruto > 0 else 0, 1)
        })

    df = pd.DataFrame(dados_resultados)

    # Display Cards Superiores (Projeção do Estúdio)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Capacidade Máxima", f"{capacidade_slots_semanais} vagas/sem")
    m2.metric("Custo com Professor", f"R$ {custo_professores_projecao:,.2f}")
    m3.metric("Faturamento Máximo", f"R$ {df.iloc[-1]['Faturamento Bruto']:,.2f}")
    m4.metric("Lucro Líquido Máximo", f"R$ {df.iloc[-1]['Lucro Líquido']:,.2f}", delta=f"{df.iloc[-1]['Margem Líquida (%)']}% Margem")

    st.divider()
    
    sub_aba_fin_resumo, sub_aba_fin_controle = st.tabs(["📈 Resumo e Projeções", "💳 Controle de Mensalidades dos Alunos"])

    with sub_aba_fin_resumo:
        st.subheader("💰 Faturamento Baseado nos Clientes Cadastrados")
        df_cadastrados_fin = carregar_clientes()
        
        if not df_cadastrados_fin.empty:
            total_cadastrados = len(df_cadastrados_fin)
            
            # Cálculo do Faturamento Bruto Real baseado nos planos cadastrados
            contagem_planos = df_cadastrados_fin['plano'].value_counts()
            q_1x = contagem_planos.get("Plano 1x por semana", 0)
            q_2x = contagem_planos.get("Plano 2x por semana", 0)
            q_3x = contagem_planos.get("Plano 3x por semana", 0)
            q_ilimitado = contagem_planos.get("Plano Ilimitado", 0)
            
            faturamento_real = (q_1x * preco_1x) + (q_2x * preco_2x) + (q_3x * preco_3x) + (q_ilimitado * preco_ilimitado)
            impostos_reais = faturamento_real * imposto_pct
            
            # CÁLCULO CORRIGIDO: Agrupa por slots únicos (dia e horário) para evitar duplicidade de horas de professor na mesma turma
            slots_unicos = set()
            for _, row_cli in df_cadastrados_fin.iterrows():
                dias = [d.strip() for d in str(row_cli.get('dias_semana', '')).split(',') if d.strip()]
                horarios = [h.strip() for h in str(row_cli.get('horarios', '')).split(',') if h.strip()]
                for d in dias:
                    for h in horarios:
                        slots_unicos.add((d, h))
            
            total_horas_semanais_reais = len(slots_unicos) if len(slots_unicos) > 0 else 0
            horas_prof_mes_real = total_horas_semanais_reais * 4.33
            custo_professores_real = horas_prof_mes_real * comissao_prof_hora
            
            lucro_real = faturamento_real - (custos_fixos + impostos_reais + custo_professores_real)

            # Display Cards Inferiores (Situação Real)
            r1, r2, r3, r4, r5 = st.columns(5)
            r1.metric("Total de Alunos", f"{total_cadastrados} alunos")
            r2.metric("Faturamento Bruto Real", f"R$ {faturamento_real:,.2f}")
            r3.metric("Impostos Reais", f"R$ {impostos_reais:,.2f}")
            r4.metric("Custo Prof. (Mão de Obra)", f"R$ {custo_professores_real:,.2f}")
            r5.metric("Lucro Líquido Real", f"R$ {lucro_real:,.2f}")
        else:
            st.info("Nenhum cliente cadastrado no momento.")

        st.markdown("---")
        st.subheader("📊 Tabela Comparativa de Cenários de Ocupação")
        st.dataframe(df, hide_index=True, use_container_width=True)

    with sub_aba_fin_controle:
        st.subheader("💳 Gestão de Mensalidades e Status de Pagamento")
        
        meses_ano = [
            "Janeiro/2026", "Fevereiro/2026", "Março/2026", "Abril/2026", 
            "Maio/2026", "Junho/2026", "Julho/2026", "Agosto/2026", 
            "Setembro/2026", "Outubro/2026", "Novembro/2026", "Dezembro/2026"
        ]
        
        mes_selecionado = st.selectbox("Selecione o Mês de Referência", meses_ano, index=datetime.today().month - 1)
        
        df_mensalidades_exib = gerar_dataframe_financeiro_completo(mes_selecionado, tabela_precos)
        
        if not df_mensalidades_exib.empty:
            total_recebido = df_mensalidades_exib[df_mensalidades_exib['Status'] == 'Pago']['Valor (R$)'].sum()
            total_pendente = df_mensalidades_exib[df_mensalidades_exib['Status'] == 'Pendente']['Valor (R$)'].sum()
            
            f1, f2, f3 = st.columns(3)
            f1.metric(f"Recebido em {mes_selecionado}", f"R$ {total_recebido:,.2f}", f"{len(df_mensalidades_exib[df_mensalidades_exib['Status'] == 'Pago'])} pagos")
            f2.metric(f"Pendente em {mes_selecionado}", f"R$ {total_pendente:,.2f}", f"{len(df_mensalidades_exib[df_mensalidades_exib['Status'] == 'Pendente'])} pendentes", delta_color="inverse")
            f3.metric("Total Previsto", f"R$ {total_recebido + total_pendente:,.2f}")
            
            st.markdown("---")
            st.markdown("### ✏️ Atualizar Status de Pagamento Individual")
            
            lista_cli_fin_sel = ["-- Selecione um Aluno --"] + [f"{row['Nome']} (CPF: {row['CPF']})" for _, row in df_mensalidades_exib.iterrows()]
            escolha_cli_fin = st.selectbox("Selecione o Aluno para Baixa / Atualização", lista_cli_fin_sel, key="sel_cli_pagamento")
            
            if escolha_cli_fin == "-- Selecione um Aluno --":
                st.info("👈 Por favor, selecione um aluno acima para gerenciar ou atualizar o status de pagamento.")
            else:
                cpf_escolhido_fin = escolha_cli_fin.split("CPF: ")[1].split(")")[0]
                aluno_info = df_mensalidades_exib[df_mensalidades_exib['CPF'] == cpf_escolhido_fin].iloc[0]
                
                df_banco_ind = carregar_financeiro(mes_selecionado)
                reg_ind = df_banco_ind[df_banco_ind['cpf_cliente'] == cpf_escolhido_fin]
                
                dt_salva_atual = ""
                if not reg_ind.empty:
                    val_banco = reg_ind.iloc[0]['data_pagamento']
                    if pd.notna(val_banco) and val_banco not in ["-", ""]:
                        dt_salva_atual = str(val_banco).replace("-", "").strip()
                
                if not dt_salva_atual:
                    dt_salva_atual = datetime.today().strftime("%d/%m/%Y")
                
                with st.form("form_atualizar_pagamento"):
                    st.markdown(f"**Aluno:** {aluno_info['Nome']} | **Plano:** {aluno_info['Plano']}")
                    
                    col_p1, col_p2, col_p3 = st.columns(3)
                    with col_p1:
                        novo_valor_pagamento = st.number_input("Valor da Mensalidade (R$)", value=float(aluno_info['Valor (R$)']), step=10.0)
                    with col_p2:
                        status_opcoes = ["Pendente", "Pago", "Atrasado", "Isento"]
                        idx_status = status_opcoes.index(aluno_info['Status']) if aluno_info['Status'] in status_opcoes else 0
                        novo_status_pagamento = st.selectbox("Status", status_opcoes, index=idx_status)
                    with col_p3:
                        raw_input_dt = st.text_input("Data do Pagamento (DD/MM/AAAA)", value=dt_salva_atual)
                        data_pgto_input = formatar_data(raw_input_dt)
                    
                    btn_salvar_pgto = st.form_submit_button("💾 Salvar Alteração de Pagamento", type="primary")
                    if btn_salvar_pgto:
                        salvar_status_mensalidade(cpf_escolhido_fin, mes_selecionado, novo_valor_pagamento, novo_status_pagamento, data_pgto_input)
                        st.success(f"Status financeiro de {aluno_info['Nome']} atualizado com sucesso para **{novo_status_pagamento}**!")
                        st.rerun()

            st.markdown("---")
            st.markdown("### 📋 Relatório de Mensalidades do Mês")
            st.dataframe(df_mensalidades_exib, hide_index=True, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado para gerar o controle de mensalidades.")

# ==============================================================================
# ESTRUTURA GLOBAL DE HORÁRIOS E CÁLCULO SEGURO DE OCUPAÇÃO
# ==============================================================================
horarios_base = []
inicio_manha = datetime.combine(datetime.today(), time(8, 0))
fim_manha = datetime.combine(datetime.today(), time(12, 0))
atual = inicio_manha
while atual + timedelta(minutes=45) <= fim_manha:
    horarios_base.append(atual.strftime("%H:%M"))
    atual += timedelta(minutes=60)
    
inicio_tarde = datetime.combine(datetime.today(), time(14, 0))
fim_tarde = datetime.combine(datetime.today(), time(21, 0))
atual = inicio_tarde
while atual + timedelta(minutes=45) <= fim_tarde:
    horarios_base.append(atual.strftime("%H:%M"))
    atual += timedelta(minutes=60)

dias_semana_lista = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

def calcular_ocupacao_matriz(df_clientes, limite_vagas):
    ocupacao = {}
    for d in dias_semana_lista:
        for h in horarios_base:
            ocupacao[(d, h)] = 0
            
    if not df_clientes.empty:
        for _, row in df_clientes.iterrows():
            if pd.notna(row.get('dias_semana')) and pd.notna(row.get('horarios')):
                dias_cli = list(set([x.strip() for x in row['dias_semana'].split(",") if x.strip()]))
                hors_cli = list(set([x.strip() for x in row['horarios'].split(",") if x.strip()]))
                for d in dias_cli:
                    for h in hors_cli:
                        if (d, h) in ocupacao:
                            ocupacao[(d, h)] += 1
    return ocupacao

# ==============================================================================
# ABA 2: NOVO CADASTRO & AGENDAMENTO
# ==============================================================================
with aba_novo_cadastro:
    st.header("➕ Novo Cadastro & Agendamento de Cliente")
    
    if "form_cad_gerado" not in st.session_state:
        st.session_state.form_cad_gerado = 0

    if "msg_sucesso_cad" in st.session_state:
        st.success(st.session_state.msg_sucesso_cad)
        del st.session_state.msg_sucesso_cad

    df_atual_clientes = carregar_clientes()
    vagas_limite = vagas_por_turma
    ocupacao_matriz = calcular_ocupacao_matriz(df_atual_clientes, vagas_limite)

    sufixo_form = st.session_state.form_cad_gerado

    st.markdown(f"📅 **Agenda Individual por Dia (Limite por Turma: {vagas_limite} vagas)**")
    dias_escolhidos = st.multiselect(
        "Selecione o(s) Dia(s) da Semana da Aula*", 
        dias_semana_lista, 
        key=f"cad_dias_multiselect_externo_{sufixo_form}"
    )

    horarios_por_dia_escolhido = []
    tem_algum_dia_sem_vaga = False

    if dias_escolhidos:
        st.markdown("🕒 **Defina o horário disponível para cada dia selecionado:**")
        cols_dias_agenda = st.columns(len(dias_escolhidos))
        for idx, dia in enumerate(dias_escolhidos):
            with cols_dias_agenda[idx]:
                opcoes_dia = []
                mapa_rotulos = {}
                
                for h in horarios_base:
                    ocupados_neste_dia = ocupacao_matriz.get((dia, h), 0)
                    vagas_restantes = vagas_limite - ocupados_neste_dia
                    
                    if vagas_restantes > 0:
                        rotulo = f"⏰ {h} — [{vagas_restantes}/{vagas_limite} livres 🟢]"
                        opcoes_dia.append(rotulo)
                        mapa_rotulos[rotulo] = h
                
                if not opcoes_dia:
                    st.error(f"⚠️ Turmas de **{dia}** esgotadas!")
                    tem_algum_dia_sem_vaga = True
                else:
                    escolha_rotulo = st.selectbox(f"Horário para **{dia}**:", opcoes_dia, key=f"horario_dinamico_{dia}_{sufixo_form}")
                    horarios_por_dia_escolhido.append(mapa_rotulos[escolha_rotulo])
    else:
        st.info("👈 Selecione os dias da semana acima para escolher os horários correspondentes.")

    st.markdown("---")

    with st.form(f"form_cadastro_client_final_{sufixo_form}", clear_on_submit=True):
        raw_cpf = st.text_input("CPF (ID do Paciente)*", placeholder="000.000.000-00", key=f"cad_cpf_{sufixo_form}")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            nome = st.text_input("Nome Completo*", key=f"cad_nome_{sufixo_form}").upper()
            email = st.text_input("E-mail", placeholder="exemplo@email.com", key=f"cad_email_{sufixo_form}").lower()
            raw_nasc = st.text_input("Data de Nascimento (DD/MM/AAAA)", placeholder="Ex: 15/08/1990", key=f"cad_nasc_{sufixo_form}")
            endereco = st.text_input("Endereço", key=f"cad_end_{sufixo_form}").upper()
        with col_c2:
            raw_tel = st.text_input("Telefone / WhatsApp", key=f"cad_tel_{sufixo_form}")
            nome_emerg = st.text_input("Nome Contato de Emergência", placeholder="Nome", key=f"cad_nome_emerg_{sufixo_form}").upper()
            raw_tel_emerg = st.text_input("Telefone Contato de Emergência", placeholder="(00) 00000-0000", key=f"cad_tel_emerg_{sufixo_form}")
            plano = st.selectbox("Plano Contratado", ["Plano 1x por semana", "Plano 2x por semana", "Plano 3x por semana", "Plano Ilimitado"], key=f"cad_plano_{sufixo_form}")

        objetivo = st.text_area("Objetivo Clínico / Diagnóstico / Restrições", key=f"cad_obj_{sufixo_form}").upper()
        
        st.markdown("---")
        st.markdown("📎 **Receita Médica / Laudo Inicial (Tarefa da Secretaria)**")
        col_doc1, col_doc2, col_doc3 = st.columns(3)
        with col_doc1:
            origem_doc_cad = st.selectbox("Canal de Recebimento", ["Scanner / Arquivo Local", "E-mail da Clínica", "Entrega Física / Outros"], key=f"cad_origem_{sufixo_form}")
        with col_doc2:
            titulo_doc_cad = st.text_input("Título do Laudo / Receita", placeholder="Ex: Laudo Ortopédico Joelho", key=f"cad_tit_doc_{sufixo_form}")
        with col_doc3:
            arquivo_cad = st.file_uploader(
                "Anexar Arquivo (PDF, Imagem PNG/JPG)", 
                type=["pdf", "png", "jpg", "jpeg"], 
                key=f"cad_arq_{sufixo_form}"
            )
        desc_doc_cad = st.text_area("Observações sobre o Laudo / Receita", placeholder="Ex: Restrição de impacto...", key=f"cad_desc_doc_{sufixo_form}")

        st.markdown("")
        btn_salvar_cli = st.form_submit_button("💾 Salvar e Confirmar Agendamento", type="primary")
        
        if btn_salvar_cli:
            cpf = formatar_cpf(raw_cpf)
            telefone = formatar_telefone(raw_tel)
            tel_emerg = formatar_telefone(raw_tel_emerg)
            contato_emergencia = f"{nome_emerg} — {tel_emerg}" if nome_emerg or raw_tel_emerg else ""
            data_nasc = formatar_data(raw_nasc)
            
            idade_calculada = 0
            if len(data_nasc) == 10:
                try:
                    dt = datetime.strptime(data_nasc, "%d/%m/%Y").date()
                    hoje = date.today()
                    idade_calculada = hoje.year - dt.year - ((hoje.month, hoje.day) < (dt.month, dt.day))
                except ValueError:
                    pass

            if not cpf.strip() or not nome.strip():
                st.warning("Preencha o CPF e o Nome Completo.")
            elif not dias_escolhidos:
                st.warning("Selecione pelo menos um dia da semana.")
            elif tem_algum_dia_sem_vaga:
                st.error("⚠️ Não é possível salvar pois há dias selecionados sem vagas disponíveis.")
            elif len(horarios_por_dia_escolhido) != len(dias_escolhidos):
                st.warning("Selecione um horário válido para cada dia escolhido.")
            else:
                sucesso, msg = adicionar_cliente(cpf, nome, email, data_nasc, idade_calculada, endereco, telefone, contato_emergencia, objetivo, plano, dias_escolhidos, horarios_por_dia_escolhido)
                if sucesso:
                    data_hora_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
                    if arquivo_cad is not None or titulo_doc_cad.strip():
                        nome_arq = arquivo_cad.name if arquivo_cad is not None else "Sem arquivo anexado"
                        bin_arq = arquivo_cad.read() if arquivo_cad is not None else None
                        adicionar_receita_laudo(
                            cpf=cpf,
                            data_hora=data_hora_atual,
                            titulo=titulo_doc_cad if titulo_doc_cad.strip() else "Laudo Inicial",
                            origem=origem_doc_cad,
                            descricao=desc_doc_cad,
                            nome_arq=nome_arq,
                            bin_arq=bin_arq
                        )
                    
                    st.session_state.form_cad_gerado += 1
                    st.session_state.msg_sucesso_cad = "🎉 Cadastro realizado com Sucesso!"
                    st.rerun()
                else:
                    st.error(msg)

# ==============================================================================
# ABA 3: CLIENTES CADASTRADOS (DEDICADA)
# ==============================================================================
with aba_clientes_cadastrados:
    st.header("👥 Gestão de Clientes Cadastrados")
    
    sub_aba_lista, sub_aba_gerenciar = st.tabs(["📋 Lista Geral", "✏️ Editar / Excluir Clientes"])

    with sub_aba_lista:
        df_atual_clientes = carregar_clientes()
        if not df_atual_clientes.empty:
            buf_cli = io.BytesIO()
            with pd.ExcelWriter(buf_cli, engine='openpyxl') as writer:
                df_atual_clientes.to_excel(writer, sheet_name="Clientes", index=False)
            buf_cli.seek(0)
            
            col_b_busca, col_b_down = st.columns([3, 1])
            with col_b_busca:
                busca = st.text_input("🔍 Buscar cliente por nome ou CPF:", "", key="busca_cliente_tab")
            with col_b_down:
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar Clientes (Excel)",
                    data=buf_cli,
                    file_name="clientes_studio_sampaio.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            df_exibicao = df_atual_clientes.copy()
            if busca:
                df_exibicao = df_exibicao[
                    df_exibicao['nome'].str.contains(busca, case=False, na=False) | 
                    df_exibicao['cpf'].str.contains(busca, case=False, na=False)
                ]
            st.dataframe(df_exibicao, hide_index=True, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado.")

    with sub_aba_gerenciar:
        st.subheader("✏️ Editar ou Excluir Cadastro de Clientes")
        
        with st.expander("⚠️ Opções Avançadas (Zerar Base de Dados)"):
            if st.button("🧹 Excluir TODOS os Clientes (Zerar Banco e Reiniciar IDs)", type="secondary"):
                limpa_todos_clientes()
                st.success("Todos os clientes foram excluídos e o contador de ID foi resetado para 1!")
                st.rerun()

        df_cli_gerir = carregar_clientes()
        
        if not df_cli_gerir.empty:
            lista_clientes_editar = [f"{row['nome']} (CPF: {row['cpf']})" for _, row in df_cli_gerir.iterrows()]
            escolha_cli = st.selectbox("Selecione o cliente para gerenciar:", lista_clientes_editar, key="select_cli_edit")
            
            cpf_selecionado = escolha_cli.split("CPF: ")[1].split(")")[0]
            cliente_dados = df_cli_gerir[df_cli_gerir['cpf'] == cpf_selecionado].iloc[0]
            
            with st.form("form_edicao_cliente"):
                st.markdown(f"**Editando cadastro de:** {cliente_dados['nome']} (CPF: {cliente_dados['cpf']})")
                
                novo_nome = st.text_input("Nome Completo", value=cliente_dados.get('nome', '')).upper()
                novo_email = st.text_input("E-mail", value=cliente_dados.get('email', '') if pd.notna(cliente_dados.get('email')) else '').lower()
                
                idade_val_bruta = cliente_dados.get('idade', 30)
                try:
                    idade_val_int = int(idade_val_bruta) if pd.notna(idade_val_bruta) else 30
                except (ValueError, TypeError):
                    idade_val_int = 30
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    raw_nasc_edit = st.text_input("Data de Nascimento (DD/MM/AAAA)", value=cliente_dados.get('data_nascimento', '') if pd.notna(cliente_dados.get('data_nascimento')) else '')
                    nova_data_nasc = formatar_data(raw_nasc_edit)
                with col_e2:
                    nova_idade = st.number_input("Idade", min_value=0, max_value=120, value=max(0, idade_val_int))

                novo_endereco = st.text_input("Endereço", value=cliente_dados.get('endereco', '') if pd.notna(cliente_dados.get('endereco')) else '').upper()
                
                col_e3, col_e4 = st.columns(2)
                with col_e3:
                    novo_tel = st.text_input("Telefone / WhatsApp", value=cliente_dados.get('telefone', '') if pd.notna(cliente_dados.get('telefone')) else '')
                with col_e4:
                    novo_emerg = st.text_input("Contato de Emergência", value=cliente_dados.get('contato_emergencia', '') if pd.notna(cliente_dados.get('contato_emergencia')) else '').upper()

                novo_obj = st.text_area("Objetivo Clínico / Restrições", value=cliente_dados.get('objetivo', '') if pd.notna(cliente_dados.get('objetivo')) else '').upper()
                
                planos_disp = ["Plano 1x por semana", "Plano 2x por semana", "Plano 3x por semana", "Plano Ilimitado"]
                plano_atual = cliente_dados.get('plano', 'Plano 1x por semana')
                idx_plano = planos_disp.index(plano_atual) if plano_atual in planos_disp else 0
                novo_plano = st.selectbox("Plano Contratado", planos_disp, index=idx_plano)
                
                dias_atuais_str = cliente_dados.get('dias_semana', '')
                dias_atuais_lista = [d.strip() for d in dias_atuais_str.split(",")] if pd.notna(dias_atuais_str) and dias_atuais_str else []
                novos_dias = st.multiselect("Dias da Semana da Aula", dias_semana_lista, default=[d for d in dias_atuais_lista if d in dias_semana_lista])
                
                horarios_atuais_str = cliente_dados.get('horarios', '')
                novos_horarios = [h.strip() for h in horarios_atuais_str.split(",")] if pd.notna(horarios_atuais_str) and horarios_atuais_str else ["08:00"]

                col_btn_salvar, col_btn_del = st.columns(2)
                with col_btn_salvar:
                    btn_atualizar = st.form_submit_button("💾 Salvar Alterações", type="primary")
                with col_btn_del:
                    btn_excluir = st.form_submit_button("🗑️ Excluir Cliente", type="secondary")

                if btn_atualizar:
                    atualizar_cliente(
                        cpf_antigo=cpf_selecionado,
                        nome=novo_nome,
                        email=novo_email,
                        data_nasc=nova_data_nasc,
                        idade=nova_idade,
                        endereco=novo_endereco,
                        telefone=novo_tel,
                        contato_emergencia=novo_emerg,
                        objetivo=novo_obj,
                        plano=novo_plano,
                        dias_semana=novos_dias,
                        horarios=novos_horarios
                    )
                    st.success("Cadastro do cliente atualizado com sucesso!")
                    st.rerun()

                if btn_excluir:
                    deletar_cliente(cpf_selecionado)
                    st.success("Cliente excluído com sucesso!")
                    st.rerun()
        else:
            st.info("Nenhum cliente cadastrado para gerenciar.")

# ==============================================================================
# ABA 4: MAPA VISUAL DE OCUPAÇÃO DAS TURMAS
# ==============================================================================
with aba_mapa:
    st.header("🧩 Mapa de Ocupação das Turmas")
    st.markdown("Visualização em tempo real das vagas e alunos agendados em cada horário.")
    
    df_mapa_clientes = carregar_clientes()
    limite_vagas_mapa = vagas_por_turma
    matriz = calcular_ocupacao_matriz(df_mapa_clientes, limite_vagas_mapa)
    
    col_leg1, col_leg2, col_leg3 = st.columns(3)
    col_leg1.markdown("🟢 **Vaga Disponível**")
    col_leg2.markdown("🧘‍♀️ **Aluno Agendado (Vaga Ocupada)**")
    col_leg3.markdown(f"⚙️ **Capacidade:** {limite_vagas_mapa} aluno(s) por turma")
    
    st.divider()
    
    for dia in dias_semana_lista:
        st.subheader(f"📅 {dia}")
        cols_horarios = st.columns(len(horarios_base))
        
        for idx, h in enumerate(horarios_base):
            qtd_ocupados = matriz.get((dia, h), 0)
            qtd_livres = max(0, limite_vagas_mapa - qtd_ocupados)
            
            with cols_horarios[idx]:
                # Usa verde vibrante nítido para as bolinhas de vagas livres
                assentos_html = ""
                for _ in range(qtd_ocupados):
                    assentos_html += "🧘‍♀️ "
                for _ in range(qtd_livres):
                    assentos_html += "<span style='color: #00B050; font-size: 1.1rem; text-shadow: 0 0 2px rgba(0,0,0,0.2);'>🟢</span> "
                
                st.markdown(f"**{h}**")
                st.markdown(assentos_html, unsafe_allow_html=True)
                
                # Números em preto nítido e vivo (#000000) com fundo suave para garantir total legibilidade
                st.markdown(
                    f"<div style='color: #000000; font-weight: 800; font-size: 0.9rem; background-color: rgba(255, 255, 255, 0.7); border-radius: 6px; padding: 2px 4px; display: inline-block; text-align: center; margin-top: 4px;'>"
                    f"{qtd_ocupados}/{limite_vagas_mapa} vagas"
                    f"</div>", 
                    unsafe_allow_html=True
                )
        st.markdown("---")

# ==============================================================================
# ABA 5: CADASTRO, EDIÇÃO E EXCLUSÃO DE PROFISSIONAIS
# ==============================================================================
with aba_profissionais:
    st.header("👩‍⚕️ Gestão de Fisioterapeutas e Profissionais")
    
    sub_aba_p_novo, sub_aba_p_gerir = st.tabs(["➕ Novo Profissional", "✏️ Editar / Excluir Profissionais"])
    
    with sub_aba_p_novo:
        col_p1, col_p2 = st.columns([1, 2])
        
        with col_p1:
            st.subheader("Novo Profissional")
            with st.form("form_prof", clear_on_submit=True):
                nome_prof = st.text_input("Nome do Profissional*").upper()
                conselho = st.selectbox("Conselho", ["CREFITO", "CREF", "Outro"])
                registro = st.text_input("Número do Registro (Ex: 123456-F)*").upper()
                
                btn_cad_prof = st.form_submit_button("💾 Salvar Profissional")
                if btn_cad_prof:
                    if nome_prof.strip() and registro.strip():
                        adicionar_profissional(nome_prof, conselho, registro)
                        st.success(f"Profissional **{nome_prof}** cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.warning("Preencha o nome e o registro profissional.")
                        
        with col_p2:
            st.subheader("Profissionais Cadastrados")
            df_profs = carregar_profissionais()
            if not df_profs.empty:
                st.dataframe(df_profs, hide_index=True, use_container_width=True)
            else:
                st.info("Nenhum profissional cadastrado.")

    with sub_aba_p_gerir:
        st.subheader("✏️ Editar ou Excluir Profissionais")
        df_profs_gerir = carregar_profissionais()
        
        if not df_profs_gerir.empty:
            lista_profs_edit = [f"{row['nome_prof']} ({row['conselho']}: {row['registro']}) [ID: {row['id']}]" for _, row in df_profs_gerir.iterrows()]
            escolha_prof = st.selectbox("Selecione o profissional para gerenciar:", lista_profs_edit, key="select_prof_edit")
            
            prof_id_sel = int(escolha_prof.split("[ID: ")[1].split("]")[0])
            prof_dados = df_profs_gerir[df_profs_gerir['id'] == prof_id_sel].iloc[0]
            
            with st.form("form_edicao_prof"):
                st.markdown(f"**Editando profissional ID {prof_id_sel}**")
                
                p_nome = st.text_input("Nome do Profissional", value=prof_dados['nome_prof']).upper()
                
                conselhos_disp = ["CREFITO", "CREF", "Outro"]
                c_atual = prof_dados['conselho']
                idx_c = conselhos_disp.index(c_atual) if c_atual in conselhos_disp else 0
                p_conselho = st.selectbox("Conselho", conselhos_disp, index=idx_c)
                
                p_registro = st.text_input("Número do Registro", value=prof_dados['registro']).upper()
                
                col_p_salvar, col_p_del = st.columns(2)
                with col_p_salvar:
                    btn_salvar_prof = st.form_submit_button("💾 Salvar Alterações", type="primary")
                with col_p_del:
                    btn_del_prof = st.form_submit_button("🗑️ Excluir Profissional", type="secondary")

                if btn_salvar_prof:
                    atualizar_profissional(prof_id_sel, p_nome, p_conselho, p_registro)
                    st.success("Profissional atualizado com sucesso!")
                    st.rerun()

                if btn_del_prof:
                    deletar_profissional(prof_id_sel)
                    st.success("Profissional excluído com sucesso!")
                    st.rerun()
        else:
            st.info("Nenhum profissional cadastrado para gerenciar.")

# ==============================================================================
# ABA 6: PRONTUÁRIO ELETRÔNICO & LAUDOS/RECEITAS
# ==============================================================================
with aba_prontuario:
    st.header("📝 Prontuário Eletrônico & Gestão de Laudos/Receitas")
    
    df_clientes_pront = carregar_clientes()
    df_profs_pront = carregar_profissionais()
    
    if df_clientes_pront.empty:
        st.warning("Cadastre pelo menos um cliente na aba de 'Novo Cadastro & Agendamento' para acessar os prontuários.")
    elif df_profs_pront.empty:
        st.warning("Cadastre pelo menos um profissional na aba de 'Profissionais' para assinar os atendimentos.")
    else:
        lista_pacientes = ["-- Selecione um Paciente --"] + [f"{row['nome']} (CPF: {row['cpf']})" for _, row in df_clientes_pront.iterrows()]
        paciente_selecionado = st.selectbox("Selecione o Paciente", lista_pacientes, key="select_pac_prontuario")
        
        if paciente_selecionado == "-- Selecione um Paciente --":
            st.info("👈 Por favor, selecione um paciente acima para carregar o prontuário, dados cadastrais e bancos de mensagens.")
        else:
            cpf_atual = paciente_selecionado.split("CPF: ")[1].split(")")[0]
            dados_paciente = df_clientes_pront[df_clientes_pront['cpf'] == cpf_atual].iloc[0]
            nome_paciente_ativo = dados_paciente.get('nome', '')
            
            tel_bruto = str(dados_paciente.get('telefone', ''))
            nums_tel = "".join(filter(str.isdigit, tel_bruto))
            
            email_paciente = str(dados_paciente.get('email', ''))

            with st.expander("📌 Ver Dados Cadastrais, Plano e Anexos do Paciente", expanded=False):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Nome:** {nome_paciente_ativo}")
                
                if email_paciente and email_paciente != '-':
                    c1.write(f"**E-mail:** {email_paciente}")
                    if c1.button("📋 Copiar E-mail", key=f"btn_copiar_email_{cpf_atual}"):
                        c1.code(email_paciente, language=None)
                        c1.toast(f"E-mail {email_paciente} exibido acima!")
                else:
                    c1.write(f"**E-mail:** -")
                    
                c1.write(f"**Idade / Nasc:** {dados_paciente.get('idade', '-')} anos ({dados_paciente.get('data_nascimento', '-')})")
                
                c2.write(f"**Telefone:** {tel_bruto if tel_bruto else '-'}")
                c2.write(f"**Emergência:** {dados_paciente.get('contato_emergencia', '-')}")
                c2.write(f"**Plano:** {dados_paciente.get('plano', '-')}")
                
                c3.write(f"**Dias/Horários:** {dados_paciente.get('dias_semana', '-')} às {dados_paciente.get('horarios', '-')}")
                st.write(f"**Objetivo Clínico / Restrições:** {dados_paciente.get('objetivo', '-')}")

            # ======================================================================
            # BANCO DE MENSAGENS E ENVIOS (WHATSAPP & E-MAIL CORPORATIVO)
            # ======================================================================
            st.markdown("---")
            st.markdown("💬 **Envio de Mensagens e E-mails (Identidade Corporativa da Clínica)**")
            
            # --- SEÇÃO WHATSAPP ---
            st.markdown("##### 📱 Canal WhatsApp")
            modelos_mensagens_zap = {
                "⏰ Confirmação de Consulta / Aula (Dia Anterior)": f"Olá, {nome_paciente_ativo}! Passando para lembrar e confirmar o seu horário de atendimento agendado para amanhã aqui no Stúdio Letícia e Ítalo Sampaio. Por favor, responda com *1* para confirmar ou *2* caso precise reagendar. Te esperamos!",
                "👋 Boas-vindas ao Stúdio": f"Olá, {nome_paciente_ativo}! Seja muito bem-vindo(a) ao Stúdio de Pilates e Fisioterapia Letícia e Ítalo Sampaio. Estamos muito felizes em iniciar sua jornada de saúde e bem-estar conosco!",
                "💰 Lembrete de Mensalidade / Pagamento": f"Olá, {nome_paciente_ativo}! Esperamos que esteja bem. Este é um lembrete amigável referente à mensalidade deste mês no Stúdio Letícia e Ítalo Sampaio. Qualquer dúvida, estamos à disposição!",
                "🩺 Acompanhamento Fisioterapêutico": f"Olá, {nome_paciente_ativo}! Como estão sendo os exercícios e a evolução em casa? Qualquer dúvida ou desconforto, nos avise. Atenciosamente, equipe Letícia e Ítalo Sampaio.",
                "✍️ Mensagem Personalizada (Livre)": f"Olá, {nome_paciente_ativo}! "
            }
            
            col_z1, col_z2 = st.columns([1, 1])
            with col_z1:
                escolha_modelo_zap = st.selectbox("Selecione o Modelo WhatsApp", list(modelos_mensagens_zap.keys()), key=f"sel_modelo_zap_{cpf_atual}")
            
            texto_modelo_zap_padrao = modelos_mensagens_zap[escolha_modelo_zap]
            
            with col_z2:
                texto_personalizado_zap = st.text_area("Texto para WhatsApp:", value=texto_modelo_zap_padrao, height=85, key=f"txt_zap_dinamico_{cpf_atual}_{escolha_modelo_zap}")

            if len(nums_tel) >= 10:
                texto_codificado_zap = urllib.parse.quote(texto_personalizado_zap)
                link_zap_final = f"https://wa.me/55{nums_tel}?text={texto_codificado_zap}"
                
                st.markdown(
                    f'<a href="{link_zap_final}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:700; font-size:0.95rem;">🚀 Enviar Mensagem via WhatsApp</button></a>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("⚠️ O telefone cadastrado para este paciente não é válido para envio de WhatsApp.")

            st.markdown("---")

            # --- SEÇÃO E-MAIL CORPORATIVO ---
            st.markdown("##### ✉️ Canal E-mail Corporativo (Assunto Pré-Selecionado)")
            
            modelos_mensagens_email = {
                "👋 Boas-vindas ao Stúdio Sampaio": f"Olá, {nome_paciente_ativo}!\n\nSeja muito bem-vindo(a) ao Stúdio de Pilates e Fisioterapia Letícia e Ítalo Sampaio. Estamos extremamente felizes por iniciar sua jornada de saúde, bem-estar e reabilitação conosco.\n\nQualquer dúvida, estamos à inteira disposição.\n\nAtenciosamente,\nEquipe Stúdio Sampaio",
                "⏰ Lembrete de Agendamento": f"Olá, {nome_paciente_ativo},\n\nPassando para lembrar do seu horário agendado no Stúdio Letícia e Ítalo Sampaio. Caso precise remarcar, por favor nos avise com antecedência.\n\nAtenciosamente,\nEquipe Stúdio Sampaio",
                "💰 Informações Financeiras / Mensalidade": f"Olá, {nome_paciente_ativo},\n\nEntramos em contato referente ao acerto da mensalidade do Stúdio de Pilates e Fisioterapia Letícia e Ítalo Sampaio.\n\nAtenciosamente,\nEquipe Financeira",
                "✍️ E-mail Personalizado (Livre)": f"Olá, {nome_paciente_ativo},\n\n"
            }

            col_e1, col_e2 = st.columns([1, 1])
            with col_e1:
                escolha_modelo_email = st.selectbox("Selecione o Modelo de E-mail", list(modelos_mensagens_email.keys()), key=f"sel_modelo_email_{cpf_atual}")
            
            assunto_pre_selecionado = escolha_modelo_email.replace("👋 ", "").replace("⏰ ", "").replace("💰 ", "").replace("✍️ ", "")
            
            with col_e2:
                assunto_email_input = st.text_input("Assunto do E-mail (Pré-selecionado):", value=assunto_pre_selecionado, key=f"txt_assunto_email_{cpf_atual}")

            corpo_email_padrao = modelos_mensagens_email[escolha_modelo_email]
            corpo_email_personalizado = st.text_area("Corpo da Mensagem do E-mail:", value=corpo_email_padrao, height=95, key=f"txt_email_dinamico_{cpf_atual}_{escolha_modelo_email}")

            if email_paciente and email_paciente != '-':
                assunto_codificado = urllib.parse.quote(assunto_email_input)
                corpo_codificado = urllib.parse.quote(corpo_email_personalizado)
                
                link_gmail_web = f"https://mail.google.com/mail/?view=cm&fs=1&to={email_paciente}&su={assunto_codificado}&body={corpo_codificado}"
                
                st.markdown(
                    f'<a href="{link_gmail_web}" target="_blank" style="text-decoration:none;"><button style="background-color:#0F291E; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:700; font-size:0.95rem;">📧 Enviar E-mail Corporativo (Via Gmail)</button></a>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("⚠️ O paciente selecionado não possui um e-mail válido cadastrado.")

            st.divider()

            sub_pront_evolução, sub_pront_laudos = st.tabs(["💬 Evoluções Clínicas & Atendimentos", "📁 Receitas Médicas, Laudos & Anexos"])

            with sub_pront_evolução:
                col_evolucao_form, col_evolucao_hist = st.columns([1, 1])
                
                with col_evolucao_form:
                    st.subheader("➕ Registrar Nova Evolução / Consulta")
                    with st.form("form_evolucao", clear_on_submit=True):
                        data_atendimento_input = st.date_input("Data da Consulta", value=datetime.today(), format="DD/MM/YYYY")
                        
                        lista_nomes_profs = [f"{r['nome_prof']} ({r['conselho']}: {r['registro']})" for _, r in df_profs_pront.iterrows()]
                        prof_responsavel = st.selectbox("Profissional Responsável", lista_nomes_profs)
                        
                        atividades = st.text_area("Atividades Realizadas / Exercícios Aplicados", placeholder="Ex: Aparelho Reformer...").upper()
                        evolucao = st.text_area("Evolução Clínica / Observações do Paciente", placeholder="Ex: Paciente relatou melhora...").upper()
                        
                        btn_salvar_pront = st.form_submit_button("💾 Salvar Prontuário")
                        
                        if btn_salvar_pront:
                            if not atividades.strip() or not evolucao.strip():
                                st.warning("Preencha as atividades e a evolução clínica.")
                            else:
                                data_hora_reg = f"{data_atendimento_input.strftime('%d/%m/%Y')} às {datetime.now().strftime('%H:%M')}"
                                adicionar_prontuario(
                                    cpf=cpf_atual,
                                    data_hora=data_hora_reg,
                                    profissional=prof_responsavel,
                                    atividades=atividades,
                                    evolucao=evolucao
                                )
                                st.success("Evolução registrada com sucesso no prontuário!")
                                st.rerun()
                                
                with col_evolucao_hist:
                    st.subheader("📖 Histórico de Atendimentos")
                    df_historico = carregar_prontuarios(cpf_atual)
                    
                    if not df_historico.empty:
                        for _, hist in df_historico.iterrows():
                            with st.container(border=True):
                                st.markdown(f"👤 **Paciente:** {nome_paciente_ativo}")
                                st.markdown(f"📅 **Data/Hora:** {hist['data_atendimento']} | 👩‍⚕️ **Profissional:** {hist['profissional']}")
                                st.markdown(f"🏋️ **Atividades:** {hist['atividades']}")
                                st.markdown(f"📝 **Evolução:** {hist['evolucao']}")
                                
                                c_edit, c_del = st.columns(2)
                                with c_edit:
                                    with st.popover("✏️ Editar Evolução"):
                                        with st.form(f"form_edit_ev_{hist['id']}"):
                                            novas_ativ = st.text_area("Editar Atividades", value=hist['atividades']).upper()
                                            nova_ev = st.text_area("Editar Evolução", value=hist['evolucao']).upper()
                                            if st.form_submit_button("💾 Salvar Alterações"):
                                                atualizar_prontuario(hist['id'], novas_ativ, nova_ev)
                                                st.success("Atendimento atualizado com sucesso!")
                                                st.rerun()
                                with c_del:
                                    if st.button("🗑️ Excluir Atendimento", key=f"del_pront_{hist['id']}"):
                                        deletar_prontuario(hist['id'])
                                        st.success("Registro excluído!")
                                        st.rerun()
                    else:
                        st.info("Nenhum registro de atendimento encontrado para este paciente.")

            with sub_pront_laudos:
                st.subheader("📂 Gestão, Incremento e Atualização de Laudos e Receitas")
                st.caption(f"Gerenciando documentos para o paciente: **{nome_paciente_ativo}**")

                col_form_laudo, col_lista_laudos = st.columns([1, 1])

                with col_form_laudo:
                    with st.form(f"form_novo_laudo_{cpf_atual}", clear_on_submit=True):
                        st.markdown("**➕ Adicionar / Incrementar Novo Laudo ou Receita**")
                        origem_doc = st.selectbox("Origem do Documento", ["Scanner / Arquivo Local", "E-mail da Clínica", "Entrega Física / Outros"])
                        titulo_doc = st.text_input("Título / Descrição do Laudo", placeholder="Ex: Ressonância Magnética Atualizada")
                        obs_doc = st.text_area("Detalhes Clínicos ou Observações", placeholder="Ex: Indicado repouso parcial...")
                        arquivo_up = st.file_uploader("Arquivo Anexo (PDF, Imagem PNG/JPG)", type=["pdf", "png", "jpg", "jpeg"])

                        btn_salvar_laudo = st.form_submit_button("💾 Enviar e Anexar Documento")
                        if btn_salvar_laudo:
                            if not titulo_doc.strip():
                                st.warning("Informe o título do laudo ou receita.")
                            else:
                                nome_arq = arquivo_up.name if arquivo_up is not None else "Sem arquivo anexado"
                                bin_arq = arquivo_up.read() if arquivo_up is not None else None
                                data_hora_doc = datetime.now().strftime("%d/%m/%Y às %H:%M")
                                
                                adicionar_receita_laudo(
                                    cpf=cpf_atual,
                                    data_hora=data_hora_doc,
                                    titulo=titulo_doc,
                                    origem=origem_doc,
                                    descricao=obs_doc,
                                    nome_arq=nome_arq,
                                    bin_arq=bin_arq
                                )
                                st.success("Laudo/Receita anexado com sucesso ao prontuário do paciente!")
                                st.rerun()

                with col_lista_laudos:
                    st.subheader("📑 Documentos e Laudos Armazenados")
                    df_laudos_cli = carregar_receitas_laudos(cpf_atual)

                    if not df_laudos_cli.empty:
                        for _, doc in df_laudos_cli.iterrows():
                            with st.container(border=True):
                                st.markdown(f"📌 **{doc['titulo']}**")
                                st.markdown(f"👤 **Paciente:** {nome_paciente_ativo}")
                                st.caption(f"📅 Registrado em: {doc['data_recebimento']} | 📥 Origem: {doc['origem']}")
                                if pd.notna(doc['descricao_conteudo']) and doc['descricao_conteudo']:
                                    st.write(f"💬 **Obs:** {doc['descricao_conteudo']}")
                                st.write(f"📎 **Arquivo:** {doc['nome_arquivo']}")
                                
                                binario_arquivo = doc.get('arquivo_bin')
                                nome_arquivo_doc = doc.get('nome_arquivo', 'documento')
                                
                                col_b1, col_b2 = st.columns(2)
                                with col_b1:
                                    if binario_arquivo is not None and len(binario_arquivo) > 0:
                                        b64 = base64.b64encode(binario_arquivo).decode()
                                        
                                        ext_arq = nome_arquivo_doc.split('.')[-1].lower()
                                        mime_map = {'pdf': 'application/pdf', 'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg'}
                                        mime_type_val = mime_map.get(ext_arq, 'application/octet-stream')
                                        
                                        href = f'<a href="data:{mime_type_val};base64,{b64}" download="{nome_arquivo_doc}" target="_blank" style="text-decoration:none;"><button style="background-color:#2d6a4f; color:white; border:none; padding:6px 12px; border-radius:8px; cursor:pointer; font-weight:600; font-size:0.85rem;">👁️ Exibir / Baixar</button></a>'
                                        st.markdown(href, unsafe_allow_html=True)
                                    else:
                                        st.caption("ℹ️ Sem arquivo binário.")
                                
                                with col_b2:
                                    if st.button("🗑️ Excluir Documento", key=f"del_doc_{doc['id']}_{cpf_atual}"):
                                        deletar_receita_laudo(doc['id'])
                                        st.success("Documento removido com sucesso!")
                                        st.rerun()
                    else:
                        st.info("Nenhum laudo ou receita médica anexado para este paciente até o momento.")