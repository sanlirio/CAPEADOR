import streamlit as st
import hashlib
from passlib.utils.md4 import md4
from ldap3 import Server, Connection, NTLM
from ldap3.core.exceptions import LDAPBindError

# --- Patch para suporte a MD4 (necessário em Python 3.10+ em alguns sistemas) ---
_original_new = hashlib.new
def _patched_hashlib_new(name, *args, **kwargs):
    if name.lower() == 'md4':
        return md4()
    return _original_new(name, *args, **kwargs)
hashlib.new = _patched_hashlib_new


# --- Configurações do AD ---
AD_SERVER = "ldap://10.30.2.20"
AD_DOMAIN = "larco.intranet"  # domínio completo
AD_BASE_DN = "DC=larco,DC=intranet"


def autenticar_usuario(usuario, senha):
    """Autentica no AD via NTLM."""
    usuario_ntlm = f"{AD_DOMAIN}\\{usuario}"  # Ex: larco.intranet\\usuario
    try:
        server = Server(AD_SERVER)
        conn = Connection(server, user=usuario_ntlm, password=senha, authentication=NTLM, auto_bind=True)
        if conn.bind():
            st.write("✅ Sucesso: Login autorizado no AD!")
        else:
            st.write("❌ Falha: Login rejeitado.")
            st.write("↪ Detalhes:", conn.result)

        return True, conn
    except LDAPBindError as e:
        return False, str(e)


# --- Interface Streamlit ---
st.set_page_config(page_title="Login AD", page_icon="🔐")
st.title("🔐 Login com Active Directory (Larco)")

with st.form("login_form"):
    username = st.text_input("Usuário (sem domínio)", max_chars=50)
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Entrar")

if submitted:
    if not username or not password:
        st.warning("Por favor, preencha usuário e senha.")
    else:
        autenticado, resultado = autenticar_usuario(username, password)
        
        if autenticado:
            st.success(f"✅ Bem-vindo(a), {username}!")
            st.write("Você está autenticado com sucesso no AD.")
            # Exibir mais dados do AD, se desejar:
            # resultado.search(AD_BASE_DN, f"(sAMAccountName={username})", attributes=["displayName", "mail"])
            # st.write(resultado.entries)
        else:
            st.error("❌ Falha na autenticação. Verifique usuário e senha.")
            st.caption(f"Detalhes técnicos: {resultado}")
