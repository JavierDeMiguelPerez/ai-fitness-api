# views/auth.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("💪 Bienvenido a AI Fitness & Nutrition")
st.write("Tu entrenador personal y nutricionista impulsado por Llama 3.1")

# Creamos pestañas para las distintas acciones de autenticación
tab_login, tab_registro, tab_forgot, tab_reset = st.tabs([
    "🔒 Iniciar Sesión", 
    "📝 Registrarse", 
    "❓ Olvidé mi Contraseña",
    "🔑 Restablecer Contraseña"
])

with tab_login:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Entrar", type="primary")
        
        if submitted:
            res = requests.post(f"{API_URL}/login", data={"username": email, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

with tab_registro:
    with st.form("register_form"):
        new_email = st.text_input("Tu Email")
        new_password = st.text_input("Tu Contraseña", type="password")
        submitted = st.form_submit_button("Crear Cuenta")
        
        if submitted:
            res = requests.post(f"{API_URL}/users/", json={"email": new_email, "password": new_password})
            if res.status_code == 200:
                st.success("¡Cuenta creada! Ya puedes iniciar sesión.")
                st.balloons()
            else:
                st.error(res.json().get("detail", "Error al crear la cuenta."))

with tab_forgot:
    st.info("Introduce tu email y te daremos un token temporal para recuperar tu cuenta.")
    with st.form("forgot_form"):
        forgot_email = st.text_input("Email de recuperación")
        submitted = st.form_submit_button("Solicitar Token")
        
        if submitted:
            res = requests.post(f"{API_URL}/forgot-password", json={"email": forgot_email})
            if res.status_code == 200:
                # En producción esto iría por email. Lo mostramos aquí para probar.
                st.success("Simulación: Revisa tu correo.")
                st.code(res.json().get("token"), language="text")
            else:
                st.error("Error al procesar la solicitud.")

with tab_reset:
    st.warning("Usa el token que recibiste para crear una nueva contraseña.")
    with st.form("reset_form"):
        token_input = st.text_input("Token de recuperación")
        new_pass_input = st.text_input("Nueva Contraseña", type="password")
        submitted = st.form_submit_button("Cambiar Contraseña")
        
        if submitted:
            res = requests.post(f"{API_URL}/reset-password", json={"token": token_input, "new_password": new_pass_input})
            if res.status_code == 200:
                st.success("Contraseña actualizada con éxito. ¡Ya puedes iniciar sesión!")
            else:
                st.error(res.json().get("detail", "Token inválido o expirado."))