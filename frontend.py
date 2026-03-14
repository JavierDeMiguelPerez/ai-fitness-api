# frontend.py
import streamlit as st

st.set_page_config(page_title="AI Fitness App", page_icon="💪", layout="wide")

# Inicializamos el estado de la sesión si no existe
if "token" not in st.session_state:
    st.session_state.token = None

# Definimos las páginas apuntando a los archivos de la carpeta views/
auth_page = st.Page("views/auth.py", title="Acceso", icon="🔐")
profile_page = st.Page("views/profile.py", title="Mi Perfil", icon="👤")
workouts_page = st.Page("views/workouts.py", title="Entrenamientos", icon="🏋️‍♂️")
nutrition_page = st.Page("views/nutrition.py", title="Nutrición", icon="🥗")

# Lógica de enrutamiento protegido
if st.session_state.token is None:
    # Si no hay token, solo puede ver la página de Auth
    pg = st.navigation([auth_page])
else:
    # Si hay token, ve la app real
    pg = st.navigation([workouts_page, nutrition_page, profile_page])

# Ejecutamos la navegación
pg.run()