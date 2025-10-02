#import mysql
import psycopg2
from psycopg2 import sql, OperationalError

#Obter conexao com o banco
#def get_db_connection():
    #try:
 #       conn = mysql.connector.connect(
  #          host="localhost",
   #         user="root",
    #        password="24042004",
     #       database="formsap"
      #  )
       # return conn


#Datalakesap

def conectar_postgres():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="larco_data_data_mesh2",
            user="forms_descarga_user01",
            password="sjm316",
            port=5432
        )
        print("✅ Conexão estabelecida com sucesso!")
        return conexao
    except OperationalError as e:
        print("❌ Erro ao conectar ao banco de dados:", e)
        return None

# def conectar_postgres():
#    try:
#        conexao = psycopg2.connect(
#            host="10.30.2.106",
#            database="larco_data_data_mesh",
#            user="forms_descarga_user01",
#            password="L@rco@!2025@",
#            port=5432
#        )
#        print("✅ Conexão estabelecida com sucesso!")
#        return conexao
#    except OperationalError as e:
#        print(" Erro ao conectar ao banco de dados:", e)
#        return None
