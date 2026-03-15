# frontend.py
import streamlit as st

st.set_page_config(page_title="AI Fitness App", layout="wide")

# Inicializamos el estado de la sesión si no existe
if "token" not in st.session_state:
    st.session_state.token = None

# Definimos las páginas apuntando a los archivos de la carpeta views/
auth_page = st.Page("views/auth.py", title="Acceso")
profile_page = st.Page("views/profile.py", title="Perfil")
workouts_page = st.Page("views/workouts.py", title="Entrenamientos")
nutrition_page = st.Page("views/nutrition.py", title="Nutricion")
logout_page = st.Page("views/logout.py", title="Cerrar Sesion")

# Lógica de enrutamiento protegido
if st.session_state.token is None:
    pg = st.navigation([auth_page])
else:
    pg = st.navigation([workouts_page, nutrition_page, profile_page, logout_page])

pg.run()