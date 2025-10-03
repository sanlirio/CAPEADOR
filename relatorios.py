import subprocess
import os
import tempfile
import uuid
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import base64
import json


def rp_capeador(parametros):
  
  # Define the paths to the input and output files
  jrxml_file = os.path.abspath("./relatorios/form_capeador.jrxml")
  java_classpath = os.path.abspath("./jasper_library") +"/*"
  
  temp_dir = tempfile.mkdtemp()
  jasper_file = os.path.join(temp_dir, f"{uuid.uuid1()}.jasper")
  pdf_file = os.path.join(temp_dir, f"{uuid.uuid4()}.pdf")
  report_generator_path = os.path.abspath("./assets/")
  
  try:
     
      # Call the Java program using subprocess
      print("Running the Java program...")
      subprocess.run(
          [
              "java",
              "-cp",
              f"{report_generator_path}:{java_classpath}",
              "ReportGenerator",
              jrxml_file,
              jasper_file,
              pdf_file,              
              json.dumps(parametros)
          ],
          check=True
      )


      displayPDF(pdf_file)
  except subprocess.CalledProcessError as e:
      print(f"An error occurred: {e}")

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf">'

    os.remove(file)
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)



