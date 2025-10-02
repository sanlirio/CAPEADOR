import os
import tempfile
import uuid
import streamlit as st
import json
import sys
import base64
from io import BytesIO
from streamlit import column_config
#from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

sys.path.append(os.path.dirname(__file__))
#from funcoes_gerais import get_db_connection
from funcoes_gerais import conectar_postgres
from relatorios import rp_capeador 
import pandas as pd


st.set_page_config(page_title="Gerador de Capeador", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items={
  
        'About': "# Aplicação desenvolvida para atender temporariamente a geração de formulários da base!"
    })

base64_string =  "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"
decoded_bytes = base64.b64decode(base64_string)
bytes_io = BytesIO(decoded_bytes)
st.image(bytes_io)
st.subheader(f"Gerador de capeador", divider=True)



def add_action_buttons(df):
    df_display = df.copy()

    # Inicializar estado
    if "selected_dt" not in st.session_state:
        st.session_state["selected_dt"] = None

    # Criar coluna "Ação"
    if "Ação" not in df_display.columns:
        df_display["Ação"] = False

    # Reordenar colunas
    colunas = ["Ação"] + [col for col in df_display.columns if col != "Ação"]
    df_display = df_display[colunas]

    # Marcar apenas a linha selecionada
    df_display["Ação"] = False
    if st.session_state["selected_dt"] is not None:
        mask = df_display['SHNUMBER'] == st.session_state["selected_dt"]
        if mask.any():
            df_display.loc[mask, "Ação"] = True

    # Renderizar editor
    edited_df = st.data_editor(
        df_display,
        column_config={
            "Ação": st.column_config.CheckboxColumn(
                "📄 Gerar Capeador",
                help="Clique para gerar o capeador desta linha",
                default=False,
            ),
            "SHNUMBER": "DT",
            "MATERIAL": "CÓD PRODUTO",
            "MATERIALDESCRIPTION": "PRODUTO",
            "IDORIGEM": None,
            "ORIGEM": "ORIGEM",
            "VEHICLEDESCRIPTION": "VEÍCULO",
            "IDTRANSPORTADORA": "ID TRANSPORTADORA",
            "TRANSPORTADORA": "TRANSPORTADORA",
            "IDMOTORISTA": "ID MOTORISTA",
            "NOME": None,
            "SOBRENOME": None,
            "NOMECOMPL": "MOTORISTA",
            "IDCENTRO": "CENTRO",
            "CENTRO": "DESC CENTRO",
            "IDDEPOSITO": "DEPÓSITO",
            "DEPOSITO": None,
            "NUMNOTA": "NOTA FISCAL",
            "CARGA QTDL20": "CARGA QTDE L20 FAT",
            "DESCARGA QTDL20": "DESCARGA QTDE L20 FAT",
            "UNITL20": None,
            "CARGA QTDL": "QTDE L",
            "DESCARGA QTDL": "QTDE L",
            "UNITL": None,
            "DATACONFIRFORNECIMENTO": "DATA FORNECIMENTO",
            "HORAFORNECIMENTO": "HORA FORNECIMENTO",
            "TEMPERATURA CARGA": "TEMPERATURA CARGA",
            "TEMPERATURA DESCARGA": "TEMPERATURA DESCARGA",
            "DENSIDADE CARGA": "DENSIDADE CARGA",
            "DENSIDADE DESCARGA": "DENSIDADE DESCARGA",
            "FATOR_CONVERSAO": "FATOR CONVERSÃO"
        },
        disabled=df_display.columns.difference(["Ação"]),
        hide_index=True,
        width="stretch",
        key="data_editor",
    )

    # Verificar linha clicada
    clicked_rows = edited_df.index[edited_df["Ação"]].tolist()
    
    if clicked_rows:
        selected_idx = clicked_rows[-1]
        selected_shnumber = df_display.iloc[selected_idx]["SHNUMBER"]
        
        # Se a seleção mudou, atualizar e rerun
        if st.session_state["selected_dt"] != selected_shnumber:
            st.session_state["selected_dt"] = selected_shnumber
            st.rerun()
        
        # Processar o relatório apenas se for um clique válido
        dadosEdit = df.iloc[selected_idx]
        st.session_state["doctran"] = dadosEdit["SHNUMBER"]
        st.session_state["td_action"] = dadosEdit["IDORIGEM"]

        st.success(f"✅ Capeador gerado para DT: {dadosEdit['SHNUMBER']}")
        rel_form()


