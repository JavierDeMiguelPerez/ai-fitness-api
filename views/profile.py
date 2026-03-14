# views/profile.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("👤 Mi Perfil Físico")

# Botón para cerrar sesión arriba a la derecha
col1, col2 = st.columns([8, 2])
with col2:
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.token = None
        st.rerun()

# Obtenemos el perfil actual
res = requests.get(f"{API_URL}/users/me", headers=headers)

if res.status_code == 404:
    st.warning("⚠️ Necesitamos conocerte para que la IA diseñe tus planes.")
    current_data = {}
else:
    current_data = res.json()
    st.success("Perfil cargado correctamente. Puedes actualizar tus datos cuando quieras.")

with st.form("profile_form"):
    st.subheader("Tus Medidas y Objetivos")
    
    colA, colB = st.columns(2)
    with colA:
        age = st.number_input("Edad", min_value=12, max_value=100, value=current_data.get("age", 25))
        weight_kg = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=current_data.get("weight_kg", 75.0))
        height_cm = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=current_data.get("height_cm", 180.0))
        gender_options = ["male", "female", "other"]
        gender_index = gender_options.index(current_data.get("gender", "male")) if current_data.get("gender") in gender_options else 0
        gender = st.selectbox("Género", gender_options, index=gender_index)

    with colB:
        exp_options = ["beginner", "intermediate", "advanced"]
        exp_index = exp_options.index(current_data.get("experience_level", "beginner")) if current_data.get("experience_level") in exp_options else 0
        experience = st.selectbox("Nivel de Experiencia", exp_options, index=exp_index)
        
        goal_options = ["Hipertrophy", "Strength", "Weight Loss", "Endurance"]
        goal_index = goal_options.index(current_data.get("primary_goal", "Hipertrophy")) if current_data.get("primary_goal") in goal_options else 0
        goal = st.selectbox("Objetivo Principal", goal_options, index=goal_index)
        
        activity = st.text_input("Nivel de actividad diario (Opcional)", value=current_data.get("activity_level", ""))
        allergies = st.text_input("Alergias / Intolerancias (Opcional)", value=current_data.get("allergies", ""))

    submitted = st.form_submit_button("Guardar Perfil", type="primary")
    
    if submitted:
        payload = {
            "age": age,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "gender": gender,
            "experience_level": experience,
            "primary_goal": goal,
            "activity_level": activity,
            "allergies": allergies
        }
        update_res = requests.put(f"{API_URL}/users/me", json=payload, headers=headers)
        if update_res.status_code == 200:
            st.success("¡Perfil actualizado con éxito!")
            st.rerun()
        else:
            st.error("Hubo un error al guardar el perfil.")