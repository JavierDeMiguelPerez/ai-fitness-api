# views/auth.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Bienvenido a AI Fitness & Nutrition")
st.caption("Tu entrenador personal y nutricionista impulsado por inteligencia artificial")

tab_login, tab_registro = st.tabs(["Iniciar Sesion", "Registrarse"])

with tab_login:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Contrasena", type="password")
        submitted = st.form_submit_button("Entrar", type="primary")
        
        if submitted:
            res = requests.post(f"{API_URL}/login", data={"username": email, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    # Enlace de "Olvidé mi contraseña" como texto pequeño
    with st.expander("¿Olvidaste tu contrasena?"):
        st.write("Introduce tu email para solicitar un token de recuperacion.")
        with st.form("forgot_form"):
            forgot_email = st.text_input("Email de recuperacion")
            forgot_submitted = st.form_submit_button("Solicitar Token")
            
            if forgot_submitted:
                res = requests.post(f"{API_URL}/forgot-password", json={"email": forgot_email})
                if res.status_code == 200:
                    st.success("Si el email existe, se ha enviado un token de recuperacion.")
                    token_data = res.json().get("token")
                    if token_data:
                        st.code(token_data, language="text")
                else:
                    st.error("Error al procesar la solicitud.")

        st.divider()
        st.write("Introduce el token recibido y tu nueva contrasena.")
        with st.form("reset_form"):
            token_input = st.text_input("Token de recuperacion")
            new_pass_input = st.text_input("Nueva Contrasena", type="password")
            reset_submitted = st.form_submit_button("Cambiar Contrasena")
            
            if reset_submitted:
                res = requests.post(f"{API_URL}/reset-password", json={"token": token_input, "new_password": new_pass_input})
                if res.status_code == 200:
                    st.success("Contrasena actualizada con exito. Ya puedes iniciar sesion.")
                else:
                    st.error(res.json().get("detail", "Token invalido o expirado."))

with tab_registro:
    with st.form("register_form"):
        new_email = st.text_input("Tu Email")
        new_password = st.text_input("Tu Contrasena", type="password")
        submitted = st.form_submit_button("Crear Cuenta")
        
        if submitted:
            res = requests.post(f"{API_URL}/users/", json={"email": new_email, "password": new_password})
            if res.status_code == 200:
                st.success("Cuenta creada. Ya puedes iniciar sesion.")
            else:
                st.error(res.json().get("detail", "Error al crear la cuenta."))