def lista_principal():
            
    cols = st.columns([1,1,1,1,1,1,1,1,1,1,1,1],vertical_alignment='bottom')
    doc_transp = cols[0].text_input("Informe o Documento de Transporte")
    material = cols[1].text_input("Informe o Cód Produto")
    origem = cols[2].text_input("Informe a Origem")
    veiculo = cols[3].text_input("Informe o Veículo")
    id_transportadora = cols[4].text_input("Informe o ID Transportadora")
    transportadora = cols[5].text_input("Informe a Transportadora")
    id_motorista = cols[6].text_input("Informe o ID Motorista")
    nome_motorista = cols[7].text_input("Informe o Nome Motorista")
    id_centro = cols[8].text_input("Informe o Centro")
    desc_centro = cols[9].text_input("Informe a Desc Centro")
    id_deposito = cols[10].text_input("Informe o Depósito")
    nota_fiscal = cols[11].text_input("Informe a Nota Fiscal")

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],vertical_alignment='bottom')
    with col1:     
        start_date = st.date_input("Data Início Fornecimento", value=None)

    with col2:
        end_date = st.date_input("Data Fim Fornecimento", value=None)

    with col3:
        filtrar = st.button("Filtrar", use_container_width=True)    

    with col4:
       filtro_ApenasDescarregados = st.checkbox("Apenas Descarregados", value=False)

    # Inicializar dataframe se não existir (carrega dados iniciais)
    if 'dataframe' not in st.session_state or st.session_state.dataframe.empty:
        # Carregar dados iniciais
        list_db = conectar_postgres()
        query_inicial = """SELECT DISTINCT
                                 "SHNUMBER",
                                 "MATERIAL",
                                 "IDORIGEM",
                                 "ORIGEM",
                                 "VEHICLEDESCRIPTION",
                                 "IDTRANSPORTADORA",
                                 "TRANSPORTADORA",
                                 "IDMOTORISTA",
                                 "NOME",
                                 "SOBRENOME",
                                 "NOMECOMPL",
                                 "IDCENTRO",
                                 "CENTRO",
                                 "IDDEPOSITO",
                                 "DEPOSITO",
                                 "NUMNOTA",
                                 "CARGA QTDL20",
                                 "CARGA QTDL",
                                 "DESCARGA QTDL20",                    
                                 "DESCARGA QTDL",
                                 "DATACONFIRFORNECIMENTO",
                                 "HORAFORNECIMENTO",
                                 "TEMPERATURA CARGA",
                                 "TEMPERATURA DESCARGA",
                                 "DENSIDADE CARGA",
                                 "DENSIDADE DESCARGA",
                                 CASE WHEN ("DESCARGA QTDL20" IS NOT NULL AND "DESCARGA QTDL20" <>0)  THEN ("DESCARGA QTDL"::FLOAT) / ("DESCARGA QTDL20"::FLOAT) ELSE 0 END AS FATOR_CONVERSAO
                            FROM vw_descarga_consolidada 
                            WHERE 1=1
                           """  # Limite para performance
        st.session_state.dataframe = pd.read_sql(query_inicial, list_db)
        list_db.close()

    # Limpar seleção quando clicar em Filtrar
    if filtrar:
        st.session_state["selected_dt"] = None

        # Executar query com filtros quando clicar em Filtrar
        list_db = conectar_postgres()
        
        query = f"""SELECT DISTINCT
                         "SHNUMBER",
                         "MATERIAL",
                         "IDORIGEM",
                         "ORIGEM",
                         "VEHICLEDESCRIPTION",
                         "IDTRANSPORTADORA",
                         "TRANSPORTADORA",
                         "IDMOTORISTA",
                         "NOME",
                         "SOBRENOME",
                         "NOMECOMPL",
                         "IDCENTRO",
                         "CENTRO",
                         "IDDEPOSITO",
                         "DEPOSITO",
                         "NUMNOTA",
                         "CARGA QTDL20",
                         "CARGA QTDL",
                         "DESCARGA QTDL20",                    
                         "DESCARGA QTDL",
                         "DATACONFIRFORNECIMENTO",
                         "HORAFORNECIMENTO",
                         "TEMPERATURA CARGA",
                         "TEMPERATURA DESCARGA",
                         "DENSIDADE CARGA",
                         "DENSIDADE DESCARGA",
                         CASE WHEN ("DESCARGA QTDL20" IS NOT NULL AND "DESCARGA QTDL20" <>0)  THEN ("DESCARGA QTDL"::FLOAT) / ("DESCARGA QTDL20"::FLOAT) ELSE 0 END AS FATOR_CONVERSAO
                    FROM vw_descarga_consolidada WHERE 1=1"""
        params = []

        if filtro_ApenasDescarregados:
            query += """  AND "CARGA QTDL20" > 0
                AND "DESCARGA QTDL20" > 0
                AND "CARGA QTDL"      > 0
                AND "DESCARGA QTDL"   > 0 
                """
        if doc_transp:
           query += ' AND "SHNUMBER" ILIKE %s'
           params.append(f"%{doc_transp}%")

        if material:
           query += ' AND "MATERIAL" ILIKE %s'
           params.append(f"%{material}%")   

        if origem:
            query += ' AND "ORIGEM" ILIKE %s'
            params.append(f"%{origem}%")

        if veiculo:
           query += ' AND "VEHICLEDESCRIPTION" ILIKE %s'
           params.append(f"%{veiculo}%")

        if id_transportadora:
           query += ' AND "IDTRANSPORTADORA" ILIKE %s'
           params.append(f"%{id_transportadora}%")  

        if transportadora:
           query += ' AND "TRANSPORTADORA" ILIKE %s'
           params.append(f"%{transportadora}%")  

        if id_motorista:
           query += ' AND "IDMOTORISTA" ILIKE %s'
           params.append(f"%{id_motorista}%")  

        if nome_motorista:
           query += ' AND "NOMECOMPL" ILIKE %s'
           params.append(f"%{nome_motorista}%")  

        if id_centro:
           query += ' AND "IDCENTRO" ILIKE %s'
           params.append(f"%{id_centro}%")      

        if desc_centro:
           query += ' AND "CENTRO" ILIKE %s'
           params.append(f"%{desc_centro}%")    

        if id_deposito:
           query += ' AND "IDDEPOSITO" ILIKE %s'
           params.append(f"%{id_deposito}%")   

        if nota_fiscal:
           query += ' AND "NUMNOTA" ILIKE %s'
           params.append(f"%{nota_fiscal}%")     

        if start_date and end_date:
           query += ' AND TO_DATE("DATACONFIRFORNECIMENTO", \'YYYYMMDD\') BETWEEN %s AND %s'
           params.extend([start_date, end_date])

        # Executar query com filtros
        result_dataFrame = pd.read_sql(query, list_db, params=params)
        st.session_state['dataframe'] = result_dataFrame
        list_db.close()

    # Exibir contador de registros
    st.info(f"📊 Total de registros encontrados: {len(st.session_state.dataframe)}")

    # Exibir tabela
    if not st.session_state.dataframe.empty:
        add_action_buttons(st.session_state['dataframe'])
    else:
        st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados")

@st.dialog("Capeador" , width="large")    
def rel_form():
    
    param = []
    
    param.append({'td_action':str(st.session_state['td_action'])})
    param.append({'doctran':str(st.session_state['doctran'])})
    param.append({'ID_ABA':""})
    
    rp_capeador(param)
    
lista_principal()